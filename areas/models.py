from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from core.constants import RATING_CHOICES, PLATFORM_CHOICES


class ServiceArea(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    phone = PhoneNumberField(region='CA')
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100, db_index=True, default='Toronto')
    province = models.CharField(max_length=50, default='Ontario')
    postal_code = models.CharField(max_length=10, blank=True)
    map_embed = models.TextField(blank=True, help_text="Google Maps embed code")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Service Area'
        verbose_name_plural = 'Service Areas'



    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('location_home', kwargs={'location_slug': slugify(self.name)})


class Review(models.Model):
    customer_name = models.CharField(max_length=100)
    platform = models.CharField(
        max_length=20, 
        choices=PLATFORM_CHOICES,
        db_index=True
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    service_area = models.ForeignKey(
        ServiceArea, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviews'
    )
    review_url = models.URLField(blank=True, help_text="Link to original review")
    date = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_verified = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars ({self.get_platform_display()})"


class TrustBadge(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    url = models.URLField(blank=True, help_text="Link to certification or badge")
    order = models.IntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Trust Badge'
        verbose_name_plural = 'Trust Badges'

    def __str__(self):
        return self.name