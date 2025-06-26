import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists.")
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully.")
class CustomerInput(graphene.InputObjectType):
            name = graphene.String(required=True)
            email = graphene.String(required=True)
            phone = graphene.String()

# create BulkCreateCustomers mutation   
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created = []
        errors = []
        for entry in input:
            if Customer.objects.filter(email=entry["email"]).exists():
                errors.append(f"Duplicate email: {entry['email']}")
                continue
            customer = Customer(name=entry["name"], email=entry["email"], phone=entry.get("phone", ""))
            customer.save()
            created.append(customer)
        return BulkCreateCustomers(customers=created, errors=errors)
# this class is create a product Mutation Schema 
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive.")
        if stock < 0:
            raise Exception("Stock cannot be negative.")
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)

from django.utils import timezone

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Customer not found.")
        
        if not product_ids:
            raise Exception("At least one product must be selected.")
        
        products = Product.objects.filter(id__in=product_ids)
        if len(products) != len(product_ids):
            raise Exception("Some product IDs are invalid.")
        
        total = sum([p.price for p in products])
        order = Order(customer=customer, order_date=order_date or timezone.now(), total_amount=total)
        order.save()
        order.products.set(products)
        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

class Query(graphene.ObjectType):
    pass
