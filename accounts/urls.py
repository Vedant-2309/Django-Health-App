from django.urls import path
from .views import signup_view, login_view, home_view, health_tracking_view, professional_advice_view, air_quality_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('', home_view, name='home'),
    path('health-tracking/', health_tracking_view, name='health_tracking'),
    path('professional-advice/', professional_advice_view, name='professional_advice'),
    path('air-quality/', air_quality_view, name='air_quality'),
]