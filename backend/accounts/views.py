from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Organization
from .serializers import (
    OrganizationSerializer, 
    LoginSerializer, 
    OrganizationDetailSerializer
)


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access certain views.
    """
    def has_permission(self, request, view):
        # Check if admin password is provided in headers
        admin_password = request.META.get('HTTP_X_ADMIN_PASSWORD')
        return admin_password == settings.ADMIN_PASSWORD


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Authenticate organization with slug and password, return JWT token
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        slug = serializer.validated_data['slug']
        password = serializer.validated_data['password']
        
        try:
            organization = Organization.objects.get(slug=slug)
            if organization.check_password(password):
                # Create JWT token with organization info
                refresh = RefreshToken()
                refresh['org_id'] = organization.id
                refresh['org_slug'] = organization.slug
                
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'organization': OrganizationDetailSerializer(organization).data
                })
            else:
                return Response(
                    {'error': 'Invalid credentials'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Organization.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationListCreateView(generics.ListCreateAPIView):
    """
    List all organizations or create a new one (admin only)
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminUser]


class OrganizationDetailView(generics.RetrieveUpdateAPIView):
    """
    Get or update organization details
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationDetailSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]  # We'll add org-specific auth later
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OrganizationSerializer
        return OrganizationDetailSerializer