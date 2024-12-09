from random import randrange
from pytz import timezone
from django.db.models import Q
from requests import request
from disco.models import Ride
from disco.backend.maps import get_address, get_distance_and_duration

from users.models import Locations,  UserProfile
from listeners.producer_ride_request import ProducerRideRequest
from datetime import datetime

producerRideRequested = ProducerRideRequest()


def estimate_price(distance_km, vehicle_type):
    """
    Estimate the price of a ride based on distance and vehicle type.

    Args:
        distance_km (float): The distance of the ride in kilometers.
        vehicle_type (str): The type of vehicle (e.g., 'Sedan', 'SUV', 'Bike').

    Returns:
        dict: Estimated fare breakdown including base fare, distance rate, and total fare.
    """
    # Define base fares and per-km rates by vehicle type
    pricing = {
        "sedan": {"base_fare": 5.00, "per_km_rate": 2.00},
        "suv": {"base_fare": 7.00, "per_km_rate": 2.50},
        "bike": {"base_fare": 3.00, "per_km_rate": 1.50},
    }

    if vehicle_type not in pricing:
        raise ValueError(f"Invalid vehicle type: {
                         vehicle_type}. Supported types are: {list(pricing.keys())}")

    base_fare = pricing[vehicle_type]["base_fare"]
    per_km_rate = pricing[vehicle_type]["per_km_rate"]

    # Calculate the total fare
    distance_fare = distance_km * per_km_rate
    total_fare = base_fare + distance_fare

    # Return a breakdown of the fare
    return {
        "base_fare": round(base_fare, 2),
        "distance_fare": round(distance_fare, 2),
        "total_fare": round(total_fare, 2),
    }


def create_ride_request(
    user_profile_id,
    source_location,
    destination_location,
    vehicle_type,
):

    distance_and_duration = get_distance_and_duration(
        source_location.latitude,
        source_location.longitude,
        destination_location.latitude,
        destination_location.longitude,
    )
    distance = distance_and_duration
    duration = distance_and_duration / 20

    estimated_fare = estimate_price(distance, vehicle_type)
    print("distance_and_duration", estimated_fare)
    user = UserProfile.objects.get(id=user_profile_id)

    ride_request = Ride.objects.create(
        user=user,
        source_location=source_location,
        destination_location=destination_location,
        created_at=datetime.now(),
        distance=distance,
        estimated_fare=estimated_fare['total_fare'],
        ride_status="Waiting",
        estimated_travel_time_in_mins=duration,
        vehicle_type=vehicle_type,
    )

    return ride_request.to_dict()


def update_ride_status_helper(
    provider_profile_id, ride_id, status, current_latitude, current_longitude, otp=None
):

    try:

        ride = Ride.objects.get(
            id=ride_id, provider_profile_id=provider_profile_id)

        if status == "reaching_user":
            if ride.status in ["driver_assigned", "reaching_user"]:
                ride.status = status
                ride.save()
                notify_user_about_ride_status(ride)
                return ride.to_dict()
            else:
                return {
                    "error": "Invalid status",
                    "status": ride.status,
                    "allowed_status": "reaching_user",
                }
        elif status == "waiting_for_user":
            if ride.status in ["reaching_user", "driver_assigned"]:
                ride.status = status
                ride.arrived_at = datetime.now(tz=timezone("Asia/Kolkata"))
                ride.save()
                notify_user_about_ride_status(ride)
                # state = Scheduler.state
                # if Scheduler.state != 1:
                #     Scheduler.resume()
                # Scheduler.add_job(
                #     auto_cancel_alert,
                #     trigger="date",
                #     run_date= datetime.now() + timedelta(minutes=10),
                #     args=[
                #         ride.id
                #     ],
                #     id= str(ride.user_profile.id)+"_ACA_" + str(ride.id),
                #     replace_existing=True,
                # )
                # if not state != 1:
                #     Scheduler.pause()

                return ride.to_dict()
            else:
                return {
                    "error": "Invalid status",
                    "status": ride.status,
                    "allowed_status": "waiting_for_user",
                }
        elif status == "started":
            if ride.status in ["waiting_for_user", "reaching_user", "airport_ride"]:

                if ride.user_profile.otp == otp:
                    ride.status = status
                    ride.started_at = datetime.now(tz=timezone("Asia/Kolkata"))
                    ride.waiting_time_in_minutes = (
                        ride.started_at - ride.arrived_at
                    ).total_seconds() / 60
                    ride.save()

                    notify_user_about_ride_status(ride)

                    RidePayments.objects.create(
                        ride=ride,
                        amount=ride.estimated_fare.get("total_price"),
                        transaction_type="credit",
                        transaction_mode=ride.payment_mode,
                        transaction_status="not_initiated",
                        transaction_id="TRNX" +
                        str(datetime.now().timestamp()),
                        time=datetime.now(),
                    )

                    ride.user_profile.total_rides += 1
                    ride.user_profile.save()

                    ride.provider_profile.total_rides += 1
                    ride.provider_profile.save()

                    if ride.provider_profile.referred_by and ride.provider_profile.total_rides == 1:
                        update_provider_referral_data(ride.provider_profile)
                    elif ride.provider_profile.total_rides == 5:
                        pass

                    ProviderIncentiveLog.create_incentive_log(
                        provider_profile=ride.provider_profile
                    )
                    ProviderIncentiveLog.update_progress(
                        provider_profile=ride.provider_profile
                    )

                    return ride.to_dict()
                else:
                    return {
                        "error": "Invalid otp",
                        "status": ride.status,
                        "allowed_status": "started",
                    }
            else:
                return {
                    "error": "Invalid status",
                    "status": ride.status,
                    "allowed_status": "started",
                }
        elif status == "completed":
            if ride.status in ["started"]:
                complete_ride(ride, current_latitude, current_longitude)
                return ride.to_dict()
            elif ride.status in ["completed"]:
                raise RideAlreadyCompleted
            else:
                return {"error": "Invalid status"}

        else:
            return {"error": "Invalid status", "status": ride.status}

    except Ride.DoesNotExist:
        raise RideDoesNotExist


def accept_ride_request(
    ride_id,
    provider_profile_id,
):

    ride_request = Ride.objects.get(id=ride_id)

    if ride_request.ride_status in [
        "Waiting",
        "Completed",
        "In Progress"
    ]:
        provider = UserProfile.objects.get(id=provider_profile_id)

        # update provider and status
        ride_request.update_provider(provider)
        ride_request.update_status("In Progress")

        ride_request = Ride.objects.get(id=ride_id)

        print(ride_request)

        producerRideRequested.publish(
            "ride_requested", ride_request.to_dict())

        return ride_request.to_dict()
    else:
        return {
            "error": "Operation not allowed in present status",
            "status": ride_request.ride_status,
        }


def complete_ride_request(ride_id):

    ride_request = Ride.objects.get(id=ride_id)

    # update provider and status
    ride_request.completed()
    print(ride_request)

    producerRideRequested.publish(
        "ride_completed", ride_request.to_dict())

    return ride_request.to_dict()


def get_estimated_fares(
    source_latitude,
    source_longitude,
    destination_latitude,
    destination_longitude,
    vehicle_type,
):

    distance_and_duration = get_distance_and_duration(
        source_latitude, source_longitude, destination_latitude, destination_longitude
    )

    distance = distance_and_duration
    duration = distance_and_duration / 20

    estimated_fare = estimate_price(distance, vehicle_type)

    return {"fares": estimated_fare, "distance": distance, "duration": duration}
