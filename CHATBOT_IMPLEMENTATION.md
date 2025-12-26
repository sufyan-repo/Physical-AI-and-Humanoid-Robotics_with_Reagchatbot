# Robot Chatbot Integration

## Overview
This implementation adds a floating robot button to the Docusaurus-based textbook site that opens an AI chatbot modal when clicked. The chatbot integrates with the existing RAG (Retrieval-Augmented Generation) backend.

## Files Created

### 1. Components
- `book/src/components/Chatbot/ChatbotModal.js` - Main chatbot modal component
- `book/src/components/Chatbot/ChatbotModal.module.css` - Styling for the chatbot modal
- `book/src/components/Chatbot/FloatingRobot.js` - Floating button component that displays Robot.png
- `book/src/components/Chatbot/FloatingRobot.module.css` - Styling for the floating button

### 2. Integration
- `book/src/theme/Root.js` - Modified to include the floating robot button on all pages

## Features

### Chatbot Modal
- Real-time chat interface with message history
- Loading indicators during AI response generation
- Source citations for AI responses
- Suggested questions for new users
- Responsive design for mobile and desktop
- Session management to maintain conversation context

### Floating Robot Button
- Displays the Robot.png image from `book/static/img/`
- Smooth floating animation
- Hover effects for better UX
- Fixed position at bottom-right of screen
- Click to open chatbot modal

### Backend Integration
- Connects to the existing `/api/chat/` endpoint
- Sends user ID when authenticated
- Maintains session state between messages
- Handles error cases gracefully

## How to Use

1. The floating robot button appears on all pages of the textbook site
2. Click the robot image to open the chatbot modal
3. Type your question in the input field and press Enter or click Send
4. The AI assistant will respond with information from the textbook content
5. Responses include source citations to relevant chapters

## Running the Application

1. Start the backend API server:
   ```bash
   cd api
   uvicorn main:app --reload
   ```

2. Start the Docusaurus frontend:
   ```bash
   cd book
   npm start
   ```

The floating robot button will appear on the bottom-right corner of all pages. Click it to open the chatbot.

## Technical Details

- The chatbot uses the same API structure as the existing RAG system
- Authentication context is properly integrated to pass user ID
- CSS modules are used for component styling to avoid conflicts
- Responsive design ensures good UX on all device sizes
- Proper error handling for network issues and API failures