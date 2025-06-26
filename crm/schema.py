import graphene

from .models import Customer, Product, Order


from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Customer, Product, Order
from django.utils import timezone
import re

# This file defines the GraphQL schema for the CRM application.
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int()

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()


# It includes types for Customer, Product, and Order.
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order



    
class CustomerInput(graphene.InputObjectType):
            name = graphene.String(required=True)
            email = graphene.String(required=True)
            phone = graphene.String()


#  It includes fields for name, email, and an optional phone number.
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise GraphQLError("Email already exists.")

        # Phone validation (optional field)
        if input.phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', input.phone):
            raise GraphQLError("Invalid phone number format.")

        customer = Customer(name=input.name, email=input.email, phone=input.phone)
        customer.save()

        return CreateCustomer(customer=customer, message="Customer created successfully.")

# reate BulkCreateCustomers mutation   
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        customers_created = []
        errors = []

        for entry in input:
            if Customer.objects.filter(email=entry.email).exists():
                errors.append(f"Email '{entry.email}' already exists.")
                continue
            if entry.phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', entry.phone):
                errors.append(f"Invalid phone format for: {entry.phone}")
                continue

            customer = Customer(name=entry.name, email=entry.email, phone=entry.phone)
            customer.save()
            customers_created.append(customer)

        return BulkCreateCustomers(customers=customers_created, errors=errors)

# this class is create a product Mutation Schema 
class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0:
            raise GraphQLError("Price must be positive.")
        if input.stock is not None and input.stock < 0:
            raise GraphQLError("Stock cannot be negative.")

        product = Product(name=input.name, price=input.price, stock=input.stock or 0)
        product.save()

        return CreateProduct(product=product)
    
class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(id=input.customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError("Customer not found.")

        if not input.product_ids:
            raise GraphQLError("At least one product ID is required.")

        products = Product.objects.filter(id__in=input.product_ids)
        if products.count() != len(input.product_ids):
            raise GraphQLError("One or more product IDs are invalid.")

        total = sum([p.price for p in products])
        order_date = input.order_date or timezone.now()

        order = Order(customer=customer, total_amount=total, order_date=order_date)
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
