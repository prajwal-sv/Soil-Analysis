from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import io
from PIL import Image
import numpy as np

class SoilAnalysisAPITests(TestCase):
    """
    Test cases for the Soil Analysis API endpoints
    """
    
    def setUp(self):
        self.client = APIClient()
        self.predict_url = reverse('predict_soil_type')
    
    def create_test_image(self, color, size=(50, 50)):
        """Helper method to create a test image with a specific color"""
        image = Image.new('RGB', size, color=color)
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return image_io
    
    def test_predict_with_valid_data(self):
        """Test API with valid image and soil parameters"""
        # Create a red-colored test image (should predict 'Red' soil)
        image_io = self.create_test_image(color='red')
        
        # Test data
        data = {
            'image': image_io,
            'nitrogen': 40.5,
            'phosphorus': 25.2,
            'potassium': 30.1,
            'ph': 6.8,
            'rainfall': 120.5,
            'humidity': 55.3,
            'temperature': 24.7
        }
        
        # Make the request
        response = self.client.post(self.predict_url, data, format='multipart')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('soil_type', response.data)
        self.assertIn('recommended_crop', response.data)
        self.assertIn('parameter_analysis', response.data)
    
    def test_predict_with_missing_data(self):
        """Test API with missing required fields"""
        # Incomplete data (missing image and some parameters)
        data = {
            'nitrogen': 40.5,
            'phosphorus': 25.2,
            # Missing potassium, ph, etc.
        }
        
        # Make the request
        response = self.client.post(self.predict_url, data, format='multipart')
        
        # Check response is a 400 error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_parameter_analysis(self):
        """Test that parameter analysis returns expected assessments"""
        # Create a test image
        image_io = self.create_test_image(color='brown')
        
        # Test data with specific values that should trigger certain analysis results
        data = {
            'image': image_io,
            'nitrogen': 15.0,  # Should be "Deficient" or "Low"
            'phosphorus': 30.0,  # Should be "Optimal"
            'potassium': 50.0,  # Should be "High"
            'ph': 7.0,  # Should be "Neutral"
            'rainfall': 180.0,  # Should be "Moderate" or "High"
            'humidity': 70.0,  # Should be "High"
            'temperature': 30.0  # Should be "Warm"
        }
        
        # Make the request
        response = self.client.post(self.predict_url, data, format='multipart')
        
        # Check specific parameter analyses
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        analyses = response.data['parameter_analysis']
        
        # The specific wording may vary, but check for key terms
        self.assertTrue("Low" in analyses['Nitrogen'] or "Deficient" in analyses['Nitrogen'])
        self.assertTrue("Optimal" in analyses['Phosphorus'])
        self.assertTrue("High" in analyses['Potassium'])
        self.assertTrue("Neutral" in analyses['pH'])
        self.assertTrue("Moderate" in analyses['Rainfall'] or "High" in analyses['Rainfall'])
        self.assertTrue("High" in analyses['Humidity'])
        self.assertTrue("Warm" in analyses['Temperature'])
