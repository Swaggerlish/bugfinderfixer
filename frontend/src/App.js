import React from 'react';
import './App.css';
import CodeAnalyzer from './components/CodeAnalyzer';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🐛 Bug Finder & Fixer</h1>
        <p className="subtitle">Analyze your code for bugs, security issues, and best practices</p>
      </header>
      <main className="App-main">
        <CodeAnalyzer />
      </main>
      <footer className="App-footer">
        <p>Powered by FastAPI & React</p>
      </footer>
    </div>
  );
}

export default App;

// Made with Bob
