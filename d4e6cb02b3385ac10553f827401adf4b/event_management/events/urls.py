from django.urls import path
from .views import EventListCreateView, EventDetailView, RSVPCreateView, ReviewCreateView 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:event_id>/rsvp/', RSVPCreateView.as_view(), name='rsvp-create'),
    path('events/<int:event_id>/reviews/', ReviewCreateView.as_view(), name='review-list-create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT obtain token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh token
]
