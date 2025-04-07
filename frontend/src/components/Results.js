import React from 'react';
import ParameterAnalysis from './ParameterAnalysis';

const Results = ({ results, loading, error }) => {
  // Soil type icons - using SVG
  const soilTypeIcons = {
    Red: (
      <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '32px', height: '32px', color: '#dc2626' }} viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M4 2a2 2 0 00-2 2v11a3 3 0 106 0V4a2 2 0 00-2-2H4zm1 14a1 1 0 100-2 1 1 0 000 2zm5-1.757l4.9-4.9a2 2 0 000-2.828L13.485 5.1a2 2 0 00-2.828 0L10 5.757v8.486zM16 18H9.071l6-6H16a2 2 0 012 2v2a2 2 0 01-2 2z" clipRule="evenodd" />
      </svg>
    ),
    Clay: (
      <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '32px', height: '32px', color: '#b45309' }} viewBox="0 0 20 20" fill="currentColor">
        <path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z" />
      </svg>
    ),
    Black: (
      <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '32px', height: '32px', color: '#1f2937' }} viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
      </svg>
    ),
    Alluvial: (
      <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '32px', height: '32px', color: '#3b82f6' }} viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M17.707 9.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-7-7A.997.997 0 012 10V5a3 3 0 013-3h5c.256 0 .512.098.707.293l7 7zM5 6a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
      </svg>
    )
  };

  if (loading) {
    return (
      <div className="loading">
        <p>Analyzing soil data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-message">
        <p>{error}</p>
      </div>
    );
  }

  if (!results) {
    return (
      <div>
        <h2 className="results-title">Analysis Results</h2>
        <p style={{ textAlign: 'center', color: '#757575' }}>
          Submit soil data to see analysis results here.
        </p>
      </div>
    );
  }

  const { soil_type, recommended_crop, parameter_analysis } = results;

  return (
    <div>
      <h2 className="results-title">Analysis Results</h2>
      
      <div className="result-card">
        <h3 className="result-heading">Soil Type</h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {soilTypeIcons[soil_type]}
          <span className="result-value">{soil_type} Soil</span>
        </div>
      </div>
      
      <div className="recommended-crop">
        <h3 className="crop-heading">Recommended Crop</h3>
        <p className="crop-value">{recommended_crop}</p>
      </div>
      
      <div style={{ marginTop: '20px' }}>
        <ParameterAnalysis analysis={parameter_analysis} />
      </div>
    </div>
  );
};

export default Results;
