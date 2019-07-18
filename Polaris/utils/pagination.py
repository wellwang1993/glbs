from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = "size" 
    def get_paginated_response(self, data):
        return Response({
            'code': 1,
            'msg': {
                'current_page': self.page.number,
                'count': self.page.paginator.count,
                'results': data
            }
        })
