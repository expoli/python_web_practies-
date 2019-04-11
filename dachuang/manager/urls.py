from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.list_all_user_info),
]