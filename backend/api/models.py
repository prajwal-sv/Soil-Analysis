from django.db import models


class SoilAnalysis(models.Model):
    """Model to store soil analysis results"""
    
    SOIL_TYPE_CHOICES = (
        ('Red', 'Red Soil'),
        ('Clay', 'Clay Soil'),
        ('Black', 'Black Soil'),
        ('Alluvial', 'Alluvial Soil'),
    )
    
    # Input parameters
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    
    # Soil image
    soil_image = models.ImageField(upload_to='soil_images/')
    
    # Analysis results
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPE_CHOICES)
    recommended_crop = models.CharField(max_length=100)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Soil Analysis: {self.soil_type} - {self.recommended_crop}"
