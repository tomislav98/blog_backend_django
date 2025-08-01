from rest_framework.pagination import PageNumberPagination

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5  # number of items per page
    page_size_query_param = 'page_size'  # optional: allows client to override with ?page_size=...
    max_page_size = 20  # optional: max limit client can set
