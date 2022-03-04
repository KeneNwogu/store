from rest_framework.pagination import PageNumberPagination


class SmallResultsPagination(PageNumberPagination):
    page_size = 30
    page_query_param = 'page'
    max_page_size = 50
