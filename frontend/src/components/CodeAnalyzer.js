import React, { useState, useEffect } from 'react';
import './CodeAnalyzer.css';
import { analyzeCode, checkApiHealth } from '../services/api';
import InlineSuggestion from './InlineSuggestion';

const CodeAnalyzer = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');
  const [acceptedSuggestions, setAcceptedSuggestions] = useState([]);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  // Check API health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      const isHealthy = await checkApiHealth();
      setApiStatus(isHealthy ? 'online' : 'offline');
    };
    checkHealth();
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownOpen && !event.target.closest('.example-dropdown')) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [dropdownOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate input
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Use the API service to analyze code
      const data = await analyzeCode(code, language);
      
      // Set the result
      setResult(data);
      
      // Update API status to online if successful
      if (apiStatus === 'offline') {
        setApiStatus('online');
      }
      
    } catch (err) {
      // Set error message
      setError(err.message);
      console.error('Analysis error:', err);
      
      // Update API status if connection failed
      if (err.message.includes('Cannot connect')) {
        setApiStatus('offline');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setCode('');
    setResult(null);
    setError(null);
  };

  const handleAcceptSuggestion = (issue) => {
    // Add to accepted suggestions
    setAcceptedSuggestions(prev => [...prev, issue]);
    
    // Apply the fix to the code
    if (issue.original_code && issue.fixed_code && issue.line) {
      const lines = code.split('\n');
      if (issue.line > 0 && issue.line <= lines.length) {
        lines[issue.line - 1] = issue.fixed_code;
        setCode(lines.join('\n'));
      }
    }
  };

  const handleRejectSuggestion = (issue) => {
    // Just mark as rejected, no code changes
    console.log('Rejected suggestion:', issue);
  };

  const handleApplyAllAccepted = () => {
    if (acceptedSuggestions.length === 0) {
      alert('No suggestions have been accepted yet.');
      return;
    }

    const confirmed = window.confirm(
      `Apply ${acceptedSuggestions.length} accepted suggestion(s)?\n\n` +
      'This will apply all accepted fixes to your code.'
    );

    if (confirmed) {
      alert(`✅ ${acceptedSuggestions.length} suggestion(s) applied successfully!`);
      setAcceptedSuggestions([]);
      setResult(null);
    }
  };

  const handleApplyFixes = () => {
    if (result && result.fixed_code) {
      // Show confirmation dialog
      const confirmed = window.confirm(
        '🔧 Auto-Apply Fixes\n\n' +
        'This will replace your current code with the improved version.\n\n' +
        'Do you want to proceed?'
      );
      
      if (confirmed) {
        setCode(result.fixed_code);
        // Show success message
        alert('✅ Fixes applied successfully!\n\nYou can now review the improved code and analyze again if needed.');
        // Clear results to allow re-analysis
        setResult(null);
      }
    }
  };

  // Sample code snippets for testing - organized by language
  const sampleCodesByLanguage = {
    python: {
      security: {
        name: "Security Issues",
        code: `def process_user_input(user_data):
    # Multiple security vulnerabilities
    password = "admin123"  # Hardcoded password
    api_key = "sk-1234567890"  # Hardcoded API key
    
    # Dangerous eval usage
    result = eval(user_data)
    
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE id = %s" % user_data
    cursor.execute(query)
    
    print(f"Processing: {result}")
    return result`
      },
      style: {
        name: "Style Issues",
        code: `def calculate_total(items):
    # TODO: Add input validation
    total = 0
    for item in items:
        total += item
    print(total)  # Using print instead of logging
    return total

def another_function_with_a_very_long_name_that_exceeds_the_recommended_line_length_limit(param1, param2, param3):
    pass`
      },
      bestPractices: {
        name: "Best Practices",
        code: `def add(a, b):
    return a + b

def divide(x, y):
    try:
        return x / y
    except:
        return None

def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result`
      },
      syntaxError: {
        name: "Syntax Error",
        code: `def broken_function(x, y):
    if x > y
        print("x is greater")
    return x + y

def another_broken():
    print("Missing closing parenthesis"
    return True`
      },
      clean: {
        name: "Clean Code",
        code: `def calculate_sum(numbers: list[int]) -> int:
    """
    Calculate the sum of a list of numbers.
    
    Args:
        numbers: List of integers to sum
        
    Returns:
        The sum of all numbers
    """
    return sum(numbers)

def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"`
      },
      complex: {
        name: "Complex Example",
        code: `import os
import pickle

def process_file(filename):
    password = "secret123"
    
    # Multiple issues in one function
    with open(filename, 'rb') as f:
        data = pickle.load(f)  # Unsafe pickle
    
    result = eval(data['expression'])  # Dangerous eval
    
    # SQL injection
    query = f"SELECT * FROM users WHERE name = '{data['name']}'"
    
    print(f"Result: {result}")  # Should use logging
    
    # TODO: Add error handling
    return result`
      }
    },
    javascript: {
      security: {
        name: "Security Issues",
        code: `// Security vulnerabilities in JavaScript
const password = "admin123";  // Hardcoded password
const apiKey = "sk-1234567890";

function executeUserInput(userCode) {
    return eval(userCode);  // Dangerous eval
}

function buildQuery(username) {
    // SQL injection risk
    return "SELECT * FROM users WHERE name = '" + username + "'";
}

// XSS vulnerability
document.getElementById("output").innerHTML = userInput;`
      },
      style: {
        name: "Style Issues",
        code: `function calculateTotal(items) {
    var total = 0;  // Use const/let instead of var
    for (var i = 0; i < items.length; i++) {
        total += items[i];
    }
    console.log(total);  // Should use proper logging
    return total;
}

function anotherFunctionWithAVeryLongNameThatExceedsTheRecommendedLineLengthLimitForJavaScript(param1, param2, param3) {
    return param1 + param2 + param3;
}`
      },
      bestPractices: {
        name: "Best Practices",
        code: `function add(a, b) {
    return a + b;
}

function divide(x, y) {
    try {
        return x / y;
    } catch (e) {
        // Empty catch block
    }
}

function processData(data) {
    var result = [];
    for (var i = 0; i < data.length; i++) {
        result.push(data[i] * 2);
    }
    return result;
}`
      },
      syntaxError: {
        name: "Syntax Error",
        code: `function brokenFunction(x, y) {
    if (x > y {  // Missing closing parenthesis
        console.log("x is greater");
    }
    return x + y;
}

function anotherBroken() {
    console.log("Missing closing quote);
    return true;
}`
      },
      clean: {
        name: "Clean Code",
        code: `/**
 * Calculate the sum of an array of numbers
 * @param {number[]} numbers - Array of numbers to sum
 * @returns {number} The sum of all numbers
 */
function calculateSum(numbers) {
    return numbers.reduce((sum, num) => sum + num, 0);
}

/**
 * Greet a user by name
 * @param {string} name - The user's name
 * @returns {string} A greeting message
 */
function greet(name) {
    return \`Hello, \${name}!\`;
}`
      },
      complex: {
        name: "Complex Example",
        code: `const fs = require('fs');

function processFile(filename) {
    const password = "secret123";  // Hardcoded
    
    // Multiple issues
    const data = eval(fs.readFileSync(filename, 'utf8'));  // Dangerous
    
    const query = "SELECT * FROM users WHERE id = " + data.id;  // SQL injection
    
    console.log("Result: " + data);  // Should use logger
    
    // TODO: Add error handling
    return data;
}`
      }
    },
    java: {
      security: {
        name: "Security Issues",
        code: `import java.sql.*;

public class SecurityIssues {
    // Hardcoded credentials
    private static final String PASSWORD = "admin123";
    private static final String API_KEY = "sk-1234567890";
    
    public void executeQuery(String username) {
        // SQL injection vulnerability
        String query = "SELECT * FROM users WHERE name = '" + username + "'";
        // Execute query...
    }
    
    public void processInput(String input) {
        // Command injection risk
        Runtime.getRuntime().exec("cmd /c " + input);
    }
}`
      },
      style: {
        name: "Style Issues",
        code: `public class StyleIssues {
    public int calculateTotal(int[] items) {
        int total = 0;
        for (int i = 0; i < items.length; i++) {
            total += items[i];
        }
        System.out.println(total);  // Should use logger
        return total;
    }
    
    public void anotherMethodWithAVeryLongNameThatExceedsTheRecommendedLineLengthLimitForJavaCode(String param1, String param2) {
        // Method body
    }
}`
      },
      bestPractices: {
        name: "Best Practices",
        code: `public class BestPractices {
    public int add(int a, int b) {
        return a + b;
    }
    
    public Integer divide(int x, int y) {
        try {
            return x / y;
        } catch (Exception e) {
            // Empty catch block
        }
        return null;
    }
    
    public List processData(List data) {  // Missing generics
        List result = new ArrayList();
        for (Object item : data) {
            result.add(item);
        }
        return result;
    }
}`
      },
      syntaxError: {
        name: "Syntax Error",
        code: `public class SyntaxError {
    public int brokenMethod(int x, int y) {
        if (x > y {  // Missing closing parenthesis
            System.out.println("x is greater");
        }
        return x + y;
    }
    
    public boolean anotherBroken() {
        System.out.println("Missing closing quote);
        return true;
    }
}`
      },
      clean: {
        name: "Clean Code",
        code: `/**
 * Calculator utility class
 */
public class Calculator {
    /**
     * Calculate the sum of an array of numbers
     * @param numbers Array of integers to sum
     * @return The sum of all numbers
     */
    public int calculateSum(int[] numbers) {
        int sum = 0;
        for (int num : numbers) {
            sum += num;
        }
        return sum;
    }
    
    /**
     * Greet a user by name
     * @param name The user's name
     * @return A greeting message
     */
    public String greet(String name) {
        return "Hello, " + name + "!";
    }
}`
      },
      complex: {
        name: "Complex Example",
        code: `import java.io.*;
import java.sql.*;

public class ComplexExample {
    private static final String PASSWORD = "secret123";  // Hardcoded
    
    public Object processFile(String filename) throws Exception {
        // Multiple issues
        FileInputStream fis = new FileInputStream(filename);
        ObjectInputStream ois = new ObjectInputStream(fis);
        Object data = ois.readObject();  // Unsafe deserialization
        
        String query = "SELECT * FROM users WHERE id = " + data;  // SQL injection
        
        System.out.println("Result: " + data);  // Should use logger
        
        // TODO: Add error handling
        return data;
    }
}`
      }
    },
    cpp: {
      security: {
        name: "Security Issues",
        code: `#include <iostream>
#include <cstring>
using namespace std;

int main() {
    // Hardcoded credentials
    char password[] = "admin123";
    char apiKey[] = "sk-1234567890";
    
    // Buffer overflow risk
    char buffer[10];
    char input[100];
    cin >> input;
    strcpy(buffer, input);  // Unsafe copy
    
    cout << "Password: " << password << endl;
    return 0;
}`
      },
      style: {
        name: "Style Issues",
        code: `#include <iostream>
using namespace std;

int calculateTotal(int items[], int size) {
    int total = 0;
    for (int i = 0; i < size; i++) {
        total += items[i];
    }
    cout << total << endl;  // Should use proper output
    return total;
}

void anotherFunctionWithAVeryLongNameThatExceedsTheRecommendedLineLengthLimitForCPlusPlus(int param1, int param2) {
    // Function body
}`
      },
      bestPractices: {
        name: "Best Practices",
        code: `#include <iostream>
using namespace std;

int add(int a, int b) {
    return a + b;
}

int divide(int x, int y) {
    // No error checking for division by zero
    return x / y;
}

void processData(int data[], int size) {
    int* result = new int[size];
    for (int i = 0; i < size; i++) {
        result[i] = data[i] * 2;
    }
    // Memory leak - no delete[]
}`
      },
      syntaxError: {
        name: "Syntax Error",
        code: `int main() {
    char op;
    double num1, num2;

    cout << "Enter operator (+, -, *, /): ";
    cin >> op;

    cout << "Enter two numbers: ";
    cin >> num1 >> num2;

    switch(op) {
        case '+':
            cout << "Result = " << num1 + num2;
            break;

        case '-':
            cout << "Result = " << num1 - num2;
            break;

        case '*':
            cout << "Result = " << num1 * num2;
            break;

        case '/':
            if(num2 != 0)
                cout << "Result = " << num1 /;
            else
                cou << "Error! Division by zero.";
            break;

        default:
            cout << "Invalid operator!";
    }

    return 0;
}`
      },
      clean: {
        name: "Clean Code",
        code: `#include <iostream>
#include <vector>
using namespace std;

/**
 * Calculate the sum of a vector of numbers
 * @param numbers Vector of integers to sum
 * @return The sum of all numbers
 */
int calculateSum(const vector<int>& numbers) {
    int sum = 0;
    for (int num : numbers) {
        sum += num;
    }
    return sum;
}

/**
 * Greet a user by name
 * @param name The user's name
 * @return A greeting message
 */
string greet(const string& name) {
    return "Hello, " + name + "!";
}

int main() {
    vector<int> nums = {1, 2, 3, 4, 5};
    cout << "Sum: " << calculateSum(nums) << endl;
    cout << greet("World") << endl;
    return 0;
}`
      },
      complex: {
        name: "Complex Example",
        code: `#include <iostream>
#include <fstream>
#include <cstring>
using namespace std;

int main() {
    // Multiple issues
    char password[] = "secret123";  // Hardcoded
    
    char buffer[50];
    char input[200];
    
    cout << "Enter data: ";
    cin >> input;
    strcpy(buffer, input);  // Buffer overflow
    
    // Missing error checking
    ifstream file("data.txt");
    string line;
    getline(file, line);
    
    // No validation
    int value = stoi(line);
    int result = 100 / value;  // Potential division by zero
    
    cout << "Result: " << result << endl;
    
    // Memory leak
    int* data = new int[100];
    // No delete[]
    
    return 0;
}`
      }
    },
    other: {
      security: {
        name: "Security Issues",
        code: `// Generic code example
// This analyzer works best with Python, JavaScript, Java, and C++

function example() {
    const password = "hardcoded123";
    const apiKey = "secret-key";
    
    // Add your code here for analysis
    return "Hello World";
}`
      },
      style: {
        name: "Style Issues",
        code: `// Generic style example
function longFunctionNameThatExceedsRecommendedLength() {
    console.log("This is a style issue");
    // Add your code here
}`
      },
      bestPractices: {
        name: "Best Practices",
        code: `// Generic best practices example
function divide(x, y) {
    try {
        return x / y;
    } catch (e) {
        // Empty catch
    }
}`
      },
      syntaxError: {
        name: "Syntax Error",
        code: `// Generic syntax error example
function broken() {
    if (true {
        console.log("missing parenthesis");
    }
}`
      },
      clean: {
        name: "Clean Code",
        code: `// Generic clean code example
/**
 * Well-documented function
 */
function greet(name) {
    return "Hello, " + name;
}`
      },
      complex: {
        name: "Complex Example",
        code: `// Generic complex example
// Paste your code here for analysis
function example() {
    // Your code here
    return true;
}`
      }
    }
  };

  const loadExample = (exampleKey = 'security') => {
    const languageSamples = sampleCodesByLanguage[language] || sampleCodesByLanguage.python;
    if (languageSamples[exampleKey]) {
      setCode(languageSamples[exampleKey].code);
      setResult(null);
      setError(null);
      setDropdownOpen(false); // Close dropdown after selection
    }
  };

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'critical':
        return 'severity-critical';
      case 'warning':
        return 'severity-warning';
      case 'info':
        return 'severity-info';
      default:
        return '';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return '🔴';
      case 'warning':
        return '🟡';
      case 'info':
        return '🔵';
      default:
        return '⚪';
    }
  };

  return (
    <div className="code-analyzer">
      <div className="analyzer-container">
        {/* API Status Indicator */}
        {apiStatus === 'offline' && (
          <div className="api-status-warning">
            ⚠️ Backend API is offline. Please start the backend server at http://localhost:8000
          </div>
        )}
        
        {/* Input Section */}
        <div className="input-section">
          <div className="section-header">
            <h2>📝 Code Input</h2>
            <div className="header-actions">
              <div className={`api-status ${apiStatus}`}>
                <span className="status-dot"></span>
                <span className="status-text">
                  {apiStatus === 'online' ? 'API Connected' :
                   apiStatus === 'offline' ? 'API Offline' :
                   'Checking...'}
                </span>
              </div>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="language-select"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
                <option value="other">Other</option>
              </select>
              <div className="example-dropdown">
                <button
                  className="btn-secondary dropdown-toggle"
                  onClick={toggleDropdown}
                  type="button"
                >
                  📚 Load Sample Code
                </button>
                <div className={`dropdown-menu ${dropdownOpen ? 'show' : ''}`}>
                  <button onClick={() => loadExample('security')} className="dropdown-item">
                    🔒 Security Issues
                  </button>
                  <button onClick={() => loadExample('style')} className="dropdown-item">
                    🎨 Style Issues
                  </button>
                  <button onClick={() => loadExample('bestPractices')} className="dropdown-item">
                    💡 Best Practices
                  </button>
                  <button onClick={() => loadExample('syntaxError')} className="dropdown-item">
                    ❌ Syntax Error
                  </button>
                  <button onClick={() => loadExample('clean')} className="dropdown-item">
                    ✅ Clean Code
                  </button>
                  <button onClick={() => loadExample('complex')} className="dropdown-item">
                    🔥 Complex Example
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <form onSubmit={handleSubmit}>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste your code here..."
              className="code-input"
              rows="15"
            />
            
            <div className="button-group">
              <button 
                type="submit" 
                className="btn-primary"
                disabled={loading}
              >
                {loading ? '🔄 Analyzing...' : '🔍 Analyze Code'}
              </button>
              <button 
                type="button" 
                onClick={handleClear}
                className="btn-secondary"
                disabled={loading}
              >
                🗑️ Clear
              </button>
            </div>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <strong>❌ Error:</strong> {error}
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="results-section">
            {/* Issues Display */}
            <div className="issues-section">
              <h2>🐛 Detected Issues</h2>
              
              {result.has_syntax_errors && (
                <div className="alert alert-critical">
                  ⚠️ Code has syntax errors. Fix them before proceeding.
                </div>
              )}

              {Object.keys(result.issues).length === 0 ? (
                <div className="no-issues">
                  ✅ No issues detected! Your code looks good.
                </div>
              ) : (
                <div className="issues-list">
                  {/* Syntax Errors */}
                  {result.issues.syntax_errors && result.issues.syntax_errors.length > 0 && (
                    <div className="issue-category">
                      <h3 className="category-title">Syntax Errors</h3>
                      {result.issues.syntax_errors.map((issue, index) => (
                        <div key={index} className={`issue-item ${getSeverityClass(issue.severity)}`}>
                          <div className="issue-header">
                            <span className="severity-icon">{getSeverityIcon(issue.severity)}</span>
                            <span className="issue-line">Line {issue.line || 'N/A'}</span>
                            <span className="severity-badge">{issue.severity}</span>
                          </div>
                          <p className="issue-message">{issue.message}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Security Issues */}
                  {result.issues.security_issues && result.issues.security_issues.length > 0 && (
                    <div className="issue-category">
                      <h3 className="category-title">🔒 Security Issues</h3>
                      {result.issues.security_issues.map((issue, index) => (
                        <div key={index} className={`issue-item ${getSeverityClass(issue.severity)}`}>
                          <div className="issue-header">
                            <span className="severity-icon">{getSeverityIcon(issue.severity)}</span>
                            <span className="issue-line">Line {issue.line || 'N/A'}</span>
                            <span className="severity-badge">{issue.severity}</span>
                          </div>
                          <p className="issue-message">{issue.message}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Style Issues */}
                  {result.issues.style_issues && result.issues.style_issues.length > 0 && (
                    <div className="issue-category">
                      <h3 className="category-title">🎨 Style Issues</h3>
                      {result.issues.style_issues.map((issue, index) => (
                        <div key={index} className={`issue-item ${getSeverityClass(issue.severity)}`}>
                          <div className="issue-header">
                            <span className="severity-icon">{getSeverityIcon(issue.severity)}</span>
                            <span className="issue-line">Line {issue.line || 'N/A'}</span>
                            <span className="severity-badge">{issue.severity}</span>
                          </div>
                          <p className="issue-message">{issue.message}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Best Practices */}
                  {result.issues.best_practices && result.issues.best_practices.length > 0 && (
                    <div className="issue-category">
                      <h3 className="category-title">💡 Best Practices</h3>
                      {result.issues.best_practices.map((issue, index) => (
                        <div key={index} className={`issue-item ${getSeverityClass(issue.severity)}`}>
                          <div className="issue-header">
                            <span className="severity-icon">{getSeverityIcon(issue.severity)}</span>
                            <span className="issue-line">Line {issue.line || 'N/A'}</span>
                            <span className="severity-badge">{issue.severity}</span>
                          </div>
                          <p className="issue-message">{issue.message}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Inline Suggestions - GitHub Style */}
            {result && (
              <div className="inline-suggestions-section">
                <div className="section-header-with-actions">
                  <h2>🔧 Inline Suggestions</h2>
                  {acceptedSuggestions.length > 0 && (
                    <button
                      onClick={handleApplyAllAccepted}
                      className="btn-apply-accepted"
                    >
                      ✓ Apply {acceptedSuggestions.length} Accepted ({acceptedSuggestions.length})
                    </button>
                  )}
                </div>
                
                {(() => {
                  // Collect all issues with inline fixes
                  const allIssuesWithFixes = [];
                  
                  Object.values(result.issues).forEach(issueArray => {
                    if (Array.isArray(issueArray)) {
                      issueArray.forEach(issue => {
                        if (issue.original_code && issue.fixed_code) {
                          allIssuesWithFixes.push(issue);
                        }
                      });
                    }
                  });

                  if (allIssuesWithFixes.length === 0) {
                    return (
                      <div className="no-inline-suggestions">
                        💡 No inline suggestions available. Issues may not have specific line fixes or code has syntax errors.
                      </div>
                    );
                  }

                  return allIssuesWithFixes.map((issue, index) => (
                    <InlineSuggestion
                      key={`${issue.line}-${index}`}
                      issue={issue}
                      onAccept={handleAcceptSuggestion}
                      onReject={handleRejectSuggestion}
                    />
                  ));
                })()}
              </div>
            )}

            {/* Suggestions */}
            {result.suggestions && result.suggestions.length > 0 && (
              <div className="suggestions-section">
                <h2>💡 Suggestions</h2>
                <ul className="suggestions-list">
                  {result.suggestions.map((suggestion, index) => (
                    <li key={index} className="suggestion-item">
                      {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Fixed Code */}
            {result.fixed_code && !result.has_syntax_errors && (
              <div className="fixed-code-section">
                <div className="section-header-with-actions">
                  <h2>✨ Improved Code</h2>
                  <button
                    onClick={handleApplyFixes}
                    className="btn-apply-fixes"
                    title="Replace your code with the improved version"
                  >
                    🔧 Auto-Apply Fixes
                  </button>
                </div>
                <div className="code-comparison">
                  <div className="code-block">
                    <h3>Original</h3>
                    <pre className="code-display original">{code}</pre>
                  </div>
                  <div className="code-block">
                    <h3>Fixed</h3>
                    <pre className="code-display fixed">{result.fixed_code}</pre>
                    <div className="button-group-inline">
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(result.fixed_code);
                          alert('📋 Fixed code copied to clipboard!');
                        }}
                        className="btn-copy"
                      >
                        📋 Copy Fixed Code
                      </button>
                      <button
                        onClick={handleApplyFixes}
                        className="btn-apply"
                      >
                        ✅ Apply to Editor
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CodeAnalyzer;

// Made with Bob
