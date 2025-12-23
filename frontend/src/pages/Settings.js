import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { authService } from '../services/authService';
import { businessService } from '../services/businessService';
import { validatePassword } from '../utils/passwordValidation';
import './Settings.css';

const Settings = () => {
  const navigate = useNavigate();
  const { user, business, refreshProfile } = useAuth();
  
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const [profileData, setProfileData] = useState({
    username: user?.username || '',
    email: user?.email || '',
  });

  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const [businessData, setBusinessData] = useState({
    businessName: business?.business_name || '',
    currency: business?.currency || 'USD',
    logo: null,
  });

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleBusinessChange = (e) => {
    const { name, value, files } = e.target;
    setBusinessData(prev => ({
      ...prev,
      [name]: files ? files[0] : value
    }));
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      await authService.updateProfile(profileData);
      await refreshProfile();
      setMessage({ type: 'success', text: 'Profile updated successfully' });
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.message || 'Failed to update profile' });
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMessage({ type: 'error', text: 'Passwords do not match' });
      setLoading(false);
      return;
    }

    const passwordErrors = validatePassword(passwordData.newPassword);
    if (passwordErrors.length > 0) {
      setMessage({ type: 'error', text: passwordErrors[0] });
      setLoading(false);
      return;
    }

    try {
      await authService.changePassword(
        passwordData.currentPassword,
        passwordData.newPassword,
        passwordData.confirmPassword
      );
      setMessage({ type: 'success', text: 'Password changed successfully. Redirecting to login...' });
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.message || 'Failed to change password' });
    } finally {
      setLoading(false);
    }
  };

  const handleBusinessSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      await businessService.updateBusiness(businessData);
      await refreshProfile();
      setMessage({ type: 'success', text: 'Business updated successfully' });
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.message || 'Failed to update business' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="settings-container">
      <div className="settings-header">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          ← Back to Dashboard
        </button>
        <h1>Account Settings</h1>
      </div>

      <div className="settings-content">
        <div className="settings-tabs">
          <button 
            className={`tab ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            Profile
          </button>
          <button 
            className={`tab ${activeTab === 'password' ? 'active' : ''}`}
            onClick={() => setActiveTab('password')}
          >
            Password
          </button>
          <button 
            className={`tab ${activeTab === 'business' ? 'active' : ''}`}
            onClick={() => setActiveTab('business')}
          >
            Business
          </button>
        </div>

        {message.text && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}

        {activeTab === 'profile' && (
          <form onSubmit={handleProfileSubmit} className="settings-form">
            <h2>Profile Information</h2>
            
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={profileData.username}
                onChange={handleProfileChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={profileData.email}
                onChange={handleProfileChange}
              />
            </div>

            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        )}

        {activeTab === 'password' && (
          <form onSubmit={handlePasswordSubmit} className="settings-form">
            <h2>Change Password</h2>
            
            <div className="form-group">
              <label htmlFor="currentPassword">Current Password</label>
              <input
                type="password"
                id="currentPassword"
                name="currentPassword"
                value={passwordData.currentPassword}
                onChange={handlePasswordChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="newPassword">New Password</label>
              <input
                type="password"
                id="newPassword"
                name="newPassword"
                value={passwordData.newPassword}
                onChange={handlePasswordChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm New Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={passwordData.confirmPassword}
                onChange={handlePasswordChange}
                required
              />
            </div>

            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? 'Changing...' : 'Change Password'}
            </button>
          </form>
        )}

        {activeTab === 'business' && business && (
          <form onSubmit={handleBusinessSubmit} className="settings-form">
            <h2>Business Information</h2>
            
            <div className="form-group">
              <label htmlFor="businessName">Business Name</label>
              <input
                type="text"
                id="businessName"
                name="businessName"
                value={businessData.businessName}
                onChange={handleBusinessChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="currency">Currency</label>
              <select
                id="currency"
                name="currency"
                value={businessData.currency}
                onChange={handleBusinessChange}
              >
                <option value="USD">US Dollar (USD)</option>
                <option value="GBP">British Pound (GBP)</option>
                <option value="EUR">Euro (EUR)</option>
                <option value="NGN">Nigerian Naira (NGN)</option>
                <option value="KES">Kenyan Shilling (KES)</option>
                <option value="ZAR">South African Rand (ZAR)</option>
                <option value="GHS">Ghanaian Cedi (GHS)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="logo">Business Logo</label>
              <input
                type="file"
                id="logo"
                name="logo"
                accept="image/jpeg,image/png,image/jpg"
                onChange={handleBusinessChange}
              />
            </div>

            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default Settings;
