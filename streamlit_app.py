#!/usr/bin/env python3
"""
Streamlit Web Interface for Knowledge RAG System
"""

import streamlit as st
from knowledge_rag import KnowledgeRAG
import os
from pathlib import Path
import time

# Configure page
st.set_page_config(
    page_title="Knowledge RAG System",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'documents_indexed' not in st.session_state:
    st.session_state.documents_indexed = False

def initialize_rag_system(documents_dir: str, model_name: str):
    """Initialize the RAG system."""
    try:
        with st.spinner("Initializing RAG system..."):
            rag = KnowledgeRAG(documents_dir=documents_dir, model_name=model_name)
            st.session_state.rag_system = rag
            return True
    except Exception as e:
        st.error(f"Error initializing RAG system: {e}")
        return False

def load_and_index_documents():
    """Load and index documents."""
    if st.session_state.rag_system is None:
        st.error("RAG system not initialized")
        return False
    
    try:
        with st.spinner("Loading and indexing documents..."):
            documents = st.session_state.rag_system.load_documents()
            if documents:
                st.session_state.rag_system.index_documents(documents)
                st.session_state.documents_indexed = True
                st.success(f"Successfully indexed {len(documents)} documents!")
                return True
            else:
                st.warning("No documents found in the specified directory.")
                return False
    except Exception as e:
        st.error(f"Error indexing documents: {e}")
        return False

def main():
    st.title("🤖 Knowledge RAG System")
    st.subheader("Chat with your local documents using AI")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Model selection
        model_name = st.selectbox(
            "Select Ollama Model",
            ["llama3.1:8b", "llama3.1:70b", "mistral", "codellama"],
            index=0
        )
        
        # Documents directory
        documents_dir = st.text_input(
            "Documents Directory",
            value="documents",
            help="Directory containing your documents"
        )
        
        # Initialize button
        if st.button("Initialize System"):
            if initialize_rag_system(documents_dir, model_name):
                st.success("System initialized!")
        
        # Index documents button
        if st.button("Load & Index Documents"):
            if st.session_state.rag_system:
                load_and_index_documents()
            else:
                st.error("Please initialize the system first")
        
        # System status
        st.header("System Status")
        if st.session_state.rag_system:
            st.success("✅ RAG System: Ready")
            
            # Check document count
            try:
                doc_count = st.session_state.rag_system.collection.count()
                st.info(f"📄 Documents: {doc_count} chunks indexed")
            except:
                st.warning("📄 Documents: Not indexed")
        else:
            st.warning("⚠️ RAG System: Not initialized")
    
    # Main chat interface
    if st.session_state.rag_system:
        # Chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your documents..."):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.rag_system.chat(prompt)
                        st.write(response)
                        
                        # Add assistant response to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"Error generating response: {e}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        
        # Clear chat history button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    else:
        st.info("Please initialize the RAG system using the sidebar controls.")
        
        # Instructions
        st.header("Getting Started")
        st.markdown("""
        1. **Initialize System**: Click "Initialize System" in the sidebar
        2. **Add Documents**: Place your documents in the 'documents' directory
        3. **Index Documents**: Click "Load & Index Documents" to process your files
        4. **Start Chatting**: Ask questions about your documents!
        
        **Supported File Types**: .txt, .md, .py, .js, .json, .csv
        """)

if __name__ == "__main__":
    main()