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
                        GenParams.MAX_NEW_TOKENS: 3000,
                        GenParams.MIN_NEW_TOKENS: 50,
                        GenParams.TEMPERATURE: 0.1,
                        GenParams.TOP_K: 50,
                        GenParams.TOP_P: 0.95,
                        GenParams.REPETITION_PENALTY: 1.1
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
        
        # Language-specific syntax rules
        language_rules = {
            "python": """
PYTHON-SPECIFIC RULES:
- No semicolons needed at end of lines
- Indentation is critical (use 4 spaces)
- Use 'import' for modules, not 'include'
- Common functions: print(), len(), range(), input()
- No curly braces for blocks, use indentation""",
            "cpp": """
C++ SPECIFIC RULES:
- Every statement needs semicolon (;)
- Use #include for headers (e.g., #include <iostream>)
- Use 'cout' for output, 'cin' for input
- Need 'using namespace std;' or 'std::' prefix
- Curly braces {} for blocks
- Main function: int main() { ... return 0; }""",
            "java": """
JAVA SPECIFIC RULES:
- Every statement needs semicolon (;)
- Use 'import' for packages (e.g., import java.util.Scanner;)
- Use 'System.out.println()' for output
- Class names start with capital letter
- Main method: public static void main(String[] args)
- Curly braces {} for blocks""",
            "javascript": """
JAVASCRIPT SPECIFIC RULES:
- Semicolons recommended but optional
- Use 'console.log()' for output
- Variable declarations: let, const, var
- No type declarations needed
- Curly braces {} for blocks
- Functions: function name() {} or () => {}""",
            "c": """
C SPECIFIC RULES:
- Every statement needs semicolon (;)
- Use #include for headers (e.g., #include <stdio.h>)
- Use 'printf()' for output, 'scanf()' for input
- Curly braces {} for blocks
- Main function: int main() { ... return 0; }"""
        }
        
        lang_specific = language_rules.get(language.lower(), "")
        
        prompt = f"""You are an expert {prompt_language} programmer and code analyzer.

LANGUAGE: {prompt_language.upper()}
{lang_specific}

CODE TO ANALYZE:
```{fenced_language}
{code}
```

CRITICAL: This is {prompt_language.upper()} code. Apply {prompt_language.upper()}-specific syntax rules ONLY.

ANALYSIS TASKS:
1. Verify this is valid {prompt_language.upper()} syntax
2. Find ALL errors specific to {prompt_language.upper()}:
   - Syntax errors (missing semicolons in C++/Java/C, wrong indentation in Python)
   - Typos in {prompt_language.upper()} keywords
   - Missing {prompt_language.upper()}-specific imports/includes
   - Incomplete expressions
   - Logic errors (division by zero, null pointers, array bounds)
   - Runtime errors (type mismatches, undefined variables, index errors)
   - Type mismatches

3. For EACH error found:
   - Line number
   - Original buggy code
   - Corrected code
   - PLAIN LANGUAGE explanation (explain like teaching a beginner)
   - What would happen at runtime if not fixed

4. Generate COMPLETE fixed {prompt_language.upper()} code

RESPONSE FORMAT (JSON only):
{{
  "issues": {{
    "syntax_errors": [
      {{
        "line": <number>,
        "severity": "critical",
        "message": "PLAIN LANGUAGE: What's wrong and why it's a problem",
        "original_code": "buggy line",
        "fixed_code": "corrected line",
        "explanation": "Simple explanation of what would happen at runtime"
      }}
    ],
    "logic_errors": [
      {{
        "line": <number>,
        "severity": "warning",
        "message": "PLAIN LANGUAGE: What's wrong",
        "original_code": "buggy code",
        "fixed_code": "corrected code",
        "explanation": "What error would occur when this code runs"
      }}
    ],
    "runtime_errors": [
      {{
        "line": <number>,
        "severity": "critical",
        "message": "PLAIN LANGUAGE: What runtime error will occur",
        "original_code": "buggy code",
        "fixed_code": "corrected code",
        "explanation": "Example: 'This will crash with IndexError because the list only has 3 items but you're trying to access item 5'"
      }}
    ]
  }},
  "suggestions": [
    "PLAIN LANGUAGE suggestion 1",
    "PLAIN LANGUAGE suggestion 2"
  ],
  "fixed_code": "COMPLETE corrected {prompt_language.upper()} code",
  "has_syntax_errors": true
}}

EXAMPLE OF PLAIN LANGUAGE EXPLANATIONS:
- BAD: "IndexError on line 5"
- GOOD: "Line 5 will crash because you're trying to access the 10th item in a list that only has 5 items"

- BAD: "Division by zero"
- GOOD: "Line 8 will crash with 'ZeroDivisionError' because you're dividing by zero, which is mathematically impossible"

- BAD: "Undefined variable"
- GOOD: "Line 3 will crash with 'NameError' because you're using variable 'x' before creating it"

CRITICAL RULES:
- Return ONLY valid JSON (no markdown)
- Apply {prompt_language.upper()} syntax rules ONLY
- fixed_code must be complete, valid {prompt_language.upper()} code
- Do NOT mix syntax from other languages
- Be thorough - find ALL bugs

ANALYZE THIS {prompt_language.upper()} CODE NOW:"""
        
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