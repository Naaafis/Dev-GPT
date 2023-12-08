import React, { useState, useEffect } from 'react';
import styles from './ChatBox.module.css';


const ChatBox = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [generatingMsg, setGeneratingMsg] = useState('');

  const addMessage = (content, imageUrl = null) => {
    const newMessage = {
      content,
      timestamp: new Date().toISOString(),
      imageUrl
    };
    const updatedMessages = [...messages, newMessage];
    setMessages(updatedMessages);

    localStorage.setItem('chatMessages', JSON.stringify(updatedMessages));
  };

  useEffect(() => {
    // localStorage.removeItem('chatMessages');
    const savedMessages = localStorage.getItem('chatMessages');
    if (savedMessages) {
      setMessages(JSON.parse(savedMessages));
    }
    let intervalId;

    if (generatingMsg) {
      // Update the generating message every 500 ms
      let dotCount = 1;
      intervalId = setInterval(() => {
        setGeneratingMsg(`Generating${'.'.repeat(dotCount)}`);
        dotCount = (dotCount % 3) + 1; // Cycle through 1 to 3 dots
      }, 500);
    }

    return () => clearInterval(intervalId); // Clear interval on component unmount
  }, [generatingMsg]);
  
  const handleSubmit = async () => {
    if (!message) {
      alert('Please enter your request');
      return;
    };
    // Add the user's text message to the chat
    addMessage(message);

    // Set generating message
    setGeneratingMsg('Generating.');


    // Send the message to the backend
    const data = { message };

  // Send the message to the backend using fetch
  try {
    const response = await fetch('http://localhost:5000/submit-message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    const responseData = await response.json();


    console.log('Response from backend:', responseData);

    // Check if the response contains an image URL
    if (responseData && responseData.message) {
        // Extract the image URL from the response
        const imageUrl = `/images/${responseData.message}`;
        addMessage(message, imageUrl);
    }
    } catch (error) {
      console.error('Error submitting message:', error);
    }
    setGeneratingMsg(''); // Clear the generating message
    setMessage('');
  };

  return (
    <div className={styles.messages}>
      <h1>DEV GPT</h1>
      <div id="messageBoard">
        {messages.map((msg, index) => (
          <div key={index} className={styles.message}>
            <div className={styles.content}>
              Looking for: {msg.content}
            </div>
            {msg.imageUrl && <img src={msg.imageUrl} alt="Generated" style={{maxHeight: '60%'}} />}
          </div>
        ))}
      </div>
      <div className={styles.generatingMessage}>
        {generatingMsg}
      </div>
      <div className={styles.form}>
        <textarea
          placeholder="Describe what webpage you want to build"
          id="message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button className={styles.submitBtn} onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
};

export default ChatBox;
