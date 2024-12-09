from django.db import models
from config.helper_functions import remove_empty_keys

from django.db import models
# Assuming you're using Django's default User model
from django.utils.timezone import now
from users.models import Locations,  UserProfile, User


class Ride(models.Model):
    WAITING = 'Waiting'
    SCHEDULED = 'Scheduled'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (SCHEDULED, 'Scheduled'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        (WAITING, "Waiting")
    ]

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='user_id')
    provider = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='provider_id', null=True)
    source_location = models.ForeignKey(
        Locations, on_delete=models.CASCADE, related_name="ride_source_location"
    )
    destination_location = models.ForeignKey(
        Locations, on_delete=models.CASCADE, related_name="ride_destination_location"
    )
    available_seats = models.PositiveIntegerField(
        null=True, blank=True)  # For drivers

    distance = models.FloatField(null=True)
    estimated_fare = models.JSONField(null=True)
    estimated_travel_time_in_mins = models.FloatField(null=True)
    final_fare = models.JSONField(null=True)
    vehicle_type = models.CharField(max_length=255, null=True)
    notes = models.TextField(blank=True, null=True)  # Optional ride notes
    ride_status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def update_status(self, status):
        self.ride_status = status
        self.save()

    def completed(self):
        self.ride_status = "Completed"
        self.save()

    def update_provider(self, provider):
        self.provider = provider
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.to_dict(),
            "provider": self.provider.to_dict() if self.provider else None,
            "distance": self.distance,
            "estimated_fare": self.estimated_fare,
            "estimated_travel_time_in_mins": self.estimated_travel_time_in_mins,
            "final_fare": self.final_fare,
            "vehicle_type": self.vehicle_type,
            "source_location": self.source_location.to_dict(),
            "destination_location": self.destination_location.to_dict(),
            "available_seats": self.available_seats,
            "notes": self.notes,
            "ride_status": self.ride_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
