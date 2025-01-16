from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField(help_text="Duration of the event (e.g., 2 hours)")
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events')
    location = models.CharField(max_length=255, help_text="e.g., Zoom, Google Meet link")
    max_attendees = models.PositiveIntegerField()   
    featured_image = models.ImageField(upload_to='event_images/', blank=True, null=True, help_text="Primary event image")
    image1 = models.ImageField(upload_to='event_images/', blank=True, null=True, help_text="Additional image 1")
    image2 = models.ImageField(upload_to='event_images/', blank=True, null=True, help_text="Additional image 2")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.date} {self.time})"

class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"
