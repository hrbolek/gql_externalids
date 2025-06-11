import strawberry
import datetime
import typing
from typing import Optional, List, Union, Annotated
from dataclasses import dataclass

from uoishelpers.resolvers import (
    createInputs2,
    PageResolver,
    VectorResolver,
    ScalarResolver,

    Insert, InsertError,
    Update, UpdateError,
    Delete, DeleteError
)
from uoishelpers.gqlpermissions import OnlyForAuthentized
from .BaseGQLModel import BaseGQLModel, IDType

from src.Dataloaders import getLoadersFromInfo

@createInputs2
class ExternalidTypeInputWhereFilter:
    id: IDType
    name: str
    name_en: str


@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id ()""",
)
class ExternalIdTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ExternalIdTypeModel

    name: typing.Optional[str] = strawberry.field(
        description="",
        permission_classes=[],
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="",
        permission_classes=[],
        default=None
    )

    master_id: typing.Optional[IDType] = strawberry.field(
        description="who changed this entity", 
        default=None,
        permission_classes=[OnlyForAuthentized]
        )

    urlformat: typing.Optional[str] = strawberry.field(
        description="",
        permission_classes=[],
        default=None
    )

    master_type: typing.Optional["ExternalIdTypeGQLModel"] = strawberry.field(
        permission_classes=[],
        description="Master type of this type, allows tree organization of types",
        resolver=ScalarResolver["ExternalIdTypeGQLModel"](fkey_field_name="master_id")
    )

    sub_types: typing.List["ExternalIdTypeGQLModel"] = strawberry.field(
        permission_classes=[],
        description="subtypes",
        resolver=VectorResolver["ExternalIdTypeGQLModel"](fkey_field_name="master_id", whereType=ExternalidTypeInputWhereFilter)
    )


#####################################################################
#
# Special fields for query
#
#####################################################################

@strawberry.interface(description="Base External type queries")
class ExternalIdTypeQuery:
    externalidType_page: typing.List[ExternalIdTypeGQLModel] = strawberry.field(
        description="page of types",
        permission_classes=[],
        resolver=PageResolver[ExternalIdTypeGQLModel](whereType=ExternalidTypeInputWhereFilter)
    )

    externalidType_by_id: typing.Optional[ExternalIdTypeGQLModel] = strawberry.field(
        description="type by its id",
        permission_classes=[],
        resolver=ExternalIdTypeGQLModel.resolve_reference
    )
    
#####################################################################
#
# Mutation section
#
#####################################################################

import datetime
from .utils import InputModelMixin

@strawberry.input(description="")
class ExternalIdTypeInsertGQLModel(InputModelMixin):
    getLoader = ExternalIdTypeGQLModel.getLoader

    name: str = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of type")
    id: Optional[IDType] = strawberry.field(default=None, description="Could be uuid primary key")
    master_id: Optional[IDType] = strawberry.field(default=None, description="master")
    sub_types: typing.Optional[typing.List["ExternalIdTypeInsertGQLModel"]] = strawberry.field(
        description="",
        default_factory=list
    )
    createdby: strawberry.Private[IDType] = None

@strawberry.input(description="")
class ExternalIdTypeUpdateGQLModel:
    id: IDType = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(default=None, description="Timestamp")
    name: Optional[str] = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of type")
    changedby: strawberry.Private[IDType] = None
    
@strawberry.input(description="")
class ExternalIdTypeDeleteGQLModel:
    id: IDType = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(default=None, description="Timestamp")
    
    
@strawberry.interface(description="")
class ExternalIdTypeMutation:

    @strawberry.mutation(
        description="defines a new external id type for an entity",
            permission_classes=[OnlyForAuthentized]
        )
    async def externalidtype_insert(
        self, 
        info: strawberry.types.Info, 
        externalidtype: ExternalIdTypeInsertGQLModel
    ) -> typing.Union[ExternalIdTypeGQLModel, InsertError[ExternalIdTypeGQLModel]]:
        print(strawberry.asdict(externalidtype), flush=True)
        modelinstance = externalidtype.intoModel(info=info)
        return await Insert[ExternalIdTypeGQLModel].DoItSafeWay(
            info=info, entity=modelinstance
        )

    @strawberry.mutation(
        description="Update existing external id type for an entity",
        permission_classes=[OnlyForAuthentized]
        )
    async def externalidtype_update(
        self, 
        info: strawberry.types.Info, 
        externalidtype: ExternalIdTypeUpdateGQLModel
    ) -> typing.Union[ExternalIdTypeGQLModel, UpdateError[ExternalIdTypeGQLModel]]:
        return await Update[ExternalIdTypeGQLModel].DoItSafeWay(
            info=info, entity=externalidtype
        )

    @strawberry.mutation(
        description="Update existing external id type for an entity",
        permission_classes=[OnlyForAuthentized]
        )
    async def externalidtype_delete(
        self, 
        info: strawberry.types.Info, 
        externalidtype: ExternalIdTypeDeleteGQLModel
    ) -> typing.Optional[DeleteError[ExternalIdTypeGQLModel]]:
        return await Delete[ExternalIdTypeGQLModel].DoItSafeWay(
            info=info, entity=externalidtype
        )
