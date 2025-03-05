import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';

function ScraperForm({ onScrape }) {
  const [url, setUrl] = useState('');
  const [errorMessage, setErrorMessage] = useState(null);

  const handleSubmit = async (e) => { // handleSubmit is async
    e.preventDefault();
    
    if (!url) {  // Client-side validation
        setErrorMessage("Please enter a URL.");
        return; // Stop form submission
    }

    try {  // try...catch block is *inside* the async function
      const response = await fetch('/api/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error scraping URL');
      }

      const data = await response.json();
      onScrape(data.pdf_url);
      setErrorMessage(null);

    } catch (error) { // Catch errors here
      setErrorMessage(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {errorMessage && <Typography color="error">{errorMessage}</Typography>}
      <Box mb={2}>
        <TextField
          label="Enter URL"
          variant="outlined"
          fullWidth
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
      </Box>
      <Button variant="contained" color="primary" type="submit">
        Scrape
      </Button>
    </form>
  );
}

export default ScraperForm;