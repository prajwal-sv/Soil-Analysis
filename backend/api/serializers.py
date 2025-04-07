from rest_framework import serializers
from .models import SoilAnalysis


class SoilAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for the SoilAnalysis model"""
    
    class Meta:
        model = SoilAnalysis
        fields = [
            'id', 'nitrogen', 'phosphorus', 'potassium', 
            'ph', 'rainfall', 'humidity', 'temperature', 
            'soil_image', 'soil_type', 'recommended_crop', 'created_at'
        ]
        read_only_fields = ['id', 'soil_type', 'recommended_crop', 'created_at']


class SoilPredictionRequestSerializer(serializers.Serializer):
    """Serializer for soil prediction request"""
    
    image = serializers.ImageField()
    nitrogen = serializers.FloatField()
    phosphorus = serializers.FloatField()
    potassium = serializers.FloatField()
    ph = serializers.FloatField()
    rainfall = serializers.FloatField()
    humidity = serializers.FloatField()
    temperature = serializers.FloatField()


class SoilPredictionResponseSerializer(serializers.Serializer):
    """Serializer for soil prediction response"""
    
    soil_type = serializers.CharField()
    recommended_crop = serializers.CharField()
    parameter_analysis = serializers.DictField(child=serializers.CharField())
