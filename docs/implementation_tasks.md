# Implementation Tasks for Dynamic Salesforce Object Metadata Retrieval

This document outlines the specific implementation tasks required to fulfill the [User Story: Dynamic Salesforce Object Metadata Retrieval and Storage](user_story_metadata_retrieval.md).

## Database Schema Changes

1. **Modify the `table_conf` table schema**
   - Change the `query` column to an optional `filter` column
   - SQL example:
     ```sql
     ALTER TABLE table_conf 
     DROP COLUMN query,
     ADD COLUMN filter TEXT NULL;
     ```

2. **Ensure SObject metadata tables are properly set up**
   - Verify that the `sobject_describes` table is created with the correct schema
   - Verify that the `field_describes` table is created with the correct schema
   - Ensure proper foreign key relationships between these tables

## PostgreSQL Class Changes

1. **Update the `fetch_table_queries` method**
   - Modify to return table_name and filter instead of query
   - Update SQL query to reflect the new schema

2. **Enhance the `create_table` method**
   - Modify to create tables based on object metadata
   - Use field metadata to determine column types
   - Consider using SQLAlchemy models for table creation

3. **Update the `insert_data` method**
   - Modify to insert all fields from the records
   - Use object metadata to determine which fields to insert
   - Consider using SQLAlchemy models for data insertion

## SalesforceAPI Class Changes

1. **Enhance the `fetch_data` method**
   - Modify to accept an object name and filter instead of a full query
   - Use object metadata to dynamically generate a query

2. **Implement the `generate_query_from_metadata` method**
   - Retrieve object metadata if not already cached
   - Extract all queryable field names from the metadata
   - Generate a SOQL query with all fields
   - Add the filter clause if provided

## SObject Model Changes

1. **Fix inheritance from Base**
   - Ensure the SObject class inherits from Base for proper SQLAlchemy integration

2. **Add methods to work with metadata**
   - Add methods to populate the model from Salesforce metadata
   - Add methods to generate table creation SQL from metadata
   - Add methods to generate field mappings for data insertion

3. **Enhance query generation**
   - Implement `get_all_queryable_fields` method to get all queryable fields
   - Implement `generate_complete_query` method to generate a query with all fields

## Main Workflow Changes

1. **Update the main processing loop**
   - Modify to work with table_name and filter instead of query
   - Add a step to check if metadata exists for the object
   - Add a step to retrieve and store metadata if needed
   - Add a step to generate a query from the metadata and filter

2. **Update the job enqueuing**
   - Modify job parameters to reflect the new workflow
   - Ensure proper error handling for metadata retrieval

## Testing

1. **Update existing tests**
   - Modify tests to reflect the new schema and workflow
   - Add tests for metadata retrieval and storage
   - Add tests for dynamic query generation

2. **Add new tests**
   - Test the end-to-end workflow with the new approach
   - Test edge cases like objects with many fields
   - Test error handling for invalid objects or filters

## Documentation

1. **Update user documentation**
   - Document the new configuration approach
   - Provide examples of using filters

2. **Update developer documentation**
   - Document the metadata-driven architecture
   - Explain how to extend or customize the implementation