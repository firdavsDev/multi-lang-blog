from django.contrib import admin
from django.conf import settings
from django.http import Http404, HttpResponseServerError
from .views import RegisterApi
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
)
#Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from django.conf.urls.i18n import  i18n_patterns

schema_view = get_schema_view(
    openapi.Info(
        title='Artel API',
        description="Artel multi blog API",
        default_version='v1',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email="xackercoder@gmail.com@gmail.com"),
        license=openapi.License(name='Artel License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)


urlpatterns = [
    #post blog
    path('api/', include('api.v1.blog.urls')),
    #home
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    #login and register JWT
    path('api/token/register/', RegisterApi.as_view(), name='api_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #Swagger UI documentation
    path('api/docs/', include_docs_urls(title='Blog APi')),
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
#transaction
urlpatterns += i18n_patterns(
    path('secret/', admin.site.urls),
)
#media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Error handlers
# handler404 = lambda request: HttpResponseServerError('Not found')
handler500 = lambda request: HttpResponseServerError("Internal Server Error")
