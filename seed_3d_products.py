import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faction_store.settings')
django.setup()

from products.models import Product, Category

def seed():
    print("Starting seeding process for 3D showcase products...")
    
    # Define source paths and destination paths
    brain_dir = r"C:\Users\romin\.gemini\antigravity-ide\brain\75e23154-59b2-4531-a250-013268829c32"
    media_products_dir = os.path.join("media", "products")
    
    # Create destination directory if it doesn't exist
    os.makedirs(media_products_dir, exist_ok=True)
    
    # 10 Products info matching the uploaded files in brain_dir
    products_data = [
        {
            'name': 'Elephant Embroidered Black T-Shirt',
            'price': 490.00,
            'image_src': 'media__1782018073002.png',
            'image_dst': 'products/elephant_black.png',
            'description': 'A premium black crewneck t-shirt featuring a detailed, colorful embroidered elephant head design on the chest. Crafted from 100% organic cotton for ultimate comfort.',
            'rating': 4.8,
            'brand': 'Embro Premium',
        },
        {
            'name': 'Tropical Palms Brown T-Shirt',
            'price': 350.00,
            'image_src': 'media__1782018088523.png',
            'image_dst': 'products/tropical_palms_brown.png',
            'description': 'Earth-toned brown t-shirt featuring an elegant embroidery of tropical palm trees against a setting sun. Relaxed fit for casual wear.',
            'rating': 4.5,
            'brand': 'Embro Basics',
        },
        {
            'name': 'Marvel Icons Cream T-Shirt',
            'price': 350.00,
            'image_src': 'media__1782018098266.png',
            'image_dst': 'products/marvel_icons_cream.png',
            'description': 'Cream-colored streetwear t-shirt embroidered with minimalist Marvel superhero shield, hammer, fist, mask, helmet, and hourglass icons.',
            'rating': 4.7,
            'brand': 'Embro Street',
        },
        {
            'name': 'Snoopy Chill Maroon T-Shirt',
            'price': 350.00,
            'image_src': 'media__1782018108414.png',
            'image_dst': 'products/snoopy_maroon.png',
            'description': 'Maroon casual t-shirt with a cozy Snoopy embroidery resting above a "CHILL" logo. Perfect for comfortable loungewear.',
            'rating': 4.6,
            'brand': 'Embro Basics',
        },
        {
            'name': 'Royal Enfield Cream T-Shirt',
            'price': 370.00,
            'image_src': 'media__1782018127825.png',
            'image_dst': 'products/royal_enfield_cream.png',
            'description': 'Premium cream t-shirt with a detailed embroidery of a classic Royal Enfield motorcycle. A must-have for riding enthusiasts.',
            'rating': 4.9,
            'brand': 'Embro Premium',
        },
        {
            'name': 'Majestic Stag Black T-Shirt',
            'price': 300.00,
            'image_src': 'media__1782018775030.png',
            'image_dst': 'products/majestic_stag_black.png',
            'description': 'Jet black premium cotton t-shirt with a detailed orange embroidered stag head on the chest. Bold design, lightweight fabric.',
            'rating': 4.4,
            'brand': 'Embro Street',
        },
        {
            'name': 'Marvel Team Cream T-Shirt',
            'price': 350.00,
            'image_src': 'media__1782018775078.png',
            'image_dst': 'products/marvel_team_cream.png',
            'description': 'Alternative cream streetwear t-shirt embroidered with minimalist Marvel superhero character insignia. Premium knit material.',
            'rating': 4.7,
            'brand': 'Embro Street',
        },
        {
            'name': 'Tropical Palms Espresso T-Shirt',
            'price': 350.00,
            'image_src': 'media__1782018775149.png',
            'image_dst': 'products/tropical_palms_espresso.png',
            'description': 'Espresso brown heavy-cotton t-shirt featuring tropical palm tree embroidery. Styled for modern streetwear aesthetics.',
            'rating': 4.5,
            'brand': 'Embro Basics',
        },
        {
            'name': 'Forest Deer Black T-Shirt',
            'price': 350.00,
            'image_src': 'media__1782018775214.png',
            'image_dst': 'products/forest_deer_black.png',
            'description': 'Heavyweight black crewneck t-shirt with a beautifully stitched orange forest deer embroidery. Comfortable and durable.',
            'rating': 4.6,
            'brand': 'Embro Street',
        },
        {
            'name': 'Running Stallion Black T-Shirt',
            'price': 350.00,
            'image_src': 'media__1782018775255.png',
            'image_dst': 'products/running_stallion_black.png',
            'description': 'Stunning black t-shirt featuring a highly detailed, golden-threaded embroidery of a running stallion. Perfect statement piece.',
            'rating': 4.9,
            'brand': 'Embro Premium',
        }
    ]
    
    # Get or create Category for Men's T-Shirts
    category, created = Category.objects.get_or_create(
        name='T-Shirts', 
        gender='MEN',
        defaults={'slug': 'men-t-shirts'}
    )
    if created:
        print("[OK] Created Men's T-Shirts Category.")
    else:
        print("[OK] Found existing Men's T-Shirts Category.")
        
    for p in products_data:
        src_path = os.path.join(brain_dir, p['image_src'])
        dst_path = os.path.join("media", p['image_dst'])
        
        # Copy image file if it exists in source
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"Copied image {p['image_src']} to {dst_path}")
        else:
            print(f"WARNING: Image file {src_path} not found in brain directory.")
            
        # Create or update product in DB
        product, p_created = Product.objects.update_or_create(
            slug=p['name'].lower().replace(" ", "-").replace("'", ""),
            defaults={
                'name': p['name'],
                'price': p['price'],
                'description': p['description'],
                'category': category,
                'brand': p['brand'],
                'stock': 15,
                'rating': p['rating'],
                'image': p['image_dst'],
                'sizes': 'S,M,L,XL',
                'colors': 'Black,White,Cream,Maroon,Brown',
            }
        )
        if p_created:
            print(f"Created product record: {p['name']}")
        else:
            print(f"Updated product record: {p['name']}")
            
    print("Database seeding and asset copies completed successfully!")

if __name__ == "__main__":
    seed()
