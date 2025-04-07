from django.contrib import admin
from .models import SoilAnalysis

@admin.register(SoilAnalysis)
class SoilAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'soil_type', 'recommended_crop', 'created_at')
    list_filter = ('soil_type', 'created_at')
    search_fields = ('soil_type', 'recommended_crop')
    readonly_fields = ('created_at',)
