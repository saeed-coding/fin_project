from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import F
from .models import FastinnData
from .serializers import GetDataSerializer
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def get_data(request):
    queryset = FastinnData.objects.all()

    # Ordering params from query string
    order_by = request.query_params.get('order_by')  # column name
    order_type = request.query_params.get('order_type', 'asc')  # 'asc' or 'desc'

    if order_by:
        if order_type == 'desc':
            order_by = '-' + order_by
        # Defensive: check if order_by is a valid model field name
        if order_by.lstrip('-') in [f.name for f in FastinnData._meta.get_fields()]:
            queryset = queryset.order_by(order_by)

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 20  # default page size

    result_page = paginator.paginate_queryset(queryset, request)
    serializer = GetDataSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_single_entry(request, pk):
    try:
        entry = FastinnData.objects.get(pk=pk)
    except FastinnData.DoesNotExist:
        return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetDataSerializer(entry)
    return Response(serializer.data)
