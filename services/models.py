from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from core.constants import RATING_CHOICES, SERVICE_ICONS


class Service(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    price_range = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, choices=SERVICE_ICONS, default='wrench')
    is_emergency = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service_detail', kwargs={'pk': self.pk})


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=200, blank=True)
    location = models.ForeignKey(
        'areas.ServiceArea', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='testimonials'
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='testimonials'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    is_featured = models.BooleanField(default=False, db_index=True)
    is_approved = models.BooleanField(default=True, db_index=True)
    is_verified = models.BooleanField(default=False, help_text="Verified customer review")
    google_review_url = models.URLField(blank=True, help_text="Link to Google review")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"
    
    @property
    def star_range(self):
        """Return range for template star display"""
        return range(1, 6)
    
    @property
    def filled_stars(self):
        """Return range of filled stars"""
        return range(1, self.rating + 1)
    
    @property
    def empty_stars(self):
        """Return range of empty stars"""
        return range(self.rating + 1, 6)


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.IntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    category = models.CharField(max_length=50, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question