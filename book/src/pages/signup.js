import React, { useState } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useAuth } from '../hooks/useAuth';

function SignupContent() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [skillLevel, setSkillLevel] = useState('beginner');
  const authResult = useAuth();

  if (!authResult) return null;

  const { register } = authResult;

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register(email, password, username, skillLevel);
      alert('Signup successful! Please log in.');
      window.location.href = '/login';
    } catch (error) {
      alert(`Signup failed: ${error.message}`);
    }
  };

  return (
    <main>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <div style={{ width: '400px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h1>Sign Up</h1>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="email" style={{ display: 'block', marginBottom: '5px' }}>Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
              />
            </div>
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="password" style={{ display: 'block', marginBottom: '5px' }}>Password:</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
              />
            </div>
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="username" style={{ display: 'block', marginBottom: '5px' }}>Username:</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
              />
            </div>
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="skillLevel" style={{ display: 'block', marginBottom: '5px' }}>Skill Level:</label>
              <select
                id="skillLevel"
                value={skillLevel}
                onChange={(e) => setSkillLevel(e.target.value)}
                style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Sign Up</button>
          </form>
          <p style={{ textAlign: 'center', marginTop: '15px' }}>
            Already have an account? <a href="/login">Log In</a>
          </p>
        </div>
      </div>
    </main>
  );
}

function Signup() {
  return (
    <Layout title="Sign Up" description="Sign up for an account">
      <BrowserOnly>
        {() => <SignupContent />}
      </BrowserOnly>
    </Layout>
  );
}

export default Signup;