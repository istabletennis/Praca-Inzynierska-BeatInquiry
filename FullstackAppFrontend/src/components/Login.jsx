import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import TopBar from './TopBar';
import '../styles/TopBar.css';
import '../styles/Login.css'; // Import the new CSS file

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const auth = useAuth();
  let navigate = useNavigate();

  async function handleLogin() {
    try {
      await auth.login(username, password);
      navigate('/dashboard');
    } catch (error) {
      setError('Failed to login. Check your credentials.');
    }
  }

  const buttons = [
    <button onClick={() => navigate('/register')} className="nav-link">Register</button>
  ];

  return (
    <div>
      <TopBar buttons={buttons}/>
      <div className="login-container">
        <h1>Login</h1>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          className="login-input"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="login-input"
        />
        <button onClick={handleLogin} className="login-button">Log In</button>
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
}

export default Login;