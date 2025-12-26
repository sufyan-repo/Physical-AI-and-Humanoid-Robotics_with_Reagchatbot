import React, { useState, useEffect, useRef } from 'react';
import { useBaseUrl } from '@docusaurus/useBaseUrl';
import { useAuth } from '../../hooks/useAuth';

import styles from './ChatbotModal.module.css';

const ChatbotModal = ({ isOpen, onClose }) => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    // Add user message to chat
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send message to backend
      // Use absolute URL to ensure proper connection to backend
      const response = await fetch('http://localhost:8000/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId,
          user_id: user?.id ? parseInt(user.id) || null : null,  // Send user ID if available as integer
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        role: 'assistant',
        content: data.response,
        sources: data.sources || [],
        timestamp: new Date().toISOString(),
      };

      // Update messages with bot response
      setMessages([...updatedMessages, botMessage]);

      // Set session ID if not already set
      if (!sessionId) {
        setSessionId(data.session_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      let errorMessageContent = 'Sorry, I encountered an error. Please try again.';

      // Check if it's a network error or specific API error
      if (error.message.includes('401') || error.message.includes('403')) {
        errorMessageContent = 'Authentication error. Please log in again.';
      } else if (error.message.includes('404')) {
        errorMessageContent = 'Chat service not found. Backend might be down. Please contact admin.';
      } else if (error.message.includes('500')) {
        errorMessageContent = 'Server error occurred. Backend might be experiencing issues. Please try again later.';
      } else if (error.message.includes('AI service error')) {
        errorMessageContent = 'AI service is temporarily unavailable. Please try again later.';
      } else if (error.message.includes('fetch')) {
        errorMessageContent = 'Network error. Please check your connection or if backend is running.';
      } else if (error.message.includes('ECONNREFUSED') || error.message.includes('Failed to fetch')) {
        errorMessageContent = 'Cannot connect to backend server. Please make sure backend is running on http://localhost:8000.';
      }

      const errorMessage = {
        role: 'assistant',
        content: errorMessageContent,
        timestamp: new Date().toISOString(),
      };
      setMessages([...updatedMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h3>AI Chatbot</h3>
          <button className={styles.closeButton} onClick={onClose}>
            ×
          </button>
        </div>
        <div className={styles.chatContainer}>
          <div className={styles.messagesContainer}>
            {messages.length === 0 ? (
              <div className={styles.welcomeMessage}>
                <p>Hello! I'm your AI assistant for the Intelligent Robotics textbook. How can I help you today?</p>
                <div className={styles.suggestedQuestions}>
                  <p>Suggested questions:</p>
                  <ul>
                    <li>What is inverse kinematics?</li>
                    <li>Explain PID controllers</li>
                    <li>How do humanoid robots maintain balance?</li>
                  </ul>
                </div>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`${styles.message} ${
                    message.role === 'user' ? styles.userMessage : styles.botMessage
                  }`}
                >
                  <div className={styles.messageContent}>
                    <strong>
                      {message.role === 'user' ? 'You' : 'AI Assistant'}
                    </strong>
                    <p>{message.content}</p>
                    {message.sources && message.sources.length > 0 && (
                      <div className={styles.sources}>
                        <small>Sources: {message.sources.join(', ')}</small>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className={styles.message + ' ' + styles.botMessage}>
                <div className={styles.messageContent}>
                  <strong>AI Assistant</strong>
                  <div className={styles.typingIndicator}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className={styles.inputContainer}>
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about robotics..."
              className={styles.messageInput}
              rows="3"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className={styles.sendButton}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotModal;