import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime


def geocode_location(location_name):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit=1&appid={settings.OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return {
            'name': data['name'],
            'latitude': data['lat'],
            'longitude': data['lon'],
            'country_code': data.get('country', '')
        }
    return None

def fetch_current_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure'],
            'weather_condition': data['weather'][0]['description'],
            'icon_url': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png",
        }
    return None



def fetch_forecast(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecasts = []


        # Short-term (5 ngày, 3 giờ/lần)
        short_term = []
        for item in data['list'][:8]:  # Lấy 24 giờ đầu tiên (8 khoảng 3 giờ)
            short_term.append({
                'forecast_type': 'short',
                'forecast_time': datetime.fromtimestamp(item['dt']),
                'high_temperature': item['main']['temp_max'],
                'low_temperature': item['main']['temp_min'],
                'rain_probability': item.get('pop', 0) * 100,  # Tỷ lệ mưa (%)
                'uv_index': item.get('uvi', 0),  # API miễn phí không có UV, cần API khác nếu muốn chính xác
            })


        # Daily (5 ngày, tổng hợp mỗi ngày)
        daily = {}
        for item in data['list']:
            day = datetime.fromtimestamp(item['dt']).date()
            if day not in daily:
                daily[day] = {
                    'forecast_type': 'daily',
                    'forecast_time': datetime.fromtimestamp(item['dt']),
                    'high_temperature': item['main']['temp_max'],
                    'low_temperature': item['main']['temp_min'],
                    'rain_probability': item.get('pop', 0) * 100,
                    'uv_index': item.get('uvi', 0),
                }
            else:
                daily[day]['high_temperature'] = max(daily[day]['high_temperature'], item['main']['temp_max'])
                daily[day]['low_temperature'] = min(daily[day]['low_temperature'], item['main']['temp_min'])
                daily[day]['rain_probability'] = max(daily[day]['rain_probability'], item.get('pop', 0) * 100)


        forecasts.extend(short_term)
        forecasts.extend(daily.values())


        # Weekly (tổng hợp 5 ngày thành 1 tuần)
        weekly = {
            'forecast_type': 'weekly',
            'forecast_time': timezone.now(),
            'high_temperature': max(item['main']['temp_max'] for item in data['list']),
            'low_temperature': min(item['main']['temp_min'] for item in data['list']),
            'rain_probability': max(item.get('pop', 0) * 100 for item in data['list']),
            'uv_index': max(item.get('uvi', 0) for item in data['list']),
        }
        forecasts.append(weekly)


        return forecasts
    return None

