StudyMate is an AI-powered collaborative learning platform designed to make studying smarter, simpler, and more engaging. It helps students and professionals efficiently extract and understand information from PDF study materials by enabling instant, contextual question-answering. This reduces time spent searching through documents and accelerates learning by delivering direct, relevant answers with source references.

Key Features
Upload multiple PDF study materials (up to 200MB each).

Extracts and processes text from PDFs using PyMuPDF for accurate content capture.

Splits text into meaningful, overlapping chunks for semantic search.

Utilizes SentenceTransformer embeddings and FAISS for fast, relevance-based document chunk retrieval.

Supports both extractive and generative question answering with HuggingFace transformer models.

Provides contextual answers with referenced paragraphs from original documents.

Maintains Q&A history with timestamps and the number of sources referenced.

Configurable chunk size, overlap, and retrieval settings for flexible performance.

Secure usage with HuggingFace API token integration.

User-friendly interface built using Streamlit for smooth interactions.

Installation Steps
Clone the repository:

bash
git clone https://github.com/24rithika/Studymate.git
cd Studymate
Create and activate a virtual environment:

bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
Install dependencies from requirements file:

bash
pip install -r requirements.txt
Set up your HuggingFace API token:

Get your token from https://huggingface.co/settings/tokens

Provide the token in the app when prompted or set it as an environment variable.

Run the Streamlit app:

bash
streamlit run streamlit_app/main.py
How to Use
Open the app URL shown on the terminal (usually http://localhost:8501).

Upload one or more PDF study documents via drag and drop or file browse.

Click “Process Documents” to extract and index the content.

Enter your questions related to the uploaded content in the Q&A interface.

Receive instant, contextual answers with source paragraph references.

Review previous questions and answers in the Q&A history panel.

Download your Q&A history if needed for offline review.

Tech Stack
Frontend: Streamlit (Python framework for interactive web apps)

PDF Processing: PyMuPDF (fitz library) for efficient PDF text extraction

Text Embeddings: SentenceTransformers (all-MiniLM-L6-v2 model) for semantic understanding

Vector Search: FAISS for fast nearest neighbor search on embeddings

Q&A Models: HuggingFace transformers (DialoGPT, DistilBERT, etc.) for extractive and generative answering

Python Libraries: numpy, base64, datetime, re, typing, OS

Version Control: Git & GitHub
