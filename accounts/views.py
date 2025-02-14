from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm
from django.views.generic import TemplateView
import requests
from django.conf import settings

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')

def health_tracking_view(request):
    return render(request, 'health_tracking.html')

def professional_advice_view(request):
    return render(request, 'professional_advice.html')

def air_quality_view(request):
    cities = ["London", "New York", "Tokyo", "Sydney", "Mumbai"]
    air_quality_data = []

    token = settings.AQICN_API_TOKEN

    for city in cities:
        url = f"http://api.waqi.info/feed/{city}/?token={token}"
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'ok':
            aqi = data['data']['aqi']
            dominant_pollutant = data['data']['dominentpol']
            advice = generate_advice(aqi)

            air_quality_data.append({
                "city": city,
                "aqi": aqi,
                "dominant_pollutant": dominant_pollutant,
                "advice": advice
            })

    return render(request, "air_quality.html", {"air_quality_data": air_quality_data})

def generate_advice(aqi):
    if aqi <= 50:
        return "Air quality is good. It's safe to go outside."
    elif aqi <= 100:
        return "Air quality is moderate. Sensitive individuals should limit prolonged outdoor exertion."
    elif aqi <= 150:
        return "Unhealthy for sensitive groups. Consider reducing prolonged or heavy exertion outdoors."
    elif aqi <= 200:
        return "Unhealthy. Everyone may experience health effects; sensitive groups should avoid outdoor exertion."
    elif aqi <= 300:
        return "Very Unhealthy. Health alert: everyone may experience more serious health effects."
    else:
        return "Hazardous. Health warnings of emergency conditions. The entire population is more likely to be affected."
