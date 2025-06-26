from crm.models import Customer, Product

def seed_data():
    Customer.objects.create(name="Demo", email="demo@example.com")
    Product.objects.create(name="Phone", price=500, stock=20)
