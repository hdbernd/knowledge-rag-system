#!/usr/bin/env python3
"""
Basic test of the knowledge system without requiring a specific model
"""

import os
import sys
from pathlib import Path
from knowledge_rag import KnowledgeRAG
import ollama

def test_basic_functionality():
    # Test document loading
    print("Testing document loading...")
    rag = KnowledgeRAG(documents_dir="documents")
    
    # Load documents
    documents = rag.load_documents()
    print(f"Loaded {len(documents)} documents")
    
    # Test indexing
    print("Testing document indexing...")
    rag.index_documents(documents)
    
    # Test search
    print("Testing document search...")
    results = rag.search_documents("machine learning", n_results=3)
    print(f"Found {len(results)} search results")
    
    for i, result in enumerate(results):
        print(f"Result {i+1}:")
        print(f"  Distance: {result['distance']:.3f}")
        print(f"  Source: {result['metadata']['source']}")
        print(f"  Content: {result['content'][:100]}...")
        print()
    
    # Test available models
    print("Testing Ollama connection...")
    try:
        # Try to list available models
        models = ollama.list()
        print(f"Available models: {models}")
        
        # If we have models, test one
        if models and 'models' in models and models['models']:
            model_name = models['models'][0].model
            print(f"Testing model: {model_name}")
            
            # Test simple generation
            response = ollama.generate(
                model=model_name,
                prompt="Hello, how are you?",
                options={'num_predict': 50}
            )
            print(f"Model response: {response['response']}")
        else:
            print("No models available. You can download one with: ollama pull phi3:mini")
    except Exception as e:
        print(f"Ollama error: {e}")

if __name__ == "__main__":
    test_basic_functionality()