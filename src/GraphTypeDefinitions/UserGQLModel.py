import strawberry
from .BaseGQLModel import IDType
from .externals import external_ids

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: IDType = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: IDType):
        if id is None:
            return None
        return UserGQLModel(id=id)

    external_ids = external_ids


