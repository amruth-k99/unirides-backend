from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from config.request_param_validators import get_request_body
from disco.models import Ride
from users.models import UserProfile, Locations
from disco.backend.dispatch import (
    create_ride_request,
    get_estimated_fares,
    accept_ride_request,
    complete_ride_request
)
from datetime import datetime, timedelta


@csrf_exempt
@require_http_methods(["POST"])
def create_ride_request_api(request):

    request_body = get_request_body(request)

    user_profile_id = request_body.get("user_profile_id")
    source_latitude = request_body.get("source_latitude")
    source_longitude = request_body.get("source_longitude")
    destination_latitude = request_body.get("destination_latitude")
    destination_longitude = request_body.get("destination_longitude")
    source_address = request_body.get("source_address")
    destination_address = request_body.get("destination_address")
    vehicle_type = request_body.get("vehicle_type")
    payment_type = request_body.get("payment_type")

    vehicle_type = 'sedan'

    source_location = Locations.add_location(
        source_latitude,
        source_longitude,
        source_address,
        user_profile_id=user_profile_id,
    )

    destination_location = Locations.add_location(
        destination_latitude,
        destination_longitude,
        destination_address,
        user_profile_id=user_profile_id,
    )
    response = create_ride_request(
        user_profile_id,
        source_location,
        destination_location,
        vehicle_type,
    )
    print("source_location: ", response)

    return JsonResponse(response)


@ csrf_exempt
@ require_http_methods(["POST"])
def get_nearby_riders(request):

    request_body = get_request_body(request)

    user_profile = request.user_profile

    user_profile.current_latitude = request_body.get("current_latitude")
    user_profile.current_longitude = request_body.get("current_longitude")
    user_profile.last_active_time = datetime.now()

    user_profile.save()

    return JsonResponse(
        {
            "nearby_riders": get_riders(
                user_profile.current_latitude,
                user_profile.current_longitude,
                radius=2000,
            )
        }
    )


@ csrf_exempt
@ require_http_methods(["POST"])
def get_estimated_fare(request):

    request_body = get_request_body(request)

    source_latitude = request_body.get("source_latitude")
    source_longitude = request_body.get("source_longitude")
    destination_latitude = request_body.get("destination_latitude")
    destination_longitude = request_body.get("destination_longitude")
    vehicle_type = request_body.get("vehicle_type")

    return JsonResponse(
        get_estimated_fares(
            source_latitude,
            source_longitude,
            destination_latitude,
            destination_longitude,
            vehicle_type,
        )
    )


@ csrf_exempt
@ require_http_methods(["GET"])
def get_ride_details(request, ride_id):
    try:
        ride_id = int(ride_id)
        print("ride_id: ", ride_id)
        ride = Ride.objects.get(id=ride_id)
        return JsonResponse({'status': "success", 'data': ride.to_dict()})
    except ValueError:
        return JsonResponse({'status': "error", 'message': "Invalid ride_id"})


@ csrf_exempt
@ require_http_methods(["GET"])
def get_all_rides(request, user_id):
    try:
        user_id = int(user_id)
        print("user_id: ", user_id)
        rides = Ride.objects.filter(user_id=user_id)
        return JsonResponse({'status': "success", 'data': [ride.to_dict() for ride in rides]})
    except ValueError:
        return JsonResponse({'status': "error", 'message': "Invalid ride_id"})


@ csrf_exempt
@ require_http_methods(["GET"])
def get_ride_requests(request):
    try:
        rides = Ride.objects.filter(ride_status="Waiting")
        return JsonResponse({'status': "success", 'data': [ride.to_dict() for ride in rides]})
    except ValueError:
        return JsonResponse({'status': "error", 'message': "Invalid ride_id"})


@ csrf_exempt
@ require_http_methods(["POST"])
def accept_ride_api(request):
    try:
        body = get_request_body(request)
        ride_id = body.get("ride_id")
        provider_id = body.get("provider_id")
        print("Provider with id: ", provider_id,
              " accepted the ride: ", ride_id)
        ride = accept_ride_request(ride_id, provider_id)
        return JsonResponse({'status': "success", 'data': ride})
    except ValueError:
        return JsonResponse({'status': "error", 'message': "Invalid ride_id"})


@ csrf_exempt
@ require_http_methods(["POST"])
def complete_ride(request):
    try:
        body = get_request_body(request)
        ride_id = body.get("ride_id")
        ride = complete_ride_request(ride_id)
        return JsonResponse({'status': "success", 'data': ride})
    except ValueError:
        return JsonResponse({'status': "error", 'message': "Invalid ride_id"})
