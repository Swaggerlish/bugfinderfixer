# IBM watsonx AI Integration Setup Guide

This guide will help you set up IBM watsonx AI for intelligent code analysis across ANY programming language.

## 🎯 Benefits of AI-Powered Analysis

- ✅ **Universal Language Support**: Analyze code in ANY language (C++, Java, Python, JavaScript, Go, Rust, PHP, Ruby, etc.)
- ✅ **Intelligent Error Detection**: Finds syntax errors, typos, incomplete expressions, logic errors
- ✅ **Context-Aware Fixes**: Provides smart fixes based on code context
- ✅ **Security Analysis**: Detects security vulnerabilities and best practice violations
- ✅ **Learning Capability**: Improves with usage and understands complex patterns

## 📋 Prerequisites

1. **IBM Cloud Account**: Sign up at https://cloud.ibm.com
2. **watsonx.ai Access**: Enable watsonx.ai in your IBM Cloud account
3. **Project Created**: Create a project in watsonx.ai

## 🔑 Step 1: Get Your watsonx Credentials

### 1.1 Get API Key

1. Go to https://cloud.ibm.com/iam/apikeys
2. Click **"Create an IBM Cloud API key"**
3. Give it a name (e.g., "BugFinderFixer")
4. Click **"Create"**
5. **Copy and save the API key** (you won't see it again!)

### 1.2 Get Project ID

1. Go to https://dataplatform.cloud.ibm.com/projects
2. Click on your project
3. Go to **"Manage"** tab
4. Copy the **"Project ID"** (looks like: `12345678-1234-1234-1234-123456789abc`)

### 1.3 Get API Endpoint

Your endpoint depends on your region:
- **US South**: `https://us-south.ml.cloud.ibm.com`
- **EU Germany**: `https://eu-de.ml.cloud.ibm.com`
- **Japan Tokyo**: `https://jp-tok.ml.cloud.ibm.com`

## 🛠️ Step 2: Configure Backend

### 2.1 Create `.env` File

In the `backend/` directory, create a `.env` file:

```bash
cd backend
cp .env.example .env
```

### 2.2 Add Your Credentials

Edit `backend/.env` and add your credentials:

```env
# Enable AI Analyzer
USE_AI_ANALYZER=true

# IBM watsonx Configuration
WATSONX_API_KEY=your-actual-api-key-here
WATSONX_PROJECT_ID=your-actual-project-id-here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL=ibm/granite-13b-chat-v2
```

**Replace:**
- `your-actual-api-key-here` with your IBM Cloud API key
- `your-actual-project-id-here` with your watsonx project ID

### 2.3 Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `ibm-watsonx-ai` - IBM watsonx SDK
- `requests` - HTTP library
- Other required packages

## 🚀 Step 3: Start the Backend

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 🧪 Step 4: Test AI Analysis

### 4.1 Test with API Docs

1. Open http://localhost:8000/docs
2. Click on **POST /analyze**
3. Click **"Try it out"**
4. Paste test code (any language):

```cpp
int main() {
    cout << "Hello";  // Missing include
    return 0
}  // Missing semicolon
```

5. Click **"Execute"**
6. See AI-powered analysis results!

### 4.2 Test with Frontend

1. Start frontend: `cd frontend && npm start`
2. Open http://localhost:3000
3. Select any language (C++, Java, Python, etc.)
4. Paste code with errors
5. Click **"Analyze Code"**
6. See intelligent error detection and fixes!

## 🎨 Available Models

You can change the model in `.env`:

### Code-Specialized Models (Recommended)
```env
# Best for code analysis
WATSONX_MODEL=ibm/granite-20b-code-instruct-v2

# Good for code understanding
WATSONX_MODEL=codellama/codellama-34b-instruct-hf
```

### General Purpose Models
```env
# Balanced performance
WATSONX_MODEL=ibm/granite-13b-chat-v2

# More powerful but slower
WATSONX_MODEL=meta-llama/llama-2-70b-chat
```

## 🔄 Switching Between AI and Rule-Based

### Use AI Analyzer (Recommended)
```env
USE_AI_ANALYZER=true
```

### Use Rule-Based Analyzer (Fallback)
```env
USE_AI_ANALYZER=false
```

The system automatically falls back to rule-based analysis if:
- watsonx credentials are missing
- API is unavailable
- Rate limits are reached

## 📊 What AI Can Detect

### Syntax Errors
- Missing semicolons, brackets, parentheses
- Incomplete expressions (`x +`, `y /`)
- Typos in keywords (`cou` → `cout`, `printl` → `println`)
- Missing imports/includes

### Logic Errors
- Division by zero
- Null pointer dereferences
- Array out of bounds
- Infinite loops

### Security Issues
- SQL injection vulnerabilities
- Buffer overflows
- Hardcoded credentials
- Unsafe deserialization

### Best Practices
- Code style violations
- Missing error handling
- Memory leaks
- Inefficient algorithms

## 🌍 Supported Languages

The AI analyzer supports **ANY** programming language:

- ✅ C/C++
- ✅ Java
- ✅ Python
- ✅ JavaScript/TypeScript
- ✅ Go
- ✅ Rust
- ✅ PHP
- ✅ Ruby
- ✅ Swift
- ✅ Kotlin
- ✅ C#
- ✅ And many more!

## 🚀 Production Deployment

### For Render

Add environment variables in Render dashboard:

```
USE_AI_ANALYZER=true
WATSONX_API_KEY=your-api-key
WATSONX_PROJECT_ID=your-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL=ibm/granite-13b-chat-v2
```

### For Vercel (Frontend)

No changes needed! Frontend automatically uses the backend API.

## 🐛 Troubleshooting

### Issue: "AI analysis unavailable"

**Solution:**
1. Check `.env` file exists in `backend/` directory
2. Verify credentials are correct
3. Ensure `USE_AI_ANALYZER=true`
4. Check API key is valid: https://cloud.ibm.com/iam/apikeys

### Issue: "Authentication failed"

**Solution:**
1. Regenerate API key in IBM Cloud
2. Update `.env` with new key
3. Restart backend server

### Issue: "Project not found"

**Solution:**
1. Verify project ID is correct
2. Ensure project exists in watsonx.ai
3. Check you have access to the project

### Issue: "Rate limit exceeded"

**Solution:**
1. Wait a few minutes
2. Upgrade your IBM Cloud plan
3. Use rule-based analyzer temporarily: `USE_AI_ANALYZER=false`

## 💡 Tips for Best Results

1. **Be Specific**: Provide complete code context
2. **Use Correct Language**: Select the right language in dropdown
3. **Check Suggestions**: Review AI suggestions carefully
4. **Iterate**: Apply fixes and re-analyze
5. **Report Issues**: If AI misses errors, report them

## 📚 Additional Resources

- **IBM watsonx Docs**: https://www.ibm.com/docs/en/watsonx-as-a-service
- **API Reference**: https://ibm.github.io/watsonx-ai-python-sdk/
- **Model Catalog**: https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html
- **Pricing**: https://www.ibm.com/products/watsonx-ai/pricing

## 🎉 Success!

Once configured, your code analyzer will:
- ✅ Detect errors in ANY programming language
- ✅ Provide intelligent fixes
- ✅ Learn from patterns
- ✅ Improve code quality

Happy coding! 🚀

---

**Made with Bob**