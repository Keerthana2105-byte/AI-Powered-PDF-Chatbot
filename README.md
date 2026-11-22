README.md
# AI-Powered PDF Chatbot

An AI-powered PDF chatbot using Retrieval-Augmented Generation (RAG), Python, Streamlit, Sentence Transformers, and Gemini API to answer questions from uploaded PDF documents with relevant page references.

## Features

- Upload and process PDF documents.
- Extract text from PDF pages.
- Split documents into smaller text chunks.
- Generate semantic embeddings using Sentence Transformers.
- Retrieve relevant passages using semantic and hybrid search.
- Ask questions about uploaded documents in natural language.
- Generate AI-powered answers using Gemini API.
- Display relevant PDF page references.
- Provide retrieved passages when Gemini is temporarily unavailable.
- Interactive chat interface using Streamlit.

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Sentence Transformers
- NumPy
- PyPDF
- Python-dotenv

## Project Structure

```text
AI-Powered-PDF-Chatbot/
│
├── app/
│   └── app.py
│
├── src/
│   ├── pdf_processor.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   └── chatbot.py
│
├── data/
├── models/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Keerthana2105-byte/AI-Powered-PDF-Chatbot.git
```

### 2. Navigate to the project

```bash
cd AI-Powered-PDF-Chatbot
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your API key to GitHub.

### 7. Run the application

```bash
python -m streamlit run app/app.py
```

Open the local URL displayed in your terminal.

## How It Works

1. The user uploads a PDF document.
2. The application extracts text from the document.
3. Extracted text is divided into smaller chunks.
4. Sentence Transformers converts chunks into vector embeddings.
5. The retrieval system identifies relevant passages for the user's question.
6. Gemini generates an answer using the retrieved PDF context.
7. The application displays the answer and relevant page references.

## Future Improvements

- Support multiple PDF documents.
- Improve retrieval accuracy.
- Add conversation memory.
- Add downloadable chat history.
- Add support for more document formats.
- Improve AI response reliability.

## Author

Keerthana

## License

This project is available for educational and learning purposes.