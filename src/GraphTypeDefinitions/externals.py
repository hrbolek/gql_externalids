import strawberry
from typing import List

from .externalIdGQLModel import ExternalIdGQLModel
from ._GraphResolvers import IDType
def getLoadersFromInfo(info):
    return info.context["all"]

###########################################################################################################################
#
# zde definujte sve rozsirene GQL modely,
# ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
# venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
# vsimnete si,
# - jak je definovan dekorator tridy (extend=True)
# - jaky dekorator je pouzit (federation.type)
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
# - ma odlisnou implementaci v porovnani s modelem, za ktery jste odpovedni
#
###########################################################################################################################


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: IDType = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: IDType):
        if id is None:
            return None
        return UserGQLModel(id=id)

    @strawberry.field(description="""All external ids related to the user""")
    async def external_ids(
        self, info: strawberry.types.Info
    ) -> List["ExternalIdGQLModel"]:

        loader = getLoadersFromInfo(info=info).externalids_inner_id
        result = await loader.load(self.id)    
        return result


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: IDType = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: IDType):
        return GroupGQLModel(id=id)

    @strawberry.field(description="""All external ids related to a group""")
    async def external_ids(
        self, info: strawberry.types.Info
    ) -> List["ExternalIdGQLModel"]:
        loader = getLoadersFromInfo(info=info).externalids_inner_id
        result = await loader.load(self.id)    
        return result