# 📄 SmartDoc AI

## Intelligent PDF Question Answering and Document Assistant

SmartDoc AI is an AI-powered document assistant that allows users to upload PDF files, generate concise document summaries, and ask natural-language questions about the uploaded content.

The application combines PDF text extraction, semantic search, transformer-based question answering, source-page identification, supporting context, unsupported-question detection, and question history in a clean Streamlit interface.

---

## 🚀 Features

- 📤 Upload text-based PDF documents
- 📖 Extract text from multiple PDF pages
- ✂️ Divide document text into searchable chunks
- 🔎 Perform semantic search using sentence embeddings
- 🧠 Retrieve the most relevant document sections
- 💬 Ask natural-language questions about the PDF
- 🤖 Generate answers directly from document content
- 📄 Identify the source page of an answer
- 📚 Display supporting context and retrieved sources
- ⚠️ Detect questions whose answers are not available in the PDF
- 📝 Generate an extractive document summary
- 🧠 Maintain question-and-answer history
- 🖥️ Use a clean and user-friendly Streamlit interface

---

## 🎯 Project Objective

Long PDF documents can require significant time to read and search manually.

SmartDoc AI was developed to make document exploration easier by allowing users to:

1. Upload a PDF document.
2. Extract and process its text.
3. Generate a concise document summary.
4. Ask questions in natural language.
5. Retrieve the most relevant sections using semantic search.
6. Generate answers from the document itself.
7. View the source page and supporting context.
8. Detect when the requested information is not available in the PDF.

---

## 🧠 System Workflow

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Sentence Embeddings
    ↓
FAISS Semantic Search
    ↓
Relevant Context Retrieval
    ↓
Question Answering Model
    ↓
Answer + Source Page + Supporting Context
```

The document summary feature uses an extractive approach to select representative sentences directly from the uploaded PDF.

---

## 🛠️ Technologies Used

- Python
- Streamlit
- PyPDF
- Sentence Transformers
- FAISS
- Hugging Face Transformers
- PyTorch
- NumPy

---

## 🤖 AI Models

### Semantic Retrieval Model

SmartDoc AI uses:

```text
all-MiniLM-L6-v2
```

This model converts document chunks and user questions into semantic embeddings so that FAISS can retrieve the most relevant parts of the PDF.

### Question Answering Model

SmartDoc AI uses:

```text
deepset/minilm-uncased-squad2
```

This model performs extractive question answering and supports unanswerable-question detection.

---

## 📁 Project Structure

```text
SmartDoc_AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── src/
    ├── pdf_processor.py
    ├── text_processor.py
    ├── retriever.py
    ├── qa_engine.py
    └── summarizer.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kaunaingul-ai/SmartDoc-AI.git
```

### 2. Open the project directory

```bash
cd SmartDoc-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment on Windows

```bash
venv\Scripts\activate
```

### 5. Install the required dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start SmartDoc AI using:

```bash
streamlit run app.py
```

Then open the local Streamlit address shown in the terminal.

Usually:

```text
http://localhost:8501
```

---

## 🧪 Testing and Validation

SmartDoc AI was tested using multiple PDF documents and different types of questions.

### Test 1 — Main Purpose

**Question**

```text
What is the main purpose of community solar microgrids?
```

**Answer**

```text
improve energy reliability while reducing dependence on the central electricity grid
```

**Source Page**

```text
1
```

---

### Test 2 — Battery Storage

**Question**

```text
Why is battery storage important in a microgrid?
```

**Answer**

```text
solar generation is variable and does not always match electricity demand
```

**Source Page**

```text
2
```

---

### Test 3 — Unsupported Question

**Question**

```text
Who invented the community microgrid?
```

**Result**

```text
No reliable answer found.
```

This demonstrates that SmartDoc AI does not force an unsupported answer when the requested information is not available in the document.

---

## 📝 Document Summarization

SmartDoc AI includes an extractive summarization feature.

Instead of generating unsupported text, the summarizer selects representative sentences directly from the uploaded PDF using semantic similarity.

This helps reduce hallucination and keeps the summary grounded in the source document.

---

## 🔍 Semantic Search

The application divides PDF text into smaller overlapping chunks.

Each chunk is converted into a semantic embedding using Sentence Transformers.

FAISS is then used to compare the user question with the stored document embeddings and retrieve the most relevant sections.

---

## 💬 Question Answering

After semantic retrieval, the most relevant document sections are passed to the question-answering model.

The system returns:

- the extracted answer,
- the source page,
- model confidence,
- supporting context,
- and retrieved source sections.

If a reliable answer cannot be found, SmartDoc AI clearly informs the user instead of forcing a response.

---

## ⚠️ Current Limitation

SmartDoc AI currently works best with PDFs that contain extractable text.

Image-only or scanned PDFs may require OCR before their contents can be processed.

OCR is not included in the current version.

---

## 🔮 Future Improvements

Possible future extensions include:

- OCR support for scanned PDFs
- Multi-document question answering
- Multilingual PDF support
- Conversational follow-up questions
- Advanced document citations
- Cloud deployment
- Downloadable question-answer history
- User authentication
- Document comparison
- Exportable summaries

---

## 📌 Internship Project

This project was developed as part of an Artificial Intelligence internship with **SAM AI Technologies**.

### Internship Task

**AI PDF Question Answering**

The original task requirements included:

- Upload a PDF document
- Ask questions related to the PDF
- Extract relevant answers
- Display responses with context
- Provide a user-friendly interface

SmartDoc AI satisfies these requirements and extends them with:

- semantic retrieval,
- source-page identification,
- unsupported-question detection,
- extractive summarization,
- question history,
- retrieved supporting sources,
- and a polished Streamlit interface.

---

## 👩‍💻 Author

**Kaunain Gul Khalid**

BS Artificial Intelligence Student

---

## 📜 License

This project is intended for educational, internship, portfolio, and learning purposes.
