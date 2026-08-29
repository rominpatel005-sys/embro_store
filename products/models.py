from django.db import models
from django.utils.text import slugify

GENDER_CHOICES = (
    ('MEN', 'Men'),
    ('WOMEN', 'Women'),
    ('UNISEX', 'Unisex'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='UNISEX')
    
    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ('name', 'gender')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.gender}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_gender_display()} - {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=100, default='Embro')
    stock = models.IntegerField(default=10)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='products/', default='products/default.jpg')
    sizes = models.CharField(max_length=100, default='S,M,L,XL', help_text="Comma-separated sizes (e.g., S,M,L,XL)")
    colors = models.CharField(max_length=100, default='Black,White,Grey', help_text="Comma-separated colors (e.g., Black,White,Grey)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # If slug already exists, append unique counter
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def get_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    @property
    def is_discounted(self):
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def get_discount_percentage(self):
        if self.is_discounted:
            diff = self.price - self.discount_price
            return int((diff / self.price) * 100)
        return 0

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def rating_percentage(self):
        return float(self.rating) * 20

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='products/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"
