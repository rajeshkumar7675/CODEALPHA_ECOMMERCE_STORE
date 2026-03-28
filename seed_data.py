import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin / admin123")

products = [
    {
        "name": "Premium Wireless Headphones",
        "description": "Experience high-fidelity audio with active noise cancellation and 30-hour battery life. Designed for comfort and immersive sound.",
        "price": 299.99,
        "stock": 50
    },
    {
        "name": "Mechanical Gaming Keyboard",
        "description": "RGB backlit mechanical keyboard with tactile switches. Perfect for gaming or typing with anti-ghosting technology.",
        "price": 129.50,
        "stock": 100
    },
    {
        "name": "Ultra-Wide Monitor 34\"",
        "description": "Immerse yourself in work or play with this 34-inch curved ultra-wide monitor. Features 144Hz refresh rate and HDR support.",
        "price": 499.00,
        "stock": 25
    },
    {
        "name": "Ergonomic Office Chair",
        "description": "Adjustable ergonomic chair with lumbar support, breathable mesh back, and 3D armrests for maximum comfort.",
        "price": 199.99,
        "stock": 10
    }
]

for p_data in products:
    Product.objects.get_or_create(name=p_data['name'], defaults=p_data)

print("Seed data populated successfully.")
