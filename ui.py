#!/usr/bin/env python3
"""
Simple Terminal UI for Knowledge RAG System
A lightweight interface with chat and document management
"""

import os
import sys
import time
from pathlib import Path
from knowledge_rag import KnowledgeRAG
import ollama

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class KnowledgeUI:
    def __init__(self):
        self.rag = None
        self.current_model = "phi3:mini"
        self.documents_dir = "documents"
        self.chat_history = []
        self.max_history_size = 50  # Maximum number of exchanges to keep
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def print_header(self):
        self.clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════╗")
        print("║                 🤖 Knowledge RAG UI                  ║")
        print("║           Chat with your documents locally           ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        
    def print_status(self):
        # Check system status
        model_status = "✅ Ready" if self.check_model_available() else f"❌ Not Available"
        doc_count = self.rag.collection.count() if self.rag else 0
        
        print(f"{Colors.OKCYAN}📊 System Status:{Colors.ENDC}")
        print(f"   Model: {Colors.OKGREEN}{self.current_model}{Colors.ENDC} ({model_status})")
        print(f"   Documents: {Colors.OKGREEN}{doc_count} chunks indexed{Colors.ENDC}")
        print(f"   Directory: {Colors.OKGREEN}{self.documents_dir}{Colors.ENDC}")
        print()
        
    def print_menu(self):
        print(f"{Colors.OKBLUE}🎯 Quick Actions:{Colors.ENDC}")
        print(f"   {Colors.BOLD}1{Colors.ENDC} - Chat with documents")
        print(f"   {Colors.BOLD}2{Colors.ENDC} - Refresh document index")
        print(f"   {Colors.BOLD}3{Colors.ENDC} - Change model")
        print(f"   {Colors.BOLD}4{Colors.ENDC} - View chat history")
        print(f"   {Colors.BOLD}5{Colors.ENDC} - Clear chat history")
        print(f"   {Colors.BOLD}6{Colors.ENDC} - System info")
        print(f"   {Colors.BOLD}7{Colors.ENDC} - Clear database (if issues)")
        print(f"   {Colors.BOLD}q{Colors.ENDC} - Quit")
        print()
        
    def check_model_available(self):
        try:
            models = ollama.list()
            available_models = [model.model for model in models['models']]
            return self.current_model in available_models
        except:
            return False
            
    def initialize_rag(self):
        if not self.rag:
            print(f"{Colors.WARNING}Initializing RAG system...{Colors.ENDC}")
            try:
                self.rag = KnowledgeRAG(documents_dir=self.documents_dir, model_name=self.current_model)
                
                # Auto-index if no documents
                if self.rag.collection.count() == 0:
                    self.refresh_index()
                    
                print(f"{Colors.OKGREEN}✅ RAG system ready!{Colors.ENDC}")
                time.sleep(1)
            except Exception as e:
                print(f"{Colors.FAIL}❌ Error initializing RAG: {e}{Colors.ENDC}")
                input("Press Enter to continue...")
                return False
        return True
        
    def refresh_index(self):
        print(f"{Colors.WARNING}🔄 Refreshing document index...{Colors.ENDC}")
        try:
            if not self.rag:
                self.rag = KnowledgeRAG(documents_dir=self.documents_dir, model_name=self.current_model)
                
            print(f"{Colors.OKCYAN}Loading documents from {self.documents_dir}...{Colors.ENDC}")
            documents = self.rag.load_documents()
            
            if documents:
                print(f"{Colors.OKCYAN}Found {len(documents)} documents to process{Colors.ENDC}")
                print(f"{Colors.WARNING}This may take a few minutes for large document collections...{Colors.ENDC}")
                
                # The index_documents method now handles batching internally
                self.rag.index_documents(documents)
                
                # Get final count
                final_count = self.rag.collection.count()
                print(f"{Colors.OKGREEN}✅ Indexing complete! {final_count} chunks in database{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠️ No documents found in {self.documents_dir}{Colors.ENDC}")
                print(f"{Colors.OKCYAN}Supported file types: .txt, .md, .py, .js, .json, .csv{Colors.ENDC}")
                
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error refreshing index: {e}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Try clearing the database: rm -rf chroma_db/{Colors.ENDC}")
            
        input("Press Enter to continue...")
        
    def chat_mode(self):
        if not self.initialize_rag():
            return
            
        self.clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}💬 Chat Mode{Colors.ENDC}")
        print(f"Model: {Colors.OKGREEN}{self.current_model}{Colors.ENDC}")
        print(f"Type 'back' to return to main menu")
        print("─" * 60)
        
        while True:
            try:
                query = input(f"\n{Colors.OKCYAN}You: {Colors.ENDC}").strip()
                
                if query.lower() in ['back', 'exit', 'quit']:
                    break
                elif not query:
                    continue
                    
                print(f"{Colors.OKBLUE}🤖 Assistant: {Colors.ENDC}", end="", flush=True)
                
                try:
                    # Pass conversation history to RAG system
                    response = self.rag.chat(query, self.chat_history)
                    print(response)
                    
                    # Save to history
                    self.chat_history.append({
                        'query': query,
                        'response': response,
                        'timestamp': time.strftime("%H:%M:%S")
                    })
                    
                    # Manage history size
                    if len(self.chat_history) > self.max_history_size:
                        self.chat_history = self.chat_history[-self.max_history_size:]
                    
                except Exception as e:
                    print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
                    
            except KeyboardInterrupt:
                break
                
    def change_model(self):
        print(f"{Colors.HEADER}🔧 Change Model{Colors.ENDC}")
        
        # Get available models
        try:
            models = ollama.list()
            available_models = [model.model for model in models['models']]
            
            if not available_models:
                print(f"{Colors.FAIL}❌ No models available. Install models with: ollama pull phi3:mini{Colors.ENDC}")
                input("Press Enter to continue...")
                return
                
            print(f"\n{Colors.OKBLUE}Available models:{Colors.ENDC}")
            for i, model in enumerate(available_models, 1):
                current = "← Current" if model == self.current_model else ""
                print(f"   {i}. {model} {Colors.OKGREEN}{current}{Colors.ENDC}")
                
            try:
                choice = input(f"\nSelect model (1-{len(available_models)}) or press Enter to cancel: ").strip()
                if choice and choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(available_models):
                        old_model = self.current_model
                        self.current_model = available_models[idx]
                        
                        # Reset RAG system to use new model
                        self.rag = None
                        
                        print(f"{Colors.OKGREEN}✅ Model changed from {old_model} to {self.current_model}{Colors.ENDC}")
                        time.sleep(1)
                        
            except ValueError:
                print(f"{Colors.FAIL}❌ Invalid selection{Colors.ENDC}")
                time.sleep(1)
                
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error getting models: {e}{Colors.ENDC}")
            input("Press Enter to continue...")
            
    def view_history(self):
        self.clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}📜 Chat History{Colors.ENDC}")
        
        if not self.chat_history:
            print(f"{Colors.WARNING}No chat history yet. Start a conversation first!{Colors.ENDC}")
        else:
            for i, entry in enumerate(self.chat_history[-10:], 1):  # Show last 10
                print(f"\n{Colors.OKCYAN}[{entry['timestamp']}] You:{Colors.ENDC} {entry['query']}")
                print(f"{Colors.OKGREEN}🤖 Assistant:{Colors.ENDC} {entry['response'][:200]}{'...' if len(entry['response']) > 200 else ''}")
                print("─" * 60)
                
        input("\nPress Enter to continue...")
        
    def clear_database(self):
        """Clear the vector database to resolve issues."""
        print(f"{Colors.WARNING}🗑️ Clear Vector Database{Colors.ENDC}")
        print(f"{Colors.FAIL}⚠️ This will permanently delete all indexed documents!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}You will need to re-index your documents afterwards.{Colors.ENDC}")
        
        confirm = input(f"\n{Colors.BOLD}Are you sure? Type 'yes' to confirm: {Colors.ENDC}").strip().lower()
        
        if confirm == 'yes':
            try:
                import shutil
                from pathlib import Path
                
                db_path = Path("chroma_db")
                if db_path.exists():
                    shutil.rmtree(db_path)
                    print(f"{Colors.OKGREEN}✅ Database cleared successfully{Colors.ENDC}")
                else:
                    print(f"{Colors.WARNING}⚠️ Database directory not found{Colors.ENDC}")
                
                # Reset RAG system
                self.rag = None
                print(f"{Colors.OKCYAN}System reset. You can now try refreshing the index.{Colors.ENDC}")
                
            except Exception as e:
                print(f"{Colors.FAIL}❌ Error clearing database: {e}{Colors.ENDC}")
        else:
            print(f"{Colors.OKCYAN}Operation cancelled{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
        
    def clear_chat_history(self):
        """Clear the chat history."""
        print(f"{Colors.WARNING}🗑️ Clear Chat History{Colors.ENDC}")
        print(f"{Colors.FAIL}⚠️ This will permanently delete all chat history!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}The AI will lose all conversation context.{Colors.ENDC}")
        
        confirm = input(f"\n{Colors.BOLD}Are you sure? Type 'yes' to confirm: {Colors.ENDC}").strip().lower()
        
        if confirm == 'yes':
            history_count = len(self.chat_history)
            self.chat_history = []
            print(f"{Colors.OKGREEN}✅ Chat history cleared ({history_count} entries removed){Colors.ENDC}")
        else:
            print(f"{Colors.OKCYAN}Operation cancelled{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
        
    def system_info(self):
        self.clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}ℹ️ System Information{Colors.ENDC}")
        
        # Document info
        doc_count = 0
        file_count = 0
        if Path(self.documents_dir).exists():
            for file_path in Path(self.documents_dir).rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.md', '.py', '.js', '.json', '.csv']:
                    file_count += 1
                    
        if self.rag:
            doc_count = self.rag.collection.count()
            
        print(f"\n{Colors.OKBLUE}📁 Documents:{Colors.ENDC}")
        print(f"   Directory: {self.documents_dir}")
        print(f"   Files found: {file_count}")
        print(f"   Chunks indexed: {doc_count}")
        
        print(f"\n{Colors.OKBLUE}🤖 Model:{Colors.ENDC}")
        print(f"   Current: {self.current_model}")
        print(f"   Status: {'Available' if self.check_model_available() else 'Not available'}")
        
        print(f"\n{Colors.OKBLUE}💾 Session:{Colors.ENDC}")
        print(f"   Chat entries: {len(self.chat_history)}")
        print(f"   RAG initialized: {'Yes' if self.rag else 'No'}")
        
        # Show available models
        try:
            models = ollama.list()
            print(f"\n{Colors.OKBLUE}🎯 Available Models:{Colors.ENDC}")
            for model in models['models']:
                size_gb = model.size / (1024**3)
                print(f"   • {model.model} ({size_gb:.1f}GB)")
        except:
            print(f"\n{Colors.WARNING}⚠️ Could not fetch model list{Colors.ENDC}")
            
        input("\nPress Enter to continue...")
        
    def run(self):
        while True:
            self.print_header()
            self.print_status()
            self.print_menu()
            
            try:
                choice = input(f"{Colors.BOLD}Select option: {Colors.ENDC}").strip().lower()
                
                if choice == '1':
                    self.chat_mode()
                elif choice == '2':
                    self.refresh_index()
                elif choice == '3':
                    self.change_model()
                elif choice == '4':
                    self.view_history()
                elif choice == '5':
                    self.clear_chat_history()
                elif choice == '6':
                    self.system_info()
                elif choice == '7':
                    self.clear_database()
                elif choice in ['q', 'quit', 'exit']:
                    break
                else:
                    print(f"{Colors.WARNING}Invalid option. Try again.{Colors.ENDC}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
                
        print(f"\n{Colors.OKGREEN}👋 Goodbye!{Colors.ENDC}")

if __name__ == "__main__":
    ui = KnowledgeUI()
    ui.run()