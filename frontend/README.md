# Bug Finder & Fixer - Frontend

React-based frontend for the Bug Finder & Fixer application.

## Features

- 📝 **Code Input**: Large textarea for pasting code
- 🔍 **Code Analysis**: Submit code to FastAPI backend for analysis
- 🐛 **Issue Display**: Categorized display of detected issues:
  - Syntax Errors
  - Security Issues
  - Style Issues
  - Best Practices
- 💡 **Suggestions**: List of actionable suggestions
- ✨ **Fixed Code**: Side-by-side comparison of original and improved code
- 📋 **Copy to Clipboard**: Easy copying of fixed code
- 🎨 **Modern UI**: Clean, responsive design with gradient backgrounds
- 🌐 **Multi-language Support**: Python, JavaScript, Java, and more

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend API running on http://localhost:8000

## Installation

1. Install dependencies:
```bash
npm install
```

## Running the Application

Start the development server:
```bash
npm start
```

The app will open at http://localhost:3000

## Project Structure

```
frontend/
├── public/              # Static files
├── src/
│   ├── components/      # React components
│   │   ├── CodeAnalyzer.js    # Main analyzer component
│   │   └── CodeAnalyzer.css   # Component styles
│   ├── App.js          # Main app component
│   ├── App.css         # App styles
│   ├── index.js        # Entry point
│   └── index.css       # Global styles
└── package.json        # Dependencies
```

## Usage

1. **Enter Code**: Paste or type your code in the textarea
2. **Select Language**: Choose the programming language (default: Python)
3. **Analyze**: Click "🔍 Analyze Code" button
4. **Review Results**:
   - View categorized issues with severity levels
   - Read suggestions for improvements
   - Compare original vs. fixed code
5. **Copy Fixed Code**: Click "📋 Copy Fixed Code" to copy improvements

## Features in Detail

### Code Input
- Large, syntax-highlighted textarea
- Language selector (Python, JavaScript, Java, Other)
- "Load Example" button for quick testing
- "Clear" button to reset

### Issue Display
Issues are categorized and color-coded by severity:
- 🔴 **Critical**: Red (security issues, syntax errors)
- 🟡 **Warning**: Yellow (potential problems)
- 🔵 **Info**: Blue (style suggestions, best practices)

Each issue shows:
- Line number
- Severity level
- Detailed message

### Fixed Code Comparison
- Side-by-side view of original and improved code
- Syntax highlighting
- One-click copy to clipboard

## API Integration

The frontend connects to the FastAPI backend at:
```
POST http://localhost:8000/api/analyze
```

Request format:
```json
{
  "code": "your code here",
  "language": "python"
}
```

Response format:
```json
{
  "success": true,
  "message": "Code analysis completed successfully",
  "issues": {
    "syntax_errors": [...],
    "security_issues": [...],
    "style_issues": [...],
    "best_practices": [...]
  },
  "suggestions": [...],
  "fixed_code": "improved code",
  "has_syntax_errors": false
}
```

## Customization

### Changing API URL
Edit `src/components/CodeAnalyzer.js`:
```javascript
const API_URL = 'http://your-api-url/api/analyze';
```

### Styling
- Modify `src/App.css` for overall app styling
- Modify `src/components/CodeAnalyzer.css` for component-specific styles

## Building for Production

Create an optimized production build:
```bash
npm run build
```

The build folder will contain the production-ready files.

## Technologies Used

- **React 19**: UI framework
- **Hooks**: useState for state management
- **Fetch API**: HTTP requests to backend
- **CSS3**: Modern styling with gradients and animations
- **Responsive Design**: Mobile-friendly layout

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### CORS Errors
Make sure the backend CORS middleware allows requests from http://localhost:3000

### API Connection Failed
1. Verify backend is running on http://localhost:8000
2. Check backend logs for errors
3. Verify network connectivity

### Styling Issues
Clear browser cache and reload the page

## Future Enhancements

- [ ] Syntax highlighting in code editor
- [ ] Dark mode toggle
- [ ] Save/load code snippets
- [ ] Export analysis reports
- [ ] Real-time analysis as you type
- [ ] Multiple file analysis
- [ ] Integration with GitHub
