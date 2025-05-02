from typing import Annotated, List, Optional
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from ..Base import Base

class FieldDescribe(Base):
    __tablename__ = "field_describes"

    id: Mapped[int] = mapped_column(primary_key=True)
    sobject_id: Mapped[int] = mapped_column(ForeignKey("sobject_describes.id"), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    label: Mapped[Optional[str]]
    type: Mapped[Optional[str]]
    length: Mapped[Optional[int]]

    createable: Mapped[Optional[bool]]
    updateable: Mapped[Optional[bool]]
    nillable: Mapped[Optional[bool]]
    defaulted_on_create: Mapped[Optional[bool]]
    calculated: Mapped[Optional[bool]]
    filterable: Mapped[Optional[bool]]
    sortable: Mapped[Optional[bool]]
    unique: Mapped[Optional[bool]]
    deprecated_and_hidden: Mapped[Optional[bool]]

    reference_to: Mapped[Optional[list]] = mapped_column(JSONB)
    picklist_values: Mapped[Optional[list]] = mapped_column(JSONB)

    sobject: Mapped["SObjectDescribe"] = relationship(back_populates="fields")
