import strawberry

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from .externalIdGQLModel import ExternalIdsQuery
from .externalIdTypeGQLModel import ExternalIdTypeQuery

@strawberry.type(description="""Type for query root""")
class Query(ExternalIdsQuery, ExternalIdTypeQuery):
    pass
