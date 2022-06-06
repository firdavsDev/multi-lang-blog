from django.utils.timezone import now
from django.db.models import Q
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    )
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.v1.blog.permissions import  IsAuthorOrReadOnly

from .models import Blog
from .serializers import (
    BlogSerializer,
    BlogDetailSerializer,
    )

class BlogAPIView(ListCreateAPIView):
    queryset = Blog.objects.filter( Q(active=True) & Q(published_at__lte=now()))
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.filter( Q(active=True) & Q(published_at__lte=now()) )
    serializer_class = BlogDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'
