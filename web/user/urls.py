from django.urls import include, path

from . import views

urlpatterns = [
    path('signup/', views.SignupListView.as_view(), name='signup'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('', include('django.contrib.auth.urls')),
]
