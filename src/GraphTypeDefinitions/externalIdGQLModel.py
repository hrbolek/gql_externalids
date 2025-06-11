import strawberry
import datetime
import typing

from typing import Union, Optional, List, Annotated
from dataclasses import dataclass
from uoishelpers.resolvers import (
    createInputs2,
    PageResolver,
    VectorResolver,
    ScalarResolver,

    Update, UpdateError,
    Insert, InsertError,
    Delete, DeleteError

)

from src.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

from ._GraphPermissions import OnlyForAuthentized
from ._GraphResolvers import (
    resolve_reference,
    resolve_id,
    resolve_createdby,
    resolve_changedby,
    resolve_lastchange,
    resolve_created,

    encapsulateInsert,
    encapsulateUpdate,
    encapsulateDelete,

    IDType
)

from .externalIdTypeGQLModel import ExternalIdTypeGQLModel

###########################################################################################################################
#
# zde definujte sve nove GQL modely, kde mate zodpovednost
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
###########################################################################################################################

@strawberry.field(description="""All related external ids""")
async def external_ids(
    self, info: strawberry.types.Info
) -> List["ExternalIdGQLModel"]:

    loader = ExternalIdGQLModel.getLoader(info=info)
    result = await loader.filter_by(inner_id=self.id)    
    return result

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ExternalIdModel

    resolve_reference = resolve_reference    

    inner_id: typing.Optional[IDType] = strawberry.field(description="""Inner id""")
    outer_id: typing.Optional[IDType] = strawberry.field(description="""Outer id""")

    @strawberry.field(description="""Type of id""")
    async def type(self, info: strawberry.types.Info) -> Optional["ExternalIdTypeGQLModel"]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        return result

    @strawberry.field(description="""Type name of id""")
    async def type_name(self, info: strawberry.types.Info) -> Optional[str]:
        result = await ExternalIdTypeGQLModel.load_with_loader(info=info, id=self.typeid_id)
        return None if result is None else result.name

    @strawberry.field(description="""html link""")
    async def link(self, info: strawberry.types.Info) -> Optional[str]:
        result = None
        type_id = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        if type_id:
            format = type_id.urlformat
            if format:
                result = format % (self.outer_id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################
@createInputs2
class ExternalidInputWhereFilter:
    id: IDType
    inner_id: IDType
    outer_id: str
    typeid_id: IDType
    from .externalIdTypeGQLModel import ExternalidTypeInputWhereFilter
    type: ExternalidTypeInputWhereFilter

@strawberry.interface()
class ExternalIdsQuery:


    @strawberry.field(
        description="""Returns inner id based on external id type and external id value""",
        permission_classes=[]
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
        return row.id if row else None


    @strawberry.field(
        description="""Returns outer ids based on external id type and inner id value""",
        permission_classes=[]
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
        return (ExternalIdGQLModel.from_dataclass(row) for row in rows)

    external_ids_page: typing.List[ExternalIdGQLModel] = strawberry.field(
        permission_classes=[],
        description="returns list of externalids",
        resolver=PageResolver[ExternalIdGQLModel](whereType=ExternalidInputWhereFilter)
    )


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


@strawberry.input(description="")
class ExternalIdDeleteGQLModel:
    id: IDType
    lastchange: datetime.datetime


@strawberry.interface(description="")
class ExternalIdsMutation:
    @strawberry.mutation(
        description="defines a new external id for an entity",
        permission_classes=[OnlyForAuthentized]
        )
    async def externalid_insert(
        self, 
        info: strawberry.types.Info, 
        externalid: ExternalIdInsertGQLModel
    ) -> typing.Union[ExternalIdGQLModel, InsertError[ExternalIdGQLModel]]:
        loader = ExternalIdGQLModel.getLoader(info)
        rows = await loader.filter_by(inner_id = externalid.inner_id, typeid_id= externalid.typeid_id, outer_id=externalid.outer_id)
        row = next(rows, None)
        if row is not None:
            return InsertError[ExternalIdGQLModel](msg="Allready exists", _input=externalid)
        return await Insert[ExternalIdGQLModel].DoItSafeWay(info=info, entity=externalid)

    @strawberry.mutation(
        description="update the external id for an entity",
        permission_classes=[OnlyForAuthentized]
        )
    async def externalid_update(
        self, 
        info: strawberry.types.Info, 
        externalid: ExternalIdUpdateGQLModel
    ) -> typing.Union[ExternalIdGQLModel, UpdateError[ExternalIdGQLModel]]:
        return await Update[ExternalIdGQLModel].DoItSafeWay(
            info=info, entity=externalid
        )

    @strawberry.mutation(
        description="deletes the external id for an entity",
        permission_classes=[OnlyForAuthentized]
        )
    async def externalid_delete(
        self, 
        info: strawberry.types.Info, 
        externalid: ExternalIdDeleteGQLModel
    ) -> typing.Optional[DeleteError[ExternalIdGQLModel]]:
        return await Delete[ExternalIdGQLModel].DoItSafeWay(
            info=info, entity=externalid
        )
