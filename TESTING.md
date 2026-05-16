# Testing Guide - Bug Finder & Fixer

This guide will help you test the complete application, including API communication between frontend and backend.

## Prerequisites

Before testing, ensure you have:
- Python 3.8+ installed
- Node.js 14+ installed
- Both backend and frontend running

## Setup for Testing

### 1. Start the Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Backend should be running at: http://localhost:8000

### 2. Start the Frontend

In a new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend should open at: http://localhost:3000

## Test Cases

### Test 1: API Connection Status

**Expected Behavior:**
- Green "API Connected" indicator should appear in the header
- If backend is not running, you'll see a yellow warning banner

**Steps:**
1. Open http://localhost:3000
2. Check the API status indicator in the top right
3. Stop the backend server
4. Refresh the page - should show "API Offline"
5. Restart backend - status should turn green

### Test 2: Basic Code Analysis

**Test Code:**
```python
def add(a, b):
    return a + b
```

**Expected Results:**
- Issues detected:
  - Missing docstring
  - Missing type hints
- Suggestions provided
- Fixed code generated with docstring and type hints

**Steps:**
1. Paste the code in the textarea
2. Click "🔍 Analyze Code"
3. Wait for results (should take 1-2 seconds)
4. Verify issues are displayed
5. Check fixed code section

### Test 3: Security Issues Detection

**Test Code:**
```python
def unsafe_function(user_input):
    password = "admin123"
    result = eval(user_input)
    print(result)
    return result
```

**Expected Results:**
- Security issues:
  - Hardcoded password (critical)
  - Dangerous use of eval() (critical)
- Style issues:
  - Print statement (info)
- Fixed code with improvements

**Steps:**
1. Load the example code (or paste above)
2. Click "🔍 Analyze Code"
3. Verify security issues are marked as critical (red)
4. Check that fixed code replaces eval with ast.literal_eval
5. Verify password is replaced with environment variable

### Test 4: Syntax Error Detection

**Test Code:**
```python
def broken_function(
    print("Missing closing parenthesis"
```

**Expected Results:**
- Syntax error detected
- Line number shown
- No fixed code generated (due to syntax errors)
- Clear error message

**Steps:**
1. Paste the broken code
2. Click "🔍 Analyze Code"
3. Verify syntax error is displayed
4. Check that "has_syntax_errors" is true
5. Verify no fixed code is shown

### Test 5: Empty Input Validation

**Expected Results:**
- Error message: "Please enter some code to analyze"
- No API call made

**Steps:**
1. Clear the textarea
2. Click "🔍 Analyze Code"
3. Verify error message appears
4. Check browser console - no network request should be made

### Test 6: Network Error Handling

**Expected Results:**
- User-friendly error message
- API status changes to offline

**Steps:**
1. Stop the backend server
2. Enter some code
3. Click "🔍 Analyze Code"
4. Verify error message mentions backend connection
5. Check API status indicator turns red

### Test 7: Language Selection

**Test Code (JavaScript):**
```javascript
function add(a, b) {
    // TODO: Add validation
    return a + b;
}
```

**Expected Results:**
- Generic analysis for non-Python code
- TODO comment detected
- Basic suggestions provided

**Steps:**
1. Select "JavaScript" from language dropdown
2. Paste the code
3. Click "🔍 Analyze Code"
4. Verify analysis completes
5. Check that TODO is detected

### Test 8: Copy Fixed Code

**Expected Results:**
- Fixed code copied to clipboard
- Success alert shown

**Steps:**
1. Analyze any code that generates fixed code
2. Scroll to "Improved Code" section
3. Click "📋 Copy Fixed Code"
4. Verify alert appears
5. Paste in a text editor to confirm

### Test 9: Clear Functionality

**Expected Results:**
- Textarea cleared
- Results removed
- Error messages cleared

**Steps:**
1. Enter code and analyze
2. Click "🗑️ Clear" button
3. Verify all fields are reset
4. Verify results section disappears

### Test 10: Load Example

**Expected Results:**
- Example code loaded into textarea
- Code contains multiple issues for testing

**Steps:**
1. Click "Load Example" button
2. Verify code appears in textarea
3. Analyze the example
4. Verify multiple issue types are detected

## API Testing with cURL

You can also test the backend API directly:

### Test Analyze Endpoint

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def test():\n    print(\"hello\")",
    "language": "python"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Code analysis completed successfully",
  "issues": {
    "style_issues": [...]
  },
  "suggestions": [...],
  "fixed_code": "...",
  "has_syntax_errors": false
}
```

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy"
}
```

### Test Root Endpoint

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "Bug Finder & Fixer API",
  "status": "running",
  "docs": "/docs"
}
```

## Browser Developer Tools Testing

### Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Analyze some code
4. Check the request:
   - Method: POST
   - URL: http://localhost:8000/api/analyze
   - Status: 200 OK
   - Response: JSON with analysis results

### Console Tab
1. Check for any JavaScript errors
2. Verify API calls are logged
3. Check error handling messages

## Performance Testing

### Response Time
- Analysis should complete in < 2 seconds for typical code
- Loading state should be visible during processing
- No UI freezing during analysis

### Large Code Files
Test with code > 1000 lines:
- Should handle gracefully
- May take longer to analyze
- Should not crash

## Error Scenarios to Test

1. **Backend Crash**: Stop backend mid-request
2. **Invalid JSON**: Modify API service to send malformed data
3. **Timeout**: Test with very large code files
4. **CORS Issues**: Access from different origin
5. **Rate Limiting**: Send many requests quickly

## Accessibility Testing

1. **Keyboard Navigation**: Tab through all interactive elements
2. **Screen Reader**: Test with screen reader software
3. **Color Contrast**: Verify text is readable
4. **Focus Indicators**: Check visible focus states

## Mobile Testing

1. Open http://localhost:3000 on mobile device (same network)
2. Test all functionality
3. Verify responsive design
4. Check touch interactions

## Common Issues and Solutions

### Issue: API Status shows "Offline"
**Solution:** 
- Verify backend is running on port 8000
- Check CORS configuration in backend
- Verify no firewall blocking

### Issue: "CORS Error" in console
**Solution:**
- Check backend CORS middleware
- Verify frontend URL is in allow_origins
- Restart backend after changes

### Issue: Analysis takes too long
**Solution:**
- Check backend logs for errors
- Verify code isn't too large
- Check system resources

### Issue: Fixed code not showing
**Solution:**
- Check if syntax errors exist
- Verify backend is generating fixed code
- Check browser console for errors

## Automated Testing (Future)

Consider adding:
- Unit tests for API service
- Integration tests for components
- E2E tests with Cypress or Playwright
- Backend API tests with pytest

## Reporting Issues

When reporting issues, include:
1. Steps to reproduce
2. Expected vs actual behavior
3. Browser console errors
4. Backend logs
5. Screenshots if applicable

---

**Happy Testing! 🧪**