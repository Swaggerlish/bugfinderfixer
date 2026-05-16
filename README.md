# 🐛 Bug Finder & Fixer

A full-stack application for analyzing code, detecting bugs, security issues, and automatically generating improved code.

## 🌟 Features

### Backend (FastAPI)
- ✅ **Syntax Error Detection**: AST-based Python syntax validation
- 🔒 **Security Analysis**: Detects dangerous patterns (eval, exec, SQL injection, hardcoded passwords, etc.)
- 🎨 **Style Checking**: PEP 8 compliance, code formatting issues
- 💡 **Best Practices**: Missing docstrings, type hints, proper exception handling
- ✨ **Automatic Code Fixing**: Generates improved code with fixes applied
- 🔧 **Modular Architecture**: Easy to replace with AI-based analyzers
- 📚 **Interactive API Docs**: Swagger UI at `/docs`

### Frontend (React)
- 📝 **Code Editor**: Large textarea with syntax support
- 🔍 **Real-time Analysis**: Submit code to backend for instant analysis
- 🎯 **Categorized Issues**: Organized by type (syntax, security, style, best practices)
- 🚦 **Severity Levels**: Color-coded critical, warning, and info issues
- 💡 **Actionable Suggestions**: Clear recommendations for improvements
- 🔄 **Side-by-Side Comparison**: Original vs. fixed code
- 📋 **Copy to Clipboard**: Easy copying of improved code
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the server:
```bash
uvicorn main:app --reload
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Frontend will open at: http://localhost:3000

## ☁️ IBM watsonx Cloud Integration

This repo includes support for IBM watsonx in the backend. To enable it, set the following environment variables in your backend environment:

```bash
USE_AI_ANALYZER=true
WATSONX_API_KEY=<your-ibm-watsonx-api-key>
WATSONX_PROJECT_ID=<your-watsonx-project-id>
WATSONX_URL=<your-watsonx-service-url>
WATSONX_MODEL=ibm/granite-20b-code-instruct-v2
```

With these settings, the backend will route analysis through IBM watsonx and use a code-specialized model for more accurate bug fixing.

### Other API Options

If you want to replace or extend the AI integration, the backend is designed to support additional analysis APIs. You can swap in a different analyzer by updating `backend/routers/analyze.py` and implementing the analyzer interface in `backend/services/`.

Common API integrations include:
- IBM watsonx
- OpenAI GPT models
- Anthropic Claude
- Any custom web API that returns structured analysis results

## 📁 Project Structure

```
BugFinderFixer/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt           # Python dependencies
│   ├── routers/
│   │   ├── __init__.py
│   │   └── analyze.py            # Analysis endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base_analyzer.py      # Abstract analyzer interface
│   │   ├── code_analyzer.py      # Rule-based analyzer (default)
│   │   └── ai_analyzer.py        # AI analyzer stub
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CodeAnalyzer.js   # Main analyzer component
│   │   │   └── CodeAnalyzer.css  # Component styles
│   │   ├── App.js                # Main app component
│   │   ├── App.css               # App styles
│   │   └── index.js              # Entry point
│   ├── package.json
│   └── README.md
│
└── README.md                      # This file
```

## 🔧 API Documentation

### POST /api/analyze

Analyze code for issues and get improved version.

**Request:**
```json
{
  "code": "def example():\n    password = 'admin123'\n    print('Hello')",
  "language": "python"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Code analysis completed successfully",
  "issues": {
    "security_issues": [
      {
        "line": 2,
        "severity": "critical",
        "message": "Hardcoded password detected"
      }
    ],
    "style_issues": [
      {
        "line": 3,
        "severity": "info",
        "message": "Print statement found"
      }
    ]
  },
  "suggestions": [
    "Use environment variables for passwords",
    "Use logging instead of print"
  ],
  "fixed_code": "import os\nimport logging\n\ndef example():\n    password = os.getenv('PASSWORD')\n    logging.info('Hello')",
  "has_syntax_errors": false
}
```

## 🎯 Use Cases

1. **Code Review**: Automatically check code before commits
2. **Learning**: Understand best practices and security issues
3. **Refactoring**: Get suggestions for code improvements
4. **Security Audits**: Identify security vulnerabilities
5. **Style Enforcement**: Ensure code follows standards

## 🔒 Security Issues Detected

- Dangerous use of `eval()` and `exec()`
- Unsafe `pickle.load()` operations
- SQL injection vulnerabilities
- Hardcoded passwords and secrets
- Shell injection risks
- Bare except clauses

## 🎨 Style Issues Detected

- Missing docstrings
- Print statements (should use logging)
- Long lines (>100 characters)
- Inconsistent indentation
- TODO/FIXME comments

## 💡 Best Practices Checked

- Type hints presence
- Function documentation
- Proper exception handling
- Code organization

## 🔄 Modular Architecture

The analyzer uses an abstract base class pattern, making it easy to swap implementations:

```python
# Current: Rule-based
from services.code_analyzer import CodeAnalyzerService
analyzer = CodeAnalyzerService()

# Future: AI-based
from services.ai_analyzer import AICodeAnalyzer
analyzer = AICodeAnalyzer(api_key="your-key")
```

Both follow the same interface, enabling:
- Easy A/B testing
- Gradual migration to AI
- Multiple analyzer strategies

## 🚀 Future Enhancements

### Backend
- [ ] Support for more languages (JavaScript, Java, C++, etc.)
- [ ] Integration with AI models (OpenAI, Claude)
- [ ] Custom rule configuration
- [ ] Batch file analysis
- [ ] Performance profiling
- [ ] Code complexity metrics

### Frontend
- [ ] Syntax highlighting in editor
- [ ] Dark mode
- [ ] Save/load code snippets
- [ ] Export analysis reports (PDF, JSON)
- [ ] Real-time analysis as you type
- [ ] Multiple file upload
- [ ] GitHub integration
- [ ] Diff view for changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 👥 Authors

Built with ❤️ using FastAPI and React

## 🙏 Acknowledgments

- FastAPI for the excellent backend framework
- React for the powerful frontend library
- Python AST module for syntax parsing

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation in `/backend/README.md` and `/frontend/README.md`

---

**Happy Coding! 🎉**