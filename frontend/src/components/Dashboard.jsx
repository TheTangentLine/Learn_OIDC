import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <nav className="dashboard-nav">
        <div className="nav-content">
          <h2>OIDC Auth App</h2>
          <button onClick={handleLogout} className="btn btn-logout">
            Logout
          </button>
        </div>
      </nav>

      <main className="dashboard-main">
        <div className="welcome-section">
          <h1>🎉 Welcome to Your Dashboard!</h1>
          <p className="subtitle">You have successfully authenticated</p>
        </div>

        <div className="dashboard-grid">
          <div className="dashboard-card">
            <div className="card-icon">🔐</div>
            <h3>Secure Authentication</h3>
            <p>Your session is protected with JWT tokens and secure refresh mechanisms.</p>
          </div>

          <div className="dashboard-card">
            <div className="card-icon">🚀</div>
            <h3>Fast & Modern</h3>
            <p>Built with React and FastAPI for optimal performance and developer experience.</p>
          </div>

          <div className="dashboard-card">
            <div className="card-icon">🔗</div>
            <h3>OAuth Integration</h3>
            <p>Seamlessly integrated with Google OAuth for social authentication.</p>
          </div>

          <div className="dashboard-card">
            <div className="card-icon">✨</div>
            <h3>Ready to Extend</h3>
            <p>Add your own features and customize the authentication flow as needed.</p>
          </div>
        </div>

        <div className="info-section">
          <h2>Authentication Details</h2>
          <div className="info-card">
            <div className="info-item">
              <span className="info-label">Access Token:</span>
              <span className="info-value">
                {localStorage.getItem('access_token') ? 
                  `${localStorage.getItem('access_token').substring(0, 30)}...` : 
                  'Not available'
                }
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">Status:</span>
              <span className="info-value status-active">Active</span>
            </div>
            <div className="info-item">
              <span className="info-label">Refresh Token:</span>
              <span className="info-value">Stored in HTTP-only cookie</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;


