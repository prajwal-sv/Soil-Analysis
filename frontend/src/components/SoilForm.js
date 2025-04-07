import React, { useState } from 'react';
import axios from 'axios';

const SoilForm = ({ setResults, setLoading, setError }) => {
  const [formData, setFormData] = useState({
    nitrogen: '',
    phosphorus: '',
    potassium: '',
    ph: '',
    rainfall: '',
    humidity: '',
    temperature: ''
  });
  
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const validateForm = () => {
    const errors = {};
    const fields = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall', 'humidity', 'temperature'];
    
    fields.forEach(field => {
      if (!formData[field]) {
        errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
      }
    });

    if (!image) {
      errors.image = 'Soil image is required';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setError(null);
    
    // Create form data for multipart/form-data request
    const submitData = new FormData();
    submitData.append('image', image);
    
    // Append all form fields
    Object.keys(formData).forEach(key => {
      submitData.append(key, formData[key]);
    });

    try {
      const response = await axios.post('http://0.0.0.0:8000/api/predict/', submitData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setResults(response.data);
    } catch (error) {
      console.error('Error submitting form:', error);
      setError(error.response?.data?.detail || 'An error occurred while processing your request.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="form-title">Soil Analysis Form</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">
            Soil Image
          </label>
          <div className="file-input-container">
            {imagePreview ? (
              <div>
                <img
                  src={imagePreview}
                  alt="Soil preview"
                  style={{ maxWidth: '100%', maxHeight: '200px', marginBottom: '10px' }}
                />
                <button 
                  type="button"
                  onClick={() => {
                    setImage(null);
                    setImagePreview(null);
                  }}
                  className="upload-button"
                  style={{ backgroundColor: '#f44336' }}
                >
                  Remove Image
                </button>
              </div>
            ) : (
              <div>
                <label
                  htmlFor="image-upload"
                  className="upload-button"
                >
                  <span>Upload Soil Image</span>
                  <input
                    id="image-upload"
                    name="image-upload"
                    type="file"
                    style={{ display: 'none' }}
                    accept="image/*"
                    onChange={handleImageChange}
                  />
                </label>
                <div className="file-name">
                  {image ? image.name : 'No file selected'}
                </div>
              </div>
            )}
          </div>
          {formErrors.image && (
            <p className="error-message">{formErrors.image}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="nitrogen" className="form-label">
            Nitrogen (N)
          </label>
          <input
            type="number"
            name="nitrogen"
            id="nitrogen"
            value={formData.nitrogen}
            onChange={handleChange}
            className="form-input"
            placeholder="e.g., 40"
          />
          {formErrors.nitrogen && (
            <p className="error-message">{formErrors.nitrogen}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="phosphorus" className="form-label">
            Phosphorus (P)
          </label>
          <input
            type="number"
            name="phosphorus"
            id="phosphorus"
            value={formData.phosphorus}
            onChange={handleChange}
            className="form-input"
            placeholder="e.g., 30"
          />
          {formErrors.phosphorus && (
            <p className="error-message">{formErrors.phosphorus}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="potassium" className="form-label">
            Potassium (K)
          </label>
          <input
            type="number"
            name="potassium"
            id="potassium"
            value={formData.potassium}
            onChange={handleChange}
            className="form-input"
            placeholder="e.g., 35"
          />
          {formErrors.potassium && (
            <p className="error-message">{formErrors.potassium}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="ph" className="form-label">
            pH Value
          </label>
          <input
            type="number"
            name="ph"
            id="ph"
            value={formData.ph}
            onChange={handleChange}
            className="form-input"
            placeholder="e.g., 6.5"
            step="0.1"
            min="0"
            max="14"
          />
          {formErrors.ph && (
            <p className="error-message">{formErrors.ph}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="rainfall" className="form-label">
            Rainfall (mm)
          </label>
          <input
            type="number"
            name="rainfall"
            id="rainfall"
            value={formData.rainfall}
            onChange={handleChange}
            className="form-input"
            placeholder="e.g., 200"
          />
          {formErrors.rainfall && (
            <p className="error-message">{formErrors.rainfall}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="humidity" className="form-label">
            Humidity (%)
          </label>
          <input
            type="number"
            name="humidity"
            id="humidity"
            value={formData.humidity}
            onChange={handleChange}
            className="form-input"
            placeholder="e.g., 65"
            min="0"
            max="100"
          />
          {formErrors.humidity && (
            <p className="error-message">{formErrors.humidity}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="temperature" className="form-label">
            Temperature (°C)
          </label>
          <input
            type="number"
            name="temperature"
            id="temperature"
            value={formData.temperature}
            onChange={handleChange}
            className="form-input"
            placeholder="e.g., 25"
          />
          {formErrors.temperature && (
            <p className="error-message">{formErrors.temperature}</p>
          )}
        </div>

        <button
          type="submit"
          className="submit-button"
        >
          Analyze Soil
        </button>
      </form>
    </div>
  );
};

export default SoilForm;
