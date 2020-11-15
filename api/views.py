from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from .models import Profile, Product, Order
from .serializers import ProfileSerializer, UserSerializer
from rest_framework import status
from datetime import datetime


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def users(request, pk=None):
    """
    Return all users or user by id
    """
    if pk is None:
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    else:
        profile = Profile.objects.get(id=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def users_filter(request):
    """
    Filtering users with date_joined parameter
    """
    min_date = datetime.strptime(request.POST['min_date'], '%d-%m-%Y').strftime('%Y-%m-%d %H:%M:%S')
    max_date = datetime.strptime(request.POST['max_date'], '%d-%m-%Y').strftime('%Y-%m-%d %H:%M:%S')
    profiles = Profile.objects.filter(user__date_joined__range=(min_date, max_date))
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    """
    User registration
    """
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    profile = Profile.objects.get(user=user)
    profile.date_of_birth = request.data['date_of_birth']
    profile.save()
    return Response(status.HTTP_201_CREATED)
