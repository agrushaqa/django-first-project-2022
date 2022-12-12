from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .v1 import api_view

schema_view = get_schema_view(
   openapi.Info(
      title="Askme API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('v1/api/list', api_view.list_questions, name='api_list_questions'),
    path('v1/api/user', api_view.user, name='api_list_user'),
    path('v1/api/search/<str:text>', api_view.search, name='api_search'),
    path('v1/api/question/<int:question_id>', api_view.question_by_id),
    path('v1/api/answers/<int:question_id>', api_view.get_answers_for_question,
         name='api_get_answers_for_question'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
