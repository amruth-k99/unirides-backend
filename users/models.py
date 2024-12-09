from urllib.request import Request
from django.db import models
from django.contrib.auth.models import User

import geopy.distance


class UserProfile(models.Model):
    """
    user_profile
    app_shared_count: ( int, not null) Number of times user shared the app
    show_app_rating: (tinyint(1),  not null) 1 to ask user to rate app, else 0
    """
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, default=None, null=True)

    class Meta:
        db_table = "user_profile"

    def to_dict(self):

        return {
            "name": self.name,
            "surname": self.surname,
            "mobile_number": self.mobile_number,
            "email": self.email,
            "user_profile_id": self.id
        }


class Locations(models.Model):

    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    address = models.CharField(max_length=255, null=False)
    frequency = models.IntegerField(
        null=False, default=1
    )  # Number of times this location is used

    class Meta:
        db_table = "locations"
        unique_together = ("latitude", "longitude")

    def to_dict(self, only_location_info=True):
        """Returns the dict object of a Location object

        Returns:
            [dict]: The dict of the Location object containing the latitude, longitude, address and frequency
        """
        location_info = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
        }

        if not only_location_info:
            location_info["frequency"] = self.frequency

        return location_info

    @classmethod
    def add_location(self, latitude, longitude, address, user_profile_id):
        if Locations.objects.filter(latitude=latitude, longitude=longitude).exists():
            location = Locations.objects.get(
                latitude=latitude, longitude=longitude)
            location.frequency += 1
        else:
            location = Locations.objects.create(
                latitude=latitude, longitude=longitude, address=address
            )
        location.save()

        return location

    def get_distance(self, latitude, longitude):
        return geopy.distance.geodesic(
            (self.latitude, self.longitude), (latitude, longitude)
        ).km
