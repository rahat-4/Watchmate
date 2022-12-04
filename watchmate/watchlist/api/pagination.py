from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from watchlist.models import WatchList

class WatchPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'p'
    page_size_query_param = 'y'
    max_page_size = 10
    # last_page_strings = 'end'
    
class WatchLOPagination(LimitOffsetPagination):
    default_limit = 17
    limit_query_param = 'l'
    offset_query_param = 'o'
    max_limit  = 3

class WatchCPagination(CursorPagination):
    page_size = 17
