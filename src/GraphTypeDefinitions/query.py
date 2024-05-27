import strawberry

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################


@strawberry.type(description="""Type for query root""")
class Query:

    from .externalIdGQLModel import (
        internal_id, 
        external_ids, 
        external_ids_page
        )
    external_ids = external_ids
    internal_id = internal_id
    external_ids_page = external_ids_page

    from .externalIdTypeGQLModel import (
        externalidtype_page,
        externalidtype_by_id
    )
    externalidtype_page = externalidtype_page
    externalidtype_by_id = externalidtype_by_id

    from .externalIdCategoryGQLModel import externalidcategory_page
    externalidcategory_page = externalidcategory_page