from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrganizationListCreateView.as_view(), name='org-list'),
    path('<slug:slug>/', views.OrganizationDetailView.as_view(), name='org-detail'),
]
