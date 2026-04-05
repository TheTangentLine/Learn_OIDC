import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const LoginSuccess = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState('processing'); // processing, success, error

  useEffect(() => {
    const handleLoginSuccess = () => {
      // Bước 1: Đọc access_token từ URL
      const accessToken = searchParams.get('access_token');
      
      console.log('Login Success - Processing OAuth callback');
      
      if (accessToken) {
        console.log('Access token found, saving to localStorage');
        
        // Bước 2: Lưu vào localStorage (State)
        localStorage.setItem('access_token', accessToken);
        
        setStatus('success');
        
        // Bước 3: Xóa access_token khỏi URL (để bảo mật và đẹp hơn)
        // Bước 4: Chuyển hướng về Dashboard
        setTimeout(() => {
          // Replace state để xóa token khỏi history
          window.history.replaceState({}, document.title, '/login-success');
          
          // Chuyển về dashboard
          navigate('/dashboard', { replace: true });
        }, 800); // Delay nhỏ để user thấy success message
      } else {
        console.error('No access token found in URL');
        setStatus('error');
        
        // Redirect về login nếu không có token
        setTimeout(() => {
          navigate('/login', { 
            replace: true,
            state: { error: 'Authentication failed. Please try again.' }
          });
        }, 2000);
      }
    };

    handleLoginSuccess();
  }, [navigate, searchParams]);

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      gap: '24px',
      padding: '20px'
    }}>
      {status === 'processing' && (
        <>
          <div style={{ fontSize: '64px', animation: 'spin 2s linear infinite' }}>
            ⏳
          </div>
          <h2 style={{ margin: 0, fontSize: '24px' }}>Processing your login...</h2>
          <p style={{ margin: 0, opacity: 0.9 }}>Please wait a moment</p>
        </>
      )}
      
      {status === 'success' && (
        <>
          <div style={{ fontSize: '64px', animation: 'bounce 0.6s ease-in-out' }}>
            ✅
          </div>
          <h2 style={{ margin: 0, fontSize: '24px' }}>Login Successful!</h2>
          <p style={{ margin: 0, opacity: 0.9 }}>Redirecting to dashboard...</p>
        </>
      )}
      
      {status === 'error' && (
        <>
          <div style={{ fontSize: '64px' }}>❌</div>
          <h2 style={{ margin: 0, fontSize: '24px' }}>Authentication Failed</h2>
          <p style={{ margin: 0, opacity: 0.9 }}>Redirecting to login page...</p>
        </>
      )}
      
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
      `}</style>
    </div>
  );
};

export default LoginSuccess;

