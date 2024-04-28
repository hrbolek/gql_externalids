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

@strawberry.field(description="""All related external ids""")
async def external_ids(
    self, info: strawberry.types.Info
) -> List["ExternalIdGQLModel"]:

    loader = ExternalIdGQLModel.getLoader(info=info)
    result = await loader.filter_by(inner_id=self.id)    
    return result

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: IDType = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: IDType):
        if id is None:
            return None
        return UserGQLModel(id=id)

    external_ids = external_ids


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: IDType = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: IDType):
        return GroupGQLModel(id=id)

    external_ids = external_ids

@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:

    id: IDType = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: IDType):
        return EventGQLModel(id=id)

    external_ids = external_ids

@strawberry.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:

    id: IDType = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: IDType):
        return FacilityGQLModel(id=id)

    external_ids = external_ids