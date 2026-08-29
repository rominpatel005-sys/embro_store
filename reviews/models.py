from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from products.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    profile_image = models.ImageField(upload_to='reviews/profiles/', blank=True, null=True, help_text="Optional review profile picture override")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star review for {self.product.name}"

    @property
    def rating_percentage(self):
        return int(self.rating) * 20

# Signal helper to update the average product rating
def update_product_average_rating(product):
    # Calculate average rating of approved reviews
    stats = Review.objects.filter(product=product, approved=True).aggregate(avg=Avg('rating'))
    if stats['avg'] is not None:
        product.rating = round(stats['avg'], 2)
    else:
        product.rating = 0.00
    product.save()

@receiver(post_save, sender=Review)
def handle_review_save(sender, instance, **kwargs):
    update_product_average_rating(instance.product)

@receiver(post_delete, sender=Review)
def handle_review_delete(sender, instance, **kwargs):
    update_product_average_rating(instance.product)
