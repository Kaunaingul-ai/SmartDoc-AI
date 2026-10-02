import streamlit as st

from src.pdf_processor import extract_text_from_pdf
from src.text_processor import create_text_chunks
from src.retriever import SemanticRetriever
from src.qa_engine import QAEngine
from src.summarizer import DocumentSummarizer


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartDoc AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD AI COMPONENTS
# =========================================================

@st.cache_resource
def load_retriever():
    return SemanticRetriever()


@st.cache_resource
def load_qa_engine():
    return QAEngine()


@st.cache_resource
def load_summarizer():
    return DocumentSummarizer()


# =========================================================
# SESSION STATE
# =========================================================

if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

if "document_summary" not in st.session_state:
    st.session_state.document_summary = None

if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📄 SmartDoc AI")

    st.caption(
        "AI-powered PDF Question Answering "
        "and Document Assistant"
    )

    st.divider()

    st.markdown("### ✨ Features")

    st.write("✓ PDF text extraction")
    st.write("✓ Document summarization")
    st.write("✓ Semantic search")
    st.write("✓ AI question answering")
    st.write("✓ Source-page identification")
    st.write("✓ Supporting context")
    st.write("✓ Unsupported-question detection")
    st.write("✓ Question history")

    st.divider()

    st.markdown("### 🧠 AI Pipeline")

    st.caption(
        "PDF → Text Extraction → Chunking → "
        "Semantic Retrieval → Question Answering"
    )

    st.divider()

    st.caption(
        "SmartDoc AI Project"
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.title("📄 SmartDoc AI")

st.markdown(
    "### Intelligent PDF Question Answering "
    "and Document Assistant"
)

st.write(
    "Transform PDF documents into searchable knowledge. "
    "Upload a document, generate a concise summary, "
    "ask natural-language questions, and inspect the "
    "supporting source context."
)

st.divider()


# =========================================================
# PDF UPLOAD
# =========================================================

st.markdown("## 📤 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"],
    help="Upload a text-based PDF document."
)


# =========================================================
# DOCUMENT PROCESSING
# =========================================================

if uploaded_file is not None:

    # -----------------------------------------------------
    # RESET STATE FOR NEW DOCUMENT
    # -----------------------------------------------------

    if (
        st.session_state.current_file_name
        != uploaded_file.name
    ):

        st.session_state.current_file_name = (
            uploaded_file.name
        )

        st.session_state.qa_history = []

        st.session_state.document_summary = None


    try:

        with st.spinner(
            "Reading and preparing your document..."
        ):

            full_text, page_texts, total_pages = (
                extract_text_from_pdf(
                    uploaded_file
                )
            )

            chunks = create_text_chunks(
                page_texts
            )


        # =================================================
        # VALID DOCUMENT
        # =================================================

        if full_text and len(chunks) > 0:

            st.success(
                "Document processed successfully."
            )


            # =================================================
            # DOCUMENT INFORMATION
            # =================================================

            st.markdown(
                "## 📌 Document Information"
            )

            info_col1, info_col2, info_col3, info_col4 = (
                st.columns(4)
            )

            with info_col1:

                st.metric(
                    "File",
                    uploaded_file.name
                )

            with info_col2:

                st.metric(
                    "Total Pages",
                    total_pages
                )

            with info_col3:

                st.metric(
                    "Readable Pages",
                    len(page_texts)
                )

            with info_col4:

                st.metric(
                    "Searchable Chunks",
                    len(chunks)
                )


            # =================================================
            # DOCUMENT PREVIEW
            # =================================================

            with st.expander(
                "📖 View extracted document text"
            ):

                preview_length = 3000

                preview_text = full_text[
                    :preview_length
                ]

                st.text_area(
                    "Document Preview",
                    preview_text,
                    height=300,
                    disabled=True
                )

                if len(full_text) > preview_length:

                    st.info(
                        "Only the first part of the PDF "
                        "is displayed. SmartDoc AI still "
                        "uses all extracted text."
                    )


            st.divider()


            # =================================================
            # DOCUMENT SUMMARY
            # =================================================

            st.markdown(
                "## 📝 AI Document Summary"
            )

            st.write(
                "Generate an extractive summary using "
                "representative sentences selected directly "
                "from the uploaded document."
            )

            summary_col1, summary_col2 = (
                st.columns([1, 1])
            )

            with summary_col1:

                generate_summary = st.button(
                    "✨ Generate Summary",
                    type="primary",
                    use_container_width=True
                )

            with summary_col2:

                clear_summary = st.button(
                    "Clear Summary",
                    use_container_width=True
                )


            if clear_summary:

                st.session_state.document_summary = None


            if generate_summary:

                try:

                    with st.spinner(
                        "Generating document summary..."
                    ):

                        summarizer = load_summarizer()

                        summary = (
                            summarizer.summarize_document(
                                page_texts
                            )
                        )

                        st.session_state.document_summary = (
                            summary
                        )

                except Exception as summary_error:

                    st.error(
                        "Summary generation failed: "
                        f"{summary_error}"
                    )


            if st.session_state.document_summary:

                st.success(
                    "Summary generated successfully."
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### Document Summary"
                    )

                    st.write(
                        st.session_state.document_summary
                    )


            st.divider()


            # =================================================
            # QUESTION ANSWERING
            # =================================================

            st.markdown(
                "## 💬 Ask SmartDoc AI"
            )

            st.write(
                "Ask a specific question about information "
                "contained in the uploaded PDF."
            )

            with st.form(
                "question_form",
                clear_on_submit=True
            ):

                question = st.text_input(
                    "Your question",
                    placeholder=(
                        "Example: What is the main "
                        "goal of this document?"
                    )
                )

                ask_button = st.form_submit_button(
                    "🤖 Ask SmartDoc AI",
                    type="primary"
                )


            if ask_button:

                if not question.strip():

                    st.warning(
                        "Please enter a question first."
                    )

                else:

                    try:

                        with st.spinner(
                            "Searching the document..."
                        ):

                            retriever = (
                                load_retriever()
                            )

                            retriever.build_index(
                                chunks
                            )

                            results = (
                                retriever.search(
                                    question,
                                    top_k=5
                                )
                            )


                            qa_engine = (
                                load_qa_engine()
                            )

                            answer_result = (
                                qa_engine.answer_question(
                                    question,
                                    results
                                )
                            )


                        history_item = {
                            "question": question,
                            "found": answer_result[
                                "found"
                            ],
                            "answer": answer_result[
                                "answer"
                            ],
                            "page_number": answer_result[
                                "page_number"
                            ],
                            "confidence": answer_result[
                                "confidence"
                            ],
                            "context": answer_result[
                                "context"
                            ],
                            "sources": results
                        }

                        st.session_state.qa_history.append(
                            history_item
                        )


                    except Exception as question_error:

                        st.error(
                            "Question answering failed: "
                            f"{question_error}"
                        )


            # =================================================
            # QUESTION HISTORY
            # =================================================

            if st.session_state.qa_history:

                st.markdown(
                    "## 🧠 Question & Answer History"
                )

                for item in reversed(
                    st.session_state.qa_history
                ):

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**Question:** "
                            f"{item['question']}"
                        )


                        # -------------------------------------
                        # ANSWER FOUND
                        # -------------------------------------

                        if item["found"]:

                            st.success(
                                "Reliable answer found"
                            )

                            st.markdown(
                                f"**Answer:** "
                                f"{item['answer']}"
                            )

                            metric1, metric2 = (
                                st.columns(2)
                            )

                            with metric1:

                                st.metric(
                                    "Source Page",
                                    item[
                                        "page_number"
                                    ]
                                )

                            with metric2:

                                confidence = (
                                    item[
                                        "confidence"
                                    ]
                                    * 100
                                )

                                st.metric(
                                    "Model Confidence",
                                    f"{confidence:.1f}%"
                                )


                            with st.expander(
                                "📄 Supporting context"
                            ):

                                st.write(
                                    item[
                                        "context"
                                    ]
                                )


                        # -------------------------------------
                        # NO ANSWER
                        # -------------------------------------

                        else:

                            st.warning(
                                "No reliable answer found"
                            )

                            st.write(
                                item[
                                    "answer"
                                ]
                            )


                        # -------------------------------------
                        # SOURCES
                        # -------------------------------------

                        with st.expander(
                            "📚 Retrieved sources"
                        ):

                            for (
                                source_number,
                                source
                            ) in enumerate(
                                item["sources"],
                                start=1
                            ):

                                relevance = (
                                    source[
                                        "score"
                                    ]
                                    * 100
                                )

                                st.markdown(
                                    f"**Source "
                                    f"{source_number} | "
                                    f"Page "
                                    f"{source['page_number']} | "
                                    f"Semantic relevance: "
                                    f"{relevance:.1f}%**"
                                )

                                st.write(
                                    source[
                                        "text"
                                    ]
                                )

                                st.divider()


                if st.button(
                    "🗑️ Clear Question History"
                ):

                    st.session_state.qa_history = []

                    st.rerun()


        # =================================================
        # UNREADABLE PDF
        # =================================================

        else:

            st.warning(
                "No readable text was found in this PDF."
            )

            st.info(
                "The document may be image-based or scanned. "
                "OCR support is not included in this version "
                "of SmartDoc AI."
            )


    # =====================================================
    # PDF PROCESSING ERROR
    # =====================================================

    except Exception as error:

        st.error(
            "The PDF could not be processed: "
            f"{error}"
        )


# =========================================================
# NO FILE
# =========================================================

else:

    st.info(
        "👆 Upload a PDF document to start using SmartDoc AI."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "SmartDoc AI • Intelligent PDF Question Answering "
    "and Document Assistant"
)