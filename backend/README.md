# Bug Finder & Fixer - Backend API

FastAPI backend for analyzing code and detecting potential bugs.

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── routers/               # API route handlers
│   ├── __init__.py
│   └── analyze.py         # Code analysis endpoints
└── services/              # Business logic layer
    ├── __init__.py
    ├── base_analyzer.py   # Abstract base class for analyzers
    ├── code_analyzer.py   # Rule-based code analysis (default)
    └── ai_analyzer.py     # AI-based analyzer (stub for future use)
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source venv/bin/activate
  ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

### POST /api/analyze
Analyze code for potential bugs and issues.

**Request Body:**
```json
{
  "code": "def add(a, b):\n    return a + b",
  "language": "python"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Code analysis completed successfully",
  "issues": {
    "syntax_errors": [],
    "security_issues": [],
    "style_issues": [
      {"line": 1, "severity": "info", "message": "Missing docstring in function"}
    ],
    "best_practices": [
      {"line": 1, "severity": "info", "message": "Missing type hints"}
    ]
  },
  "suggestions": [
    "Add docstring to document function purpose and parameters",
    "Add type hints: def func(x: int) -> str:"
  ],
  "fixed_code": "def add(a: int, b: int) -> int:\n    \"\"\"Function description.\"\"\"\n    return a + b",
  "has_syntax_errors": false
}
```

### GET /
Root endpoint - API information

### GET /health
Health check endpoint

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:3000 (React frontend default)

To add more origins, modify the `allow_origins` list in `main.py`.

## Features

### Code Analysis Capabilities

The analyzer detects:

1. **Syntax Errors**: Uses Python AST parsing to catch syntax issues
2. **Security Issues**:
   - Dangerous use of `eval()` and `exec()`
   - Unsafe `pickle.load()` usage
   - SQL injection vulnerabilities
   - Hardcoded passwords
   - Shell injection risks
3. **Style Issues**:
   - Print statements (should use logging)
   - TODO/FIXME comments
   - Long lines (>100 chars)
4. **Best Practices**:
   - Missing docstrings
   - Bare except clauses
   - Missing type hints

### Automatic Code Fixing

The analyzer generates improved code by:
- Replacing `eval()` with `ast.literal_eval()`
- Converting bare `except:` to `except Exception as e:`
- Replacing `print()` with `logging.info()`
- Adding basic docstrings to functions
- Replacing hardcoded passwords with environment variables

## Architecture

### Modular Design

The analyzer uses an abstract base class (`BaseCodeAnalyzer`) that allows easy replacement with different implementations:

```python
# Current: Rule-based analyzer
from services.code_analyzer import CodeAnalyzerService
analyzer = CodeAnalyzerService()

# Future: AI-based analyzer
from services.ai_analyzer import AICodeAnalyzer
analyzer = AICodeAnalyzer(api_key="your-key")
```

Both implementations follow the same interface, making it easy to:
- Switch between analyzers
- A/B test different approaches
- Integrate AI models (OpenAI, Claude, etc.)

### Project Structure

- **routers/**: API route definitions
- **services/**: Business logic and analyzer implementations
  - `base_analyzer.py`: Abstract interface
  - `code_analyzer.py`: Rule-based implementation (default)
  - `ai_analyzer.py`: Stub for AI integration
- **main.py**: Application configuration and middleware

### Adding New Features

1. Create a new router in `routers/`
2. Create corresponding service in `services/`
3. Register the router in `main.py`

### Replacing the Analyzer

To use a different analyzer implementation:

1. Create a new class inheriting from `BaseCodeAnalyzer`
2. Implement the `analyze()` method
3. Update `routers/analyze.py` to use your analyzer:
   ```python
   from services.your_analyzer import YourAnalyzer
   analyzer = YourAnalyzer()
   ```