from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Location, CurrentWeather, Forecast, NewsArticle,UserProfile
from .serializers import CurrentWeatherSerializer, ForecastSerializer, NewsArticleSerializer, LocationInputSerializer, UserRegistrationSerializer, UserLoginSerializer
from .utils import fetch_current_weather, fetch_forecast, geocode_location
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import uuid
from django.core.mail import send_mail

class CurrentWeatherViewSet(viewsets.ModelViewSet):
    queryset = CurrentWeather.objects.all()
    serializer_class = CurrentWeatherSerializer

# Action mới để lấy thời tiết theo địa điểm
    @action(detail=False, methods=['post'], serializer_class=LocationInputSerializer)
    def by_location(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        location_data = None
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')
        location_name = serializer.validated_data.get('name')

        # Trường hợp người dùng nhập tọa độ
        if latitude and longitude:
            try:
                location = Location.objects.get(latitude=latitude, longitude=longitude)
            except Location.DoesNotExist:
                location_data = {'name': 'Custom Location', 'latitude': latitude, 'longitude': longitude, 'country_code': ''}
                location = Location.objects.create(**location_data)
        
        # Trường hợp người dùng nhập tên địa điểm
        elif location_name:
            location_data = geocode_location(location_name)
            if not location_data:
                return Response({"error": "Could not find location"}, status=404)
            try:
                location = Location.objects.get(latitude=location_data['latitude'], longitude=location_data['longitude'])
            except Location.DoesNotExist:
                location = Location.objects.create(**location_data)

        # Lấy hoặc cập nhật dữ liệu thời tiết
        try:
            current_weather = CurrentWeather.objects.get(location=location)
            if timezone.now() - current_weather.timestamp > timedelta(minutes=5):
                weather_data = fetch_current_weather(location.latitude, location.longitude)
                if weather_data:
                    for key, value in weather_data.items():
                        setattr(current_weather, key, value)
                    current_weather.timestamp = timezone.now()
                    current_weather.save()
        except CurrentWeather.DoesNotExist:
            weather_data = fetch_current_weather(location.latitude, location.longitude)
            if weather_data:
                current_weather = CurrentWeather.objects.create(location=location, **weather_data)
            else:
                return Response({"error": "Failed to fetch weather data"}, status=500)

        serializer = CurrentWeatherSerializer(current_weather)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        location_id = kwargs.get('pk')
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=404)


        # Kiểm tra và cập nhật dữ liệu nếu quá 5 phút
        try:
            current_weather = CurrentWeather.objects.get(location=location)
            if timezone.now() - current_weather.timestamp > timedelta(minutes=5):
                weather_data = fetch_current_weather(location.latitude, location.longitude)
                if weather_data:
                    for key, value in weather_data.items():
                        setattr(current_weather, key, value)
                    current_weather.timestamp = timezone.now()  # Cập nhật thời điểm lấy dữ liệu
                    current_weather.save()
        except CurrentWeather.DoesNotExist:
            weather_data = fetch_current_weather(location.latitude, location.longitude)
            if weather_data:
                current_weather = CurrentWeather.objects.create(location=location, **weather_data)
            else:
                return Response({"error": "Failed to fetch weather data"}, status=500)


        serializer = self.get_serializer(current_weather)
        return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        # Lấy tất cả vị trí và cập nhật nếu cần
        locations = Location.objects.all()
        updated_weathers = []
        for location in locations:
            try:
                current_weather = CurrentWeather.objects.get(location=location)
                if timezone.now() - current_weather.timestamp > timedelta(minutes=5):
                    weather_data = fetch_current_weather(location.latitude, location.longitude)
                    if weather_data:
                        for key, value in weather_data.items():
                            setattr(current_weather, key, value)
                        current_weather.timestamp = timezone.now()
                        current_weather.save()
                updated_weathers.append(current_weather)
            except CurrentWeather.DoesNotExist:
                weather_data = fetch_current_weather(location.latitude, location.longitude)
                if weather_data:
                    current_weather = CurrentWeather.objects.create(location=location, **weather_data)
                    updated_weathers.append(current_weather)


        serializer = self.get_serializer(updated_weathers, many=True)
        return Response(serializer.data)
   
class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer


    def retrieve(self, request, *args, **kwargs):
        location_id = kwargs.get('pk')
        forecast_type = request.query_params.get('type', 'daily')  # Mặc định là daily
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=404)


        # Xóa dữ liệu cũ và cập nhật dự báo mới
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


        # Xóa dữ liệu cũ và cập nhật dự báo mới
        Forecast.objects.filter(location=location).delete()
        forecast_data = fetch_forecast(location.latitude, location.longitude)
        if not forecast_data:
            return Response({"error": "Failed to fetch forecast data"}, status=500)


        forecasts = [Forecast.objects.create(location=location, **item) for item in forecast_data]
        serializer = self.get_serializer(forecasts, many=True)
        return Response(serializer.data)


class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by('-published_at')  # Sắp xếp theo thời gian mới nhất
    serializer_class = NewsArticleSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
        print("Request data:", request.data)
        serializer = UserLoginSerializer(data=request.data)
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
        print("Validation errors:", serializer.errors)
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

