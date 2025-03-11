import React, { useState } from 'react';
import ScraperForm from './ScraperForm';
import PdfDisplay from './PdfDisplay';
import { Container, Typography } from '@mui/material';

function App() {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleScrape = async (url) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/scrape", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    console.log("Raw Response:", response); // Debugging

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Scraping failed");
    }

    const data = await response.json();
    console.log("Parsed Data:", data); // Debugging

    // If data.pdf_url is just a path like "/uploads/file.pdf"
    setPdfUrl(`http://127.0.0.1:5000${data.pdf_url}`);
    setError(null);
  } catch (error) {
    console.error("Error:", error);
    setError(error.message);
    setPdfUrl(null);
  }
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