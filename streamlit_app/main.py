import streamlit as st
from datetime import datetime
# Define StudyMateRAG here since studymate_rag module is missing
class StudyMateRAG:
    def __init__(self, hf_token):
        self.hf_token = hf_token
        self.chunks = []
        self.index = None

    def extract_text_from_pdf(self, uploaded_file):
        # Dummy implementation: replace with actual PDF extraction logic
        return "Extracted text from PDF."

    def create_chunks(self, text, chunk_size, chunk_overlap):
        # Dummy implementation: split text into chunks
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - chunk_overlap):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append(chunk)
        return chunks

    def build_faiss_index(self, all_texts, filenames):
        # Dummy implementation: store chunks and filenames
        self.chunks = [{"text": t, "metadata": {"filename": f}} for t, f in zip(all_texts, filenames)]
        self.index = True  # Placeholder

    def retrieve_relevant_chunks(self, question, k):
        # Dummy implementation: return first k chunks
        return self.chunks[:k]

    def generate_answer(self, question, relevant_chunks):
        # Dummy implementation: concatenate chunk texts as answer
        return " ".join([chunk["text"] for chunk in relevant_chunks]) if relevant_chunks else "No relevant information found."

def main():
    st.title("📚 StudyMate - AI-Powered PDF Q&A System")
    st.markdown("Upload your study materials and ask questions to get instant, contextual answers!")
    
    # Initialize session state
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # HuggingFace API Key input
        hf_token = st.text_input(
            "HuggingFace API Token", 
            type="password",
            help="Your HuggingFace API token for accessing models"
        )
        
        # Model selection
        st.subheader("Model Configuration")
        model_choice = st.selectbox(
            "Choose Model Type",
            ["Extractive QA (Fast)", "Generative QA (Better)", "Conversational"],
            help="Extractive: Fast, direct answers. Generative: More comprehensive responses."
        )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            chunk_size = st.slider("Chunk Size (words)", 300, 800, 500)
            chunk_overlap = st.slider("Chunk Overlap (words)", 50, 200, 100)
            retrieval_k = st.slider("Number of chunks to retrieve", 1, 10, 3)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Upload Documents")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload your PDF study materials",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files containing your study materials"
        )
        
        # Process documents
        if uploaded_files and hf_token:
            if st.button("Process Documents") or not st.session_state.documents_processed:
                with st.spinner("Processing documents..."):
                    try:
                        # Initialize RAG system
                        st.session_state.rag_system = StudyMateRAG(hf_token)
                        
                        # Extract text from all PDFs
                        all_texts = []
                        filenames = []
                        
                        for uploaded_file in uploaded_files:
                            st.info(f"Processing {uploaded_file.name}...")
                            text = st.session_state.rag_system.extract_text_from_pdf(uploaded_file)
                            
                            if text:
                                chunks = st.session_state.rag_system.create_chunks(
                                    text, chunk_size, chunk_overlap
                                )
                                all_texts.extend(chunks)
                                filenames.extend([uploaded_file.name] * len(chunks))
                        
                        # Build search index
                        if all_texts:
                            st.session_state.rag_system.build_faiss_index(all_texts, filenames)
                            st.session_state.documents_processed = True
                            st.success(f"Successfully processed {len(uploaded_files)} documents with {len(all_texts)} chunks!")
                        else:
                            st.error("No text could be extracted from the uploaded files.")
                    
                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")
        
        # Question-Answer Interface
        if st.session_state.documents_processed and st.session_state.rag_system:
            st.header("Ask Questions")
            
            # Question input
            question = st.text_input(
                "Enter your question about the uploaded documents:",
                placeholder="e.g., What is overfitting in machine learning?",
                key="question_input"
            )
            
            # Generate answer
            if st.button("Get Answer") and question:
                with st.spinner("Finding answer..."):
                    try:
                        # Retrieve relevant chunks
                        relevant_chunks = st.session_state.rag_system.retrieve_relevant_chunks(
                            question, retrieval_k
                        )
                        
                        # Generate answer
                        answer = st.session_state.rag_system.generate_answer(question, relevant_chunks)
                        
                        # Display answer
                        st.markdown('<div class="answer-container">', unsafe_allow_html=True)
                        st.markdown(f"*Answer:* {answer}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display referenced chunks
                        if relevant_chunks:
                            with st.expander("Referenced Paragraphs"):
                                for i, chunk in enumerate(relevant_chunks):
                                    st.markdown(f"*Source {i+1}:*")
                                    st.markdown(f"File: {chunk['metadata'].get('filename', 'Unknown')}")
                                    st.markdown('<div class="reference-container">', unsafe_allow_html=True)
                                    st.markdown(chunk['text'][:300] + "..." if len(chunk['text']) > 300 else chunk['text'])
                                    st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Add to history
                        st.session_state.qa_history.append({
                            'question': question,
                            'answer': answer,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'sources': len(relevant_chunks)
                        })
                        
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
    
    with col2:
        st.header("Status")
        
        if st.session_state.documents_processed:
            st.success("✅ Documents processed and ready!")
            st.info(f"📊 {len(st.session_state.rag_system.chunks)} text chunks indexed")
        else:
            st.warning("⏳ Upload and process documents to get started")
        
        # Model info
        if st.session_state.rag_system:
            st.subheader("Model Information")
            st.info("🔧 Embedding: all-MiniLM-L6-v2")
            if model_choice == "Extractive QA (Fast)":
                st.info("🤖 QA Model: DistilBERT Squad")
            elif model_choice == "Generative QA (Better)":
                st.info("🤖 QA Model: DialoGPT-medium")
    
    # Q&A History
    if st.session_state.qa_history:
        st.header("Q&A History")
        
        # Download history button
        history_text = ""
        for i, entry in enumerate(st.session_state.qa_history):
            history_text += f"Q{i+1}: {entry['question']}\n"
            history_text += f"A{i+1}: {entry['answer']}\n"
            history_text += f"Timestamp: {entry['timestamp']}\n"
            history_text += f"Sources used: {entry['sources']}\n"
            history_text += "-" * 50 + "\n\n"
        
        st.download_button(
            label="📥 Download Q&A History",
            data=history_text,
            file_name=f"studymate_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
        # Display recent history
        st.subheader("Recent Questions")
        for entry in reversed(st.session_state.qa_history[-5:]):  # Show last
            st.markdown(f"**Q:** {entry['question']}")
            st.markdown(f"**A:** {entry['answer']}")
            st.markdown(f"_Timestamp:_ {entry['timestamp']}")
            st.markdown(f"_Sources used:_ {entry['sources']}")
            st.markdown("---")