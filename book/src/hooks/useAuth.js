import React, { createContext, useContext, useState, useEffect } from 'react';
import { getUserProfile, login, signup, logout, updateProfile } from '../utils/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const currentUser = await getUserProfile();
        setUser(currentUser);
      } catch (error) {
        // Not logged in or error fetching profile
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    loadUser();
  }, []);

  const signIn = async (email, password) => {
    const userData = await login(email, password);
    setUser(userData);
  };

  const register = async (email, password, username, skill_level) => {
    const userData = await signup(email, password, username, skill_level);
    setUser(userData);
  };

  const signOut = async () => {
    await logout();
    setUser(null);
  };

  const updateUserData = async (updates) => {
    const updatedUser = await updateProfile(updates);
    setUser(updatedUser);
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn, register, signOut, updateUserData }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};