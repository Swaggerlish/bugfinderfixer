from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from services.code_analyzer import CodeAnalyzerService

router = APIRouter()

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
                "has_syntax_errors": False
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
        
        # Use the code analyzer service
        analyzer = CodeAnalyzerService()
        result = analyzer.analyze(request.code, request.language or "python")
        
        return CodeAnalysisResponse(
            success=True,
            message="Code analysis completed successfully",
            issues=result.get("issues", {}),
            suggestions=result.get("suggestions", []),
            fixed_code=result.get("fixed_code"),
            has_syntax_errors=result.get("has_syntax_errors", False)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Made with Bob
