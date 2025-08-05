from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from services.models import Service
from areas.models import ServiceArea


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('diy', 'DIY Tips'),
        ('maintenance', 'Maintenance Guides'),
        ('seasonal', 'Seasonal Advice'),
        ('case_study', 'Case Studies'),
        ('news', 'News & Updates'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Brief description for SEO")
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    related_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    related_area = models.ForeignKey(ServiceArea, on_delete=models.SET_NULL, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]