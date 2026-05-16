# How to Use Auto-Apply Fixes Feature

## 📍 Where to Find the Buttons

The Auto-Apply buttons **only appear** after you analyze code that has issues and the backend generates fixed code.

## Step-by-Step Guide

### Step 1: Start the Application
```bash
# Terminal 1
start-backend.bat

# Terminal 2  
start-frontend.bat
```

### Step 2: Load Sample Code
1. Open http://localhost:3000 in your browser
2. Click the **"📚 Load Sample Code"** dropdown button
3. Select **"🔒 Security Issues"** from the menu

### Step 3: Analyze the Code
1. Click the **"🔍 Analyze Code"** button
2. Wait 1-2 seconds for analysis to complete

### Step 4: Scroll Down to See Results
After analysis completes, you'll see several sections:
1. **🐛 Detected Issues** - List of problems found
2. **💡 Suggestions** - Recommendations
3. **✨ Improved Code** - This is where the buttons are!

### Step 5: Find the Auto-Apply Buttons

In the **"✨ Improved Code"** section, you'll see:

```
┌─────────────────────────────────────────────────────┐
│  ✨ Improved Code          🔧 Auto-Apply Fixes      │  ← Button 1 (Orange)
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐        ┌──────────────┐          │
│  │  Original    │        │    Fixed     │          │
│  │              │        │              │          │
│  │  Your code   │        │  Improved    │          │
│  │  here        │        │  code here   │          │
│  │              │        │              │          │
│  └──────────────┘        │              │          │
│                          │  📋 Copy     │          │
│                          │  ✅ Apply    │  ← Button 2 (Blue)
│                          └──────────────┘          │
└─────────────────────────────────────────────────────┘
```

### Button Locations:

**Button 1: 🔧 Auto-Apply Fixes**
- Location: Top right of "Improved Code" section
- Color: Orange gradient
- Large and prominent

**Button 2: ✅ Apply to Editor**
- Location: Bottom of the "Fixed" code block
- Color: Blue
- Next to "📋 Copy Fixed Code" button

## Why You Might Not See the Buttons

### Reason 1: No Fixed Code Generated
- **Problem:** Code has syntax errors
- **Solution:** Fix syntax errors first, then analyze

### Reason 2: Code is Already Perfect
- **Problem:** No issues found, no fixes needed
- **Solution:** Try a sample with issues (Security Issues, Style Issues, etc.)

### Reason 3: Backend Not Running
- **Problem:** API is offline
- **Solution:** Start backend with `start-backend.bat`

### Reason 4: Analysis Not Complete
- **Problem:** Still loading
- **Solution:** Wait for analysis to finish

### Reason 5: Need to Scroll Down
- **Problem:** Buttons are below the fold
- **Solution:** Scroll down to "✨ Improved Code" section

## Testing Right Now

### Quick Test (30 seconds):

1. **Make sure both servers are running:**
   ```bash
   # Check Terminal 1 shows:
   INFO: Uvicorn running on http://0.0.0.0:8000
   
   # Check Terminal 2 shows:
   Compiled successfully!
   ```

2. **In the browser:**
   - Click "📚 Load Sample Code"
   - Select "🔒 Security Issues"
   - Click "🔍 Analyze Code"
   - **Scroll down** to see results
   - Look for "✨ Improved Code" section
   - You should see the orange "🔧 Auto-Apply Fixes" button

3. **If you still don't see it:**
   - Open browser console (F12)
   - Check for any errors
   - Verify the "✨ Improved Code" section exists
   - Check if `result.fixed_code` has content

## Using the Buttons

### Method 1: Top Button (Recommended)
1. Click **"🔧 Auto-Apply Fixes"** (orange button)
2. Read the confirmation dialog
3. Click **"OK"** to apply or **"Cancel"** to abort
4. If OK: Code is replaced in editor
5. Success message appears

### Method 2: Bottom Button
1. Review the fixed code first
2. Click **"✅ Apply to Editor"** (blue button)
3. Same confirmation dialog appears
4. Click **"OK"** to apply

## What Happens When You Click

1. **Confirmation Dialog Appears:**
   ```
   🔧 Auto-Apply Fixes
   
   This will replace your current code with the improved version.
   
   Do you want to proceed?
   
   [Cancel] [OK]
   ```

2. **If you click OK:**
   - Original code in textarea is replaced
   - Fixed code becomes the new code
   - Success alert appears
   - Results section clears
   - You can analyze the new code again

3. **If you click Cancel:**
   - Nothing changes
   - Original code remains
   - You can continue reviewing

## Troubleshooting

### "I clicked but nothing happened"
- Check browser console for errors
- Make sure you clicked "OK" in the confirmation dialog
- Try refreshing the page and analyzing again

### "The button is grayed out"
- This shouldn't happen, but if it does:
- Refresh the page
- Analyze code again

### "I don't see the 'Improved Code' section"
- Make sure analysis completed successfully
- Check that backend returned fixed_code
- Try a different sample code
- Check browser console for errors

## Visual Checklist

After clicking "🔍 Analyze Code", you should see:

- ✅ Loading indicator disappears
- ✅ "🐛 Detected Issues" section appears
- ✅ Issues are listed with colors
- ✅ "💡 Suggestions" section appears
- ✅ "✨ Improved Code" section appears
- ✅ Orange "🔧 Auto-Apply Fixes" button visible
- ✅ Side-by-side code comparison shown
- ✅ Blue "✅ Apply to Editor" button visible

If all checkmarks are present, the feature is working!

## Need More Help?

1. **Check if frontend updated:**
   - Stop frontend (Ctrl+C)
   - Run `npm start` again
   - Refresh browser

2. **Check browser cache:**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

3. **Check console:**
   - Press F12
   - Go to Console tab
   - Look for errors

4. **Verify files:**
   - Make sure `frontend/src/components/CodeAnalyzer.js` has `handleApplyFixes` function
   - Make sure `frontend/src/components/CodeAnalyzer.css` has button styles

---

**The buttons are there! Just scroll down to the "✨ Improved Code" section after analyzing code with issues.** 🎉