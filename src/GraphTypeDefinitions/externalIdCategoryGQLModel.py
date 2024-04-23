import strawberry
import datetime
from typing import Optional, List, Union, Annotated
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

from src.Dataloaders import getLoadersFromInfo, getUserFromInfo
from ._GraphPermissions import OnlyForAuthentized
from ._GraphResolvers import (
    resolve_reference,
    resolve_id,
    resolve_createdby,
    resolve_changedby,
    resolve_lastchange,
    resolve_created,

    resolve_name,
    resolve_name_en,

    encapsulateInsert,
    encapsulateUpdate,
    encapsulateDelete,

    IDType
)

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external category id ()""",
)
class ExternalIdCategoryGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ExternalIdCategoryModel

    resolve_reference = resolve_reference    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    lastchange = resolve_lastchange
    created = resolve_created

    changed_by = resolve_changedby
    created_by = resolve_createdby

#####################################################################
#
# Special fields for query
#
#####################################################################
from ..DBResolvers import DBResolvers

@createInputs
@dataclass
class ExternalidCategoryInputWhereFilter:
    id: IDType
    name: str
    name_en: str

externalidcategory_page = strawberry.field(
    description="Rows of externalcategoryids",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.ExternalIdCategoryModel.resolve_page(ExternalIdCategoryGQLModel, WhereFilterModel=ExternalidCategoryInputWhereFilter)
    )

#####################################################################
#
# Mutation section
#
#####################################################################

import datetime

@strawberry.input(description="")
class ExternalIdCategoryInsertGQLModel:
    name: str = strawberry.field(default=None, description="Name of category")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of category")
    id: Optional[IDType] = strawberry.field(default=None, description="Could be uuid primary key")
    createdby: strawberry.Private[IDType]

@strawberry.input(description="")
class ExternalIdCategoryUpdateGQLModel:
    id: IDType = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(default=None, description="Timestamp")
    name: Optional[str] = strawberry.field(default=None, description="Name of category")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of category")
    changedby: strawberry.Private[IDType]
    
@strawberry.type(description="")
class ExternalIdCategoryResultGQLModel:
    id: Optional[IDType] = strawberry.field(default=None, description="Primary key of table row")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(
            description="""Result of insert operation""",
            permission_classes=[OnlyForAuthentized])
    async def externalidcategory(self, info: strawberry.types.Info) -> Union[ExternalIdCategoryGQLModel, None]:
        result = await ExternalIdCategoryGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="defines a new external id category for an entity",
        permission_classes=[OnlyForAuthentized]
    )
async def externalidcategory_insert(self, info: strawberry.types.Info, externalidcategory: ExternalIdCategoryInsertGQLModel) -> ExternalIdCategoryResultGQLModel:
    return await encapsulateInsert(info, ExternalIdCategoryGQLModel.getLoader(info), externalidcategory, ExternalIdCategoryResultGQLModel(id=externalidcategory, msg="ok"))

@strawberry.mutation(
    description="Update existing external id category for an entity",
    permission_classes=[OnlyForAuthentized]
    )
async def externalidcategory_update(self, info: strawberry.types.Info, externalidcategory: ExternalIdCategoryUpdateGQLModel) -> ExternalIdCategoryResultGQLModel:
    return await encapsulateUpdate(info, ExternalIdCategoryGQLModel.getLoader(info), externalidcategory, ExternalIdCategoryResultGQLModel(id=externalidcategory, msg="ok"))

@strawberry.mutation(
    description="Update existing external id category for an entity",
    permission_classes=[OnlyForAuthentized]
    )
async def externalidcategory_delete(self, info: strawberry.types.Info, id: IDType) -> ExternalIdCategoryResultGQLModel:
    return await encapsulateDelete(info, ExternalIdCategoryGQLModel.getLoader(info), id, ExternalIdCategoryResultGQLModel(id=id, msg="ok"))
