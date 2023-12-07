from rest_framework import generics, permissions
from category.models import Category
from category import serializers


class CategoryCreateListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()

    # serializer_class = serializers.CategorySerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CategoryListSerializer
        return serializers.CategorySerializers

    def get_permission(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializers

    def get_permission(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
