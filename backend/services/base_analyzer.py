from abc import ABC, abstractmethod
from typing import Dict

class BaseCodeAnalyzer(ABC):
    """
    Abstract base class for code analyzers.
    This allows easy replacement with different analyzer implementations,
    including AI-based analyzers in the future.
    """
    
    @abstractmethod
    def analyze(self, code: str, language: str = "python") -> Dict:
        """
        Analyze code and return results.
        
        Args:
            code: The source code to analyze
            language: Programming language
            
        Returns:
            Dictionary with structure:
            {
                "issues": {
                    "syntax_errors": [...],
                    "security_issues": [...],
                    "style_issues": [...],
                    "best_practices": [...]
                },
                "suggestions": [...],
                "fixed_code": str or None,
                "has_syntax_errors": bool
            }
        """
        pass
    
    def validate_response(self, response: Dict) -> bool:
        """
        Validate that the response has the correct structure.
        """
        required_keys = {"issues", "suggestions", "fixed_code", "has_syntax_errors"}
        return all(key in response for key in required_keys)

# Made with Bob
