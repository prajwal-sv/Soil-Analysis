from django.urls import path
from .views import PredictSoilTypeView

urlpatterns = [
    path('predict/', PredictSoilTypeView.as_view(), name='predict_soil_type'),
]
