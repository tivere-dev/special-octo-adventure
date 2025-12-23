from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Business
from .serializers import BusinessSerializer, BusinessSetupSerializer, BusinessUpdateSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_business(request):
    serializer = BusinessSetupSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        business = serializer.save()
        business_serializer = BusinessSerializer(business)
        
        return Response({
            'business': business_serializer.data,
            'message': 'Business setup successful'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business(request):
    try:
        business = request.user.business
        serializer = BusinessSerializer(business)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Business.DoesNotExist:
        return Response({
            'error': True,
            'message': 'Business not found. Please complete business setup.'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_business(request):
    try:
        business = request.user.business
        serializer = BusinessUpdateSerializer(business, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'business': serializer.data,
                'message': 'Business updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Business.DoesNotExist:
        return Response({
            'error': True,
            'message': 'Business not found. Please complete business setup first.'
        }, status=status.HTTP_404_NOT_FOUND)
