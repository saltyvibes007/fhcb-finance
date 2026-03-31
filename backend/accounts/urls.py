from django.urls import path
from .views import login_view, OrganizationListCreateView, OrganizationDetailView

app_name = 'accounts'

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('orgs/', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('orgs/<slug:slug>/', OrganizationDetailView.as_view(), name='organization-detail'),
]