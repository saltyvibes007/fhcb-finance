from django.urls import path
from . import views

urlpatterns = [
    path('orgs/<slug:slug>/chat/', views.ChatView.as_view(), name='chat'),
]
