"""
Global REST Framework exception handler for JustBaddo.
Transforms standard DRF error payloads into a predictable contract:
{
    "status": "error",
    "code": "VALIDATION_ERROR" | "NOT_FOUND" | "UNAUTHORIZED" | etc.,
    "message": "Human-readable summary",
    "errors": { ... field specific details ... }
}
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'status': 'error',
            'code': getattr(exc, 'default_code', 'ERROR').upper(),
            'message': 'An error occurred while processing the request.',
            'errors': response.data
        }

        # Provide friendly summary messages for common HTTP codes
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_data['code'] = 'VALIDATION_ERROR'
            custom_data['message'] = 'One or more request parameters are invalid.'
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_data['code'] = 'UNAUTHENTICATED'
            custom_data['message'] = 'Authentication credentials were not provided or are invalid.'
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_data['code'] = 'PERMISSION_DENIED'
            custom_data['message'] = 'You do not have permission to perform this action.'
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_data['code'] = 'NOT_FOUND'
            custom_data['message'] = 'The requested resource was not found.'
        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            custom_data['code'] = 'RATE_LIMIT_EXCEEDED'
            custom_data['message'] = 'Request rate limit exceeded. Please try again later.'

        response.data = custom_data
        return response

    # Unhandled 500 exceptions
    logger.exception('Unhandled backend exception: %s', str(exc))
    return Response(
        {
            'status': 'error',
            'code': 'SERVER_ERROR',
            'message': 'An unexpected server error occurred.',
            'errors': None
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
