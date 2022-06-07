from django.db.models import Count, F, Q
from django.utils.timezone import now
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.v1.blog.permissions import IsAuthorOrReadOnly

from .models import Blog, PostLanguage
from .serializers import (BlogDetailSerializer, BlogSerializer,
                          PostDetailLanguageSerializer)
from .utils import clean_query_data


class BlogAPIView(ListCreateAPIView):
    queryset = Blog.cus_objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        queryset = super().get_queryset()
        queries = clean_query_data(self.request.query_params)
        if search := queries.get("search", None):
            queryset = queryset.filter(Q(lang_post__title__icontains=search) | Q(lang_post__content__icontains=search)  |  Q(title__icontains=search) | Q(content__icontains=search))
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogDetailAPIView(RetrieveUpdateDestroyAPIView):
    # queryset = Blog.objects.filter( Q(active=True) & Q(published_at__lte=now()) )
    serializer_class = BlogDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'pk'




    def get_queryset(self):
        queryset = (
            Blog.objects.all()
            .annotate(num_categories=Count("categories"))
            .order_by("-categories")
        )
        queryset.filter(pk=self.kwargs.get("pk")).update(
            views_count=F("views_count") + 1
        )
        queries = clean_query_data(self.request.query_params)
        lang = queries.get("lang", None)
        #TODO add lang to queryset (bu yerda blog detailning tilariga qoshim kerak edi. )
        if lang == "uz":
            queryset = queryset.filter(Q(lang_post__language__code = "uz"))
        elif lang == "ru":
            queryset = queryset.filter(language__code="ru")

        return queryset
