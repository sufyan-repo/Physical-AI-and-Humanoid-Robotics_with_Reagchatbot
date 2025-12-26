import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useAuth } from '../hooks/useAuth';

function ProfileContent() {
  const authResult = useAuth();
  const [username, setUsername] = useState('');
  const [skillLevel, setSkillLevel] = useState('');
  const [preferredLanguage, setPreferredLanguage] = useState('');

  if (!authResult) return null;

  const { user, loading, updateUserData, signOut } = authResult;

  useEffect(() => {
    if (user) {
      setUsername(user.username || '');
      setSkillLevel(user.skill_level || 'beginner');
      setPreferredLanguage(user.preferred_language || 'en');
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateUserData({ username, skill_level: skillLevel, preferred_language: preferredLanguage });
      alert('Profile updated successfully!');
    } catch (error) {
      alert(`Profile update failed: ${error.message}`);
    }
  };

  const handleLogout = async () => {
    if (confirm('Are you sure you want to log out?')) {
      try {
        await signOut();
        window.location.href = '/';
      } catch (error) {
        console.error('Logout error:', error);
        alert('Logout failed. Please try again.');
      }
    }
  };

  if (loading) {
    return <main>Loading profile...</main>;
  }

  if (!user) {
    return <main>Please log in to view your profile.</main>;
  }

  return (
    <main>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
        <div style={{ width: '400px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h1>User Profile</h1>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="email" style={{ display: 'block', marginBottom: '5px' }}>Email:</label>
              <input
                type="email"
                id="email"
                value={user.email}
                disabled
                style={{ width: '100%', padding: '8px', boxSizing: 'border-box', backgroundColor: '#f0f0f0' }}
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
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="preferredLanguage" style={{ display: 'block', marginBottom: '5px' }}>Preferred Language:</label>
              <select
                id="preferredLanguage"
                value={preferredLanguage}
                onChange={(e) => setPreferredLanguage(e.target.value)}
                style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
              >
                <option value="en">English</option>
                <option value="ur">Urdu</option>
              </select>
            </div>
            <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Update Profile</button>
          </form>
        </div>
      </div>
    </main>
  );
}

function Profile() {
  return (
    <Layout title="User Profile" description="Manage your user profile">
      <BrowserOnly>
        {() => <ProfileContent />}
      </BrowserOnly>
    </Layout>
  );
}

export default Profile;