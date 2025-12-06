from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import SoilPredictionRequestSerializer, SoilPredictionResponseSerializer, SoilAnalysisSerializer
from .models import SoilAnalysis
from .soil_analyzer import SoilAnalyzer

import logging

logger = logging.getLogger(__name__)

class PredictSoilTypeView(APIView):
    """
    API view to predict soil type and recommend crops based on soil parameters and image
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, format=None):
        """Handle POST request with soil parameters and image"""
        
        # Validate the incoming data
        request_serializer = SoilPredictionRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(
                {"detail": "Invalid input data", "errors": request_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract validated data
        validated_data = request_serializer.validated_data
        
        try:
            # Initialize soil analyzer
            soil_analyzer = SoilAnalyzer()
            
            # Predict soil type from image
            soil_type = soil_analyzer.analyze_soil_image(validated_data['image'])
            
            # Get recommended crop based on soil type and parameters
            recommended_crop = soil_analyzer.recommend_crop(
                soil_type=soil_type,
                nitrogen=validated_data['nitrogen'],
                phosphorus=validated_data['phosphorus'],
                potassium=validated_data['potassium'],
                ph=validated_data['ph'],
                rainfall=validated_data['rainfall'],
                humidity=validated_data['humidity'],
                temperature=validated_data['temperature']
            )
            
            # Analyze parameters
            parameter_analysis = soil_analyzer.analyze_parameters(
                nitrogen=validated_data['nitrogen'],
                phosphorus=validated_data['phosphorus'],
                potassium=validated_data['potassium'],
                ph=validated_data['ph'],
                rainfall=validated_data['rainfall'],
                humidity=validated_data['humidity'],
                temperature=validated_data['temperature']
            )
            
            # Save the analysis to the database
            analysis_data = {
                'soil_type': soil_type,
                'recommended_crop': recommended_crop,
                'soil_image': validated_data['image'],
                'nitrogen': validated_data['nitrogen'],
                'phosphorus': validated_data['phosphorus'],
                'potassium': validated_data['potassium'],
                'ph': validated_data['ph'],
                'rainfall': validated_data['rainfall'],
                'humidity': validated_data['humidity'],
                'temperature': validated_data['temperature']
            }
            
            analysis_serializer = SoilAnalysisSerializer(data=analysis_data)
            if analysis_serializer.is_valid():
                analysis_serializer.save()
            
            # Prepare response
            response_data = {
                'soil_type': soil_type,
                'recommended_crop': recommended_crop,
                'parameter_analysis': parameter_analysis
            }
            
            response_serializer = SoilPredictionResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                logger.error(f"Response serializer errors: {response_serializer.errors}")
                return Response(
                    {"detail": "Error formatting response data"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            logger.exception("Error processing soil analysis request")
            return Response(
                {"detail": f"Error processing request: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
