import React from 'react';

const ParameterAnalysis = ({ analysis }) => {
  const getStatusClass = (status) => {
    if (!status) return '';
    
    status = status.toLowerCase();
    
    if (status.includes('optimal') || status.includes('good') || status.includes('neutral')) {
      return 'status-optimal';
    } else if (status.includes('high') || status.includes('low') || status.includes('moderate')) {
      return 'status-warning';
    } else if (status.includes('deficient') || status.includes('excess') || status.includes('poor')) {
      return 'status-low';
    }
    
    return '';
  };
  
  const getParameterIcon = (param) => {
    param = param.toLowerCase();
    
    if (param.includes('n') || param === 'nitrogen') {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }} viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd" />
        </svg>
      );
    } else if (param.includes('p') || param === 'phosphorus') {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }} viewBox="0 0 20 20" fill="currentColor">
          <path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z" />
        </svg>
      );
    } else if (param.includes('k') || param === 'potassium') {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }} viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M12 13a1 1 0 100 2h5a1 1 0 001-1V9a1 1 0 00-1-1h-5a1 1 0 100 2h4v2h-4zm-1-5a1 1 0 011-1h5a1 1 0 011 1v4a1 1 0 01-1 1h-5a1 1 0 010-2h4V9h-4a1 1 0 01-1-1zm-7-2a1 1 0 00-1 1v8a2 2 0 104 0V8a1 1 0 00-1-1H4z" clipRule="evenodd" />
        </svg>
      );
    } else if (param.includes('ph')) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }} viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M7 2a1 1 0 00-.707 1.707L7 4.414v3.758a1 1 0 01-.293.707l-4 4C.817 14.769 2.156 18 4.828 18h10.343c2.673 0 4.012-3.231 2.122-5.121l-4-4A1 1 0 0113 8.172V4.414l.707-.707A1 1 0 0013 2H7zm2 6.172V4h2v4.172a3 3 0 00.879 2.12l1.168 1.168a4 4 0 01-8.092.67L6.71 8.538a3 3 0 00.879-2.121z" clipRule="evenodd" />
        </svg>
      );
    } else if (param.includes('rain')) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }} viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M5.05 3.636a1 1 0 010 1.414 7 7 0 000 9.9 1 1 0 11-1.414 1.414 9 9 0 010-12.728 1 1 0 011.414 0zm9.9 0a1 1 0 011.414 0 9 9 0 010 12.728 1 1 0 11-1.414-1.414 7 7 0 000-9.9 1 1 0 010-1.414zM7.879 6.464a1 1 0 010 1.414 3 3 0 000 4.243 1 1 0 11-1.415 1.414 5 5 0 010-7.07 1 1 0 011.415 0zm4.242 0a1 1 0 011.415 0 5 5 0 010 7.072 1 1 0 01-1.415-1.415 3 3 0 000-4.242 1 1 0 010-1.415z" clipRule="evenodd" />
        </svg>
      );
    } else if (param.includes('humid')) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }} viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M7 2a1 1 0 00-.707 1.707L7 4.414v3.758a1 1 0 01-.293.707l-4 4C.817 14.769 2.156 18 4.828 18h10.343c2.673 0 4.012-3.231 2.122-5.121l-4-4A1 1 0 0113 8.172V4.414l.707-.707A1 1 0 0013 2H7zm2 6.172V4h2v4.172a3 3 0 00.879 2.12l1.168 1.168a4 4 0 01-8.092.67L6.71 8.538a3 3 0 00.879-2.121z" clipRule="evenodd" />
        </svg>
      );
    } else if (param.includes('temp')) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }} viewBox="0 0 20 20" fill="currentColor">
          <path d="M7 2a1 1 0 012 0v.092a4.535 4.535 0 00-2 0V2zm3 0a1 1 0 00-2 0v4.92a4.535 4.535 0 002 0V2z" />
          <path strokeLinecap="round" strokeWidth={1} d="M8 9a1 1 0 011-1V6H7v2a1 1 0 011 1z" />
          <path fillRule="evenodd" d="M3 2a2 2 0 00-2 2v10a2 2 0 002 2h14a2 2 0 002-2V4a2 2 0 00-2-2h-2v8a1 1 0 01-1.707.707l-.293-.293A.996.996 0 0111 8V2H9v8c0 .276-.112.525-.293.707L8.414 11a1 1 0 01-1.414 0L6.707 10.7A.996.996 0 016 10V2H3zm6 5v-.071A3.003 3.003 0 008 5V5a3 3 0 00-1 5.83l.03.007A4.984 4.984 0 018 11c1.31 0 2.52.471 3.453 1.255l.01-.01A3 3 0 109 6.17z" clipRule="evenodd" />
          <path d="M8 10a1 1 0 100-2 1 1 0 000 2z" />
        </svg>
      );
    }
    
    return (
      <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }} viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
      </svg>
    );
  };
  
  if (!analysis) {
    return (
      <div style={{ textAlign: 'center', padding: '1rem 0' }}>
        <p>No parameter analysis available</p>
      </div>
    );
  }
  
  return (
    <div>
      <h3 className="parameter-title">Parameter Analysis</h3>
      <ul className="parameter-list">
        {Object.entries(analysis).map(([param, value]) => (
          <li key={param} className="parameter-item">
            <div className="parameter-name">
              {getParameterIcon(param)} {param}
            </div>
            <div className="parameter-desc">{value}</div>
            <div className={`parameter-status ${getStatusClass(value)}`}>
              {getStatusClass(value) === 'status-optimal' && '✓ Optimal Level'}
              {getStatusClass(value) === 'status-warning' && '⚠ Attention Required'}
              {getStatusClass(value) === 'status-low' && '⚠ Critical Level'}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ParameterAnalysis;
