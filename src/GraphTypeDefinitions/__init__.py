import strawberry

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .query import Query
from .mutation import Mutation

from .UserGQLModel import UserGQLModel
from .GroupGQLModel import GroupGQLModel
from .EventGQLModel import EventGQLModel
from .FacilityGQLModel import FacilityGQLModel

from .BaseGQLModel import Relation

schema = strawberry.federation.Schema(
    query=Query, 
    mutation=Mutation, 
    types=(UserGQLModel, GroupGQLModel, EventGQLModel, FacilityGQLModel),
    schema_directives=[Relation],
    extensions=[]
)

from uoishelpers.schema import WhoAmIExtension
schema.extensions.append(WhoAmIExtension)