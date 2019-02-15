import graphene

import Barebones.schema


class Query(Barebones.schema.Query, graphene.ObjectType):
    pass


class Mutation(Barebones.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)