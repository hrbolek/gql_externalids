import sqlalchemy
import sys
import asyncio

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from src.DBDefinitions import BaseModel
from src.DBDefinitions import ExternalIdTypeModel, ExternalIdModel, ExternalIdCategoryModel


async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


from src.DBFeeder import get_demodata


async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            ExternalIdCategoryModel,
            ExternalIdTypeModel, 
            ExternalIdModel
        ],
        data,
    )


from src.Dataloaders import createLoadersContext


async def createContext(asyncSessionMaker):
    loadersContext = createLoadersContext(asyncSessionMaker)
    return {
        **loadersContext,
        "asyncSessionMaker": asyncSessionMaker,
        "user": {"id": "f8089aa6-2c4a-4746-9503-105fcc5d054c"}
    }
