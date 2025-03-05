import React from 'react';
import { Button } from '@mui/material'; // Import Material UI components

function PdfDisplay({ pdfUrl }) {
  return (
    <div>
      <Button variant="contained" color="secondary" href={pdfUrl} target="_blank" rel="noopener noreferrer">
        View PDF
      </Button>
    </div>
  );
}

export default PdfDisplay;