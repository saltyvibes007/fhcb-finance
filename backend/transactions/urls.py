from django.urls import path
from . import views

urlpatterns = [
    path('orgs/<slug:slug>/transactions/', views.TransactionListCreateView.as_view(), name='transaction-list'),
    path('orgs/<slug:slug>/transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('orgs/<slug:slug>/uploads/', views.UploadCreateView.as_view(), name='upload-create'),
]
