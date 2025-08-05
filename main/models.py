from django.db import models
from services.models import Service
from areas.models import ServiceArea


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('before_after', 'Before & After'),
        ('emergency', 'Emergency Repairs'),
        ('installation', 'Installations'),
        ('maintenance', 'Maintenance'),
        ('tools', 'Tools & Equipment'),
        ('team', 'Our Team'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    before_image = models.ImageField(upload_to='gallery/before/', blank=True, null=True, help_text="Before image for before/after comparisons")
    after_image = models.ImageField(upload_to='gallery/after/', blank=True, null=True, help_text="After image for before/after comparisons")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='installation')
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='gallery_images',
        help_text="Related service (optional)"
    )
    location = models.ForeignKey(
        ServiceArea, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='gallery_images',
        help_text="Location where work was done (optional)"
    )
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        return self.title
    
    @property
    def is_before_after(self):
        """Check if this is a before/after image"""
        return self.before_image and self.after_image
    
    @property
    def primary_image(self):
        """Get the primary image to display"""
        if self.is_before_after:
            return self.after_image
        return self.image
