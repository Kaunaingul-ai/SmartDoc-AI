import torch

from transformers import (
    AutoTokenizer,
    AutoModelForQuestionAnswering
)


class QAEngine:
    """
    SmartDoc AI question-answering engine.

    Uses a SQuAD 2.0 model so the system can detect
    when a reliable answer is not present in the PDF.
    """

    def __init__(
        self,
        model_name="deepset/minilm-uncased-squad2",
        min_answerability=0.55,
        min_retrieval_score=0.20
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = AutoModelForQuestionAnswering.from_pretrained(
            model_name
        )

        self.model.eval()

        self.min_answerability = min_answerability
        self.min_retrieval_score = min_retrieval_score


    def _answer_single_context(
        self,
        question,
        context
    ):
        """
        Try to answer a question from one text chunk.

        Returns:
            answer
            answerability
        """

        inputs = self.tokenizer(
            question,
            context,
            return_tensors="pt",
            truncation="only_second",
            max_length=512
        )

        with torch.no_grad():

            outputs = self.model(
                **inputs
            )

        start_logits = outputs.start_logits[0]
        end_logits = outputs.end_logits[0]

        # -----------------------------------------
        # Score for "no answer"
        # -----------------------------------------

        null_score = (
            start_logits[0]
            + end_logits[0]
        ).item()

        # -----------------------------------------
        # Identify context tokens only
        # -----------------------------------------

        sequence_ids = inputs.sequence_ids(0)

        context_indexes = [
            index
            for index, sequence_id
            in enumerate(sequence_ids)
            if sequence_id == 1
        ]

        if not context_indexes:
            return "", 0.0

        # -----------------------------------------
        # Find best answer span
        # -----------------------------------------

        best_score = float("-inf")
        best_start = None
        best_end = None

        max_answer_length = 40

        for start_index in context_indexes:

            maximum_end = min(
                start_index + max_answer_length,
                len(start_logits)
            )

            for end_index in range(
                start_index,
                maximum_end
            ):

                if end_index not in context_indexes:
                    continue

                span_score = (
                    start_logits[start_index]
                    + end_logits[end_index]
                ).item()

                if span_score > best_score:

                    best_score = span_score
                    best_start = start_index
                    best_end = end_index

        if best_start is None:
            return "", 0.0

        # -----------------------------------------
        # Compare answer vs no-answer score
        # -----------------------------------------

        score_difference = (
            best_score - null_score
        )

        answerability = torch.sigmoid(
            torch.tensor(score_difference)
        ).item()

        # -----------------------------------------
        # Decode answer
        # -----------------------------------------

        answer_tokens = inputs[
            "input_ids"
        ][0][
            best_start:best_end + 1
        ]

        answer = self.tokenizer.decode(
            answer_tokens,
            skip_special_tokens=True
        ).strip()

        return answer, answerability


    def answer_question(
        self,
        question,
        retrieved_results
    ):
        """
        Evaluate retrieved PDF chunks and return
        the strongest reliable answer.

        If no reliable answer exists, return a
        clear 'answer not found' response.
        """

        if not retrieved_results:

            return {
                "found": False,
                "answer": (
                    "I could not find a reliable answer "
                    "to this question in the uploaded document."
                ),
                "confidence": 0.0,
                "page_number": None,
                "context": None
            }

        candidates = []

        # -----------------------------------------
        # Test each retrieved chunk independently
        # -----------------------------------------

        for result in retrieved_results:

            retrieval_score = result["score"]

            answer, answerability = (
                self._answer_single_context(
                    question,
                    result["text"]
                )
            )

            # Ignore weak semantic matches
            if (
                retrieval_score
                < self.min_retrieval_score
            ):
                continue

            # Ignore weak QA answers
            if (
                answerability
                < self.min_answerability
            ):
                continue

            # Ignore empty / meaningless answers
            if (
                not answer
                or len(answer.strip()) < 2
            ):
                continue

            # -------------------------------------
            # Combined quality score
            # -------------------------------------

            combined_score = (
                answerability * 0.75
                + max(retrieval_score, 0) * 0.25
            )

            candidates.append(
                {
                    "answer": answer,
                    "confidence": answerability,
                    "page_number": result[
                        "page_number"
                    ],
                    "context": result["text"],
                    "combined_score": combined_score,
                    "retrieval_score": retrieval_score
                }
            )

        # -----------------------------------------
        # No reliable answer found
        # -----------------------------------------

        if not candidates:

            return {
                "found": False,
                "answer": (
                    "I could not find a reliable answer "
                    "to this question in the uploaded document."
                ),
                "confidence": 0.0,
                "page_number": None,
                "context": None
            }

        # -----------------------------------------
        # Choose strongest candidate
        # -----------------------------------------

        best_result = max(
            candidates,
            key=lambda item: item[
                "combined_score"
            ]
        )

        best_result["found"] = True

        return best_result