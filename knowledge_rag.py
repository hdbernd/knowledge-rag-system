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
import hashlib
import time

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
        
        # File for tracking document states
        self.index_state_file = Path("chroma_db/index_state.json")
        
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
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get SHA256 hash of file contents."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""
    
    def _load_index_state(self) -> Dict[str, Dict[str, Any]]:
        """Load the current index state from file."""
        if not self.index_state_file.exists():
            return {}
        try:
            with open(self.index_state_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _save_index_state(self, state: Dict[str, Dict[str, Any]]):
        """Save the current index state to file."""
        # Ensure directory exists
        self.index_state_file.parent.mkdir(exist_ok=True)
        try:
            with open(self.index_state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save index state: {e}")
    
    def _get_files_to_process(self) -> tuple[List[Document], List[str]]:
        """Get files that need to be processed (new or modified)."""
        current_state = self._load_index_state()
        files_to_process = []
        files_to_remove = []
        new_state = {}
        
        # Check existing files
        supported_extensions = ['.txt', '.md', '.py', '.js', '.json', '.csv']
        
        if self.documents_dir.exists():
            for file_path in self.documents_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    file_key = str(file_path.relative_to(self.documents_dir))
                    current_hash = self._get_file_hash(file_path)
                    current_mtime = file_path.stat().st_mtime
                    
                    # Check if file is new or modified
                    if file_key not in current_state or \
                       current_state[file_key]['hash'] != current_hash or \
                       current_state[file_key]['mtime'] != current_mtime:
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                doc = Document(
                                    page_content=content,
                                    metadata={"source": str(file_path)}
                                )
                                files_to_process.append(doc)
                                print(f"Will process: {file_path}")
                        except Exception as e:
                            print(f"Error loading {file_path}: {e}")
                            continue
                    
                    # Update state for this file
                    new_state[file_key] = {
                        'hash': current_hash,
                        'mtime': current_mtime,
                        'size': file_path.stat().st_size
                    }
        
        # Check for deleted files
        for file_key in current_state:
            if file_key not in new_state:
                files_to_remove.append(file_key)
                print(f"Will remove: {file_key}")
        
        # Save new state
        self._save_index_state(new_state)
        
        return files_to_process, files_to_remove
    
    def smart_index_documents(self):
        """Intelligently index only new or modified documents."""
        print("🔍 Checking for document changes...")
        
        files_to_process, files_to_remove = self._get_files_to_process()
        
        # Remove chunks for deleted files
        if files_to_remove:
            print(f"🗑️ Removing {len(files_to_remove)} deleted files from index...")
            for file_key in files_to_remove:
                try:
                    # Build full path to match against source metadata
                    full_path = str(self.documents_dir / file_key)
                    
                    # Remove all chunks with this exact source path
                    results = self.collection.get(
                        where={"source": full_path}
                    )
                    if results['ids']:
                        self.collection.delete(ids=results['ids'])
                        print(f"   Removed {len(results['ids'])} chunks for: {file_key}")
                    else:
                        print(f"   No chunks found for: {file_key}")
                except Exception as e:
                    print(f"   Warning: Could not remove chunks for {file_key}: {e}")
        
        # Process new/modified files
        if files_to_process:
            print(f"📝 Processing {len(files_to_process)} new/modified files...")
            self._index_new_documents(files_to_process)
        elif not files_to_remove:
            print("✅ No changes detected - index is up to date!")
        
        final_count = self.collection.count()
        print(f"📊 Total chunks in database: {final_count}")
        
        return len(files_to_process) > 0 or len(files_to_remove) > 0
    
    def _index_new_documents(self, documents: List[Document]):
        """Index new documents without clearing existing ones."""
        if not documents:
            return
            
        print(f"Indexing {len(documents)} documents...")
        
        # Remove existing chunks for these documents first
        for doc in documents:
            try:
                source_path = doc.metadata['source']
                results = self.collection.get(
                    where={"source": source_path}
                )
                if results['ids']:
                    self.collection.delete(ids=results['ids'])
                    print(f"   Removed old chunks for: {source_path}")
            except Exception as e:
                print(f"   Warning: Could not remove old chunks for {doc.metadata['source']}: {e}")
        
        # Process new chunks
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
            
        print(f"Processing {len(all_chunks)} new chunks...")
        
        # Process in batches
        batch_size = 1000
        total_batches = (len(all_chunks) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min((batch_idx + 1) * batch_size, len(all_chunks))
            batch_chunks = all_chunks[start_idx:end_idx]
            
            print(f"   Processing batch {batch_idx + 1}/{total_batches} ({len(batch_chunks)} chunks)...")
            
            # Generate embeddings for this batch
            contents = [chunk['content'] for chunk in batch_chunks]
            try:
                embeddings = self.embedding_model.encode(contents).tolist()
            except Exception as e:
                print(f"   Error generating embeddings for batch {batch_idx + 1}: {e}")
                continue
            
            # Add batch to ChromaDB
            try:
                self.collection.add(
                    ids=[chunk['id'] for chunk in batch_chunks],
                    documents=contents,
                    embeddings=embeddings,
                    metadatas=[chunk['metadata'] for chunk in batch_chunks]
                )
                print(f"   ✅ Batch {batch_idx + 1} indexed successfully")
            except Exception as e:
                print(f"   ❌ Error indexing batch {batch_idx + 1}: {e}")
                continue
        
        print(f"✅ Indexing complete!")
    
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