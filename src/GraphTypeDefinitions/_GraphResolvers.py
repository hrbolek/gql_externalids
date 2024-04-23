import strawberry
import uuid
import datetime
import typing

IDType = uuid.UUID

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".externals")]
from ._GraphPermissions import OnlyForAuthentized
from src.Dataloaders import getUserFromInfo


@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: IDType):
    if id is not None:
        loader = cls.getLoader(info)
        if isinstance(id, str): id = uuid.UUID(id)
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result
    return None

@strawberry.field(description="""Entity primary key""")
def resolve_id(self) -> IDType:
    return self.id

@strawberry.field(
    description="""Name """,
    permission_classes=[OnlyForAuthentized])
def resolve_name(self) -> str:
    return self.name

@strawberry.field(
    description="""English name""",
    permission_classes=[OnlyForAuthentized])
def resolve_name_en(self) -> str:
    result = self.name_en if self.name_en else ""
    return result

@strawberry.field(
    description="""Time of last update""",
    permission_classes=[OnlyForAuthentized])
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(
    description="""Time of entity introduction""",
    permission_classes=[OnlyForAuthentized])
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created

async def resolve_user(user_id):
    from .externals import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
    return result
    
@strawberry.field(
    description="""Who created entity""",
    permission_classes=[OnlyForAuthentized])
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.createdby)

@strawberry.field(
    description="""Who made last change""",
    permission_classes=[OnlyForAuthentized])
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.changedby)

# @strawberry.field(description="""Who made last change""")
# async def resolve_rbacobject(self) -> typing.Optional[RBACObjectGQLModel]:
#     from ._RBACObjectGQLModel import RBACObjectGQLModel
#     result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(self.rbacobject_id)
#     return result


async def encapsulateUpdate(info, loader, entity, result):
    user = getUserFromInfo(info)
    entity.changedby = user["id"]

    row = await loader.update(entity)
    result.msg = "fail" if row is None else "ok"
    return result

async def encapsulateInsert(info, loader, entity, result):
    user = getUserFromInfo(info)
    entity.createdby = user["id"]
    
    row = await loader.insert(entity)
    result.msg = "ok"
    result.id = result.id if result.id else row.id       
    return result   

import sqlalchemy.exc

async def encapsulateDelete(info, loader, id, result):
    # try:
    #     await loader.delete(id)
    # except sqlalchemy.exc.IntegrityError as e:
    #     result.msg='fail'
    # return result
    await loader.delete(id)
    return result
    

resolve_result_id: IDType = strawberry.field(description="primary key of CU operation object",
    permission_classes=[OnlyForAuthentized])
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""",
    permission_classes=[OnlyForAuthentized])

from inspect import signature
import inspect 
from functools import wraps

# def asPage(field, *, extendedfilter=None):
#     def decorator(field):
#         # print(field.__name__, field.__annotations__)
#         signatureField = signature(field)
#         return_annotation = signatureField.return_annotation

#         skipParameter = signatureField.parameters.get("skip", None)
#         skipParameterDefault = 0
#         if skipParameter:
#             skipParameterDefault = skipParameter.default

#         limitParameter = signatureField.parameters.get("limit", None)
#         limitParameterDefault = 10
#         if limitParameter:
#             limitParameterDefault = limitParameter.default

#         whereParameter = signatureField.parameters.get("where", None)
#         whereParameterDefault = None
#         whereParameterAnnotation = str
#         if whereParameter:
#             whereParameterDefault = whereParameter.default
#             whereParameterAnnotation = whereParameter.annotation

#         async def foreignkeyVectorSimple(
#             self, info: strawberry.types.Info,
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signature(field).return_annotation:
#             loader = await field(self, info)
#             results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorSimple.__name__ = field.__name__
#         foreignkeyVectorSimple.__doc__ = field.__doc__

#         async def foreignkeyVectorComplex(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = None, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation:
#             wf = None if where is None else strawberry.asdict(where)
#             loader = await field(self, info, where=wf)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorComplex.__name__ = field.__name__
#         foreignkeyVectorComplex.__doc__ = field.__doc__
        
#         if return_annotation._name == "List":
#             if whereParameter:
#                 return foreignkeyVectorComplex
#             else:
#                 return foreignkeyVectorSimple
#         else:
#             raise Exception("Unable to recognize decorated function, I am sorry")

#     if field:
#         return decorator(field)
#     return decorator

# def asForeignList(*, foreignKeyName: str):
#     assert foreignKeyName is not None, "foreignKeyName must be defined"
#     def decorator(field):
#         print(field.__name__, field.__annotations__)
#         signatureField = signature(field)
#         return_annotation = signatureField.return_annotation

#         skipParameter = signatureField.parameters.get("skip", None)
#         skipParameterDefault = 0
#         if skipParameter:
#             skipParameterDefault = skipParameter.default

#         limitParameter = signatureField.parameters.get("limit", None)
#         limitParameterDefault = 10
#         if limitParameter:
#             limitParameterDefault = limitParameter.default

#         whereParameter = signatureField.parameters.get("where", None)
#         whereParameterDefault = None
#         whereParameterAnnotation = str
#         if whereParameter:
#             whereParameterDefault = whereParameter.default
#             whereParameterAnnotation = whereParameter.annotation

#         async def foreignkeyVectorSimple(
#             self, info: strawberry.types.Info,
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signature(field).return_annotation:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
#             if inspect.isawaitable(loader):
#                 loader = await loader
#             results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorSimple.__name__ = field.__name__
#         foreignkeyVectorSimple.__doc__ = field.__doc__
#         foreignkeyVectorSimple.__module__ = field.__module__

#         async def foreignkeyVectorComplex(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = whereParameterDefault, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
#             if inspect.isawaitable(loader):
#                 loader = await loader
            
#             wf = None if where is None else strawberry.asdict(where)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorComplex.__name__ = field.__name__
#         foreignkeyVectorComplex.__doc__ = field.__doc__
#         foreignkeyVectorComplex.__module__ = field.__module__

#         async def foreignkeyVectorComplex2(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = whereParameterDefault, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation: #typing.List[str]:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
            
#             wf = None if where is None else strawberry.asdict(where)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorComplex2.__module__ = field.__module__
#         if return_annotation._name == "List":
#             if whereParameter:
#                 print("RETURNING foreignkeyVectorComplex")
#                 return foreignkeyVectorComplex               
#             else:
#                 print("RETURNING foreignkeyVectorSimple")
#                 return foreignkeyVectorSimple
#         else:
#             raise Exception("Unable to recognize decorated function, I am sorry")

#     return decorator
# def createAttributeScalarResolver(

# def createAttributeScalarResolver(
#     scalarType: None = None, 
#     foreignKeyName: str = None,
#     description="Retrieves item by its id",
#     permission_classes=()
#     ):

#     assert scalarType is not None
#     assert foreignKeyName is not None

#     @strawberry.field(description=description, permission_classes=permission_classes)
#     async def foreignkeyScalar(
#         self, info: strawberry.types.Info
#     ) -> typing.Optional[scalarType]:
#         # 👇 self must have an attribute, otherwise it is fail of definition
#         assert hasattr(self, foreignKeyName)
#         id = getattr(self, foreignKeyName, None)
        
#         result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
#         return result
#     return foreignkeyScalar

# def createAttributeVectorResolver(
#     scalarType: None = None, 
#     whereFilterType: None = None,
#     foreignKeyName: str = None,
#     loaderLambda = lambda info: None, 
#     description="Retrieves items paged", 
#     skip: int=0, 
#     limit: int=10):

#     assert scalarType is not None
#     assert foreignKeyName is not None

#     @strawberry.field(description=description)
#     async def foreignkeyVector(
#         self, info: strawberry.types.Info,
#         skip: int = skip,
#         limit: int = limit,
#         where: typing.Optional[whereFilterType] = None
#     ) -> typing.List[scalarType]:
        
#         params = {foreignKeyName: self.id}
#         loader = loaderLambda(info)
#         assert loader is not None
        
#         wf = None if where is None else strawberry.asdict(where)
#         result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
#         return result
#     return foreignkeyVector

# def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
#     assert scalarType is not None
#     @strawberry.field(description=description,
#     permission_classes=[OnlyForAuthentized])
#     async def by_id(
#         self, info: strawberry.types.Info, id: IDType
#     ) -> typing.Optional[scalarType]:
#         result = await scalarType.resolve_reference(info=info, id=id)
#         return result
#     return by_id

# def createRootResolver_by_page(
#     scalarType: None, 
#     whereFilterType: None,
#     loaderLambda = lambda info: None, 
#     description="Retrieves items paged", 
#     skip: int=0, 
#     limit: int=10,
#     orderby: typing.Optional[str] = None,
#     desc: typing.Optional[bool] = None):

#     assert scalarType is not None
#     assert whereFilterType is not None
    
#     @strawberry.field(description=description,
#     permission_classes=[OnlyForAuthentized])
#     async def paged(
#         self, info: strawberry.types.Info, 
#         skip: int=skip, limit: int=limit, where: typing.Optional[whereFilterType] = None,
#         orderby: typing.Optional[str] = None
#     ) -> typing.List[scalarType]:
#         loader = loaderLambda(info)
#         assert loader is not None
#         wf = None if where is None else strawberry.asdict(where)
#         result = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc)
#         return result
#     return paged
