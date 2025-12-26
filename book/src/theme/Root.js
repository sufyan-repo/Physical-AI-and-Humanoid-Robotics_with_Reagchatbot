import React from 'react';
import { AuthProvider } from '../hooks/useAuth';
import FloatingRobot from '../components/Chatbot/FloatingRobot';

export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
      <FloatingRobot />
    </AuthProvider>
  );
}