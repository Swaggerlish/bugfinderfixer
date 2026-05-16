import React, { useState } from 'react';
import './InlineSuggestion.css';

const InlineSuggestion = ({ issue, onAccept, onReject }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [status, setStatus] = useState('pending'); // 'pending', 'accepted', 'rejected'

  const handleAccept = () => {
    setStatus('accepted');
    onAccept(issue);
  };

  const handleReject = () => {
    setStatus('rejected');
    onReject(issue);
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

  if (!issue.original_code || !issue.fixed_code) {
    return null; // Don't show if no inline fix available
  }

  return (
    <div className={`inline-suggestion ${getSeverityClass(issue.severity)} ${status}`}>
      <div className="suggestion-header" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="header-left">
          <span className="severity-icon">{getSeverityIcon(issue.severity)}</span>
          <span className="line-number">Line {issue.line || 'N/A'}</span>
          <span className="severity-badge">{issue.severity}</span>
          {status === 'accepted' && <span className="status-badge accepted">✓ Accepted</span>}
          {status === 'rejected' && <span className="status-badge rejected">✗ Rejected</span>}
        </div>
        <button className="expand-toggle">
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>

      {isExpanded && (
        <div className="suggestion-body">
          <div className="issue-message">
            <strong>{issue.message}</strong>
          </div>

          <div className="code-diff">
            <div className="diff-section removed">
              <div className="diff-header">
                <span className="diff-icon">−</span>
                <span>Current Code</span>
              </div>
              <pre className="diff-code">{issue.original_code}</pre>
            </div>

            <div className="diff-section added">
              <div className="diff-header">
                <span className="diff-icon">+</span>
                <span>Suggested Fix</span>
              </div>
              <pre className="diff-code">{issue.fixed_code}</pre>
            </div>
          </div>

          {status === 'pending' && (
            <div className="suggestion-actions">
              <button 
                onClick={handleAccept}
                className="btn-accept"
                title="Accept this suggestion"
              >
                ✓ Accept
              </button>
              <button 
                onClick={handleReject}
                className="btn-reject"
                title="Reject this suggestion"
              >
                ✗ Reject
              </button>
            </div>
          )}

          {status === 'accepted' && (
            <div className="status-message accepted">
              ✓ This suggestion has been accepted and will be applied to your code.
            </div>
          )}

          {status === 'rejected' && (
            <div className="status-message rejected">
              ✗ This suggestion has been rejected and will not be applied.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default InlineSuggestion;

// Made with Bob
