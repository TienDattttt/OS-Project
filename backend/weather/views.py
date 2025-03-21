# weather/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Location, CurrentWeather, Forecast, NewsArticle, UserProfile, WeatherAlert, NotificationSetting
from .serializers import (
    CurrentWeatherSerializer, ForecastSerializer, NewsArticleSerializer, LocationInputSerializer,
    UserRegistrationSerializer, UserLoginSerializer, WeatherAlertSerializer, NotificationSettingSerializer,LocationSerializer,UserUpdateSerializer
)
from .utils import fetch_current_weather, fetch_forecast, geocode_location, check_weather_alerts
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import uuid
from django.core.mail import send_mail
from webpush import send_user_notification



class CurrentWeatherViewSet(viewsets.ModelViewSet):
    queryset = CurrentWeather.objects.all()
    serializer_class = CurrentWeatherSerializer

    @action(detail=False, methods=['post'], serializer_class=LocationInputSerializer)
    def by_location(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        location_data = None
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')
        location_name = serializer.validated_data.get('name')

        if latitude and longitude:
            try:
                location = Location.objects.get(latitude=latitude, longitude=longitude)
            except Location.DoesNotExist:
                location_data = {'name': 'Custom Location', 'latitude': latitude, 'longitude': longitude, 'country_code': ''}
                location = Location.objects.create(**location_data)
        elif location_name:
            location_data = geocode_location(location_name)
            if not location_data:
                return Response({"error": "Could not find location"}, status=404)
            try:
                location = Location.objects.get(latitude=location_data['latitude'], longitude=location_data['longitude'])
            except Location.DoesNotExist:
                location = Location.objects.create(**location_data)

        weather_data = None
        try:
            current_weather = CurrentWeather.objects.get(location=location)
            if timezone.now() - current_weather.timestamp > timedelta(minutes=5):
                weather_data = fetch_current_weather(location.latitude, location.longitude)
                if weather_data:
                    for key, value in weather_data.items():
                        setattr(current_weather, key, value)
                    current_weather.timestamp = timezone.now()
                    current_weather.save()
                else:
                    weather_data = {
                        'temperature': current_weather.temperature,
                        'humidity': current_weather.humidity,
                        'wind_speed': current_weather.wind_speed,
                        'pressure': current_weather.pressure,
                        'weather_condition': current_weather.weather_condition,
                        'icon_url': current_weather.icon_url
                    }
        except CurrentWeather.DoesNotExist:
            weather_data = fetch_current_weather(location.latitude, location.longitude)
            if weather_data:
                current_weather = CurrentWeather.objects.create(location=location, **weather_data)
            else:
                return Response({"error": "Failed to fetch weather data"}, status=500)

        forecast_data = fetch_forecast(location.latitude, location.longitude)
        if weather_data:
            alerts = check_weather_alerts(location, weather_data, forecast_data)
        else:
            alerts = []

        serializer = CurrentWeatherSerializer(current_weather)
        db_alerts = WeatherAlert.objects.filter(location=location)
        alert_serializer = WeatherAlertSerializer(db_alerts, many=True)

        return Response({
            'weather': serializer.data,
            'alerts': alert_serializer.data
        })

class WeatherAlertViewSet(viewsets.ModelViewSet):
    queryset = WeatherAlert.objects.all()
    serializer_class = WeatherAlertSerializer

    @action(detail=False, methods=['post'], serializer_class=LocationInputSerializer)
    def by_location(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')
        location_name = serializer.validated_data.get('name')

        if latitude and longitude:
            try:
                location = Location.objects.get(latitude=latitude, longitude=longitude)
            except Location.DoesNotExist:
                location_data = {'name': 'Custom Location', 'latitude': latitude, 'longitude': longitude, 'country_code': ''}
                location = Location.objects.create(**location_data)
        elif location_name:
            location_data = geocode_location(location_name)
            if not location_data:
                return Response({"error": "Could not find location"}, status=status.HTTP_404_NOT_FOUND)
            try:
                location = Location.objects.get(latitude=location_data['latitude'], longitude=location_data['longitude'])
            except Location.DoesNotExist:
                location = Location.objects.create(**location_data)
        else:
            return Response({"error": "Invalid location data"}, status=status.HTTP_400_BAD_REQUEST)

        weather_data = fetch_current_weather(location.latitude, location.longitude)
        if not weather_data:
            return Response({"error": "Failed to fetch weather data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        forecast_data = fetch_forecast(location.latitude, location.longitude)
        alerts = check_weather_alerts(location, weather_data, forecast_data)

        return Response(alerts, status=status.HTTP_200_OK)

class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer

    def retrieve(self, request, *args, **kwargs):
        location_id = kwargs.get('pk')
        forecast_type = request.query_params.get('type', 'daily')
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=404)

        Forecast.objects.filter(location=location).delete()
        forecast_data = fetch_forecast(location.latitude, location.longitude)
        if not forecast_data:
            return Response({"error": "Failed to fetch forecast data"}, status=500)

        forecasts = []
        for item in forecast_data:
            if item['forecast_type'] == forecast_type:
                forecast = Forecast.objects.create(location=location, **item)
                forecasts.append(forecast)

        serializer = self.get_serializer(forecasts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def all_types(self, request, pk=None):
        try:
            location = Location.objects.get(id=pk)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=404)

        Forecast.objects.filter(location=location).delete()
        forecast_data = fetch_forecast(location.latitude, location.longitude)
        if not forecast_data:
            return Response({"error": "Failed to fetch forecast data"}, status=500)

        forecasts = [Forecast.objects.create(location=location, **item) for item in forecast_data]
        serializer = self.get_serializer(forecasts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def check_notifications(self, request):
        """Kiểm tra dự báo thời tiết tại vị trí hiện tại và gửi thông báo đẩy nếu cần"""
        location_name = request.data.get('location_name')
        if not location_name:
            return Response({'error': 'location_name is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy cài đặt thông báo của người dùng
        try:
            setting = NotificationSetting.objects.get(user=request.user)
        except NotificationSetting.DoesNotExist:
            return Response({'error': 'Notification settings not found'}, status=status.HTTP_404_NOT_FOUND)

        # Lấy hoặc tạo vị trí
        location_data = geocode_location(location_name)
        if not location_data:
            return Response({"error": "Could not find location"}, status=status.HTTP_404_NOT_FOUND)
        try:
            location = Location.objects.get(latitude=location_data['latitude'], longitude=location_data['longitude'])
        except Location.DoesNotExist:
            location = Location.objects.create(**location_data)

        # Lấy dự báo thời tiết
        forecast_data = fetch_forecast(location.latitude, location.longitude)
        if not forecast_data:
            return Response({"error": "Failed to fetch forecast data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Kiểm tra điều kiện thông báo và gửi thông báo đẩy
        for forecast in forecast_data:
            if forecast['forecast_type'] != 'daily':
                continue  # Chỉ kiểm tra dự báo hàng ngày
            forecast_time = forecast['forecast_time']
            high_temp = forecast['high_temperature']
            low_temp = forecast['low_temperature']
            rain_prob = forecast['rain_probability']

            if setting.notify_rain and rain_prob > 50:
                send_user_notification(
                    user=request.user,
                    payload={
                        'head': 'Cảnh Báo Thời Tiết',
                        'body': f"Sắp có mưa tại {location_name} vào {forecast_time.strftime('%Y-%m-%d')}",
                    },
                    ttl=1000
                )
            if setting.notify_low_temp and low_temp < 20:
                send_user_notification(
                    user=request.user,
                    payload={
                        'head': 'Cảnh Báo Thời Tiết',
                        'body': f"Nhiệt độ tại {location_name} sẽ dưới 20°C ({low_temp}°C) vào {forecast_time.strftime('%Y-%m-%d')}",
                    },
                    ttl=1000
                )
            if setting.notify_high_temp and high_temp > 35:
                send_user_notification(
                    user=request.user,
                    payload={
                        'head': 'Cảnh Báo Thời Tiết',
                        'body': f"Nhiệt độ tại {location_name} sẽ trên 35°C ({high_temp}°C) vào {forecast_time.strftime('%Y-%m-%d')}",
                    },
                    ttl=1000
                )

        return Response({'message': 'Notifications checked and sent if applicable.'}, status=status.HTTP_200_OK)

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by('-published_at')
    serializer_class = NewsArticleSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Registration successful.',
                'user': {
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def request_password_reset(self, request):
        email = request.data.get('email')
        user = get_object_or_404(UserProfile, email=email)
        token = str(uuid.uuid4())
        user.confirmation_token = token
        user.save()

        reset_link = f"http://localhost:8000/api/auth/reset-password/{token}/"
        send_mail(
            'Reset Your Password',
            f'Click this link to reset your password: {reset_link}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='reset-password/(?P<token>[^/.]+)')
    def reset_password(self, request, token=None):
        user = get_object_or_404(UserProfile, confirmation_token=token)
        new_password = request.data.get('password')
        if not new_password or len(new_password) < 8:
            return Response({'error': 'Password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.confirmation_token = None
        user.save()
        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def save_subscription(self, request):
        """Lưu subscription của người dùng để gửi thông báo đẩy"""
        subscription_data = request.data
        try:
            # Lưu subscription vào database
            from webpush.models import PushInformation
            subscription, created = PushInformation.objects.get_or_create(
                user=request.user,
                subscription=subscription_data
            )
            return Response({'message': 'Subscription saved successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Lấy thông tin người dùng"""
        user = request.user
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Cập nhật thông tin người dùng"""
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully.',
                'user': {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Quản lý vị trí yêu thích
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favorite_locations(self, request):
        """Lấy danh sách vị trí yêu thích của người dùng"""
        locations = request.user.favorite_locations.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_favorite_location(self, request):
        """Thêm một vị trí yêu thích"""
        location_name = request.data.get('location_name')
        if not location_name:
            return Response({'error': 'location_name is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy hoặc tạo vị trí
        location_data = geocode_location(location_name)
        if not location_data:
            return Response({"error": "Could not find location"}, status=status.HTTP_404_NOT_FOUND)
        try:
            location = Location.objects.get(latitude=location_data['latitude'], longitude=location_data['longitude'])
        except Location.DoesNotExist:
            location = Location.objects.create(**location_data)

        # Thêm vị trí vào danh sách yêu thích
        if location in request.user.favorite_locations.all():
            return Response({'error': 'Location already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.favorite_locations.add(location)
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='favorite-locations/(?P<location_id>[^/.]+)', permission_classes=[IsAuthenticated])
    def remove_favorite_location(self, request, location_id=None):
        """Xóa một vị trí yêu thích"""
        try:
            location = Location.objects.get(id=location_id)
            if location not in request.user.favorite_locations.all():
                return Response({'error': 'Location not in favorites'}, status=status.HTTP_404_NOT_FOUND)
            request.user.favorite_locations.remove(location)
            return Response({'message': 'Location removed from favorites'}, status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    # Quản lý cài đặt thông báo
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def notification_settings(self, request):
        """Lấy cài đặt thông báo của người dùng"""
        setting, created = NotificationSetting.objects.get_or_create(user=request.user)
        serializer = NotificationSettingSerializer(setting)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_notification_settings(self, request):
        """Cập nhật cài đặt thông báo của người dùng"""
        setting, created = NotificationSetting.objects.get_or_create(user=request.user)
        serializer = NotificationSettingSerializer(setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)