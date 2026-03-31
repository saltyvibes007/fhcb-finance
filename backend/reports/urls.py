from django.urls import path
from . import views

urlpatterns = [
    path('orgs/<slug:slug>/reports/summary/', views.SummaryView.as_view(), name='report-summary'),
    path('orgs/<slug:slug>/reports/monthly/', views.MonthlyView.as_view(), name='report-monthly'),
    path('orgs/<slug:slug>/reports/categories/', views.CategoriesView.as_view(), name='report-categories'),
]
