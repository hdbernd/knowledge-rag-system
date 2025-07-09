#!/bin/bash

# Knowledge RAG UI Startup Script
# Quick launcher for the terminal UI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Knowledge RAG UI...${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run the setup first:${NC}"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install ollama chromadb sentence-transformers langchain langchain-community streamlit"
    exit 1
fi

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "${YELLOW}⚠️ Ollama service not running. Starting it...${NC}"
    if command -v brew >/dev/null 2>&1; then
        brew services start ollama
        echo -e "${GREEN}✅ Ollama started via Homebrew${NC}"
    else
        echo -e "${RED}❌ Please start Ollama manually: brew services start ollama${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if basic dependencies are installed
python -c "import ollama, chromadb, sentence_transformers" 2>/dev/null || {
    echo -e "${RED}❌ Dependencies not installed!${NC}"
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install ollama chromadb sentence-transformers langchain langchain-community streamlit
}

# Check if at least one model is available
echo -e "${BLUE}Checking available models...${NC}"
MODELS=$(ollama list 2>/dev/null | tail -n +2 | wc -l)
if [ "$MODELS" -eq 0 ]; then
    echo -e "${YELLOW}⚠️ No models found. Installing phi3:mini...${NC}"
    ollama pull phi3:mini
    echo -e "${GREEN}✅ phi3:mini installed${NC}"
else
    echo -e "${GREEN}✅ Found $MODELS model(s)${NC}"
fi

# Start the UI
echo -e "${GREEN}🚀 Launching Knowledge RAG UI...${NC}"
python ui.py