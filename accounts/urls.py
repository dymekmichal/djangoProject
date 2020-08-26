from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from accounts import views

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('user/<int:pk>', views.UserUpdateView.as_view(), name='permission'),
    path('registration/', views.CreateUserView.as_view(), name='registration'),
]