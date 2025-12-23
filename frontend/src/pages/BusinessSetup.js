import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { businessService } from '../services/businessService';
import './Auth.css';

const BusinessSetup = () => {
  const navigate = useNavigate();
  const { refreshProfile } = useAuth();
  
  const [formData, setFormData] = useState({
    businessName: '',
    currency: 'USD',
    logo: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [logoPreview, setLogoPreview] = useState(null);

  const currencies = [
    { value: 'USD', label: 'US Dollar (USD)' },
    { value: 'GBP', label: 'British Pound (GBP)' },
    { value: 'EUR', label: 'Euro (EUR)' },
    { value: 'NGN', label: 'Nigerian Naira (NGN)' },
    { value: 'KES', label: 'Kenyan Shilling (KES)' },
    { value: 'ZAR', label: 'South African Rand (ZAR)' },
    { value: 'GHS', label: 'Ghanaian Cedi (GHS)' },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLogoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        setError('Logo file size must not exceed 5MB');
        return;
      }
      
      if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
        setError('Only JPEG and PNG images are allowed');
        return;
      }

      setFormData(prev => ({
        ...prev,
        logo: file
      }));
      
      const reader = new FileReader();
      reader.onloadend = () => {
        setLogoPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.businessName.length < 2) {
      setError('Business name must be at least 2 characters long');
      return;
    }

    setLoading(true);

    try {
      await businessService.setupBusiness(
        formData.businessName,
        formData.currency,
        formData.logo
      );
      await refreshProfile();
      navigate('/dashboard');
    } catch (error) {
      setError(error.response?.data?.message || 'Business setup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">Business Setup</h1>
        <p className="auth-subtitle">Let's set up your business profile</p>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="businessName">Business Name *</label>
            <input
              type="text"
              id="businessName"
              name="businessName"
              value={formData.businessName}
              onChange={handleChange}
              required
              placeholder="Your Business Name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="currency">Currency *</label>
            <select
              id="currency"
              name="currency"
              value={formData.currency}
              onChange={handleChange}
              required
            >
              {currencies.map(currency => (
                <option key={currency.value} value={currency.value}>
                  {currency.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="logo">Business Logo (optional)</label>
            <input
              type="file"
              id="logo"
              name="logo"
              accept="image/jpeg,image/png,image/jpg"
              onChange={handleLogoChange}
            />
            {logoPreview && (
              <div style={{ marginTop: '10px' }}>
                <img 
                  src={logoPreview} 
                  alt="Logo preview" 
                  style={{ 
                    maxWidth: '150px', 
                    maxHeight: '150px', 
                    borderRadius: '8px',
                    border: '1px solid #cbd5e0'
                  }} 
                />
              </div>
            )}
          </div>

          <button 
            type="submit" 
            className="auth-button"
            disabled={loading}
          >
            {loading ? 'Setting up...' : 'Complete Setup'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default BusinessSetup;
