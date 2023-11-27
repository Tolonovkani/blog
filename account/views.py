from django.contrib.auth.models import User
from rest_framework import generics, permissions
from . import serializers

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer

