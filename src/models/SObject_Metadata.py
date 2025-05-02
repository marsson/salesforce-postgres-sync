from typing import Annotated, List, Optional
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from ..Base import Base


class SObject:
    # TODO: Ensure this class inherits from Base for proper SQLAlchemy integration
    __tablename__ = "sobject_describes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    label: Mapped[Optional[str]]
    label_plural: Mapped[Optional[str]]
    key_prefix: Mapped[Optional[str]]

    custom: Mapped[Optional[bool]]
    custom_setting: Mapped[Optional[bool]]
    activateable: Mapped[Optional[bool]]
    createable: Mapped[Optional[bool]]
    deletable: Mapped[Optional[bool]]
    deprecated_and_hidden: Mapped[Optional[bool]]
    feed_enabled: Mapped[Optional[bool]]
    layoutable: Mapped[Optional[bool]]
    mergeable: Mapped[Optional[bool]]
    queryable: Mapped[Optional[bool]]
    replicateable: Mapped[Optional[bool]]
    retrieveable: Mapped[Optional[bool]]
    searchable: Mapped[Optional[bool]]
    triggerable: Mapped[Optional[bool]]
    undeletable: Mapped[Optional[bool]]
    updateable: Mapped[Optional[bool]]

    urls: Mapped[Optional[dict]] = mapped_column(JSONB)

    # TODO: Add methods to populate this model from Salesforce metadata
    # TODO: Add methods to generate table creation SQL from this metadata
    # TODO: Add methods to generate field mappings for data insertion

    fields: Mapped[List["FieldDescribe"]] = relationship(back_populates="sobject", cascade="all, delete-orphan")

    # This appears to be a duplicate of the above line - should be removed
    fields = relationship("FieldDescribe", back_populates="sobject", cascade="all, delete-orphan")

    def __init__(self, sf_instance, object_name):
        """
        Initialize a generic SObject.

        Args:
            sf_instance: Salesforce instance from simple_salesforce
            object_name: API name of the Salesforce object (e.g., 'Account', 'Contact')
        """
        self._sf = sf_instance
        self._object_name = object_name
        self._sobject = getattr(self._sf, object_name)
        self._selected_fields


    def describe(self):
        """Get the object's metadata description"""
        return self._sobject.describe()

    def query(self, query):
        """Execute a SOQL query"""
        return self._sf.query_all(query)

    def get(self, record_id):
        """Get a single record by ID"""
        return self._sobject.get(record_id)

    def create(self, data):
        """Create a new record"""
        return self._sobject.create(data)

    def update(self, record_id, data):
        """Update an existing record"""
        return self._sobject.update(record_id, data)

    def delete(self, record_id):
        """Delete a record"""
        return self._sobject.delete(record_id)

    def get_by_custom_query(self, fields=None, where=None, limit=None):
        """
        Construct and execute a SOQL query with the given parameters

        Args:
            fields: List of field names to query
            where: WHERE clause string
            limit: Maximum number of records to return
        """
        # TODO: Enhance this method to use object metadata to determine available fields
        # TODO: If fields is None, use all queryable fields from the metadata
        # TODO: Add validation to ensure requested fields exist in the object
        fields_str = ", ".join(fields) if fields else "Id"
        query = f"SELECT {fields_str} FROM {self._object_name}"

        if where:
            query += f" WHERE {where}"
        if limit:
            query += f" LIMIT {limit}"

        return self.query(query)

    # TODO: Add a method to get all queryable fields from the metadata
    # def get_all_queryable_fields(self):
    #     """
    #     Get all queryable fields from the object metadata
    #     
    #     Returns:
    #         list: List of field names that can be queried
    #     """
    #     pass

    # TODO: Add a method to generate a complete SOQL query with all fields
    # def generate_complete_query(self, filter_clause=None):
    #     """
    #     Generate a SOQL query with all queryable fields
    #     
    #     Args:
    #         filter_clause (str, optional): WHERE clause to filter the query
    #         
    #     Returns:
    #         str: A SOQL query string with all queryable fields
    #     """
    #     pass
