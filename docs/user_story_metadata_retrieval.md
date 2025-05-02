# User Story: Dynamic Salesforce Object Metadata Retrieval and Storage

## Description
As a user of the Salesforce Postgres Sync system, I want to simplify the configuration process by only specifying the Salesforce object name and an optional filter in the configuration table. The system should automatically retrieve the object's metadata, store it in the database, and use it to query all fields from Salesforce.

## Acceptance Criteria
1. The `table_conf` table schema is modified to only require `table_name` (Salesforce object name) and an optional `filter` field (replacing the current `query` field)
2. When a new object is defined in the `table_conf` table, the system automatically retrieves its metadata using the Salesforce describe API
3. The retrieved metadata is stored in the database using the existing `SObject` and `FieldDescribe` models
4. The system dynamically generates a SOQL query that includes all fields from the object's metadata
5. The generated query respects the optional filter specified in the configuration
6. The system creates appropriate tables in PostgreSQL to store the retrieved data
7. All existing functionality continues to work with this new approach

## Business Value
This change will:
1. Simplify the configuration process by requiring less information from users
2. Ensure all available fields are captured without manual query writing
3. Make the system more maintainable by centralizing query generation logic
4. Provide rich metadata that can be used for reporting and analysis
5. Reduce the risk of missing important fields in queries

## Technical Implementation Tasks
1. Modify the `table_conf` table schema to replace the `query` field with an optional `filter` field
2. Update the `PostgreSQL.fetch_table_queries` method to return object names and filters
3. Implement a workflow to check if metadata exists for an object and retrieve it if needed
4. Create a method to dynamically generate SOQL queries based on object metadata and filters
5. Update the main workflow to use the new metadata-driven approach
6. Ensure proper error handling for metadata retrieval and query generation
7. Update tests to reflect the new functionality