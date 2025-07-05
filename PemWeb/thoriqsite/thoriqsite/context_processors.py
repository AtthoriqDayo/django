# portaltech_project/context_processors.py
from pages.views import get_weather_data

def weather_context(request):
    weather = get_weather_data()
    return {'weather': weather}