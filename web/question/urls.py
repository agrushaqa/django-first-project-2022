from django.urls import include, path

from . import api_view, views

urlpatterns = [
    path('ask/', views.ask_question, name='ask'),
    path('', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('test_auth/', views.test_auth, name='test_auth'),
    path('settings/', views.settings, name='settings'),
    path('likepost/', views.likepost, name='likepost'),
    path('question/', views.list_questions, name='list_all_questions'),
    path('question/<int:question_id>', views.show_question,
         name='show_question'),
    path('query/', views.list_queried_questions,
         name='list_queried_questions'),
    path('tag/', views.list_queried_tags, name='list_questions_by_tag'),
    path('v1/api/list', api_view.list_questions, name='api_list_questions'),
    path('v1/api/user', api_view.user, name='api_list_user'),
    path('v1/api/search/<str:text>', api_view.search, name='api_search'),
    path('v1/api/question/<int:question_id>', api_view.question_by_id),
    path('v1/api/answers/<int:question_id>', api_view.get_answers_for_question,
         name='api_get_answers_for_question')
]
