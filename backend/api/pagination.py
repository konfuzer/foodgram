from django.conf import settings

from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    page_size = getattr(settings, "PAGINATOR_DEFAULT_SIZE", 10)
    page_size_query_param = "limit"
