"use client";

import { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import './app.css';

// Define the type for chat messages
type ChatMessage = {
  role: string;
  content: string;
};

export default function Home() {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [message, setMessage] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null); // Session ID can be null initially

  // Set a random UUID when the component is first rendered
  useEffect(() => {
    if (!sessionId) {
      setSessionId(uuidv4()); // Generate a new UUID if it's null
    }
  }, [sessionId]); // Run only when sessionId is null

  const handleSendMessage = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!sessionId) {
      console.error('Session ID is missing');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: message,
        }),
      });

      if (response.ok) { // Ensure the request was successful
        const data = await response.json(); // Parse the response

        // Update chat history
        setChatHistory((prev) => [
          ...prev,
          { role: 'user', content: message },
          { role: 'assistant', content: data.response },
        ]);

        setMessage(''); // Clear the message field
      } else {
        console.error('Failed to fetch response from backend');
      }
    } catch (error) {
      console.error('Error occurred:', error);
    }
  };

  return (
      <main className="container mx-auto p-4">
        <h1 className="text-xl font-bold mb-4">Basic Chat Interface</h1>

        {/* Display chat history */}
        <div className="chat-history">
          {chatHistory.map((chat, index) => (
              <div key={index} className={`chat-message ${chat.role}`}>
                {chat.content}
              </div>
          ))}
        </div>

        {/* Form for sending messages */}
        <form onSubmit={handleSendMessage} className="mt-4">
          <input
              type="text"
              className="border p-2"
              placeholder="Type your message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
          />
          <button type="submit" className="bg-blue-500 text-white p-2 ml-2">
            Send
          </button>
        </form>
      </main>
  );
}
