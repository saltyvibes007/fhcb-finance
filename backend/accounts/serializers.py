from rest_framework import serializers
from django.conf import settings
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'created_at', 'password']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        organization = Organization(**validated_data)
        if password:
            organization.set_password(password)
        organization.save()
        return organization
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    slug = serializers.CharField()
    password = serializers.CharField()


class OrganizationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'created_at']