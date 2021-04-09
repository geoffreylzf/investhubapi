from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response

DEFAULT_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'size': self.page_size,
            'pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
