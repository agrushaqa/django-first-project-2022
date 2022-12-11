from django.urls import path

from . import views

urlpatterns = [
    path('ask/', views.AskMeListView.as_view(), name='ask'),
    path('', views.HomeRedirectView.as_view(), name='home'),
    path('likepost/', views.LikePostView.as_view(), name='likepost'),
    path('question/', views.QListView.as_view(), name='list_all_questions'),
    path('question/<int:question_id>', views.ShowQuestionView.as_view(),
         name='show_question'),
    path('query/', views.QueryRequestListView.as_view(),
         name='list_queried_questions'),
    path('tag/', views.QueryTagListView.as_view(),
         name='list_questions_by_tag'),
]
