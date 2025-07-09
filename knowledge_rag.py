#!/usr/bin/env python3
"""
Local Knowledge RAG System
A tool for natural language interaction with local documents using Ollama and ChromaDB.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import json

class KnowledgeRAG:
    def __init__(self, documents_dir: str = "documents", model_name: str = "llama3.1:8b"):
        self.documents_dir = Path(documents_dir)
        self.model_name = model_name
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
        
    def load_documents(self) -> List[Document]:
        """Load and process documents from the documents directory."""
        documents = []
        
        if not self.documents_dir.exists():
            print(f"Creating documents directory: {self.documents_dir}")
            self.documents_dir.mkdir(exist_ok=True)
            return documents
            
        supported_extensions = ['.txt', '.md', '.py', '.js', '.json', '.csv']
        
        for file_path in self.documents_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        doc = Document(
                            page_content=content,
                            metadata={"source": str(file_path)}
                        )
                        documents.append(doc)
                        print(f"Loaded: {file_path}")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    
        return documents
    
    def index_documents(self, documents: List[Document]):
        """Index documents into ChromaDB with batch processing."""
        if not documents:
            print("No documents to index")
            return
            
        print(f"Indexing {len(documents)} documents...")
        
        # Clear existing collection if it has items
        if self.collection.count() > 0:
            try:
                # Get all IDs and delete them
                results = self.collection.get()
                if results['ids']:
                    self.collection.delete(ids=results['ids'])
            except Exception as e:
                print(f"Warning: Could not clear collection: {e}")
                # Create a new collection with a different name
                import time
                collection_name = f"knowledge_base_{int(time.time())}"
                self.collection = self.chroma_client.get_or_create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
        
        all_chunks = []
        for doc in documents:
            chunks = self.text_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    'id': f"{doc.metadata['source']}_chunk_{i}",
                    'content': chunk,
                    'metadata': doc.metadata
                })
        
        if not all_chunks:
            print("No chunks to index")
            return
            
        print(f"Processing {len(all_chunks)} chunks...")
        
        # Process in batches to avoid ChromaDB limits
        batch_size = 1000  # Safe batch size for ChromaDB
        total_batches = (len(all_chunks) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min((batch_idx + 1) * batch_size, len(all_chunks))
            batch_chunks = all_chunks[start_idx:end_idx]
            
            print(f"Processing batch {batch_idx + 1}/{total_batches} ({len(batch_chunks)} chunks)...")
            
            # Generate embeddings for this batch
            contents = [chunk['content'] for chunk in batch_chunks]
            try:
                embeddings = self.embedding_model.encode(contents).tolist()
            except Exception as e:
                print(f"Error generating embeddings for batch {batch_idx + 1}: {e}")
                continue
            
            # Add batch to ChromaDB
            try:
                self.collection.add(
                    ids=[chunk['id'] for chunk in batch_chunks],
                    documents=contents,
                    embeddings=embeddings,
                    metadatas=[chunk['metadata'] for chunk in batch_chunks]
                )
                print(f"✅ Batch {batch_idx + 1} indexed successfully")
            except Exception as e:
                print(f"❌ Error indexing batch {batch_idx + 1}: {e}")
                continue
        
        final_count = self.collection.count()
        print(f"✅ Indexing complete! Total chunks in database: {final_count}")
        
        # Verify the indexing worked
        if final_count == 0:
            print("⚠️ Warning: No chunks were successfully indexed")
        elif final_count < len(all_chunks):
            print(f"⚠️ Warning: Only {final_count} out of {len(all_chunks)} chunks were indexed")
    
    def search_documents(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents."""
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        search_results = []
        for i in range(len(results['documents'][0])):
            search_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
            
        return search_results
    
    def generate_response(self, query: str, context: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Generate response using Ollama with conversation context."""
        # Build conversation context if available
        conversation_context = ""
        if conversation_history:
            # Limit to last 5 exchanges to avoid token limits
            recent_history = conversation_history[-5:]
            conversation_context = "\n\nPrevious conversation:\n"
            for entry in recent_history:
                conversation_context += f"Human: {entry['query']}\nAssistant: {entry['response']}\n\n"
        
        prompt = f"""Based on the following context, answer the user's question. If the answer is not in the context, say so.

Context from documents:
{context}{conversation_context}

Current question: {query}

Answer:"""
        
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={'temperature': 0.7}
            )
            return response['response']
        except Exception as e:
            return f"Error generating response: {e}"
    
    def chat(self, query: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Main chat function with conversation context."""
        # Search for relevant documents
        search_results = self.search_documents(query)
        
        if not search_results:
            return "No relevant documents found in the knowledge base."
        
        # Prepare context
        context = "\n\n".join([
            f"Source: {result['metadata']['source']}\n{result['content']}"
            for result in search_results
        ])
        
        # Generate response with conversation history
        response = self.generate_response(query, context, conversation_history)
        
        return response
    
    def interactive_chat(self):
        """Interactive chat loop with conversation memory."""
        print("🤖 Knowledge RAG System")
        print("Type 'quit' to exit, 'reindex' to reload documents, 'clear' to clear chat history")
        print("-" * 50)
        
        conversation_history = []
        max_history_size = 50
        
        while True:
            try:
                query = input("\nYou: ").strip()
                
                if query.lower() == 'quit':
                    break
                elif query.lower() == 'reindex':
                    print("Reindexing documents...")
                    documents = self.load_documents()
                    self.index_documents(documents)
                    print("Documents reindexed!")
                    continue
                elif query.lower() == 'clear':
                    history_count = len(conversation_history)
                    conversation_history = []
                    print(f"Chat history cleared ({history_count} entries removed)")
                    continue
                elif not query:
                    continue
                
                print("🤖 Assistant: ", end="")
                response = self.chat(query, conversation_history)
                print(response)
                
                # Save to conversation history
                conversation_history.append({
                    'query': query,
                    'response': response
                })
                
                # Manage history size
                if len(conversation_history) > max_history_size:
                    conversation_history = conversation_history[-max_history_size:]
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\nGoodbye!")

def main():
    parser = argparse.ArgumentParser(description="Local Knowledge RAG System")
    parser.add_argument("--documents-dir", default="documents", help="Directory containing documents")
    parser.add_argument("--model", default="llama3.1:8b", help="Ollama model name")
    parser.add_argument("--index", action="store_true", help="Index documents and exit")
    parser.add_argument("--query", help="Single query mode")
    
    args = parser.parse_args()
    
    # Initialize RAG system
    rag = KnowledgeRAG(documents_dir=args.documents_dir, model_name=args.model)
    
    if args.index:
        print("Loading and indexing documents...")
        documents = rag.load_documents()
        rag.index_documents(documents)
        print("Indexing complete!")
        return
    
    # Load documents if collection is empty
    if rag.collection.count() == 0:
        print("No indexed documents found. Loading documents...")
        documents = rag.load_documents()
        if documents:
            rag.index_documents(documents)
        else:
            print("No documents found. Please add files to the 'documents' directory.")
            return
    
    if args.query:
        response = rag.chat(args.query)
        print(response)
    else:
        rag.interactive_chat()

if __name__ == "__main__":
    main()