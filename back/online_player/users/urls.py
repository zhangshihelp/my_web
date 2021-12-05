from django.urls import path

from .views import UserManage

urlpatterns = [
    path('all', UserManage.as_view()),
]
