# Contributing to Knowledge RAG System

Thank you for your interest in contributing to the Knowledge RAG System! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/knowledge-rag.git
   cd knowledge-rag
   ```

3. **Set up development environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Install development dependencies**:
   ```bash
   pip install pytest black flake8 mypy
   ```

5. **Run tests** to ensure everything works:
   ```bash
   python test_basic.py
   ```

## 🎯 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating issues
3. **Include system information**:
   - OS and version
   - Python version
   - Ollama version
   - Model being used
   - Error messages and logs

### Suggesting Features

1. **Check existing feature requests** first
2. **Use the feature request template**
3. **Describe the use case** clearly
4. **Consider backwards compatibility**

### Code Contributions

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Test thoroughly**:
   ```bash
   python test_basic.py
   pytest  # If you add unit tests
   ```

6. **Submit a pull request**

## 📝 Coding Standards

### Code Style

- **Follow PEP 8** for Python code style
- **Use Black** for code formatting:
  ```bash
  black *.py
  ```
- **Use meaningful variable names**
- **Add docstrings** for functions and classes
- **Keep functions focused** and small

### Code Quality

- **Run linting** before submitting:
  ```bash
  flake8 *.py
  ```
- **Type hints** are encouraged:
  ```bash
  mypy *.py
  ```
- **Handle errors gracefully**
- **Add logging** where appropriate

### Example Code Structure

```python
#!/usr/bin/env python3
"""
Module description here.
"""

import os
import sys
from typing import List, Dict, Any

class ExampleClass:
    """Class description."""
    
    def __init__(self, param: str):
        """Initialize with parameter."""
        self.param = param
        
    def example_method(self, data: List[str]) -> Dict[str, Any]:
        """
        Method description.
        
        Args:
            data: Input data description
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When something goes wrong
        """
        if not data:
            raise ValueError("Data cannot be empty")
            
        return {"result": "success"}
```

## 🧪 Testing

### Running Tests

```bash
# Basic system test
python test_basic.py

# Unit tests (if available)
pytest

# Test specific functionality
python knowledge_rag.py --model phi3:mini --query "test query"
```

### Writing Tests

- **Test new features** you add
- **Test edge cases** and error conditions
- **Use descriptive test names**
- **Keep tests independent**

Example test structure:
```python
def test_document_loading():
    """Test document loading functionality."""
    rag = KnowledgeRAG()
    documents = rag.load_documents()
    assert len(documents) > 0
    assert documents[0].page_content is not None
```

## 📚 Documentation

### README Updates

- **Update installation instructions** if needed
- **Add new features** to the features list
- **Update usage examples** for new functionality
- **Keep the table of contents** current

### Code Documentation

- **Add docstrings** for all public functions
- **Include examples** in docstrings when helpful
- **Document parameters** and return values
- **Explain complex algorithms**

### Comments

- **Explain why**, not what
- **Keep comments up to date**
- **Remove commented-out code**
- **Use TODO comments** for future improvements

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes** thoroughly
2. **Update documentation** as needed
3. **Run code formatting**:
   ```bash
   black *.py
   flake8 *.py
   ```
4. **Check for breaking changes**
5. **Update CHANGELOG** if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** by reviewers
4. **Merge** after approval

## 🌟 Feature Ideas

Current priority areas for contributions:

### High Priority
- [ ] **PDF document support** - Add PDF parsing capabilities
- [ ] **Multi-language models** - Support for different languages
- [ ] **Document versioning** - Track document changes
- [ ] **Export conversations** - Save chat history

### Medium Priority
- [ ] **API server mode** - REST API for programmatic access
- [ ] **Docker containerization** - Easy deployment
- [ ] **Batch processing** - Process multiple documents at once
- [ ] **Configuration file** - YAML/JSON config support

### Low Priority
- [ ] **Plugin system** - Extensible architecture
- [ ] **Monitoring dashboard** - Usage statistics
- [ ] **Document clustering** - Organize similar documents
- [ ] **Scheduled indexing** - Automatic document updates

## 📞 Getting Help

### Communication Channels

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For general questions
- **Pull Request Comments** - For code-specific discussions

### Response Times

- **Bug reports**: Within 48 hours
- **Feature requests**: Within 1 week
- **Pull requests**: Within 1 week

## 🎖️ Recognition

Contributors will be:
- **Listed in the README** contributors section
- **Mentioned in release notes** for significant contributions
- **Invited to be maintainers** for consistent, quality contributions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Knowledge RAG System! 🙏**