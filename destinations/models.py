from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Destination(models.Model):
    CATEGORY_CHOICES = (
        ('Fort', 'Fort'),
        ('Beach', 'Beach'),
        ('Waterfall', 'Waterfall'),
        ('Temple', 'Temple'),
        ('Viewpoint', 'Viewpoint'),
        ('Food', 'Food Spot'),
        ('Other', 'Other'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)
    location_name = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    main_image = models.ImageField(upload_to='destinations/main/', blank=True, null=True)
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    travel_tips = models.TextField(blank=True)
    entry_fees = models.CharField(max_length=200, blank=True, default='Free')
    timings = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    submitted_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_verified', '-created_at'], name='dest_verified_created_idx'),
            models.Index(fields=['is_verified', 'category'], name='dest_verified_category_idx'),
            models.Index(fields=['category', '-created_at'], name='dest_category_created_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'destination'
            slug = base_slug
            counter = 1
            while Destination.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('destination_detail', kwargs={'slug': self.slug}) if self.slug else '#'

class Gallery(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='destinations/gallery/', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.destination.title}"
