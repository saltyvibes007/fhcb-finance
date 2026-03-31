from rest_framework import serializers
from .models import Transaction, Upload, CategoryRule


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'source', 'date', 'description', 'amount', 'type',
            'category', 'subcategory', 'vendor', 'note', 'is_restricted',
            'restricted_fund', 'raw_data', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['id', 'file', 'source_type', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class CategoryRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRule
        fields = ['id', 'pattern', 'category', 'vendor_name', 'created_at']
        read_only_fields = ['id', 'created_at']