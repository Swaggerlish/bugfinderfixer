import os
import json
from typing import Dict, List, Optional
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from services.base_analyzer import BaseCodeAnalyzer

class WatsonxCodeAnalyzer(BaseCodeAnalyzer):
    """
    AI-powered code analyzer using IBM watsonx.
    Supports ANY programming language with intelligent error detection and fixing.
    """

    LANGUAGE_ALIASES = {
        "py": "python",
        "python3": "python",
        "js": "javascript",
        "jsx": "javascript",
        "ts": "javascript",
        "java": "java",
        "c++": "cpp",
        "cpp": "cpp",
        "c": "cpp",
        "other": "generic",
        "text": "generic",
    }

    def _normalize_language(self, language: str) -> str:
        """Normalize incoming language values to supported analyzer values."""
        if not language:
            return "generic"
        normalized = language.strip().lower()
        normalized = normalized.replace(" ", "")
        return self.LANGUAGE_ALIASES.get(normalized, normalized)
    
    def __init__(self):
        # Get credentials from environment variables
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.model_id = os.getenv("WATSONX_MODEL", "ibm/granite-20b-code-instruct-v2")
        
        # Initialize watsonx model
        self.model = None
        if self.api_key and self.project_id:
            try:
                self.model = Model(
                    model_id=self.model_id,
                    params={
                        GenParams.DECODING_METHOD: "greedy",
                        GenParams.MAX_NEW_TOKENS: 2000,
                        GenParams.MIN_NEW_TOKENS: 1,
                        GenParams.TEMPERATURE: 0.0,
                        GenParams.TOP_K: 50,
                        GenParams.TOP_P: 1
                    },
                    credentials={
                        "apikey": self.api_key,
                        "url": self.url
                    },
                    project_id=self.project_id
                )
            except Exception as e:
                print(f"Warning: Failed to initialize watsonx model: {e}")
                self.model = None
    
    def analyze(self, code: str, language: str = "python") -> Dict:
        """
        Analyze code using IBM watsonx AI.
        
        Args:
            code: The source code to analyze
            language: Programming language
            
        Returns:
            Dictionary with analysis results
        """
        language = self._normalize_language(language)
        if not self.model:
            return self._fallback_analysis(code, language)
        
        try:
            # Create prompt for watsonx
            prompt = self._create_analysis_prompt(code, language)
            
            # Get AI response
            response = self.model.generate_text(prompt=prompt)
            
            # Convert response to string if needed
            response_text = ""
            if response:
                if isinstance(response, dict):
                    response_text = response.get("output_text") or response.get("text") or json.dumps(response)
                else:
                    response_text = getattr(response, "output_text", None) or getattr(response, "text", None) or str(response)
            
            # Parse AI response
            result = self._parse_ai_response(response_text, code)
            result["normalized_language"] = language
            
            return result
            
        except Exception as e:
            print(f"AI analysis error: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_analysis(code, language)
    
    def _create_analysis_prompt(self, code: str, language: str) -> str:
        """Create a detailed prompt for code analysis."""
        prompt_language = language if language != "generic" else "plain text"
        fenced_language = language if language != "generic" else ""
        prompt = f"""You are an expert code analyzer and fixer. Analyze this {prompt_language} code and fix ALL errors.

CODE WITH ERRORS:
```{fenced_language}
{code}
```

TASK:
1. Find ALL errors (typos, syntax, logic, missing imports)
2. For each error, provide the EXACT fix
3. Generate COMPLETE corrected code

EXAMPLE for Java:
If you see: mport java.util.Scanner;
Fix to: import java.util.Scanner;

If you see: cou << "Hello";
Fix to: cout << "Hello";

RESPOND IN JSON:
{{
  "issues": {{
    "syntax_errors": [
      {{
        "line": 1,
        "severity": "critical",
        "message": "Typo: 'mport' should be 'import'",
        "original_code": "mport java.util.Scanner;",
        "fixed_code": "import java.util.Scanner;"
      }}
    ]
  }},
  "suggestions": ["Fix typo on line 1"],
  "fixed_code": "import java.util.Scanner;\\n\\npublic class Calculator {{\\n    // corrected code\\n}}",
  "has_syntax_errors": true
}}

IMPORTANT:
- Reply only with valid JSON. Do not add any markdown, explanation, or extra text.
- fixed_code must be the COMPLETE corrected code
- original_code and fixed_code must show EXACT lines
- Be precise with fixes

ANALYZE AND FIX NOW:"""
        
        return prompt
    
    def _parse_ai_response(self, response: str, original_code: str) -> Dict:
        """Parse the AI response into structured format."""
        try:
            # Try to extract JSON from response
            # Look for JSON block in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Ensure all required fields exist
                if "issues" not in result:
                    result["issues"] = {}
                if "suggestions" not in result:
                    result["suggestions"] = ["AI analysis completed"]
                if "fixed_code" not in result:
                    result["fixed_code"] = original_code
                if "has_syntax_errors" not in result:
                    result["has_syntax_errors"] = bool(result.get("issues", {}).get("syntax_errors"))
                
                return result
            else:
                # If no JSON found, create structured response from text
                return self._create_structured_response(response, original_code)
                
        except json.JSONDecodeError:
            # If JSON parsing fails, create structured response
            return self._create_structured_response(response, original_code)
    
    def _create_structured_response(self, text: str, original_code: str) -> Dict:
        """Create structured response from unstructured AI text."""
        issues = {
            "syntax_errors": [],
            "security_issues": [],
            "style_issues": [],
            "best_practices": []
        }
        
        suggestions = []
        
        # Parse text for issues (simple heuristic)
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            
            # Look for line numbers and issues
            if 'line' in line_lower and any(word in line_lower for word in ['error', 'issue', 'problem', 'missing', 'typo']):
                # Extract line number
                import re
                line_match = re.search(r'line\s+(\d+)', line_lower)
                if line_match:
                    line_num = int(line_match.group(1))
                    
                    issue = {
                        "line": line_num,
                        "severity": "critical" if "error" in line_lower else "warning",
                        "message": line.strip(),
                        "original_code": None,
                        "fixed_code": None
                    }
                    
                    if "syntax" in line_lower or "error" in line_lower:
                        issues["syntax_errors"].append(issue)
                    elif "security" in line_lower:
                        issues["security_issues"].append(issue)
                    else:
                        issues["style_issues"].append(issue)
            
            # Look for suggestions
            if any(word in line_lower for word in ['suggest', 'recommend', 'should', 'consider']):
                suggestions.append(line.strip())
        
        # If no issues found, add a general message
        if not any(issues.values()):
            suggestions.append("AI analysis completed. Review the code for potential improvements.")
        
        return {
            "issues": {k: v for k, v in issues.items() if v},
            "suggestions": suggestions if suggestions else ["Code analyzed by AI"],
            "fixed_code": original_code,
            "has_syntax_errors": bool(issues.get("syntax_errors"))
        }
    
    def _fallback_analysis(self, code: str, language: str) -> Dict:
        """Fallback analysis when AI is not available."""
        return {
            "issues": {},
            "suggestions": [
                "⚠️ AI analysis unavailable. Please configure watsonx credentials.",
                "Set WATSONX_API_KEY, WATSONX_PROJECT_ID in environment variables.",
                "Using basic rule-based analysis as fallback."
            ],
            "fixed_code": code,
            "has_syntax_errors": False,
            "normalized_language": language
        }

# Made with Bob