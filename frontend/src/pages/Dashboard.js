import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import EmailVerificationBanner from '../components/EmailVerificationBanner';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, business, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <EmailVerificationBanner user={user} />
      
      <header className="dashboard-header">
        <div className="dashboard-header-content">
          <h1>SME Finance App</h1>
          <div className="dashboard-user-menu">
            <span className="user-email">{user?.email}</span>
            <button onClick={() => navigate('/settings')} className="settings-button">
              Settings
            </button>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-content">
          <div className="welcome-section">
            <h2>Welcome back!</h2>
            {business && (
              <div className="business-info">
                <h3>{business.business_name}</h3>
                <p>Currency: {business.currency}</p>
                {business.business_logo && (
                  <img 
                    src={business.business_logo} 
                    alt="Business logo" 
                    className="business-logo"
                  />
                )}
              </div>
            )}
          </div>

          <div className="dashboard-cards">
            <div className="dashboard-card">
              <h3>Quick Stats</h3>
              <p>Your business analytics will appear here</p>
            </div>
            
            <div className="dashboard-card">
              <h3>Recent Transactions</h3>
              <p>Recent transaction history will appear here</p>
            </div>
            
            <div className="dashboard-card">
              <h3>Reports</h3>
              <p>Financial reports will appear here</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
