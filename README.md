# 🤖 Knowledge RAG System

A completely local AI-powered tool for natural language interaction with your documents using Ollama and ChromaDB. Chat with your files using state-of-the-art language models without sending any data to external services.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/yourusername/knowledge-rag)

## ✨ Features

- **🔒 100% Local & Private**: No data leaves your machine - complete privacy
- **📚 Multiple File Types**: Supports .txt, .md, .py, .js, .json, .csv files
- **🧠 Semantic Search**: Advanced document retrieval using sentence transformers
- **💬 Multiple Interfaces**: Terminal UI, Web UI, and Command Line
- **🚀 Apple Silicon Optimized**: Runs efficiently on M1/M2/M4 MacBook Pro
- **🎯 Context-Aware**: Provides accurate answers based on your document content
- **🧵 Conversational Memory**: Maintains context across questions for natural follow-ups
- **⚡ Fast Response**: Optimized for quick document search and AI inference
- **🔧 Model Flexibility**: Support for multiple Ollama models (3B to 70B parameters)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/knowledge-rag.git
cd knowledge-rag
```

### 2. One-Command Setup & Launch
```bash
# This handles everything: dependencies, models, and launches the UI
./start_ui.sh
```

### 3. Quick Launch Scripts
```bash
# Terminal UI (interactive chat) - auto-initializes RAG system
./run_term

# Web UI (browser interface) - auto-initializes RAG system
./run_ui
```

**That's it!** The script will:
- Install Ollama if needed
- Create virtual environment
- Install Python dependencies  
- Download a default AI model
- Launch the Terminal UI

## 🛠️ Manual Installation

If you prefer manual setup or the quick start doesn't work:

### Prerequisites
- **macOS/Linux/Windows** with Python 3.8+
- **8GB+ RAM** (48GB+ recommended for best performance)
- **5GB+ free disk space** (for models and dependencies)

### Step 1: Install Ollama
```bash
# macOS (recommended)
brew install ollama
brew services start ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### Step 2: Download AI Models

**🚀 Recommended for M4 MacBook Pro (48GB RAM):**
```bash
# Top choices for your system
ollama pull qwen2.5:72b        # 45GB - Best overall quality
ollama pull llama3.1:70b       # 42GB - Excellent general use
ollama pull mixtral:8x7b       # 26GB - Great mixture of experts
ollama pull deepseek-coder:33b # 20GB - Best for code analysis
```

**⚡ Fast Models (for quick testing):**
```bash
ollama pull phi3:mini          # 3GB - Quick questions
ollama pull llama3.2:3b        # 2GB - Faster, newer
ollama pull llama3.2:1b        # 1GB - Ultra-fast
```

**🎯 Balanced Models (good performance/size ratio):**
```bash
ollama pull qwen2.5:14b        # 8GB - Excellent reasoning
ollama pull llama3.1:8b        # 6GB - Reliable all-rounder
ollama pull qwen2.5:7b         # 4GB - Great coding, multilingual
ollama pull mistral:7b         # 4GB - Strong general performance
```

**🔧 Code-Specialized Models:**
```bash
ollama pull deepseek-coder:6.7b # 4GB - Code analysis
ollama pull codellama:13b       # 8GB - Code generation
ollama pull codellama:34b       # 20GB - Professional coding
```

### Step 3: Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install ollama chromadb sentence-transformers langchain langchain-community streamlit
```

### Step 4: Add Your Documents
```bash
# Add your files to the documents directory
cp your_research.md documents/
cp your_notes.txt documents/
cp *.py documents/  # Add code files
```

### Step 5: Launch the System
```bash
# Terminal UI (recommended)
python ui.py

# Web interface
streamlit run streamlit_app.py

# Command line
python knowledge_rag.py --model phi3:mini --query "Your question"
```

## 🖥️ Interface Options

### 🎯 Terminal UI (Recommended)
```bash
./run_term     # Quick launcher (recommended) - auto-initializes RAG
# OR
./start_ui.sh  # Original launcher
# OR
python ui.py   # Manual start
```

**Features:**
- Interactive chat with your documents
- Real-time document index refresh
- Model switching on the fly
- Chat history and system info
- Conversational context memory
- Clear chat history option
- Colored, user-friendly interface
- **Auto-initialization**: RAG system ready immediately

**Main Menu:**
```
╔══════════════════════════════════════════════════════╗
║                 🤖 Knowledge RAG UI                  ║
║           Chat with your documents locally           ║
╚══════════════════════════════════════════════════════╝

📊 System Status:
   Model: phi3:mini (✅ Ready)
   Documents: 1,247 chunks indexed
   Directory: documents

🎯 Quick Actions:
   1 - Chat with documents
   2 - Refresh document index
   3 - Change model  
   4 - View chat history
   5 - Clear chat history
   6 - System info
   7 - Clear database (if issues)
   q - Quit
```

### 🌐 Web Interface
```bash
./run_ui       # Quick launcher (recommended) - auto-initializes RAG
# OR
streamlit run streamlit_app.py  # Manual start
# Opens at http://localhost:8501
```

**Features:**
- Beautiful browser-based chat interface
- Sidebar with system controls
- Real-time status indicators
- Easy document management
- **Auto-initialization**: RAG system ready immediately

### 💻 Command Line Interface
```bash
# Interactive chat with conversation memory
python knowledge_rag.py --model phi3:mini

# Single queries
python knowledge_rag.py --model phi3:mini --query "What is machine learning?"

# Index documents only
python knowledge_rag.py --index
```

## 📁 Repository Structure

```
knowledge-rag/
├── 🎯 Core System
│   ├── knowledge_rag.py      # Main RAG engine
│   ├── ui.py                 # Terminal UI
│   └── streamlit_app.py      # Web interface
├── 🚀 Launchers  
│   ├── start_ui.sh           # Quick bash launcher
│   └── start_ui.py           # Cross-platform Python launcher
├── 📚 Documents
│   ├── documents/            # Your documents go here
│   │   ├── .gitkeep         # Keeps directory in git
│   │   ├── sample_ai_info.txt      # Example file
│   │   └── programming_basics.md   # Example file
│   └── chroma_db/           # Vector database (auto-created)
├── 🧪 Testing
│   └── test_basic.py        # System tests
├── ⚙️ Configuration
│   ├── .gitignore           # Git ignore rules
│   ├── requirements.txt     # Python dependencies (optional)
│   └── venv/               # Virtual environment (created by setup)
└── 📖 Documentation
    └── README.md           # This file
```

## 🔧 Configuration

### Model Selection Guide

Choose the right model based on your hardware and quality needs:

| Model | RAM | Speed | Quality | Best For |
|-------|-----|-------|---------|----------|
| **phi3:mini** | 3GB | ⚡⚡⚡ | ⭐⭐ | Quick questions, testing |
| **llama3.1:8b** | 6GB | ⚡⚡ | ⭐⭐⭐ | Balanced use, technical docs |
| **llama3.1:70b** | 42GB | ⚡ | ⭐⭐⭐⭐⭐ | Complex analysis, best quality |
| **llama3.2:3b** | 2GB | ⚡⚡⚡ | ⭐⭐ | Faster than phi3, newer |
| **llama3.2:1b** | 1GB | ⚡⚡⚡⚡ | ⭐ | Ultra-fast, basic queries |
| **qwen2.5:7b** | 4GB | ⚡⚡ | ⭐⭐⭐ | Excellent coding, multilingual |
| **qwen2.5:14b** | 8GB | ⚡⚡ | ⭐⭐⭐⭐ | Better reasoning, math |
| **qwen2.5:32b** | 20GB | ⚡ | ⭐⭐⭐⭐⭐ | Advanced reasoning, analysis |
| **qwen2.5:72b** | 45GB | ⚡ | ⭐⭐⭐⭐⭐ | Top-tier quality, your 48GB ideal |
| **deepseek-coder:6.7b** | 4GB | ⚡⚡ | ⭐⭐⭐ | Specialized for code analysis |
| **deepseek-coder:33b** | 20GB | ⚡ | ⭐⭐⭐⭐⭐ | Advanced code understanding |
| **codellama:7b** | 4GB | ⚡⚡ | ⭐⭐⭐ | Meta's code specialist |
| **codellama:13b** | 8GB | ⚡⚡ | ⭐⭐⭐⭐ | Better code generation |
| **codellama:34b** | 20GB | ⚡ | ⭐⭐⭐⭐⭐ | Professional code analysis |
| **mistral:7b** | 4GB | ⚡⚡ | ⭐⭐⭐ | Great general performance |
| **mixtral:8x7b** | 26GB | ⚡ | ⭐⭐⭐⭐⭐ | Mixture of experts, excellent |
| **mixtral:8x22b** | 80GB | ⚡ | ⭐⭐⭐⭐⭐ | Largest mixture model (needs >80GB) |

### Supported Document Types

- **Text files**: `.txt`, `.md`
- **Code files**: `.py`, `.js`, `.json`  
- **Data files**: `.csv`
- **Documentation**: `.md`, `.txt`

*Easy to extend for PDF, DOCX, and other formats*

### Adding Your Documents

```bash
# Simply copy files to the documents directory
cp ~/Documents/research/* documents/
cp ~/Desktop/notes.md documents/
cp project/*.py documents/

# The system will automatically detect and index them
# Or manually refresh with option 2 in the Terminal UI
```

## 🧵 Conversational Context

The system now maintains conversation context, allowing for natural follow-up questions:

### How It Works
```
You: What is the stock service?
🤖: The stock service manages inventory levels and handles reservations...

You: How does it work?
🤖: The stock service works by maintaining atomic operations for...

You: What are its main components?
🤖: The stock service has three main components: the domain service...
```

### Managing Conversation History

**Terminal UI:**
- **View History**: Option 4 - See your last 10 conversations
- **Clear History**: Option 5 - Clear all conversation context
- **Automatic Management**: Keeps last 50 exchanges, uses last 5 for context

**Command Line:**
- **Clear History**: Type `clear` during interactive chat
- **View Commands**: Type `help` to see available commands

### Memory Management

- **Context Window**: Last 5 exchanges included in AI prompt
- **Storage Limit**: Maximum 50 exchanges stored per session
- **Automatic Cleanup**: Older conversations automatically removed
- **Session Reset**: History cleared when changing models or restarting

## 🎯 Usage Examples

### Terminal UI Workflow
```bash
./start_ui.sh
# Select: 1 (Chat with documents)
You: What are the main components of the system architecture?
🤖 Assistant: Based on your documents, the main components include...

You: How do they interact with each other?
🤖 Assistant: The components interact through... [understands "they" = main components]

You: What about error handling?
🤖 Assistant: For error handling in these components... [maintains context]

You: back
# Returns to main menu
# Select: 2 (Refresh index) - if you added new documents
# Select: 3 (Change model) - to switch to llama3.1:70b for better quality
# Select: 5 (Clear chat history) - to start fresh conversation
```

### Command Line Workflow
```bash
# Quick questions
python knowledge_rag.py --model phi3:mini --query "What microservices are mentioned?"

# Best quality analysis (recommended for your 48GB system)
python knowledge_rag.py --model qwen2.5:72b --query "Analyze the integration patterns and explain trade-offs"

# Code analysis with specialized model
python knowledge_rag.py --model deepseek-coder:33b --query "Explain the error handling patterns in the codebase"

# Interactive exploration with balanced model (with conversation context)
python knowledge_rag.py --model mixtral:8x7b
You: Explain the error handling approach
You: What are the key design decisions behind it?  # "it" = error handling
You: How do these systems communicate errors?      # maintains context
You: clear                                        # clear conversation history
You: What is the stock service?                   # fresh start
```

### Power User Tips

**Bash Aliases:**
```bash
# Add to ~/.zshrc or ~/.bash_profile
alias krag='cd /path/to/knowledge-rag && ./start_ui.sh'
alias kask='cd /path/to/knowledge-rag && source venv/bin/activate && python knowledge_rag.py --model phi3:mini --query'

# Usage
kask "What is the stock service architecture?"
```

**Automation:**
```bash
# Save answers to files
python knowledge_rag.py --model phi3:mini --query "Summarize all services" > summary.txt

# Batch processing
for question in "What is X?" "How does Y work?" "Explain Z"; do
    python knowledge_rag.py --model phi3:mini --query "$question"
done
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your Files    │───▶│  ChromaDB        │───▶│   Ollama LLM    │
│   (.txt, .md)   │    │  (Vector Store)  │    │   (phi3:mini)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Text Splitter   │    │ Sentence Trans.  │    │ Response Gen.   │
│ (LangChain)     │    │ (Embeddings)     │    │ (Local AI)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Data Flow:**
1. **Document Ingestion**: Files are loaded and split into chunks
2. **Embedding Generation**: Text chunks converted to vectors  
3. **Vector Storage**: Embeddings stored in ChromaDB
4. **Query Processing**: User questions converted to vectors
5. **Similarity Search**: Relevant document chunks retrieved
6. **Context Assembly**: Combines document context + conversation history
7. **Response Generation**: Local LLM generates answers using full context

## 📊 Performance & Optimization

### For M1/M2/M4 MacBooks
- **Recommended**: llama3.1:70b for best quality (requires 48GB+ RAM)
- **Chunk size**: 1000-2000 tokens for optimal context
- **Concurrent queries**: Fully supported
- **Large document sets**: Handles 10,000+ documents efficiently

### Memory Usage Guidelines

**🎯 For Your M4 MacBook Pro (48GB RAM):**
| Model | Memory Usage | Best Use Case |
|-------|--------------|---------------|
| **qwen2.5:72b** | ~45GB RAM | 🏆 Best overall quality |
| **llama3.1:70b** | ~42GB RAM | 🎯 Excellent for analysis |
| **mixtral:8x7b** | ~26GB RAM | ⚡ Great speed/quality balance |
| **deepseek-coder:33b** | ~20GB RAM | 💻 Best for code analysis |
| **qwen2.5:32b** | ~20GB RAM | 🧠 Advanced reasoning |
| **qwen2.5:14b** | ~8GB RAM | 📊 Good for complex queries |
| **llama3.1:8b** | ~6GB RAM | 🔄 Reliable all-rounder |
| **qwen2.5:7b** | ~4GB RAM | 🌐 Multilingual, coding |
| **phi3:mini** | ~3GB RAM | ⚡ Quick questions |

**🗄️ System Components:**
| Component | Memory Usage |
|-----------|--------------|
| **ChromaDB** | ~100MB per 1000 documents |
| **Embeddings** | ~50MB per 1000 documents |
| **UI System** | ~200MB base |

### Performance Tips
- **Use SSD storage** for faster document loading
- **Close other apps** when using 70B model
- **Batch document additions** for efficient indexing
- **Use appropriate chunk sizes** for your document types

## 🔐 Privacy & Security

- **🔒 Completely Local**: No data ever leaves your machine
- **🚫 No Telemetry**: No usage tracking or analytics
- **🔐 Secure Storage**: Documents stored locally in plain text
- **🛡️ No API Keys**: No external service dependencies
- **🕵️ Private by Design**: Perfect for sensitive business documents

## 🐛 Troubleshooting

### Common Issues & Solutions

**❌ "Model not found" error**
```bash
ollama pull phi3:mini
ollama list  # Verify installation
```

**💬 Conversation not maintaining context**
```bash
# Make sure you're using the interactive mode for conversation memory
python knowledge_rag.py --model phi3:mini  # Interactive mode (has memory)
# vs
python knowledge_rag.py --model phi3:mini --query "question"  # Single query (no memory)
```

**❌ Memory issues with large models**
```bash
# Use smaller model
python knowledge_rag.py --model phi3:mini
# Or increase system memory/swap
```

**❌ "No documents found"**
```bash
# Check file extensions and location
ls documents/
# Ensure files are .txt, .md, .py, .js, .json, or .csv
```

**❌ Slow performance**
```bash
# Restart Ollama
brew services restart ollama
# Check system resources
htop
```

**❌ Port conflicts (Streamlit)**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**❌ ChromaDB batch size errors**
```bash
# The system now automatically handles large document collections
# If you still get batch size errors, try clearing the database:
rm -rf chroma_db/
python knowledge_rag.py --index
```

**❌ ChromaDB permission errors**
```bash
# Clear database and reindex
rm -rf chroma_db/
python knowledge_rag.py --index
```

### Debug Mode
```bash
# Enable verbose logging
python knowledge_rag.py --model phi3:mini --query "test" --verbose
```

### Conversation Commands
```bash
# Interactive mode commands
python knowledge_rag.py --model phi3:mini
You: What is the stock service?     # Ask questions
You: How does it work?              # Follow-up questions maintain context
You: clear                          # Clear conversation history
You: reindex                        # Refresh document index
You: quit                           # Exit
```

### Getting Help
1. Check this troubleshooting section
2. Run the test script: `python test_basic.py`
3. Check Ollama status: `ollama list`
4. Verify Python environment: `which python`

## 🔄 Updates & Maintenance

### Update Models
```bash
# Update existing models
ollama pull phi3:mini      # Update to latest version
ollama pull llama3.1:8b    # Update to latest version
ollama pull qwen2.5:72b    # Update top-tier model
```

### Download More Powerful Models
```bash
# 🏆 Most Powerful Models (for your 48GB system)
ollama pull qwen2.5:72b        # 45GB - Best overall performance
ollama pull llama3.1:70b       # 42GB - Excellent reasoning
ollama pull mixtral:8x7b       # 26GB - Great mixture of experts

# 💻 Code-Specialized Models
ollama pull deepseek-coder:33b # 20GB - Advanced code analysis
ollama pull codellama:34b      # 20GB - Professional coding
ollama pull deepseek-coder:6.7b # 4GB - Lighter code model

# 🧠 Advanced Reasoning Models
ollama pull qwen2.5:32b        # 20GB - Advanced reasoning
ollama pull qwen2.5:14b        # 8GB - Good reasoning, fits with other apps
ollama pull qwen2.5:7b         # 4GB - Multilingual, coding

# 🚀 Newer Fast Models
ollama pull llama3.2:3b        # 2GB - Faster than phi3
ollama pull llama3.2:1b        # 1GB - Ultra-fast
```

### Update Dependencies
```bash
source venv/bin/activate
pip install --upgrade ollama chromadb sentence-transformers langchain streamlit
```

### Backup Your Setup
```bash
# Backup documents (if not in git)
tar -czf documents_backup.tar.gz documents/

# Export model list
ollama list > installed_models.txt
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** with tests
4. **Follow the existing code style**
5. **Submit a pull request**

### Development Setup
```bash
git clone https://github.com/yourusername/knowledge-rag.git
cd knowledge-rag
python -m venv venv
source venv/bin/activate
pip install -e .
python test_basic.py
```

### Feature Ideas
- [ ] PDF document support
- [ ] Multi-language models
- [ ] Document versioning
- [ ] Export conversations
- [ ] API server mode
- [ ] Docker containerization

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Ollama](https://ollama.ai/)**: For local LLM inference
- **[ChromaDB](https://www.trychroma.com/)**: For vector storage and retrieval
- **[LangChain](https://python.langchain.com/)**: For document processing
- **[Sentence Transformers](https://www.sbert.net/)**: For text embeddings
- **[Streamlit](https://streamlit.io/)**: For the web interface

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/knowledge-rag&type=Date)](https://star-history.com/#yourusername/knowledge-rag&Date)

---

**Built with ❤️ for local AI and privacy**

*Questions? Issues? Check out our [FAQ](FAQ.md) or open an [issue](https://github.com/yourusername/knowledge-rag/issues).*