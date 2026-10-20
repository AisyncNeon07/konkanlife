from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class StandardPagination(PageNumberPagination):
    """
    Default pagination for all API list views.
    Usage:  GET /api/spots/?page=2&page_size=20
    """
    page_size = 10
    page_size_query_param = 'page_size'  # client can override with ?page_size=N
    max_page_size = 100


class LargeResultsPagination(PageNumberPagination):
    """For endpoints where you need 50 items per page (e.g. admin dashboards)."""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class SmallResultsPagination(LimitOffsetPagination):
    """
    Flexible offset-based pagination for infinite scroll UIs.
    Usage:  GET /api/spots/?limit=5&offset=10
    """
    default_limit = 5
    max_limit = 50
