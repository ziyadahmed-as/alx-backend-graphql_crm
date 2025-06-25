# alx_backend_graphql_crm/schema.py
## This file defines the GraphQL schema for the CRM application.
# It includes a simple query that returns a greeting message.
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

schema = graphene.Schema(query=Query)
# This schema defines a simple GraphQL query that returns a greeting message.
