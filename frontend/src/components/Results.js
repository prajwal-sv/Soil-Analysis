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
      <div className="loading-container">
        <svg className="loading-spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle style={{ opacity: 0.25 }} cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path style={{ opacity: 0.75 }} fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p>Analyzing soil data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-card">
          <div className="error-content">
            <div>
              <svg style={{ width: '20px', height: '20px', color: '#f87171' }} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h3 className="error-title">An error occurred</h3>
              <div className="error-message">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="empty-container">
        <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '64px', height: '64px', color: '#9ca3af' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 className="empty-title">No Results Yet</h3>
        <p className="empty-text">Submit soil data to see analysis results here.</p>
      </div>
    );
  }

  const { soil_type, recommended_crop, parameter_analysis } = results;

  const getBgColorForSoilType = (type) => {
    switch (type.toLowerCase()) {
      case 'red': return '#fef2f2';
      case 'clay': return '#fef3c7'; 
      case 'black': return '#e5e7eb';
      case 'alluvial': return '#eff6ff';
      default: return '#f3f4f6';
    }
  };

  return (
    <div>
      <h2 className="results-title">Analysis Results</h2>
      
      <div className="results-container">
        <div style={{ 
          padding: '1rem', 
          borderRadius: '0.5rem', 
          backgroundColor: getBgColorForSoilType(soil_type) 
        }}>
          <div className="result-item">
            <div>
              {soilTypeIcons[soil_type] || (
                <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '32px', height: '32px', color: '#6b7280' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              )}
            </div>
            <div className="result-content">
              <h3 className="result-label">Soil Type</h3>
              <p className="result-value">{soil_type}</p>
            </div>
          </div>
        </div>

        <div style={{ 
          padding: '1rem', 
          borderRadius: '0.5rem', 
          backgroundColor: '#ecfdf5'
        }}>
          <div className="result-item">
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '32px', height: '32px', color: '#059669' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
              </svg>
            </div>
            <div className="result-content">
              <h3 className="result-label">Recommended Crop</h3>
              <p className="result-value" style={{ color: '#065f46' }}>{recommended_crop}</p>
            </div>
          </div>
        </div>

        <div className="parameter-card">
          <div className="parameter-content">
            <h3 className="parameter-title">Parameter Analysis</h3>
            <div>
              <ParameterAnalysis analysis={parameter_analysis} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
