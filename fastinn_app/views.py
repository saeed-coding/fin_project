from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .serializers import GetDataSerializer, CSVUploadSerializer, SingleDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from helper import save_data
from .models import FastinnData
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes



# Create your views here.
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
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
@authentication_classes([])
@permission_classes([AllowAny])
def get_single_entry(request, pk):
    try:
        entry = FastinnData.objects.get(pk=pk)
    except FastinnData.DoesNotExist:
        return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

    # serializer = GetDataSerializer(entry)
    serializer = SingleDataSerializer(entry)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def search_data(request):
    queryset = FastinnData.objects.all()
    search_query = request.query_params.get('heimilisfang')
    if search_query:
        queryset = FastinnData.objects.filter(heimilisfang__istartswith=search_query)
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = GetDataSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


class CSVUploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        csv_file = serializer.validated_data['file']

        # Call the external function
        rows_inserted = save_data(csv_file)

        return Response({
            "message": "CSV uploaded successfully",
            "rows_inserted": rows_inserted
        }, status=status.HTTP_201_CREATED)
