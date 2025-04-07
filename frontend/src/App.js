import React, { useState } from 'react';
import SoilForm from './components/SoilForm';
import Results from './components/Results';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  return (
    <div className="container">
      <header className="app-header">
        <h1 className="app-title">Soil Analysis</h1>
        <p className="app-subtitle">Analyze soil samples and get crop recommendations</p>
      </header>
      <main className="app-main">
        <div className="soil-form">
          <SoilForm 
            setResults={setResults} 
            setLoading={setLoading} 
            setError={setError} 
          />
        </div>
        <div className="results-container">
          <Results 
            results={results} 
            loading={loading} 
            error={error} 
          />
        </div>
      </main>
    </div>
  );
}

export default App;
