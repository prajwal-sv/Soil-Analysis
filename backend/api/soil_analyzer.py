# Import libraries - standard libraries, PIL, TensorFlow, and pandas
from PIL import Image
import io
import os
import logging
import numpy as np
import pandas as pd  # For handling the CSV file

logger = logging.getLogger(__name__)

# TensorFlow compatibility flag
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

class SoilAnalyzer:
    """Class to analyze soil types and recommend crops"""
    
    def __init__(self):
        """Initialize the soil analyzer"""
        logger.info("Initializing soil analyzer")
        self.use_model = TENSORFLOW_AVAILABLE
        
        # Create the models directory for future use
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
            logger.info(f"Created models directory at {models_dir}")
        
        # Load the model if TensorFlow is available
        self.model = None
        if self.use_model:
            model_path = os.path.join(models_dir, 'inceptionV3_traineddata.h5')
            if os.path.exists(model_path):
                try:
                    self.model = tf.keras.models.load_model(model_path)
                    logger.info(f"Loaded model from {model_path}")
                except Exception as e:
                    logger.exception(f"Failed to load model: {e}")
                    self.use_model = False
            else:
                logger.warning(f"Model file not found at {model_path}")
        
        # Load the crop recommendation CSV file
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'Crop_recommendation.csv')
        try:
            self.crop_data = pd.read_csv(csv_path)
            logger.info(f"Loaded crop recommendation data from {csv_path}")
        except FileNotFoundError:
            logger.error(f"Crop recommendation CSV file not found at {csv_path}. Please check the file path.")
            self.crop_data = None
        except PermissionError:
            logger.error(f"Permission denied for accessing the CSV file at {csv_path}. Please check file permissions.")
            self.crop_data = None
        except Exception as e:
            logger.exception(f"Failed to load crop recommendation CSV: {e}")
            self.crop_data = None

    def analyze_soil_image(self, image_file):
        """
        Analyze the soil image using the trained model
        
        Args:
            image_file: An uploaded image file
            
        Returns:
            str: The predicted soil type (Red, Clay, Black, or Alluvial)
        """
        if not self.use_model or self.model is None:
            logger.warning("Model is not available. Cannot analyze soil image.")
            return "Model not available"
        
        try:
            # Open the image and preprocess it
            img = Image.open(image_file)
            img = img.resize((224, 224))  # Resize to match the model's input size
            img_array = np.array(img) / 255.0  # Normalize pixel values
            
            # Ensure the image has 3 channels (RGB)
            if img_array.shape[-1] != 3:
                logger.warning("Image does not have 3 channels. Converting to RGB.")
                img = img.convert('RGB')
                img_array = np.array(img) / 255.0
            
            # Add batch dimension
            input_data = np.expand_dims(img_array, axis=0)
            
            # Predict the soil type
            predictions = self.model.predict(input_data)
            predicted_class_index = np.argmax(predictions[0])
            
            # Map the index to soil types
            soil_types = ['Red', 'Clay', 'Black', 'Alluvial']
            predicted_soil_type = soil_types[predicted_class_index]
            
            logger.info(f"Model-based soil type prediction: {predicted_soil_type}")
            return predicted_soil_type
        except Exception as e:
            logger.exception(f"Error analyzing soil image: {e}")
            return "Analysis failed"

    def predict_crop(self, soil_features):
        """
        Predict the crop using the trained model
        
        Args:
            soil_features (list): A list of soil parameters [nitrogen, phosphorus, potassium, pH, rainfall, humidity, temperature]
        
        Returns:
            str: The predicted crop
        """
        if not self.use_model or self.model is None:
            logger.warning("Model is not available. Cannot predict crop.")
            return "Model not available"
        
        try:
            # Prepare the input for the model
            input_data = tf.convert_to_tensor([soil_features], dtype=tf.float32)
            
            # Predict the crop
            predictions = self.model.predict(input_data)
            predicted_crop_index = np.argmax(predictions[0])
            
            # Map the index to crop names (update this list based on your model's output)
            crop_names = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybeans', 'Groundnut', 'Vegetables', 'Chickpea', 'Kidneybeans', 'Lentil', 'Pigeonpeas', 'Mothbeans', 'Blackgram', 'Mungbean', 'Orange', 'Pomegranate', 'Banana', 'Grapes', 'Watermelon', 'Mango', 'Muskmelon', 'Apple', 'Papaya', 'Coconut', 'Jute', 'Coffee']
            predicted_crop = crop_names[predicted_crop_index]
            
            logger.info(f"Model-based crop prediction: {predicted_crop}")
            return predicted_crop
        except Exception as e:
            logger.exception(f"Error during crop prediction: {e}")
            return "Prediction failed"

    def recommend_crop_from_csv(self, nitrogen, phosphorus, potassium, ph, rainfall, humidity, temperature):
        """
        Recommend a crop based on parameters using the CSV file
        
        Args:
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
        if self.crop_data is None:
            logger.warning("Crop recommendation data is not available.")
            return "Crop recommendation data not available"
        
        try:
            # Filter the crop data based on the parameters
            filtered_data = self.crop_data[
                (self.crop_data['N'] == nitrogen) &
                (self.crop_data['P'] == phosphorus) &
                (self.crop_data['K'] == potassium) &
                (self.crop_data['ph'] == ph) &
                (self.crop_data['rainfall'] == rainfall) &
                (self.crop_data['humidity'] == humidity) &
                (self.crop_data['temperature'] == temperature)
            ]
            
            if not filtered_data.empty:
                # Return the first matching crop
                recommended_crop = filtered_data.iloc[0]['label']
                logger.info(f"Recommended crop from CSV: {recommended_crop}")
                return recommended_crop
            else:
                logger.warning("No matching crop found in the CSV data.")
                return "No matching crop found"
        except Exception as e:
            logger.exception(f"Error during crop recommendation from CSV: {e}")
            return "Error during crop recommendation"

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
        # If the model is available, use it for prediction
        if self.use_model and self.model:
            soil_features = [nitrogen, phosphorus, potassium, ph, rainfall, humidity, temperature]
            return self.predict_crop(soil_features)
        
        # Fallback to CSV-based recommendation if the model is not available
        return self.recommend_crop_from_csv(nitrogen, phosphorus, potassium, ph, rainfall, humidity, temperature)

    def analyze_parameters(self, nitrogen, phosphorus, potassium, ph, rainfall, humidity, temperature):
        """
        Analyze soil parameters and provide assessments
        
        Args:
            nitrogen (float): Nitrogen content
            phosphorus (float): Phosphorus content
            potassium (float): Potassium content
            ph (float): pH value
            rainfall (dfloat): Rainfall amount in mm
            humidity (float): Humidity percentage
            temperature (float):Temperature in celsius
            
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
