from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination

class Review(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    author_name = models.CharField(max_length=100, blank=True) # For non-logged in users if allowed, or just display name
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['destination', '-created_at'], name='rev_dest_created_idx'),
            models.Index(fields=['user', '-created_at'], name='rev_user_created_idx'),
        ]

    def __str__(self):
        return f"{self.rating} stars for {self.destination.title}"
