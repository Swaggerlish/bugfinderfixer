/**
 * API Service for Bug Finder & Fixer
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Analyze code using the backend API
 * @param {string} code - The code to analyze
 * @param {string} language - Programming language (default: 'python')
 * @returns {Promise<Object>} Analysis results
 * @throws {Error} If the request fails
 */
export const analyzeCode = async (code, language = 'python') => {
  // Validate input
  if (!code || typeof code !== 'string' || !code.trim()) {
    throw new Error('Code cannot be empty');
  }

  if (!language || typeof language !== 'string') {
    throw new Error('Language must be specified');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        code: code.trim(),
        language: language.toLowerCase(),
      }),
    });

    // Handle different HTTP status codes
    if (!response.ok) {
      const contentType = response.headers.get('content-type');
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

      // Try to parse error details from response
      if (contentType && contentType.includes('application/json')) {
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
        } catch (parseError) {
          console.warn('Could not parse error response:', parseError);
        }
      }

      // Provide user-friendly error messages
      switch (response.status) {
        case 400:
          throw new Error(`Invalid input: ${errorMessage}`);
        case 404:
          throw new Error('API endpoint not found. Please check if the backend is running.');
        case 500:
          throw new Error('Server error. Please try again later.');
        case 503:
          throw new Error('Service temporarily unavailable. Please try again.');
        default:
          throw new Error(errorMessage);
      }
    }

    // Parse response
    const data = await response.json();

    // Validate response structure
    if (!data || typeof data !== 'object') {
      throw new Error('Invalid response format from server');
    }

    // Ensure required fields exist
    if (!data.hasOwnProperty('success')) {
      console.warn('Response missing "success" field');
    }

    return data;

  } catch (error) {
    // Handle network errors
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error(
        'Cannot connect to the backend server. Please ensure:\n' +
        '1. Backend is running at ' + API_BASE_URL + '\n' +
        '2. CORS is properly configured\n' +
        '3. Network connection is stable'
      );
    }

    // Handle JSON parsing errors
    if (error.name === 'SyntaxError') {
      throw new Error('Invalid response from server. The backend may be experiencing issues.');
    }

    // Re-throw other errors
    throw error;
  }
};

/**
 * Check if the backend API is available
 * @returns {Promise<boolean>} True if API is reachable
 */
export const checkApiHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });
    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};

/**
 * Get API information
 * @returns {Promise<Object>} API info
 */
export const getApiInfo = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch API info');
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to get API info:', error);
    throw error;
  }
};

export default {
  analyzeCode,
  checkApiHealth,
  getApiInfo,
};

// Made with Bob
