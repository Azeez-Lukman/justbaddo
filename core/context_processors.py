"""
Global template context processors for JustBaddo.
Provides global metadata, brand disclaimers, and version information.
"""

from django.conf import settings

def site_context(request):
    return {
        'PLATFORM_NAME': getattr(settings, 'JUSTBADDO_PLATFORM_NAME', 'JustBaddo'),
        'PLATFORM_DISCLAIMER': getattr(
            settings,
            'JUSTBADDO_AFFILIATION_DISCLAIMER',
            'Independent music and fan community platform dedicated to Olamide Baddo.'
        ),
        'API_VERSION': 'v1',
    }
