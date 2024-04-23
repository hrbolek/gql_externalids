import strawberry
import datetime
from typing import Union, Optional, List, Annotated
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

from .externalIdTypeGQLModel import ExternalIdTypeGQLModel

###########################################################################################################################
#
# zde definujte sve nove GQL modely, kde mate zodpovednost
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
###########################################################################################################################

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ExternalIdModel

    resolve_reference = resolve_reference    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    lastchange = resolve_lastchange
    created = resolve_created

    changed_by = resolve_changedby
    created_by = resolve_createdby

    @strawberry.field(description="""Inner id""")
    def inner_id(self) -> Optional[IDType]:
        return self.inner_id

    @strawberry.field(description="""Outer id""")
    def outer_id(self) -> Optional[str]:
        return self.outer_id

    @strawberry.field(description="""Type of id""")
    async def type(self, info: strawberry.types.Info) -> Optional["ExternalIdTypeGQLModel"]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        return result

    @strawberry.field(description="""Type name of id""")
    async def type_name(self, info: strawberry.types.Info) -> Optional[str]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        return None if result is None else result.name
    
#####################################################################
#
# Special fields for query
#
#####################################################################
@createInputs
@dataclass
class ExternalidInputWhereFilter:
    id: IDType
    inner_id: IDType
    outer_id: str
    typeid_id: IDType
    from .externalIdTypeGQLModel import ExternalidTypeInputWhereFilter
    type: ExternalidTypeInputWhereFilter

@strawberry.field(
    description="""Returns inner id based on external id type and external id value"""
    )
async def internal_id(
    self,
    info: strawberry.types.Info,
    typeid_id: IDType,
    outer_id: str,
) -> Optional[IDType]:
    loader = ExternalIdGQLModel.getLoader(info)
    rows = await loader.filter_by(outer_id=outer_id, typeid_id=typeid_id)
    row = next(rows, None)
    if row is None:
        return None
    else:
        return row.inner_id

@strawberry.field(
    description="""Returns outer ids based on external id type and inner id value"""
    )
async def external_ids(
    self,
    info: strawberry.types.Info,
    inner_id: IDType,
    typeid_id: Optional[IDType] = None,
) -> List[ExternalIdGQLModel]:
    loader = ExternalIdGQLModel.getLoader(info)
    if typeid_id is None:
        rows = await loader.filter_by(inner_id=inner_id)
    else:
        rows = await loader.filter_by(inner_id=inner_id, typeid_id=typeid_id)
    return rows
    
#####################################################################
#
# Mutation section
#
#####################################################################

@strawberry.input(description="")
class ExternalIdInsertGQLModel:
    inner_id: IDType = strawberry.field(default=None, description="Primary key of entity which new outeid is assigned")
    typeid_id: IDType = strawberry.field(default=None, description="Type of external id")
    outer_id: str = strawberry.field(default=None, description="Key used by other systems")
    id: Optional[IDType] = strawberry.field(default=None, description="Primary key of table row")
    changedby: strawberry.Private[IDType] = None
    createdby: strawberry.Private[IDType] = None

@strawberry.input(description="")
class ExternalIdUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    inner_id: IDType = strawberry.field(default=None, description="Primary key of entity which new outeid is assigned")
    typeid_id: IDType = strawberry.field(default=None, description="Type of external id")
    outer_id: str = strawberry.field(default=None, description="Key used by other systems")
    changedby: strawberry.Private[IDType] = None

@strawberry.type(description="")
class ExternalIdResultGQLModel:
    id: Optional[IDType] = strawberry.field(default=None, description="Primary key of table row")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(
        description="""Result of drone operation""",
        permission_classes=[OnlyForAuthentized]
    )
    async def externalid(self, info: strawberry.types.Info) -> Union[ExternalIdGQLModel, None]:
        result = await ExternalIdGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(
    description="defines a new external id for an entity",
    permission_classes=[OnlyForAuthentized]
    )
async def externalid_insert(self, info: strawberry.types.Info, externalid: ExternalIdInsertGQLModel) -> Optional[ExternalIdResultGQLModel]:
    loader = ExternalIdGQLModel.getLoader(info)
    rows = await loader.filter_by(inner_id = externalid.inner_id, typeid_id= externalid.typeid_id, outer_id=externalid.outer_id)
    row = next(rows, None)
    if row is not None:
        return ExternalIdResultGQLModel(id=row.id, msg="fail")

    return await encapsulateInsert(info, ExternalIdGQLModel.getLoader(info), externalid, ExternalIdResultGQLModel(id=externalid.id, msg="ok"))

@strawberry.mutation(
    description="update the external id for an entity",
    permission_classes=[OnlyForAuthentized]
    )
async def externalid_update(self, info: strawberry.types.Info, externalid: ExternalIdUpdateGQLModel) -> ExternalIdResultGQLModel:
    return await encapsulateUpdate(info, ExternalIdGQLModel.getLoader(info), externalid, ExternalIdResultGQLModel(id=externalid.id, msg="ok"))

@strawberry.mutation(
    description="deletes the external id for an entity",
    permission_classes=[OnlyForAuthentized]
    )
async def externalid_delete(self, info: strawberry.types.Info, id: IDType) -> ExternalIdResultGQLModel:
    return await encapsulateDelete(info, ExternalIdGQLModel.getLoader(info), id, ExternalIdResultGQLModel(id=id, msg="ok"))
