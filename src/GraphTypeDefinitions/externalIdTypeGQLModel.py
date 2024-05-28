import strawberry
import datetime
from typing import Optional, Union, List, Annotated
import src.GraphTypeDefinitions
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

from .externalIdCategoryGQLModel import ExternalIdCategoryGQLModel
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
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdTypeGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ExternalIdTypeModel

    resolve_reference = resolve_reference    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    lastchange = resolve_lastchange
    created = resolve_created

    changed_by = resolve_changedby
    created_by = resolve_createdby

    @strawberry.field(description="""Category which belongs to""")
    async def category(self, info: strawberry.types.Info) -> Optional["ExternalIdCategoryGQLModel"]:
        return await ExternalIdCategoryGQLModel.resolve_reference(info, id=self.category_id)


#####################################################################
#
# Special fields for query
#
#####################################################################
from ..DBResolvers import DBResolvers

@createInputs
@dataclass
class ExternalidTypeInputWhereFilter:
    id: IDType
    name: str
    name_en: str

    from .externalIdCategoryGQLModel import ExternalidCategoryInputWhereFilter
    category: ExternalidCategoryInputWhereFilter


externalidtype_page = strawberry.field(
    description="Rows of externaltypeids",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.ExternalIdTypeModel.resolve_page(ExternalIdTypeGQLModel, WhereFilterModel=ExternalidTypeInputWhereFilter)
    )

externalidtype_by_id = strawberry.field(
    description="externaltypeid by primary key",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.ExternalIdTypeModel.resolve_by_id(ExternalIdTypeGQLModel)
    )

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="")
class ExternalIdTypeInsertGQLModel:
    id: IDType = strawberry.field(default=None, description="Primary key")
    name: str = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of type")
    urlformat: Optional[str] = strawberry.field(default=None, description="Format for conversion of id into url link")
    id: Optional[IDType] = strawberry.field(default=None, description="Could be uuid primary key")
    category_id: Optional[IDType] = strawberry.field(default=None, description="Category of type")
    createdby: strawberry.Private[IDType] = None

@strawberry.input(description="")
class ExternalIdTypeUpdateGQLModel:
    id: IDType = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(default=None, description="Timestamp")
    name: Optional[str] = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of type")
    urlformat: Optional[str] = strawberry.field(default=None, description="Format for conversion of id into url link")
    category_id: Optional[IDType] = strawberry.field(default=None, description="Category of type")
    changedby: strawberry.Private[IDType] = None
    
@strawberry.type(description="")
class ExternalIdTypeResultGQLModel:
    id: Optional[IDType] = strawberry.field(default=None, description="Primary key of table row")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(description="""Result of insert operation""")
    async def externaltypeid(self, info: strawberry.types.Info) -> Union[ExternalIdTypeGQLModel, None]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="defines a new external type id for an entity",
    permission_classes=[OnlyForAuthentized]
    )
async def externaltypeid_insert(self, info: strawberry.types.Info, externaltypeid: ExternalIdTypeInsertGQLModel) -> ExternalIdTypeResultGQLModel:
    return await encapsulateInsert(info, ExternalIdTypeGQLModel.getLoader(info), externaltypeid, ExternalIdTypeResultGQLModel(id=externaltypeid.id, msg="ok"))

@strawberry.mutation(
    description="Update existing external type id for an entity",
    permission_classes=[OnlyForAuthentized]
    )
async def externaltypeid_update(self, info: strawberry.types.Info, externaltypeid: ExternalIdTypeUpdateGQLModel) -> ExternalIdTypeResultGQLModel:
    return await encapsulateUpdate(info, ExternalIdTypeGQLModel.getLoader(info), externaltypeid, ExternalIdTypeResultGQLModel(id=externaltypeid.id, msg="ok"))

@strawberry.mutation(
    description="Update existing external type id for an entity",
    permission_classes=[OnlyForAuthentized]
    )
async def externaltypeid_delete(self, info: strawberry.types.Info, id: IDType) -> ExternalIdTypeResultGQLModel:
    return await encapsulateDelete(info, ExternalIdTypeGQLModel.getLoader(info), id, ExternalIdTypeResultGQLModel(id=id, msg="ok"))
