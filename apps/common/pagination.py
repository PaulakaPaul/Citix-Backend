from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    page_size = settings.DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data,
            'page_size': self.get_page_size(self.request),
            'pages': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
        })
