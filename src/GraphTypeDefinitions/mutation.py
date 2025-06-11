import strawberry

from .externalIdGQLModel import ExternalIdsMutation
from .externalIdTypeGQLModel import ExternalIdTypeMutation

@strawberry.type(description="root type for mutations")
class Mutation(ExternalIdsMutation, ExternalIdTypeMutation):
    pass
    