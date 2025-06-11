import sqlalchemy
from sqlalchemy.orm import relationship

from sqlalchemy.orm import relationship, Mapped, mapped_column

from sqlalchemy import (
    ForeignKey,
)

from .BaseModel import BaseModel, IDType

class ExternalIdModel(BaseModel):
    __tablename__ = "externalids"

    typeid_id: Mapped[IDType] = mapped_column(ForeignKey("externalidtypes.id"), index=True, nullable=True, default=None)
    inner_id: Mapped[IDType] = mapped_column(index=True, nullable=True, default=None)
    outer_id: Mapped[str] = mapped_column(index=True, nullable=True, default=None)
    urlformat: Mapped[str] = mapped_column(index=True, nullable=True, default=None)

    type = relationship("ExternalIdTypeModel", viewonly=True)    