import React, { useState } from 'react';
import SoilForm from './components/SoilForm';
import Results from './components/Results';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  return (
    <div>
      <header className="header">
        <h1>Soil Analysis</h1>
      </header>
      <main>
        <div className="container">
          <div className="grid">
            <div className="card">
              <SoilForm 
                setResults={setResults} 
                setLoading={setLoading} 
                setError={setError} 
              />
            </div>
            <div className="card">
              <Results 
                results={results} 
                loading={loading} 
                error={error} 
              />
            </div>
          </div>
        </div>
      </main>
      <footer className="footer">
        <p className="footer-text">
          Soil Analysis Application &copy; {new Date().getFullYear()}
        </p>
      </footer>
    </div>
  );
}

export default App;
