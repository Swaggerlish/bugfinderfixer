from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os
from services.code_analyzer import CodeAnalyzerService

router = APIRouter()

# Determine which analyzer to use based on environment
USE_AI = os.getenv("USE_AI_ANALYZER", "false").lower() == "true"

# Only import watsonx if AI is enabled
if USE_AI:
    try:
        from services.watsonx_analyzer import WatsonxCodeAnalyzer
    except ImportError:
        print("Warning: ibm-watsonx-ai not installed. Falling back to rule-based analyzer.")
        USE_AI = False

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="The code to analyze")
    language: Optional[str] = Field(default="python", description="Programming language of the code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "def add(a, b):\n    return a + b",
                "language": "python"
            }
        }

class CodeAnalysisResponse(BaseModel):
    success: bool
    message: str
    issues: dict = {}
    suggestions: list = []
    fixed_code: Optional[str] = None
    has_syntax_errors: bool = False
    normalized_language: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Code analysis completed",
                "issues": {
                    "security_issues": [
                        {"line": 5, "severity": "critical", "message": "Dangerous use of eval()"}
                    ],
                    "style_issues": [
                        {"line": 10, "severity": "info", "message": "Print statement found"}
                    ]
                },
                "suggestions": [
                    "Avoid eval(). Use ast.literal_eval() for safe evaluation",
                    "Use logging module instead of print"
                ],
                "fixed_code": "import ast\nimport logging\n\ndef safe_func():\n    ...",
                "has_syntax_errors": False,
                "normalized_language": "python"
            }
        }

@router.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze code for potential bugs and issues.
    
    - **code**: The source code to analyze
    - **language**: Programming language (default: python)
    """
    try:
        if not request.code or not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        # Choose analyzer based on configuration
        if USE_AI:
            try:
                # Use AI-powered watsonx analyzer
                from services.watsonx_analyzer import WatsonxCodeAnalyzer
                analyzer = WatsonxCodeAnalyzer()
                analysis_type = "AI-powered (watsonx)"
            except Exception as e:
                # Fallback to rule-based if AI fails
                print(f"AI analyzer failed: {e}. Using rule-based analyzer.")
                analyzer = CodeAnalyzerService()
                analysis_type = "Rule-based (AI unavailable)"
        else:
            # Use rule-based analyzer
            analyzer = CodeAnalyzerService()
            analysis_type = "Rule-based"
        
        result = analyzer.analyze(request.code, request.language or "python")
        
        # Add analyzer type to suggestions
        suggestions = result.get("suggestions", [])
        suggestions.insert(0, f"Analysis type: {analysis_type}")
        
        return CodeAnalysisResponse(
            success=True,
            message="Code analysis completed successfully",
            issues=result.get("issues", {}),
            suggestions=suggestions,
            fixed_code=result.get("fixed_code"),
            has_syntax_errors=result.get("has_syntax_errors", False),
            normalized_language=result.get("normalized_language", request.language or "python")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Made with Bob
