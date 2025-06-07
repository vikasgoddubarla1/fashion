from django.db import models
from users.models import User
import os
# Create your models here.

def product_image_upload_path(instance, filename):
    product = instance.product_id
    # Sanitize product name to avoid file system issues
    product_name = ''.join(e for e in product.name if e.isalnum() or e in (' ', '-', '_')).replace(' ', '_')
    return os.path.join(f'products/{product_name}_{product.id}', filename)


class Category(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    fabric_type = models.CharField(max_length=55, null=True, blank=True)
    color       = models.CharField(max_length=55, null=True, blank=True)
    occasion    = models.CharField(max_length=255, null=True, blank=True)
    care        = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sale_price  = models.IntegerField()
    original_price = models.IntegerField()
    size        = models.CharField(max_length=55, null=True, blank=True)
    saree_length = models.CharField(max_length=55, null=True, blank=True)
    blouse_length = models.CharField(max_length=55, null=True, blank=True)
    number_of_available_items = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class ProductImage(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    image      = models.ImageField(upload_to=product_image_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image of {self.product_id.title}"
    
class ProductReview(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product_id', 'user_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_id.get_full_name} - {self.product_id.title} ({self.rating})"