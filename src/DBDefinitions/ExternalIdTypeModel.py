import sqlalchemy
from sqlalchemy.orm import relationship, Mapped, mapped_column

from sqlalchemy import (
    ForeignKey,
)
from .BaseModel import BaseModel, IDType

class ExternalIdTypeModel(BaseModel):
    __tablename__ = "externalidtypes"

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    urlformat: Mapped[str] = mapped_column(default=None, nullable=True)

    master_id: Mapped[IDType] = mapped_column(ForeignKey("externalidcategories.id"), index=True, default=None, nullable=True)

    master_type = relationship(
        "ExternalIdTypeModel", 
        viewonly=True, 
        uselist=False,
        remote_side="ExternalIdTypeModel.id",
        back_populates="sub_types"
    )

    sub_types = relationship(
        "ExternalIdTypeModel", 
        viewonly=True, 
        uselist=True,
        back_populates="master_type"
    )

    external_ids = relationship("ExternalIdModel", viewonly=True)    