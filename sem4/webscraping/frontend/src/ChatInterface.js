// ChatInterface.js
import React, { useState, useEffect, useRef } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Paper, 
  Typography, 
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

function ChatInterface() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState('');
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  
  useEffect(() => {
    // Fetch available documents when component mounts
    fetchDocuments();
  }, []);
  
  useEffect(() => {
    // Scroll to bottom whenever messages change
    scrollToBottom();
  }, [messages]);
  
  const fetchDocuments = async () => {
    try {
      setError(null);
      const response = await fetch('/api/documents');
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to fetch documents');
      }
      
      const data = await response.json();
      if (data.success && data.documents) {
        setDocuments(data.documents);
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
      setError(error.message);
    }
  };
  
  const handleSend = async () => {
    if (!input.trim()) return;
    
    // Add user message to chat
    const userMessage = input.trim();
    setMessages(prev => [...prev, { text: userMessage, sender: 'user' }]);
    setInput('');
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userMessage,
          document_id: selectedDocument || undefined
        }),
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to get response');
      }
      
      const data = await response.json();
      if (data.success) {
        setMessages(prev => [...prev, { text: data.response, sender: 'bot' }]);
      } else {
        throw new Error(data.error || 'Unknown error');
      }
    } catch (error) {
      console.error('Chat error:', error);
      setError(error.message);
      setMessages(prev => [...prev, { 
        text: 'Sorry, I encountered an error. Please try again.', 
        sender: 'bot' 
      }]);
    } finally {
      setLoading(false);
    }
  };
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  return (
    <Box sx={{ mt: 4, mb: 8 }}>
      <Typography variant="h5" gutterBottom>
        Chat with your documents
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      {documents.length === 0 ? (
        <Alert severity="info" sx={{ mb: 2 }}>
          No documents found. Please scrape some content first.
        </Alert>
      ) : (
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Select document to query</InputLabel>
          <Select
            value={selectedDocument}
            onChange={(e) => setSelectedDocument(e.target.value)}
            label="Select document to query"
          >
            <MenuItem value="">All documents</MenuItem>
            {documents.map((doc) => (
              <MenuItem key={doc.id} value={doc.id}>
                {doc.title || doc.url || doc.id}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )}
      
      <Paper
        elevation={3}
        sx={{
          height: 400,
          p: 2,
          overflow: 'auto',
          display: 'flex',
          flexDirection: 'column',
          mb: 2,
          bgcolor: '#f9f9f9'
        }}
      >
        {messages.length === 0 ? (
          <Box sx={{ 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center', 
            justifyContent: 'center',
            height: '100%',
            color: 'text.secondary'
          }}>
            <Typography variant="body2" color="textSecondary" align="center">
              Ask questions about your documents.
              <br />
              For example: "What is the main topic of this document?" or "Summarize the key points."
            </Typography>
          </Box>
        ) : (
          messages.map((message, index) => (
            <Box
              key={index}
              sx={{
                alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: message.sender === 'user' ? '#e3f2fd' : 'white',
                borderRadius: 2,
                p: 2,
                mb: 1,
                maxWidth: '80%',
                boxShadow: '0px 1px 3px rgba(0,0,0,0.1)'
              }}
            >
              <Typography variant="body1">
                {message.text.split('\n').map((line, i) => (
                  <React.Fragment key={i}>
                    {line}
                    <br />
                  </React.Fragment>
                ))}
              </Typography>
            </Box>
          ))
        )}
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
            <CircularProgress size={24} />
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Paper>
      
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          label="Ask a question about the document..."
          variant="outlined"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={documents.length === 0 || loading}
        />
        <Button
          variant="contained"
          color="primary"
          endIcon={<SendIcon />}
          onClick={handleSend}
          disabled={documents.length === 0 || !input.trim() || loading}
        >
          Send
        </Button>
      </Box>
    </Box>
  );
}

export default ChatInterface;