from django.db import models
from django.utils import timezone
from accounts.models import Organization


class Upload(models.Model):
    BANK = 'bank'
    VENMO = 'venmo'
    
    SOURCE_CHOICES = [
        (BANK, 'Bank Statement'),
        (VENMO, 'Venmo Statement'),
    ]
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    source_type = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.organization.name} - {self.get_source_type_display()} - {self.uploaded_at}"
    
    class Meta:
        ordering = ['-uploaded_at']


class Transaction(models.Model):
    CREDIT = 'credit'
    DEBIT = 'debit'
    
    TYPE_CHOICES = [
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    ]
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='transactions')
    source = models.CharField(max_length=50, help_text="Source of the transaction (e.g., TD Bank, Venmo)")
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100, blank=True, null=True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    vendor = models.CharField(max_length=200, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_restricted = models.BooleanField(default=False)
    restricted_fund = models.CharField(max_length=100, blank=True, null=True)
    raw_data = models.JSONField(default=dict, help_text="Original CSV data")
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.organization.name} - {self.description[:50]} - ${self.amount}"
    
    class Meta:
        ordering = ['-date', '-created_at']


class CategoryRule(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='category_rules')
    pattern = models.CharField(max_length=200, help_text="Text pattern to match in transaction description")
    category = models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.organization.name} - {self.pattern} → {self.category}"
    
    class Meta:
        ordering = ['organization', 'pattern']