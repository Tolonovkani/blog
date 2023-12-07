from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from comment.serializers import CommentSerializer
from like.models import Favorite
from like.serializers import LikeUserSerializer
from post import serializers
from post.models import Post
from post.persmissions import IsOwner, IsOwnerOrAdmin



class StandardResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'



class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandardResultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'body')
    filterset_fields = ('owner', 'category')
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCretaUpdateSerializer
        return serializers.PostDetailSerializer


    def get_permissions(self):
        #удалять может только автор поста или одмины
        if self.action == 'destroy':
            return [IsOwnerOrAdmin(),]
        #обновлять может только автор паста
        elif self.action in ('update', 'partial_update'):
            return [IsOwner(),]
        # просматривать могут все(list, retrieve)
        #
        return [permissions.IsAuthenticatedOrReadOnly(), ]

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        # post = Post.objects.get(id=pk)
        post = self.get_object()
        comments = post.comments.all()
        serializers = CommentSerializer(instance=comments, many=True)
        return Response(serializers.data, status=200)

    @action(['GET'], detail=True)
    def likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializers = LikeUserSerializer(instance=likes, many=True)
        return Response(serializers.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        post = self.get_object()
        user = request.user
        favorite = user.favorites.filter(post=post)

        if request.method == 'POST':
            if favorite.exists():
                return Response({'msg': 'Already in Favorites!'}, status=400)
            Favorite.objects.create(owner=user, post=post)
            return Response({'msg': 'Added to Favorites!'}, status=201)


        if favorite.exists():
            favorite.delete()
            return Response({'msg': 'Deleted from Favorite!'}, status=204)
        return Response({'msg': 'Post Not Found in Favorites!'}, status=404)




class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostListSerializer
        return serializers.PostCretaUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()


    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return serializers.PostCretaUpdateSerializer
        return serializers.PostDetailSerializer


    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [permissions.IsAuthenticated(), IsOwner()]

        elif self.request.method == 'DELETE':
            return [IsOwnerOrAdmin()]
        return [permissions.AllowAny()]


