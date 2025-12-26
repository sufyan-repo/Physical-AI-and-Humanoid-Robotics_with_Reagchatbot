import React, { useState } from 'react';
import ChatbotModal from './ChatbotModal';

import styles from './FloatingRobot.module.css';

const FloatingRobot = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <div className={styles.floatingRobot} onClick={openModal} title="Open AI Chatbot">
        <img
          src="/img/Robot.png"
          alt="AI Chatbot"
          className={styles.robotImage}
        />
      </div>
      <ChatbotModal isOpen={isModalOpen} onClose={closeModal} />
    </>
  );
};

export default FloatingRobot;