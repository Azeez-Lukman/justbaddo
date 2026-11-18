"""
Standardized API Response Helpers for JustBaddo.
Maintains a clean and uniform envelope for all successful and error responses.
"""

from rest_framework.response import Response
from rest_framework import status

def api_success(data=None, message="Success", meta=None, status_code=status.HTTP_200_OK):
    """
    Standard successful API response.
    """
    payload = {
        'status': 'success',
        'message': message,
        'data': data if data is not None else {}
    }
    if meta is not None:
        payload['meta'] = meta
    return Response(payload, status=status_code)

def api_error(message="An error occurred", code="BAD_REQUEST", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Standard error API response.
    """
    payload = {
        'status': 'error',
        'code': code,
        'message': message,
        'errors': errors or {}
    }
    return Response(payload, status=status_code)
