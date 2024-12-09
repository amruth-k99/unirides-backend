from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from config.request_param_validators import get_request_body
from users.models import UserProfile, Locations
from django.forms.models import model_to_dict
from listeners.producer_user_created import ProducerUserCreated

producerUserCreated = ProducerUserCreated()


@csrf_exempt
@require_http_methods(["GET"])
def list_users(request):
    try:
        user_profile = UserProfile.objects.all()

        # list all users
        return JsonResponse({'status': "success", 'data': [ride.to_dict() for ride in user_profile]})
    except ValueError:
        return JsonResponse({'status': "error", 'message': "Invalid user_id"})


@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    try:
        request_body = get_request_body(request)
        user_profile = UserProfile.objects.create(
            name=request_body.get("name"),
            surname=request_body.get("surname"),
            mobile_number=request_body.get("mobile_number"),
            email=request_body.get("email"),
        )
        producerUserCreated.publish(
            "user_created_method", user_profile.to_dict())
        return JsonResponse({'status': "success", 'data': user_profile.to_dict()})
    except Exception as e:
        return JsonResponse({'status': "error", 'message': str(e)})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_users(request):
    try:
        request_body = get_request_body(request)
        # list all users
        rides = UserProfile.objects.all().delete()
        return JsonResponse({'status': "success", 'data': "Deleted"})
    except ValueError:
        return JsonResponse({'status': "error", 'message': "Invalid user_id"})
