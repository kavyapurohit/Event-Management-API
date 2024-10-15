from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# UserProfile Model - Extends the built-in User model to store additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.full_name

# Event Model - Represents an event created by a user with related details
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_events")
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_time']  # Orders events by start time by default

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

# RSVP Model - Handles user responses to events with choices for RSVP status
class RSVP(models.Model):
    GOING = 'Going'
    MAYBE = 'Maybe'
    NOT_GOING = 'Not Going'
    
    STATUS_CHOICES = [
        (GOING, 'Going'),
        (MAYBE, 'Maybe'),
        (NOT_GOING, 'Not Going'),
    ]

    event = models.ForeignKey(Event, related_name='rsvps', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"

    def __str__(self):
        return f"{self.user.username} RSVP - {self.get_status_display()} for {self.event.title}"

# Review Model - Allows users to leave a review with a rating and comment for an event
class Review(models.Model):
    event = models.ForeignKey(Event, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Review for {self.event.title} by {self.user.username}"

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-id']  # Orders reviews by most recent first

# Signal to create UserProfile when a new User is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when a new User is created."""
    if created and not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
