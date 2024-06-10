import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import TopBar from './TopBar';
import '../styles/TopBar.css';
import '../styles/Login.css';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const auth = useAuth();
  let navigate = useNavigate();

  async function handleRegister() {
    try {
      await auth.register(username, password);
      navigate('/dashboard');
    } catch (error) {
      setError('Registration failed. Please try again.');
    }
  }

  const buttons = [
    <button onClick={() => navigate('/')} className="nav-link">Login</button>
  ];

  return (
    <div>
      <TopBar buttons={buttons}/>
      <div className="login-container">
        <h1>Register</h1>
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
        <button onClick={handleRegister} className="login-button">Register</button>
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
}

export default Register;