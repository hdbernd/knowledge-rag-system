#!/usr/bin/env python3
"""
Cross-platform Python launcher for Knowledge RAG UI
Alternative to the bash script for better compatibility
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_colored(text, color=''):
    colors = {
        'red': '\033[0;31m',
        'green': '\033[0;32m',
        'yellow': '\033[1;33m',
        'blue': '\033[0;34m',
        'cyan': '\033[0;36m',
        'reset': '\033[0m'
    }
    
    if color in colors:
        print(f"{colors[color]}{text}{colors['reset']}")
    else:
        print(text)

def check_command_exists(command):
    """Check if a command exists in PATH"""
    return shutil.which(command) is not None

def is_ollama_running():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(['pgrep', 'ollama'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        # Try alternative method for Windows/other systems
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False

def start_ollama():
    """Start Ollama service"""
    print_colored("⚠️ Ollama service not running. Starting it...", 'yellow')
    
    if check_command_exists('brew'):
        try:
            subprocess.run(['brew', 'services', 'start', 'ollama'], check=True)
            print_colored("✅ Ollama started via Homebrew", 'green')
            return True
        except subprocess.CalledProcessError:
            pass
    
    print_colored("❌ Could not start Ollama automatically.", 'red')
    print_colored("Please start Ollama manually:", 'yellow')
    print("   brew services start ollama")
    print("   OR")
    print("   ollama serve")
    return False

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = ['ollama', 'chromadb', 'sentence_transformers', 'langchain']
    
    try:
        for package in required_packages:
            __import__(package)
        return True
    except ImportError as e:
        print_colored(f"❌ Missing package: {e.name}", 'red')
        return False

def install_packages():
    """Install required packages"""
    print_colored("Installing required packages...", 'yellow')
    packages = [
        'ollama', 'chromadb', 'sentence-transformers', 
        'langchain', 'langchain-community', 'streamlit'
    ]
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install'
        ] + packages, check=True)
        print_colored("✅ Packages installed successfully", 'green')
        return True
    except subprocess.CalledProcessError:
        print_colored("❌ Failed to install packages", 'red')
        return False

def check_models():
    """Check if any models are available"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            # Skip header line, count remaining
            model_count = len([line for line in lines[1:] if line.strip()])
            return model_count
        return 0
    except:
        return 0

def install_default_model():
    """Install phi3:mini as default model"""
    print_colored("⚠️ No models found. Installing phi3:mini...", 'yellow')
    try:
        subprocess.run(['ollama', 'pull', 'phi3:mini'], check=True)
        print_colored("✅ phi3:mini installed", 'green')
        return True
    except subprocess.CalledProcessError:
        print_colored("❌ Failed to install phi3:mini", 'red')
        return False

def main():
    print_colored("🚀 Starting Knowledge RAG UI...", 'blue')
    
    # Get script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check virtual environment
    venv_path = script_dir / 'venv'
    if not venv_path.exists():
        print_colored("❌ Virtual environment not found!", 'red')
        print_colored("Please run the setup first:", 'yellow')
        print("   python3 -m venv venv")
        if os.name == 'nt':  # Windows
            print("   venv\\Scripts\\activate")
        else:  # Unix/Linux/macOS
            print("   source venv/bin/activate")
        print("   pip install ollama chromadb sentence-transformers langchain langchain-community streamlit")
        return 1
    
    # Activate virtual environment
    if os.name == 'nt':  # Windows
        activate_script = venv_path / 'Scripts' / 'activate.bat'
        python_exe = venv_path / 'Scripts' / 'python.exe'
    else:  # Unix/Linux/macOS
        activate_script = venv_path / 'bin' / 'activate'
        python_exe = venv_path / 'bin' / 'python'
    
    if not python_exe.exists():
        print_colored("❌ Python executable not found in virtual environment!", 'red')
        return 1
    
    print_colored("Activating virtual environment...", 'blue')
    
    # Check if Ollama is running
    if not is_ollama_running():
        if not start_ollama():
            return 1
        
        # Wait a moment for Ollama to start
        import time
        time.sleep(2)
    
    # Check Python packages (using the venv python)
    check_cmd = [str(python_exe), '-c', 'import ollama, chromadb, sentence_transformers']
    result = subprocess.run(check_cmd, capture_output=True)
    
    if result.returncode != 0:
        print_colored("❌ Dependencies not installed!", 'red')
        print_colored("Installing dependencies...", 'yellow')
        
        install_cmd = [
            str(python_exe), '-m', 'pip', 'install',
            'ollama', 'chromadb', 'sentence-transformers', 
            'langchain', 'langchain-community', 'streamlit'
        ]
        
        install_result = subprocess.run(install_cmd)
        if install_result.returncode != 0:
            print_colored("❌ Failed to install dependencies!", 'red')
            return 1
    
    # Check models
    print_colored("Checking available models...", 'blue')
    model_count = check_models()
    
    if model_count == 0:
        if not install_default_model():
            print_colored("⚠️ No models available. You can install one later with:", 'yellow')
            print("   ollama pull phi3:mini")
    else:
        print_colored(f"✅ Found {model_count} model(s)", 'green')
    
    # Start the UI
    print_colored("🚀 Launching Knowledge RAG UI...", 'green')
    try:
        subprocess.run([str(python_exe), 'ui.py'], check=True)
    except subprocess.CalledProcessError:
        print_colored("❌ Failed to start UI", 'red')
        return 1
    except KeyboardInterrupt:
        print_colored("\n👋 Goodbye!", 'green')
        return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())