import React, { useState } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useAuth } from '../hooks/useAuth';

function LoginContent() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const authResult = useAuth();

  if (!authResult) return null;

  const { signIn } = authResult;

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signIn(email, password);
      alert('Login successful!');
      window.location.href = '/';
    } catch (error) {
      alert(`Login failed: ${error.message}`);
    }
  };

  return (
    <main>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <div style={{ width: '400px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h1>Log In</h1>
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
            <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Log In</button>
          </form>
          <p style={{ textAlign: 'center', marginTop: '15px' }}>
            Don't have an account? <a href="/signup">Sign Up</a>
          </p>
        </div>
      </div>
    </main>
  );
}

function Login() {
  return (
    <Layout title="Log In" description="Log in to your account">
      <BrowserOnly>
        {() => <LoginContent />}
      </BrowserOnly>
    </Layout>
  );
}

export default Login;