import React, { useState, useEffect, useRef } from 'react';
import { LabIcon, infoIcon, runIcon } from '@jupyterlab/ui-components';
import { makeApiRequest } from './handler';

// A utility function to make API requests to the server extension
// async function makeApiRequest(url = '', data = {}) {
//   const response = await fetch(url, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data),
//   });
//   if (!response.ok) {
//     throw new Error(`HTTP error! status: ${response.status}`);
//   }
//   return response.json();
// }

// Define message structure
interface Message {
  sender: 'user' | 'peer' | 'tutor';
  text: string;
}

interface ChatPanelProps {
  onClose?: () => void;
}

const ChatPanel: React.FC<ChatPanelProps> = ({onClose}) => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'peer', text: "Hello! I'm here to help you with Quantum Key Distribution (QKD) - specifically BB84 and B92 protocols.\n\nGive me prompts and I'll generate code for you! For example:\n• 'Generate bb84_send_qubits method'\n• 'Write the b92_measure_qubits function'\n• 'Explain basis reconciliation'\n• 'Summarize my simulation logs'\n\nWhat method would you like me to help you code?" }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const styleId = 'chat-panel-styles';
    if (document.getElementById(styleId)) return;

    const style = document.createElement('style');
    style.id = styleId;
    style.innerHTML = `
      .chat-panel-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        background-color: var(--jp-layout-color1);
        font-family: var(--jp-ui-font-family);
        color: var(--jp-ui-font-color1);
      }
      .chat-header {
        padding: 10px 12px;
        background: var(--jp-brand-color1);
        color: white;
        font-weight: bold;
        text-align: center;
        flex-shrink: 0;
        border-bottom: 1px solid var(--jp-border-color1);
      }
      .message-list {
        flex-grow: 1;
        overflow-y: auto;
        padding: 10px;
        display: flex;
        flex-direction: column;
      }
      .input-area {
        display: flex;
        align-items: center;
        padding: 10px;
        border-top: 1px solid var(--jp-border-color1);
        background-color: var(--jp-layout-color0);
        flex-shrink: 0;
      }
      .jp-chat-input {
        flex-grow: 1;
        border: 1px solid var(--jp-border-color1);
        border-radius: var(--jp-border-radius);
        padding: 8px 12px;
        margin-right: 8px;
        background-color: var(--jp-layout-color1);
        color: var(--jp-ui-font-color1);
      }
      .jp-chat-send-button {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0;
        width: 32px;
        height: 32px;
        border: none;
        background-color: var(--jp-brand-color1);
        color: white;
        border-radius: var(--jp-border-radius);
        cursor: pointer;
      }
      .jp-chat-send-button:disabled {
          background-color: var(--jp-layout-color3);
      }
      .message-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 10px;
        max-width: 85%;
      }
      .message-container.user { align-self: flex-end; }
      .message-container.peer, .message-container.tutor { align-self: flex-start; }
      
      .message-bubble {
        padding: 8px 12px;
        border-radius: 12px;
        line-height: 1.4;
        word-wrap: break-word;
      }
      .message-bubble.user { background-color: var(--jp-brand-color1); color: white; }
      .message-bubble.peer { background-color: var(--jp-layout-color2); color: var(--jp-ui-font-color1); }
      .message-bubble.tutor { background-color: var(--jp-info-color2); color: var(--jp-info-color0); border: 1px solid var(--jp-info-color3); }

      .escalate-button {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background-color: var(--jp-layout-color1);
        border: 1px solid var(--jp-brand-color1);
        color: var(--jp-brand-color1);
        padding: 4px 10px;
        border-radius: 12px;
        cursor: pointer;
        font-size: 0.8em;
        margin-top: 8px;
        align-self: flex-start;
        transition: background-color 0.2s;
      }
      .escalate-button:hover {
        background-color: var(--jp-brand-color3);
      }
      .escalate-button .jp-icon-svg {
        width: 14px;
        height: 14px;
      }
    `;
    document.head.appendChild(style);

    return () => {
      const styleElement = document.getElementById(styleId);
      if (styleElement) styleElement.remove();
    };
  }, []);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;
    const query = inputValue;

    const userMessage: Message = { sender: 'user', text: query };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await makeApiRequest('/ask', {
        query: query,
        agent_type: 'peer',
      }, {
        method: 'POST',
      });

      const peerMessage: Message = { sender: 'peer', text: response.data };
      setMessages(prev => [...prev, peerMessage]);

    } catch (error) {
      handleApiError(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApiError = (error: unknown) => {
    const err = error as Error;
    console.error('Failed to get answer:', err);
    const errorMessage: Message = { sender: 'peer', text: `Sorry, an error occurred: ${err.message}` };
    setMessages(prev => [...prev, errorMessage]);
  };
  
  return (
    <div className="chat-panel-container">
      <div className="chat-header">
          QKD Code Assistant
      </div>
      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message-container ${msg.sender}`}>
            <div className={`message-bubble ${msg.sender}`}>
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-area">
        <input
          className="jp-chat-input"
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
          placeholder="Ask me to generate BB84/B92 code or explain concepts..."
          disabled={isLoading}
        />
        <button className="jp-chat-send-button" onClick={handleSendMessage} disabled={isLoading}>
          {isLoading ? '...' : <runIcon.react tag="span" />}
        </button>
      </div>
    </div>
  );
};

export default ChatPanel;

