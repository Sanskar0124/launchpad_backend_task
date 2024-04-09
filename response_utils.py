# response_utils.py
from django.http import JsonResponse
from rest_framework import status


def success_response(data=None, msg="Operation successful", status_code=status.HTTP_200_OK):
    return JsonResponse({
        'status': 'success',
        'msg': msg,
        'data': data,
    }, status=status_code)


def not_found_response(msg="Resource not found"):
    return JsonResponse({
        'status': 'error',
        'msg': msg,
        'data': None,
    }, status=status.HTTP_404_NOT_FOUND)


def bad_request_response(apiMsg="", error=None, msg="Internal server error please try again after some time or contact us on: sales@abc.com"):
    return JsonResponse({
        'status': 'error',
        'msg': msg,
        'error': error,
        'data': None,
        'apiMsg': apiMsg,
    }, status=status.HTTP_400_BAD_REQUEST)


def forbidden_response(msg="Forbidden"):
    return JsonResponse({
        'status': 'error',
        'msg': msg,
        'data': None,
    }, status=status.HTTP_403_FORBIDDEN)


def unauthorized_response(msg="Unauthorized"):
    return JsonResponse({
        'status': 'error',
        'msg': msg,
        'data': None,
    }, status=status.HTTP_401_UNAUTHORIZED)


def server_error_response(apiMsg="", error=None, msg="Internal server error please try again after some time or contact us on: sales@abc@gmail.com"):
    return JsonResponse({
        'status': 'error',
        'msg': msg,
        'error': error,
        'data': None,
        'apiMsg': apiMsg,
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ... you can continue adding more custom responses as needed.
