import strawberry
import typing

from .externalIdGQLModel import ExternalIdGQLModel

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
) -> typing.List["ExternalIdGQLModel"]:

    loader = ExternalIdGQLModel.getLoader(info=info)
    result = await loader.filter_by(inner_id=self.id)    
    return result
