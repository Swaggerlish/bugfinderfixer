import re
import ast
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from services.base_analyzer import BaseCodeAnalyzer

@dataclass
class Issue:
    """Represents a code issue with details."""
    type: str  # 'syntax', 'security', 'style', 'best_practice'
    severity: str  # 'critical', 'warning', 'info'
    line: Optional[int]
    message: str
    suggestion: str
    original_code: Optional[str] = None  # The problematic line(s)
    fixed_code: Optional[str] = None  # The suggested fix for this specific issue

class CodeAnalyzerService(BaseCodeAnalyzer):
    """
    Rule-based code analyzer implementation.
    Implements BaseCodeAnalyzer interface for easy replacement with AI-based analyzers.
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
    
    def __init__(self):
        self.security_patterns = {
            "eval_usage": r"\beval\s*\(",
            "exec_usage": r"\bexec\s*\(",
            "pickle_usage": r"\bpickle\.(load|loads)\s*\(",
            "sql_injection": r"(execute|cursor)\s*\([^)]*%s[^)]*\)",
            "hardcoded_password": r"(password|passwd|pwd)\s*=\s*['\"][^'\"]+['\"]",
            "shell_injection": r"(os\.system|subprocess\.call|subprocess\.run)\s*\([^)]*\+",
        }
        
        self.style_patterns = {
            "missing_docstring": r"^def\s+\w+\([^)]*\):\s*\n\s+(?!\"\"\")",
            "bare_except": r"except\s*:",
            "print_statement": r"\bprint\s*\(",
            "todo_comment": r"#\s*TODO",
            "fixme_comment": r"#\s*FIXME",
        }
    
    def analyze(self, code: str, language: str = "python") -> Dict:
        """
        Main analysis method - can be replaced with AI-based analyzer.
        
        Args:
            code: The source code to analyze
            language: Programming language (default: python)
            
        Returns:
            Dictionary with analysis results including issues, suggestions, and fixed code
        """
        language = self._normalize_language(language)
        if language == "python":
            result = self._analyze_python(code)
        elif language == "cpp":
            result = self._analyze_cpp(code)
        elif language == "java":
            result = self._analyze_java(code)
        elif language == "javascript":
            result = self._analyze_javascript(code)
        else:
            result = self._analyze_generic(code)

        result["normalized_language"] = language
        return result

    def _normalize_language(self, language: str) -> str:
        """Normalize incoming language values to supported analyzer values."""
        if not language:
            return "generic"
        normalized = language.strip().lower()
        normalized = normalized.replace(" ", "")
        return self.LANGUAGE_ALIASES.get(normalized, normalized)
    
    def _analyze_python(self, code: str) -> Dict:
        """Comprehensive Python code analysis."""
        issues_list: List[Issue] = []
        
        # 1. Syntax Error Detection
        syntax_issues = self._check_syntax(code)
        issues_list.extend(syntax_issues)
        
        # If there are syntax errors, return early as other checks may fail
        if syntax_issues:
            return self._format_response(issues_list, code, has_syntax_errors=True)
        
        # 2. Security Issue Detection
        security_issues = self._check_security(code)
        issues_list.extend(security_issues)
        
        # 3. Style and Best Practice Checks
        style_issues = self._check_style(code)
        issues_list.extend(style_issues)
        
        # 4. Generate fixed code
        fixed_code = self._generate_fixed_code(code, issues_list)
        
        return self._format_response(issues_list, fixed_code)
    
    def _check_syntax(self, code: str) -> List[Issue]:
        """Check for syntax errors using AST parsing."""
        issues = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            original = self._get_line_content(code, e.lineno)
            fixed = self._generate_syntax_fix(original, e) if original else None
            
            issues.append(Issue(
                type="syntax",
                severity="critical",
                line=e.lineno,
                message=f"Syntax Error: {e.msg}",
                suggestion=f"Fix syntax error at line {e.lineno}: {e.text.strip() if e.text else 'N/A'}",
                original_code=original,
                fixed_code=fixed
            ))
        except Exception as e:
            issues.append(Issue(
                type="syntax",
                severity="critical",
                line=None,
                message=f"Parse Error: {str(e)}",
                suggestion="Fix code structure and syntax",
                original_code=None,
                fixed_code=None
            ))
        return issues
    
    def _get_line_content(self, code: str, line_num: Optional[int]) -> Optional[str]:
        """Get the content of a specific line."""
        if line_num is None:
            return None
        lines = code.split('\n')
        if 1 <= line_num <= len(lines):
            return lines[line_num - 1]
        return None
    
    def _generate_line_fix(self, original_line: str, issue_type: str) -> Optional[str]:
        """Generate a fixed version of a problematic line."""
        if not original_line:
            return None
            
        fixed = original_line
        
        # Apply fixes based on issue type
        if "eval()" in original_line:
            fixed = re.sub(r'\beval\s*\(', 'ast.literal_eval(', fixed)
            
        elif "exec()" in original_line:
            fixed = "# exec() removed for security - refactor this code"
            
        elif re.search(r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', original_line, re.IGNORECASE):
            match = re.search(r'(\w+)\s*=\s*["\'][^"\']+["\']', original_line)
            if match:
                var_name = match.group(1)
                fixed = re.sub(r'=\s*["\'][^"\']+["\']', f' = os.getenv("{var_name.upper()}")', original_line)
        
    
    def _generate_syntax_fix(self, original_line: str, syntax_error: SyntaxError) -> Optional[str]:
        """Generate a fixed version of a line with syntax error."""
        if not original_line:
            return None
        
        fixed = original_line.strip()
        
        # Common syntax error fixes
        # Unterminated string - need to detect if opening or closing quote is missing
        if syntax_error.msg and "unterminated string" in syntax_error.msg.lower():
            # Check for mismatched quotes
            double_quotes = fixed.count('"')
            single_quotes = fixed.count("'")
            
            # If odd number of quotes, we need to add one
            if double_quotes % 2 == 1:
                # Find where the quote should be added
                # Check if it's missing at the beginning or end
                first_double = fixed.find('"')
                last_double = fixed.rfind('"')
                
                # If quote appears after a function call like print(hello")
                # We need to add opening quote before the string
                if '(' in fixed and first_double > fixed.find('('):
                    # Find the position after the opening parenthesis
                    paren_pos = fixed.find('(')
                    # Insert opening quote after the parenthesis
                    fixed = fixed[:paren_pos+1] + '"' + fixed[paren_pos+1:]
                else:
                    # Otherwise add closing quote at the end
                    fixed = fixed + '"'
                    
            elif single_quotes % 2 == 1:
                first_single = fixed.find("'")
                last_single = fixed.rfind("'")
                
                if '(' in fixed and first_single > fixed.find('('):
                    paren_pos = fixed.find('(')
                    fixed = fixed[:paren_pos+1] + "'" + fixed[paren_pos+1:]
                else:
                    fixed = fixed + "'"
        
        # Missing closing parenthesis
        elif "(" in fixed and fixed.count("(") > fixed.count(")"):
            fixed = fixed + ")"
        
        # Missing opening parenthesis (less common but possible)
        elif ")" in fixed and fixed.count(")") > fixed.count("("):
            # Add opening parenthesis at the beginning of the statement
            if re.match(r'^\s*\w+', fixed):
                match = re.match(r'^(\s*)(\w+)', fixed)
                if match:
                    fixed = match.group(1) + match.group(2) + '(' + fixed[len(match.group(0)):]
        
        # Missing closing bracket
        elif "[" in fixed and fixed.count("[") > fixed.count("]"):
            fixed = fixed + "]"
        
        # Missing opening bracket
        elif "]" in fixed and fixed.count("]") > fixed.count("["):
            if '=' in fixed:
                eq_pos = fixed.find('=')
                fixed = fixed[:eq_pos+1] + ' [' + fixed[eq_pos+1:].lstrip()
        
        # Missing closing brace
        elif "{" in fixed and fixed.count("{") > fixed.count("}"):
            fixed = fixed + "}"
        
        # Missing opening brace
        elif "}" in fixed and fixed.count("}") > fixed.count("{"):
            if '=' in fixed:
                eq_pos = fixed.find('=')
                fixed = fixed[:eq_pos+1] + ' {' + fixed[eq_pos+1:].lstrip()
        
        # Missing colon (common in if/for/while/def)
        elif re.match(r'^\s*(if|for|while|def|class|elif|else|try|except|finally|with)\s+', fixed):
            if not fixed.rstrip().endswith(':'):
                fixed = fixed.rstrip() + ':'
        
        return fixed if fixed != original_line.strip() else original_line + "  # Fix syntax error"
    
    def _check_security(self, code: str) -> List[Issue]:
        """Detect security vulnerabilities."""
        issues = []
        lines = code.split('\n')
        
        # Check for eval/exec usage
        if re.search(self.security_patterns["eval_usage"], code):
            line_num = self._find_line_number(code, self.security_patterns["eval_usage"])
            original = self._get_line_content(code, line_num)
            fixed = self._generate_line_fix(original, "eval") if original else None
            
            issues.append(Issue(
                type="security",
                severity="critical",
                line=line_num,
                message="Dangerous use of eval() detected",
                suggestion="Avoid eval(). Use ast.literal_eval() for safe evaluation or refactor code",
                original_code=original,
                fixed_code=fixed
            ))
        
        if re.search(self.security_patterns["exec_usage"], code):
            line_num = self._find_line_number(code, self.security_patterns["exec_usage"])
            original = self._get_line_content(code, line_num)
            fixed = self._generate_line_fix(original, "exec") if original else None
            
            issues.append(Issue(
                type="security",
                severity="critical",
                line=line_num,
                message="Dangerous use of exec() detected",
                suggestion="Avoid exec(). Refactor to use safer alternatives",
                original_code=original,
                fixed_code=fixed
            ))
        
        # Check for pickle usage
        if re.search(self.security_patterns["pickle_usage"], code):
            line_num = self._find_line_number(code, self.security_patterns["pickle_usage"])
            original = self._get_line_content(code, line_num)
            
            issues.append(Issue(
                type="security",
                severity="warning",
                line=line_num,
                message="Unsafe pickle.load() usage detected",
                suggestion="Only unpickle data from trusted sources or use JSON instead",
                original_code=original,
                fixed_code="# Use json.load() instead of pickle for untrusted data"
            ))
        
        # Check for SQL injection vulnerabilities
        if re.search(self.security_patterns["sql_injection"], code):
            line_num = self._find_line_number(code, self.security_patterns["sql_injection"])
            original = self._get_line_content(code, line_num)
            
            issues.append(Issue(
                type="security",
                severity="critical",
                line=line_num,
                message="Potential SQL injection vulnerability",
                suggestion="Use parameterized queries instead of string formatting",
                original_code=original,
                fixed_code="# Use: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
            ))
        
        # Check for hardcoded passwords
        if re.search(self.security_patterns["hardcoded_password"], code, re.IGNORECASE):
            line_num = self._find_line_number(code, self.security_patterns["hardcoded_password"])
            original = self._get_line_content(code, line_num)
            fixed = self._generate_line_fix(original, "password") if original else None
            
            issues.append(Issue(
                type="security",
                severity="critical",
                line=line_num,
                message="Hardcoded password detected",
                suggestion="Use environment variables or secure credential management",
                original_code=original,
                fixed_code=fixed
            ))
        
        # Check for shell injection
        if re.search(self.security_patterns["shell_injection"], code):
            issues.append(Issue(
                type="security",
                severity="critical",
                line=self._find_line_number(code, self.security_patterns["shell_injection"]),
                message="Potential shell injection vulnerability",
                suggestion="Use subprocess with list arguments instead of shell=True"
            ))
        
        return issues
    
    def _check_style(self, code: str) -> List[Issue]:
        """Check for style and best practice issues."""
        issues = []
        lines = code.split('\n')
        
        # Check for missing docstrings
        if re.search(self.style_patterns["missing_docstring"], code, re.MULTILINE):
            issues.append(Issue(
                type="best_practice",
                severity="info",
                line=self._find_line_number(code, r"^def\s+\w+"),
                message="Missing docstring in function",
                suggestion="Add docstring to document function purpose and parameters"
            ))
        
        # Check for bare except
        if re.search(self.style_patterns["bare_except"], code):
            line_num = self._find_line_number(code, self.style_patterns["bare_except"])
            original = self._get_line_content(code, line_num)
            fixed = self._generate_line_fix(original, "except") if original else None
            
            issues.append(Issue(
                type="best_practice",
                severity="warning",
                line=line_num,
                message="Bare except clause detected",
                suggestion="Specify exception types: except ValueError: or except Exception as e:",
                original_code=original,
                fixed_code=fixed
            ))
        
        # Check for print statements
        if re.search(self.style_patterns["print_statement"], code):
            line_num = self._find_line_number(code, self.style_patterns["print_statement"])
            original = self._get_line_content(code, line_num)
            fixed = self._generate_line_fix(original, "print") if original else None
            
            issues.append(Issue(
                type="style",
                severity="info",
                line=line_num,
                message="Print statement found",
                suggestion="Use logging module instead of print for production code",
                original_code=original,
                fixed_code=fixed
            ))
        
        # Check for TODO/FIXME
        if re.search(self.style_patterns["todo_comment"], code, re.IGNORECASE):
            issues.append(Issue(
                type="style",
                severity="info",
                line=self._find_line_number(code, self.style_patterns["todo_comment"]),
                message="TODO comment found",
                suggestion="Address TODO items before production deployment"
            ))
        
        # Check for long lines
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                issues.append(Issue(
                    type="style",
                    severity="info",
                    line=i,
                    message=f"Line {i} exceeds 100 characters ({len(line)} chars)",
                    suggestion="Break long lines for better readability (PEP 8)"
                ))
                break
        
        # Check for missing type hints
        if "def " in code and "->" not in code and ":" not in code.split("def ")[1].split(")")[0]:
            issues.append(Issue(
                type="best_practice",
                severity="info",
                line=self._find_line_number(code, r"def\s+\w+"),
                message="Missing type hints",
                suggestion="Add type hints: def func(x: int) -> str:"
            ))
        
        return issues
    
    def _generate_fixed_code(self, code: str, issues: List[Issue]) -> str:
        """Generate improved version of the code based on detected issues."""
        fixed_code = code
        
        # Apply fixes based on issue types
        for issue in issues:
            if issue.type == "security":
                if "eval()" in issue.message:
                    fixed_code = re.sub(r'\beval\s*\(', 'ast.literal_eval(', fixed_code)
                    if 'import ast' not in fixed_code:
                        fixed_code = 'import ast\n\n' + fixed_code
                
                elif "bare except" in issue.message.lower():
                    fixed_code = re.sub(r'except\s*:', 'except Exception as e:', fixed_code)
                
                elif "hardcoded password" in issue.message.lower():
                    fixed_code = re.sub(
                        r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
                        r'\1 = os.getenv("\1".upper())',
                        fixed_code,
                        flags=re.IGNORECASE
                    )
                    if 'import os' not in fixed_code:
                        fixed_code = 'import os\n\n' + fixed_code
            
            elif issue.type == "style":
                if "print statement" in issue.message.lower():
                    # Add logging import and replace print with logging
                    if 'import logging' not in fixed_code:
                        fixed_code = 'import logging\n\n' + fixed_code
                    fixed_code = re.sub(r'\bprint\s*\(', 'logging.info(', fixed_code)
        
        # Add docstring if missing
        if any(issue.message == "Missing docstring in function" for issue in issues):
            fixed_code = self._add_docstring(fixed_code)
        
        return fixed_code
    
    def _add_docstring(self, code: str) -> str:
        """Add basic docstring to functions missing them."""
        lines = code.split('\n')
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            result.append(line)
            # Check if this is a function definition
            if re.match(r'^\s*def\s+\w+', line):
                # Check if next line is not a docstring
                if i + 1 < len(lines) and '"""' not in lines[i + 1]:
                    indent = len(line) - len(line.lstrip())
                    result.append(' ' * (indent + 4) + '"""Function description."""')
            i += 1
        return '\n'.join(result)
    
    def _find_line_number(self, code: str, pattern: str) -> Optional[int]:
        """Find the line number where a pattern occurs."""
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                return i
        return None
    
    def _format_response(self, issues: List[Issue], fixed_code: str, has_syntax_errors: bool = False) -> Dict:
        """Format the analysis response."""
        # Group issues by type
        issues_by_type = {
            "syntax_errors": [],
            "security_issues": [],
            "style_issues": [],
            "best_practices": []
        }
        
        suggestions = []
        
        for issue in issues:
            issue_dict = {
                "line": issue.line,
                "severity": issue.severity,
                "message": issue.message,
                "original_code": issue.original_code,
                "fixed_code": issue.fixed_code
            }
            
            if issue.type == "syntax":
                issues_by_type["syntax_errors"].append(issue_dict)
            elif issue.type == "security":
                issues_by_type["security_issues"].append(issue_dict)
            elif issue.type == "style":
                issues_by_type["style_issues"].append(issue_dict)
            elif issue.type == "best_practice":
                issues_by_type["best_practices"].append(issue_dict)
            
            suggestions.append(issue.suggestion)
        
        # Remove empty categories
        issues_by_type = {k: v for k, v in issues_by_type.items() if v}
        
        if not issues:
            suggestions.append("Code looks good! No major issues detected.")
        
        return {
            "issues": issues_by_type,
            "suggestions": suggestions,
            "fixed_code": None if has_syntax_errors else fixed_code,
            "has_syntax_errors": has_syntax_errors
        }
    
    def _analyze_cpp(self, code: str) -> Dict:
        """Comprehensive C++ code analysis."""
        issues_list: List[Issue] = []
        lines = code.split('\n')
        
        # Check for missing includes
        has_iostream = '#include <iostream>' in code or '#include<iostream>' in code
        has_using_std = 'using namespace std' in code
        uses_cout = 'cout' in code
        uses_cin = 'cin' in code
        
        if (uses_cout or uses_cin) and not has_iostream:
            issues_list.append(Issue(
                type="syntax",
                severity="critical",
                line=1,
                message="Missing #include <iostream>",
                suggestion="Add #include <iostream> at the beginning",
                original_code=None,
                fixed_code="#include <iostream>"
            ))
        
        if (uses_cout or uses_cin) and not has_using_std and 'std::' not in code:
            issues_list.append(Issue(
                type="syntax",
                severity="critical",
                line=2,
                message="Missing 'using namespace std;' or 'std::' prefix",
                suggestion="Add 'using namespace std;' after includes or use std::cout",
                original_code=None,
                fixed_code="using namespace std;"
            ))
        
        # Check each line for common C++ errors
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for incomplete expressions (operators without operands)
            if re.search(r'[+\-*/]\s*;', stripped):
                issues_list.append(Issue(
                    type="syntax",
                    severity="critical",
                    line=i,
                    message="Incomplete expression: operator without right operand",
                    suggestion="Complete the expression with the missing operand",
                    original_code=line,
                    fixed_code=self._fix_incomplete_expression(line)
                ))
            
            # Check for typos in common keywords
            typo_fixes = {
                r'\bcou\b': 'cout',
                r'\bcin\b(?![\w])': 'cin',
                r'\bstd\b(?=\s*<<)': 'std',
                r'\breaurn\b': 'return',
                r'\binclude\b(?!\s*<)': '#include',
            }
            
            for pattern, correct in typo_fixes.items():
                if re.search(pattern, stripped):
                    issues_list.append(Issue(
                        type="syntax",
                        severity="critical",
                        line=i,
                        message=f"Typo detected: should be '{correct}'",
                        suggestion=f"Replace with correct keyword '{correct}'",
                        original_code=line,
                        fixed_code=re.sub(pattern, correct, line)
                    ))
            
            # Check for missing semicolons (common in C++)
            if stripped and not stripped.startswith('//') and not stripped.startswith('#'):
                if re.match(r'^(int|double|float|char|string|bool|void)\s+\w+\s*=', stripped):
                    if not stripped.rstrip().endswith(';') and not stripped.rstrip().endswith('{'):
                        issues_list.append(Issue(
                            type="syntax",
                            severity="critical",
                            line=i,
                            message="Missing semicolon at end of statement",
                            suggestion="Add semicolon at the end",
                            original_code=line,
                            fixed_code=line.rstrip() + ';'
                        ))
        
        # Generate fixed code
        fixed_code = self._generate_cpp_fixed_code(code, issues_list)
        
        return self._format_response(issues_list, fixed_code, has_syntax_errors=bool(issues_list))
    
    def _analyze_java(self, code: str) -> Dict:
        """Comprehensive Java code analysis."""
        issues_list: List[Issue] = []
        lines = code.split('\n')
        
        # Check for missing imports
        uses_scanner = 'Scanner' in code
        uses_arraylist = 'ArrayList' in code
        
        if uses_scanner and 'import java.util.Scanner' not in code:
            issues_list.append(Issue(
                type="syntax",
                severity="critical",
                line=1,
                message="Missing import for Scanner",
                suggestion="Add 'import java.util.Scanner;'",
                original_code=None,
                fixed_code="import java.util.Scanner;"
            ))
        
        if uses_arraylist and 'import java.util.ArrayList' not in code:
            issues_list.append(Issue(
                type="syntax",
                severity="critical",
                line=1,
                message="Missing import for ArrayList",
                suggestion="Add 'import java.util.ArrayList;'",
                original_code=None,
                fixed_code="import java.util.ArrayList;"
            ))
        
        # Check each line for common Java errors
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for incomplete expressions
            if re.search(r'[+\-*/]\s*;', stripped):
                issues_list.append(Issue(
                    type="syntax",
                    severity="critical",
                    line=i,
                    message="Incomplete expression: operator without right operand",
                    suggestion="Complete the expression",
                    original_code=line,
                    fixed_code=self._fix_incomplete_expression(line)
                ))
            
            # Check for typos in common keywords
            typo_fixes = {
                r'\bSytem\b': 'System',
                r'\bprintl\b': 'println',
                r'\bpubilc\b': 'public',
                r'\bprivte\b': 'private',
                r'\breaurn\b': 'return',
                r'\bmport\b': 'import',
            }
            
            for pattern, correct in typo_fixes.items():
                if re.search(pattern, stripped):
                    issues_list.append(Issue(
                        type="syntax",
                        severity="critical",
                        line=i,
                        message=f"Typo detected: should be '{correct}'",
                        suggestion=f"Replace with correct keyword '{correct}'",
                        original_code=line,
                        fixed_code=re.sub(pattern, correct, line)
                    ))
        
        fixed_code = self._generate_java_fixed_code(code, issues_list)
        return self._format_response(issues_list, fixed_code, has_syntax_errors=bool(issues_list))
    
    def _analyze_javascript(self, code: str) -> Dict:
        """Comprehensive JavaScript code analysis."""
        issues_list: List[Issue] = []
        lines = code.split('\n')
        
        # Check each line for common JavaScript errors
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for incomplete expressions
            if re.search(r'[+\-*/]\s*;', stripped):
                issues_list.append(Issue(
                    type="syntax",
                    severity="critical",
                    line=i,
                    message="Incomplete expression: operator without right operand",
                    suggestion="Complete the expression",
                    original_code=line,
                    fixed_code=self._fix_incomplete_expression(line)
                ))
            
            # Check for typos in common keywords
            typo_fixes = {
                r'\bconsoel\b': 'console',
                r'\bfunciton\b': 'function',
                r'\breaurn\b': 'return',
                r'\bconst\s+\w+\s*=\s*$': 'const variable = value;',
            }
            
            for pattern, correct in typo_fixes.items():
                if re.search(pattern, stripped):
                    issues_list.append(Issue(
                        type="syntax",
                        severity="critical",
                        line=i,
                        message=f"Typo detected: should be '{correct}'",
                        suggestion=f"Replace with correct keyword '{correct}'",
                        original_code=line,
                        fixed_code=re.sub(pattern, correct, line)
                    ))
        
        fixed_code = self._generate_js_fixed_code(code, issues_list)
        return self._format_response(issues_list, fixed_code, has_syntax_errors=bool(issues_list))
    
    def _fix_incomplete_expression(self, line: str) -> str:
        """Fix incomplete expressions like 'num1 /' by adding a placeholder."""
        # Find the incomplete operator
        match = re.search(r'(\w+)\s*([+\-*/])\s*;', line)
        if match:
            var_name = match.group(1)
            operator = match.group(2)
            # Replace with completed expression
            return re.sub(r'([+\-*/])\s*;', r'\1 operand;  // TODO: Add the missing operand', line)
        return line
    
    def _generate_cpp_fixed_code(self, code: str, issues: List[Issue]) -> str:
        """Generate fixed C++ code."""
        lines = code.split('\n')
        fixed_lines = []
        
        # Add missing includes at the beginning
        needs_iostream = any('Missing #include <iostream>' in issue.message for issue in issues)
        needs_using = any('using namespace std' in issue.message for issue in issues)
        
        if needs_iostream:
            fixed_lines.append('#include <iostream>')
        if needs_using:
            fixed_lines.append('using namespace std;')
        if needs_iostream or needs_using:
            fixed_lines.append('')
        
        # Process each line
        for i, line in enumerate(lines, 1):
            # Find issues for this line
            line_issues = [issue for issue in issues if issue.line == i and issue.fixed_code]
            
            if line_issues:
                # Use the fixed code from the first applicable issue
                fixed_lines.append(line_issues[0].fixed_code)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _generate_java_fixed_code(self, code: str, issues: List[Issue]) -> str:
        """Generate fixed Java code."""
        lines = code.split('\n')
        fixed_lines = []
        
        # Add missing imports at the beginning
        missing_imports = [issue.fixed_code for issue in issues if issue.line == 1 and 'import' in issue.message]
        if missing_imports:
            fixed_lines.extend(missing_imports)
            fixed_lines.append('')
        
        # Process each line
        for i, line in enumerate(lines, 1):
            line_issues = [issue for issue in issues if issue.line == i and issue.fixed_code]
            if line_issues:
                fixed_lines.append(line_issues[0].fixed_code)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _generate_js_fixed_code(self, code: str, issues: List[Issue]) -> str:
        """Generate fixed JavaScript code."""
        lines = code.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines, 1):
            line_issues = [issue for issue in issues if issue.line == i and issue.fixed_code]
            if line_issues:
                fixed_lines.append(line_issues[0].fixed_code)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _analyze_generic(self, code: str) -> Dict:
        """Basic analysis for non-Python languages."""
        issues_list = []
        lines = code.split('\n')
        
        # Check for long lines
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues_list.append(Issue(
                    type="style",
                    severity="info",
                    line=i,
                    message=f"Line {i} is very long ({len(line)} chars)",
                    suggestion="Break long lines for better readability"
                ))
                break
        
        # Check for TODO/FIXME
        if re.search(r"//\s*TODO|#\s*TODO|/\*\s*TODO", code, re.IGNORECASE):
            issues_list.append(Issue(
                type="style",
                severity="info",
                line=self._find_line_number(code, r"//\s*TODO|#\s*TODO|/\*\s*TODO"),
                message="TODO comment found",
                suggestion="Address TODO items"
            ))
        
        if not issues_list:
            return {
                "issues": {},
                "suggestions": ["Basic analysis complete. Consider using language-specific linters."],
                "fixed_code": code,
                "has_syntax_errors": False
            }
        
        return self._format_response(issues_list, code)

# Made with Bob
