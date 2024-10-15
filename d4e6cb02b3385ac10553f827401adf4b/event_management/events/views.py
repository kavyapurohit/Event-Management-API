from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOrganizerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'This is a protected view!'}
        return Response(content)

def home(request):
    """API Home View: Provides information about the available endpoints."""
    return JsonResponse({
        "message": "Welcome to the Event Management API!",
        "endpoints": {
            "events": "/api/events/",
            "rsvp": "/api/events/<event_id>/rsvp/",
            "reviews": "/api/events/<event_id>/reviews/"
        }
    })

class EventListCreateView(generics.ListCreateAPIView):
    """List and Create Events: GET: Lists all public events. POST: Authenticated users can create new events."""
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Event.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update, and Delete Events: GET: Retrieve details of an event. PUT/PATCH: Organizer can update an event. DELETE: Organizer can delete an event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]

class RSVPCreateView(generics.CreateAPIView):
    """Create RSVP: POST: Authenticated users can RSVP to an event."""
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewCreateView(generics.ListCreateAPIView):
    """List and Create Reviews: GET: List all reviews for an event. POST: Authenticated users can add a review."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(event_id=self.kwargs['event_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, event_id=self.kwargs['event_id'])
