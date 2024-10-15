from django.contrib import admin
from django.urls import path, include
from events.views import home
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('admin/', admin.site.urls),
    path('api/', include('events.urls')),
    path('', home, name='home'),
]
