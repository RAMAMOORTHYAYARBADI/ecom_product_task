from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return {
                'total_count':math.ceil(int(self.page.paginator.count)),
                'totalPageNo': math.ceil(int(self.page.paginator.count)/int(self.request.GET.get('page_size', self.page_size))),
                'perPage': int(self.request.GET.get('page_size', self.page_size)),
                'currentPageNo': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
                "data":data 
        }
        
    
def pagination_class(data,request):
    try:
        page=request.query_params.get('page')
        items=request.query_params.get('item')
        page=int(page)+0

        paginator = Paginator(data,items)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(1)
        
        return users
    except:
        raise Exception
    
def product_pagination(offset,limit,page):
    if page == 1:
        offset = offset
        limit = limit
    if page !=1:
        offset = (int(page) -1) * int(limit)
        limit = (int(limit) * int(page))
    
    return offset,limit