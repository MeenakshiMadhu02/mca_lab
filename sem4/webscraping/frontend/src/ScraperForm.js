import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';

function ScraperForm({ onScrape, error }) {
  const [url, setUrl] = useState('');
  const [localError, setLocalError] = useState(null);

  // Display error from parent or local validation error
  const displayError = error || localError;

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!url) {
      setLocalError("Please enter a URL.");
      return;
    }
    
    // Clear local validation errors
    setLocalError(null);
    
    // Just pass the URL to parent component
    onScrape(url);
  };

  return (
    <form onSubmit={handleSubmit}>
      {displayError && <Typography color="error">{displayError}</Typography>}
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