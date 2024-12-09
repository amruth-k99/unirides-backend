import json
from django.http import HttpResponseBadRequest, HttpResponse
from functools import wraps, WRAPPER_ASSIGNMENTS
from functools import wraps
from requests_toolbelt.multipart import decoder



def get_request_body(request):
    """Decodes the body sent in the request from the API

    Args:
        request (object): WSGIRequest object

    Returns:
        [dict]: The dict of the body sent in the request
    """
    content_type = request.META.get("CONTENT_TYPE")

    if content_type.split(";")[0] == "multipart/form-data":
        multipart_string = request.body
        request_body = {}
        for part in decoder.MultipartDecoder(multipart_string, content_type).parts:
            request_body[
                part.headers.get(b"Content-Disposition")
                .decode("utf-8", errors="ignore")
                .split("name=", 1)[1]
                .strip('"')
            ] = part.content.decode("utf-8", errors="ignore")
        return request_body
    else:
        body_unicode = request.body.decode("utf-8", errors="ignore")
        if body_unicode:
            return json.loads(body_unicode)
        else:
            return {}


def require_post_params(params):
    def decorator(func):
        @wraps(func, assigned=WRAPPER_ASSIGNMENTS)
        def inner(request, *args, **kwargs):
            for param in params:
                if param not in request.POST:
                    return HttpResponseBadRequest(
                        content=str(param) + " is required to process this request"
                    )
            return func(request, *args, **kwargs)

        return inner

    return decorator


def require_get_params(params):
    def decorator(func):
        @wraps(func, assigned=WRAPPER_ASSIGNMENTS)
        def inner(request, *args, **kwargs):
            for param in params:
                if param not in request.GET:
                    return HttpResponse()
            return func(request, *args, **kwargs)

        return inner

    return decorator
