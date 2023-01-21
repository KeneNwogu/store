from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SmallResultsPagination(PageNumberPagination):
    page_size = 9
    page_query_param = 'page'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })
