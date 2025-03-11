import React from 'react';
import { Box, Typography, Button } from '@mui/material';

const PdfDisplay = ({ pdfUrl }) => {
  // Function to open PDF in a new tab
  const openInNewTab = () => {
    window.open(pdfUrl, '_blank');
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Generated PDF
      </Typography>
      
      <Box sx={{ height: '500px', mb: 2, border: '1px solid #ddd' }}>
        <iframe
          src={pdfUrl}
          title="PDF Viewer"
          width="100%"
          height="100%"
          style={{ border: 'none' }}
        />
      </Box>
      
      <Button 
        variant="contained" 
        color="primary" 
        onClick={openInNewTab}
      >
        Open PDF in New Tab
      </Button>
      
      <Typography variant="caption" sx={{ display: 'block', mt: 2, color: 'text.secondary' }}>
        PDF URL: {pdfUrl}
      </Typography>
    </Box>
  );
};

export default PdfDisplay;