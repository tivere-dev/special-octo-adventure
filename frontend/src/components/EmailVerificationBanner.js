import React, { useState } from 'react';
import { authService } from '../services/authService';
import './EmailVerificationBanner.css';

const EmailVerificationBanner = ({ user }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [dismissed, setDismissed] = useState(false);

  if (!user || user.email_verified || dismissed) {
    return null;
  }

  const handleResend = async () => {
    setLoading(true);
    setMessage('');
    
    try {
      await authService.resendVerificationEmail();
      setMessage('Verification email sent! Please check your inbox.');
    } catch (error) {
      setMessage(error.response?.data?.message || 'Failed to send verification email. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="verification-banner">
      <div className="verification-banner-content">
        <span className="verification-banner-icon">⚠️</span>
        <span className="verification-banner-text">
          Please verify your email address to unlock all features.
        </span>
        <button 
          onClick={handleResend} 
          disabled={loading}
          className="verification-banner-button"
        >
          {loading ? 'Sending...' : 'Resend Verification Email'}
        </button>
        <button 
          onClick={() => setDismissed(true)}
          className="verification-banner-close"
        >
          ×
        </button>
      </div>
      {message && (
        <div className={`verification-banner-message ${message.includes('sent') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default EmailVerificationBanner;
