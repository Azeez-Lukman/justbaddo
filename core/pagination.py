"""
Custom pagination classes for JustBaddo REST APIs.
Provides standard metadata: count, page, page_size, total_pages, next, previous.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = self.page.paginator.num_pages if self.page.paginator else 1
        return Response({
            'status': 'success',
            'pagination': {
                'total_count': self.page.paginator.count,
                'total_pages': total_pages,
                'current_page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'next_url': self.get_next_link(),
                'previous_url': self.get_previous_link(),
            },
            'data': data
        })
