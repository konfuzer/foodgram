from rest_framework.pagination import PageNumberPagination

from main_app.settings import PAGINATOR_DEFAULT_SIZE


class PageLimitPagination(PageNumberPagination):
    page_size = PAGINATOR_DEFAULT_SIZE
    page_size_query_param = "limit"
