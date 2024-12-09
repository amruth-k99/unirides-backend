from django.urls import path
from disco.apis.ride_request import (
    complete_ride,
    get_all_rides,
    get_ride_requests,
    accept_ride_api,
    create_ride_request_api,
    get_estimated_fare,
    get_ride_details,
)

urlpatterns = [
    # params = [user_id]
    path("list/<user_id>/", get_all_rides),
    path("estimate/", get_estimated_fare),

    path("requests/", get_ride_requests),
    path("create/", create_ride_request_api),
    path("status/<ride_id>/", get_ride_details),
    path("accept-ride/", accept_ride_api),
    path("complete-ride/", complete_ride),
]
