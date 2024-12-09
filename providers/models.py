from django.db import models
from django.contrib.auth.models import User

from config.helper_functions import format_date

class ProviderProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, unique=True)
    show_app_rating = models.BooleanField(default=False)
    wallet_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    current_latitude = models.DecimalField(
        max_digits=10, decimal_places=7, null=True)
    current_longitude = models.DecimalField(
        max_digits=10, decimal_places=7, null=True)
    last_active_time = models.DateTimeField()
    vehicle_type = models.CharField(max_length=255, null=True)
    rating = models.FloatField(default=0.0)
    geohash_code = models.CharField(max_length=12, null=True)
    vehicle = models.CharField(max_length=255, null=True)
    razorpay_customer_id = models.CharField(max_length=255, null=True)
    hatchback_and_sedan = models.BooleanField(default=False)
    insurance_expiry_date = models.DateField(null=True)
    vehicle_license_expiry_date = models.DateField(null=True)
    driving_license_expiry_date = models.DateField(null=True)
    aadhar_number = models.CharField(max_length=255, null=True)
    total_rides = models.IntegerField(default=0)
    total_ratings = models.IntegerField(default=0)
    total_earnings = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
    bank_account_number = models.CharField(max_length=20, null=True)
    ifsc = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "provider_profile"

    def to_dict(self, is_new_user=False, to_user=False, summary=False, to_admin=False):
        """Returns the dict object of a UserProfile object

        Args:
            is_new_user (bool, optional): if true, the user is just created. Defaults to False.

        Returns:
            [dict]: The dict of the UserProfile object
        """

        if summary:
            return {
                "name": self.name,
                "surname": self.surname,
                "mobile_number": self.mobile_number,
                "email": self.user.email,
                "wallet_balance": self.wallet_balance,
                "provider_profile_id": self.id,
                "account_status": self.account_status,
                "status": self.status,
                "vehicle": self.vehicle.to_dict() if self.vehicle else None
            }

        dict = {
            "provider_profile_id": self.id,
            "name": self.name,
            "surname": self.surname,
            "mobile_number": self.mobile_number,
            "provider_profile_picture": self.provider_profile_picture.url
            if self.provider_profile_picture
            else None,
            "gender": self.gender,
            "vehicle": self.vehicle.to_dict() if self.vehicle else None,
            "vehicle_type": self.vehicle_type.type,
            "rating": self.rating,
            "current_latitude": self.current_latitude,
            "current_longitude": self.current_longitude
        }

        if not to_user:
            dict.update(
                {
                    "show_app_rating": self.show_app_rating,
                    "account_status": self.account_status,
                    "last_active_time": format_date(self.last_active_time) if self.last_active_time else None,
                    "status": self.status,
                    "provider_profile_id": self.id,
                    "wallet_balance": self.wallet_balance,
                    "bank_details": {
                        "account_number": self.bank_account_number,
                        "ifsc_code": self.ifsc
                    },
                    "referral_code": self.referral
                }
            )

        if to_admin:
            dict.update(
                {
                    "insurance_expiry_date": self.insurance_expiry_date,
                    "vehicle_license_expiry_date": self.vehicle_license_expiry_date,
                    "driving_license_expiry_date": self.driving_license_expiry_date,
                    "aadhar_number": self.aadhar_number,
                    "total_rides": self.total_rides,
                    "total_ratings": self.total_ratings,
                    "total_earnings": self.total_earnings
                }
            )

        return dict

    def location_info(self):
        """Returns the address of the user
        Returns:
            dict: The address of the user
        """

        return {
            "latitude": self.current_latitude,
            "longitude": self.current_longitude,
            "vehicle_type": self.vehicle_type.type,
        }
