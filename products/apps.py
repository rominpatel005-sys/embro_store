from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_categories(sender, **kwargs):
    from products.models import Category
    
    categories_data = [
        # Men Categories
        ('T-Shirts', 'MEN'),
        ('Shirts', 'MEN'),
        ('Hoodies', 'MEN'),
        ('Jackets', 'MEN'),
        ('Jeans', 'MEN'),
        # Women Categories
        ('Tops', 'WOMEN'),
        ('Dresses', 'WOMEN'),
        ('Hoodies', 'WOMEN'),
        ('Jackets', 'WOMEN'),
        ('Jeans', 'WOMEN'),
    ]
    
    for name, gender in categories_data:
        if not Category.objects.filter(name=name, gender=gender).exists():
            Category.objects.create(name=name, gender=gender)
            print(f"Created initial category: {gender} - {name}")

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        post_migrate.connect(create_default_categories, sender=self)
