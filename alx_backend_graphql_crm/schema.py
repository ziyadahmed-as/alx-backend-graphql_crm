# alx_backend_graphql_crm/schema.py
## This file defines the GraphQL schema for the CRM application.
# It includes a simple query that returns a greeting message.
import graphene
import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

schema = graphene.Schema(query=Query)
# This schema defines a simple GraphQL query that returns a greeting message.

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
