# Quick Start Guide - Bug Finder & Fixer

Get up and running in 5 minutes! 🚀

## Step 1: Start the Backend (Terminal 1)

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

✅ **Backend running at:** http://localhost:8000  
✅ **API docs at:** http://localhost:8000/docs

## Step 2: Start the Frontend (Terminal 2)

```bash
cd frontend
npm install
npm start
```

✅ **Frontend running at:** http://localhost:3000

## Step 3: Test the Application

### Quick Test - Load Sample Code

1. Open http://localhost:3000 in your browser
2. Check the **green "API Connected"** indicator in the top right
3. Click **"📚 Load Sample Code"** dropdown
4. Select **"🔒 Security Issues"**
5. Click **"🔍 Analyze Code"**
6. Wait 1-2 seconds for results

### What You'll See:

**Issues Detected:**
- 🔴 **Security Issues** (Critical)
  - Hardcoded password
  - Hardcoded API key
  - Dangerous eval() usage
  - SQL injection vulnerability
- 🔵 **Style Issues** (Info)
  - Print statement found

**Suggestions:**
- Use environment variables for passwords
- Avoid eval(). Use ast.literal_eval()
- Use parameterized queries
- Use logging instead of print

**Fixed Code:**
- Side-by-side comparison
- Original vs. Improved code
- Click "📋 Copy Fixed Code" to copy
- Click "🔧 Auto-Apply Fixes" to replace your code (with confirmation)
- Click "✅ Apply to Editor" to apply fixes directly

## Sample Codes Available

### 🔒 Security Issues
Tests detection of:
- Hardcoded passwords
- eval() usage
- SQL injection
- Unsafe operations

### 🎨 Style Issues
Tests detection of:
- TODO comments
- Print statements
- Long lines
- Style violations

### 💡 Best Practices
Tests detection of:
- Missing docstrings
- Bare except clauses
- Missing type hints
- Code improvements

### ❌ Syntax Error
Tests:
- Syntax error detection
- Line number reporting
- No fixed code generation

### ✅ Clean Code
Tests:
- Well-written code
- Proper documentation
- Type hints
- Best practices

### 🔥 Complex Example
Tests:
- Multiple issue types
- Real-world scenarios
- Comprehensive analysis

## Verify Everything Works

### ✅ Checklist

- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Green "API Connected" indicator shows
- [ ] Can load sample code
- [ ] Analysis completes in 1-2 seconds
- [ ] Issues are displayed with colors
- [ ] Suggestions are shown
- [ ] Fixed code appears
- [ ] Can copy fixed code
- [ ] Can clear and try again

## Test API Directly (Optional)

### Using cURL:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def test():\n    password = \"admin123\"\n    print(\"hello\")",
    "language": "python"
  }'
```

### Using Browser:

Visit http://localhost:8000/docs for interactive API documentation

## Common Issues

### ❌ "API Offline" Warning

**Problem:** Backend not running  
**Solution:** 
```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn main:app --reload
```

### ❌ CORS Error in Console

**Problem:** CORS not configured  
**Solution:** Backend already configured for http://localhost:3000

### ❌ Port Already in Use

**Problem:** Port 8000 or 3000 already taken  
**Solution:**
```bash
# Backend on different port
uvicorn main:app --reload --port 8001

# Update frontend/src/services/api.js:
# const API_BASE_URL = 'http://localhost:8001';
```

### ❌ Module Not Found

**Problem:** Dependencies not installed  
**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Next Steps

1. **Try Different Samples:** Test all 6 sample codes
2. **Write Your Own Code:** Paste your code and analyze
3. **Test Error Handling:** Stop backend and see error messages
4. **Check API Docs:** Visit http://localhost:8000/docs
5. **Read Full Docs:** See README.md and TESTING.md

## Features to Try

### 1. Language Selection
- Change language dropdown
- Try JavaScript, Java, or Other
- See generic analysis for non-Python

### 2. Copy Fixed Code
- Analyze any code
- Scroll to "Improved Code"
- Click "📋 Copy Fixed Code"
- Paste in your editor

### 3. Clear and Retry
- Click "🗑️ Clear" button
- Enter new code
- Analyze again

### 4. API Status Monitoring
- Watch the status indicator
- Stop backend (Ctrl+C)
- See status turn red
- Restart backend
- Status turns green

## Performance Expectations

- **Analysis Time:** < 2 seconds for typical code
- **API Response:** < 1 second
- **UI Updates:** Instant
- **Large Files:** May take longer (1000+ lines)

## What's Being Tested

### Backend API:
✅ POST /api/analyze endpoint  
✅ JSON request/response  
✅ Error handling  
✅ CORS configuration  
✅ Code analysis logic  

### Frontend:
✅ API communication  
✅ State management (useState)  
✅ Effect hooks (useEffect)  
✅ Error handling  
✅ Loading states  
✅ Result display  
✅ User interactions  

## Success Indicators

You'll know everything works when:

1. ✅ No console errors
2. ✅ Green API status indicator
3. ✅ Sample codes load instantly
4. ✅ Analysis completes quickly
5. ✅ Issues are color-coded
6. ✅ Fixed code is generated
7. ✅ Copy function works
8. ✅ Clear button resets everything

## Need Help?

- Check **TESTING.md** for detailed test cases
- Check **README.md** for full documentation
- Check backend logs for errors
- Check browser console for frontend errors
- Verify both servers are running

---

**Happy Coding! 🎉**

Now you have a fully functional code analyzer with:
- Real-time API communication
- Comprehensive error handling
- Multiple test scenarios
- Beautiful UI with results display