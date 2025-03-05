import React, { useState } from 'react';
import ScraperForm from './ScraperForm';
import PdfDisplay from './PdfDisplay';
import { Container, Typography } from '@mui/material';

function App() {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleScrape = (url) => {  // This function is now ONLY for making the API call
    fetch('/api/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => {throw new Error(err.error || 'Error scraping URL')});
        }
        return response.json();
      })
      .then(data => {
        setPdfUrl(data.pdf_url);
        setError(null);
      })
      .catch(error => {
        setError(error.message);
        setPdfUrl(null);
      });
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" align="center" gutterBottom>Web Scraper</Typography>
      <ScraperForm onScrape={handleScrape} error={error} /> {/* Pass handleScrape to ScraperForm */}
      {pdfUrl && <PdfDisplay pdfUrl={pdfUrl} />}
    </Container>
  );
}

export default App;