# Using native Python for color analysis instead of NumPy
# import numpy as np
from PIL import Image
import io
import os
import logging
import random

logger = logging.getLogger(__name__)

class SoilAnalyzer:
    """Class to analyze soil types and recommend crops"""
    
    def __init__(self):
        """Initialize the soil analyzer"""
        logger.info("Initializing simplified soil analyzer")
    
    def predict_soil_type(self, image_file):
        """
        Predict soil type from image using color analysis
        
        Args:
            image_file: An uploaded image file
            
        Returns:
            str: The predicted soil type (Red, Clay, Black, or Alluvial)
        """
        try:
            # Open the image and preprocess it
            img = Image.open(image_file)
            img = img.resize((224, 224))  # Resize for consistency
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            # Sample pixels to calculate average color (using a subset for efficiency)
            pixels = list(img.getdata())
            sample_size = min(len(pixels), 1000)  # Sample up to 1000 pixels
            sample = [pixels[i] for i in range(0, len(pixels), len(pixels)//sample_size)]
            
            # Calculate average RGB
            r_sum = sum(p[0] for p in sample)
            g_sum = sum(p[1] for p in sample)
            b_sum = sum(p[2] for p in sample)
            
            r_avg = r_sum / len(sample)
            g_avg = g_sum / len(sample)
            b_avg = b_sum / len(sample)
            
            # Normalize to [0, 1]
            r, g, b = r_avg / 255.0, g_avg / 255.0, b_avg / 255.0
            
            # Simple logic based on dominant colors
            if r > max(g, b) + 0.1:
                predicted_soil_type = 'Red'
            elif abs(r - g) < 0.1 and abs(r - b) < 0.1 and max(r, g, b) < 0.5:
                predicted_soil_type = 'Black'
            elif b > max(r, g) + 0.05:
                predicted_soil_type = 'Alluvial'
            else:
                predicted_soil_type = 'Clay'
            
            logger.info(f"Predicted soil type: {predicted_soil_type}")
            return predicted_soil_type
            
        except Exception as e:
            logger.exception(f"Error predicting soil type: {e}")
            # Default to a common soil type if prediction fails
            return 'Clay'

    def recommend_crop(self, soil_type, nitrogen, phosphorus, potassium, ph, rainfall, humidity, temperature):
        """
        Recommend suitable crops based on soil type and parameters
        
        Args:
            soil_type (str): The type of soil (Red, Clay, Black, or Alluvial)
            nitrogen (float): Nitrogen content
            phosphorus (float): Phosphorus content
            potassium (float): Potassium content
            ph (float): pH value
            rainfall (float): Rainfall amount in mm
            humidity (float): Humidity percentage
            temperature (float): Temperature in celsius
            
        Returns:
            str: The recommended crop
        """
        # Soil type specific crops
        soil_crops = {
            'Red': ['Groundnut', 'Potato', 'Cotton', 'Maize'],
            'Clay': ['Rice', 'Wheat', 'Sugarcane', 'Oats'],
            'Black': ['Cotton', 'Soybeans', 'Sugarcane', 'Wheat'],
            'Alluvial': ['Rice', 'Maize', 'Wheat', 'Vegetables']
        }
        
        # Get initial crop selection based on soil type
        potential_crops = soil_crops.get(soil_type, ['Maize', 'Wheat'])
        
        # Refine selection based on NPK values
        npk_score = {}
        for crop in potential_crops:
            if crop in ['Rice', 'Wheat']:
                # These crops need high N
                n_factor = 1.0 if nitrogen > 40 else 0.5
            elif crop in ['Cotton', 'Sugarcane']:
                # These crops need balanced NPK
                n_factor = 1.0 if (30 <= nitrogen <= 60) else 0.5
            elif crop in ['Groundnut', 'Soybeans']:
                # Legumes need less N but more P and K
                n_factor = 1.0 if nitrogen < 40 else 0.7
            else:
                n_factor = 0.8
                
            # Factor in pH preferences
            if crop in ['Potato', 'Maize']:
                # Prefer slightly acidic soil
                ph_factor = 1.0 if 5.5 <= ph <= 6.5 else 0.6
            elif crop in ['Rice']:
                # Can tolerate more acidic conditions
                ph_factor = 1.0 if 5.0 <= ph <= 6.5 else 0.7
            elif crop in ['Cotton', 'Wheat']:
                # Prefer neutral to slightly alkaline
                ph_factor = 1.0 if 6.5 <= ph <= 8.0 else 0.6
            else:
                ph_factor = 1.0 if 6.0 <= ph <= 7.5 else 0.7
                
            # Factor in climate preferences
            if crop in ['Rice']:
                # Needs high rainfall and humidity
                climate_factor = 1.0 if rainfall > 150 and humidity > 60 else 0.5
            elif crop in ['Cotton']:
                # Prefers warm and dry conditions
                climate_factor = 1.0 if temperature > 25 and humidity < 60 else 0.7
            elif crop in ['Wheat']:
                # Prefers cooler temperatures
                climate_factor = 1.0 if temperature < 25 else 0.6
            elif crop in ['Sugarcane']:
                # Needs warm and humid conditions
                climate_factor = 1.0 if temperature > 20 and humidity > 50 else 0.7
            else:
                climate_factor = 0.8
                
            # Calculate overall score
            npk_score[crop] = n_factor * ph_factor * climate_factor
        
        # Find the crop with the highest score
        max_score = -1
        recommended_crop = potential_crops[0]  # Default to first crop
        
        for crop, score in npk_score.items():
            if score > max_score:
                max_score = score
                recommended_crop = crop
        
        return recommended_crop

    def analyze_parameters(self, nitrogen, phosphorus, potassium, ph, rainfall, humidity, temperature):
        """
        Analyze soil parameters and provide assessments
        
        Args:
            nitrogen (float): Nitrogen content
            phosphorus (float): Phosphorus content
            potassium (float): Potassium content
            ph (float): pH value
            rainfall (float): Rainfall amount in mm
            humidity (float): Humidity percentage
            temperature (float): Temperature in celsius
            
        Returns:
            dict: Analysis of each parameter
        """
        analysis = {}
        
        # Analyze Nitrogen (N)
        if nitrogen < 20:
            analysis['Nitrogen'] = 'Deficient - Consider adding nitrogen fertilizers'
        elif 20 <= nitrogen < 40:
            analysis['Nitrogen'] = 'Low - May need supplementation'
        elif 40 <= nitrogen < 80:
            analysis['Nitrogen'] = 'Optimal - Good for most crops'
        else:
            analysis['Nitrogen'] = 'High - May cause excessive vegetative growth'
        
        # Analyze Phosphorus (P)
        if phosphorus < 10:
            analysis['Phosphorus'] = 'Deficient - Add phosphate fertilizers'
        elif 10 <= phosphorus < 20:
            analysis['Phosphorus'] = 'Low - Consider supplementation'
        elif 20 <= phosphorus < 40:
            analysis['Phosphorus'] = 'Optimal - Good for root development'
        else:
            analysis['Phosphorus'] = 'High - May inhibit micronutrient uptake'
        
        # Analyze Potassium (K)
        if potassium < 15:
            analysis['Potassium'] = 'Deficient - Add potash fertilizers'
        elif 15 <= potassium < 25:
            analysis['Potassium'] = 'Low - May need supplementation'
        elif 25 <= potassium < 45:
            analysis['Potassium'] = 'Optimal - Good for disease resistance'
        else:
            analysis['Potassium'] = 'High - Generally beneficial but watch for imbalances'
        
        # Analyze pH
        if ph < 5.5:
            analysis['pH'] = 'Acidic - May need lime to raise pH'
        elif 5.5 <= ph < 6.5:
            analysis['pH'] = 'Slightly Acidic - Ideal for many crops'
        elif 6.5 <= ph < 7.5:
            analysis['pH'] = 'Neutral - Excellent for most crops'
        elif 7.5 <= ph < 8.5:
            analysis['pH'] = 'Slightly Alkaline - Good for some crops'
        else:
            analysis['pH'] = 'Alkaline - May need sulfur to lower pH'
        
        # Analyze Rainfall
        if rainfall < 50:
            analysis['Rainfall'] = 'Very Low - Irrigation required'
        elif 50 <= rainfall < 100:
            analysis['Rainfall'] = 'Low - May need supplemental irrigation'
        elif 100 <= rainfall < 200:
            analysis['Rainfall'] = 'Moderate - Sufficient for many crops'
        else:
            analysis['Rainfall'] = 'High - Good for water-loving crops, drainage may be needed'
        
        # Analyze Humidity
        if humidity < 30:
            analysis['Humidity'] = 'Low - May increase evapotranspiration'
        elif 30 <= humidity < 60:
            analysis['Humidity'] = 'Moderate - Good for most crops'
        else:
            analysis['Humidity'] = 'High - Watch for fungal diseases'
        
        # Analyze Temperature
        if temperature < 15:
            analysis['Temperature'] = 'Cool - Suitable for cool-season crops'
        elif 15 <= temperature < 25:
            analysis['Temperature'] = 'Moderate - Ideal for many crops'
        elif 25 <= temperature < 35:
            analysis['Temperature'] = 'Warm - Good for heat-loving crops'
        else:
            analysis['Temperature'] = 'Hot - May cause heat stress in some crops'
        
        return analysis
