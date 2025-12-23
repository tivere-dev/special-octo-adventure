from django.db import models
from django.conf import settings


class Business(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('GBP', 'British Pound'),
        ('EUR', 'Euro'),
        ('NGN', 'Nigerian Naira'),
        ('KES', 'Kenyan Shilling'),
        ('ZAR', 'South African Rand'),
        ('GHS', 'Ghanaian Cedi'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business')
    business_name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    business_logo = models.ImageField(upload_to='business_logos/', null=True, blank=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return f"{self.business_name} ({self.user.email})"
