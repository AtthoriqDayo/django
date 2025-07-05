from django.shortcuts import render
from django.shortcuts import render
import requests
import os

def get_weather_data():
    """
    Mengambil data cuaca dari OpenWeatherMap API.
    """
    api_key = os.getenv('OPENWEATHER_API_KEY')
    # Koordinat untuk Samarinda
    lat, lon = -0.5021, 117.1536
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=id"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': f"{data['main']['temp']:.0f}°C",
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
        }
        return weather
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None

def welcoming_view(request):
    return render(request, 'pages/welcoming.html')