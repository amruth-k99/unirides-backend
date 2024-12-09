from config.helper_functions import paginate
from disco.models import Ride, RideSchedule


def get_rides(page_size, page_number, sort_by, sort_order, filters):
    """
    Returns a list of rides.
    """
    rides = Ride.objects.all()

    if filters:
        if "user_profile_id" in filters:
            rides = rides.filter(user_profile_id=filters["user_profile_id"])
        if "provider_profile_id" in filters:
            rides = rides.filter(provider_profile_id=filters["provider_profile_id"])
        if "status" in filters:
            if filters["status"] == "searching":
                rides = rides.filter(status="assigning_driver")
            elif filters["status"] == "in_progress":
                rides = rides.filter(
                    status__in = [ 
                        "reaching_user",
                        "waiting_for_user",
                        "started",
                        "driver_assigned"
                    ]
                )
            elif filters["status"] == "completed":
                rides = rides.filter(status="completed")
            else:
                rides = rides.filter(status= "cancelled")
        
        if "ride_id" in filters:
            rides = rides.filter(id=filters["ride_id"])

    if sort_by == "created_at":
        if sort_order == "asc":
            rides = rides.order_by("created_at")
        else:
            rides = rides.order_by("-created_at")

    total_count = rides.count()

    rides, total_pages, page_number = paginate(rides, page_number, page_size)

    return {
        "page_number": page_number,
        "total_pages": total_pages,
        "total_count": total_count,
        "data": [ride.to_dict(summary_only=True) for ride in rides],
    }


def get_scheduled_rides_helper(page_size, page_number, sort_by, sort_order, filters):
    
    scheduled_rides = RideSchedule.objects.all()
    
    if filters:
        if filter.get("user_profile_id"):
            scheduled_rides = scheduled_rides.filter(user_profile_id=filters["user_profile_id"])
        if filters.get("status"):
            scheduled_rides = scheduled_rides.filter(status=filters["status"])
        if filters.get("scheduled_ride_id"):
            scheduled_rides = scheduled_rides.filter(id=filters["scheduled_ride_id"])
        if filters.get("ride_id"):
            scheduled_rides = scheduled_rides.filter(ride_id=filters["ride_id"])
        
    
    if sort_by == "created_at":
        if sort_order == "asc":
            scheduled_rides = scheduled_rides.order_by("created_at")
        else:
            scheduled_rides = scheduled_rides.order_by("-created_at")
    total_count = scheduled_rides.count()
    scheduled_rides, total_pages, page_number = paginate(scheduled_rides, page_number, page_size)
    
    return {
        "page_number": page_number,
        "total_pages": total_pages,
        "total_count": total_count,
        "data": [scheduled_ride.to_dict() for scheduled_ride in scheduled_rides]
    }
