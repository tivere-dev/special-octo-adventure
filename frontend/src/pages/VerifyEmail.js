import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authService } from '../services/authService';
import './Auth.css';

const VerifyEmail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('verifying');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    
    if (!token) {
      setStatus('error');
      setMessage('Invalid verification link');
      return;
    }

    verifyEmail(token);
  }, [searchParams]);

  const verifyEmail = async (token) => {
    try {
      await authService.verifyEmail(token);
      setStatus('success');
      setMessage('Email verified successfully! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (error) {
      setStatus('error');
      setMessage(error.response?.data?.message || 'Email verification failed. The link may be invalid or expired.');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">Email Verification</h1>
        
        {status === 'verifying' && (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <div className="spinner"></div>
            <p>Verifying your email...</p>
          </div>
        )}

        {status === 'success' && (
          <div className="auth-success">{message}</div>
        )}

        {status === 'error' && (
          <>
            <div className="auth-error">{message}</div>
            <button 
              onClick={() => navigate('/login')}
              className="auth-button"
              style={{ marginTop: '20px' }}
            >
              Go to Login
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default VerifyEmail;
