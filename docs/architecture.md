# Salesforce Postgres Sync - Architecture Documentation

## System Overview

The Salesforce Postgres Sync application is designed to synchronize data between Salesforce and PostgreSQL databases. It follows a modular architecture with clear separation of concerns, utilizing Redis for job queuing to ensure reliable and scalable data processing.

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Salesforce    │◄────┤  Sync Service   │────►│   PostgreSQL    │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 │
                        ┌────────▼────────┐
                        │                 │
                        │  Redis Queue    │
                        │                 │
                        └─────────────────┘
```

## Component Description

### 1. Salesforce Integration (src/salesforce.py)

The Salesforce component handles all interactions with the Salesforce API:

- **Authentication**: Manages Salesforce authentication using username/password/token or Salesforce CLI
- **Data Fetching**: Retrieves data from Salesforce using SOQL queries
- **Record Deletion**: Provides functionality to delete records from Salesforce (optional)
- **Error Handling**: Implements retry logic and error handling for API calls

### 2. PostgreSQL Integration (src/postgres.py)

The PostgreSQL component manages all database operations:

- **Connection Management**: Handles database connections and transactions
- **Table Management**: Creates and manages database tables
- **Data Operations**: Inserts, updates, and queries data
- **Configuration Storage**: Manages the table_conf table that stores synchronization configurations

### 3. Redis Queue System (src/worker.py)

The Redis Queue component provides asynchronous job processing:

- **Job Queuing**: Enqueues synchronization jobs
- **Worker Processes**: Processes jobs from the queue
- **Job Monitoring**: Tracks job status and handles failures
- **Concurrency Management**: Manages parallel job execution

### 4. Wrapper Functions (src/wrapper.py)

The wrapper functions provide a simplified interface to the core components:

- **Setup Functions**: Initialize connections and configurations
- **Data Processing Functions**: Handle data transformation and processing
- **Error Handling**: Provide consistent error handling across components

### 5. Main Application (main.py)

The main application orchestrates the entire synchronization process:

- **Workflow Management**: Coordinates the synchronization workflow
- **Configuration**: Sets up logging and application configuration
- **Worker Management**: Starts and manages worker processes
- **Error Recovery**: Handles application-level errors and recovery

## Data Flow

1. **Configuration Retrieval**:
   - The application reads synchronization configurations from the `table_conf` table in PostgreSQL
   - Each configuration specifies a Salesforce object and a SOQL query

2. **Data Fetching**:
   - For each configuration, the application enqueues a job to fetch data from Salesforce
   - The worker processes the job and retrieves the data using the Salesforce API

3. **Table Creation**:
   - The application enqueues a job to create or verify the corresponding table in PostgreSQL
   - The worker processes the job and ensures the table exists with the correct structure

4. **Data Insertion**:
   - The application enqueues a job to insert the fetched data into PostgreSQL
   - The worker processes the job and inserts the data into the appropriate table

5. **Optional Record Deletion**:
   - If configured, the application can enqueue a job to delete the processed records from Salesforce
   - This functionality is disabled by default for safety

## Database Schema

### PostgreSQL Tables

1. **table_conf**:
   - Stores synchronization configurations
   - Schema:
     ```
     id: SERIAL PRIMARY KEY
     table_name: VARCHAR(255) NOT NULL
     query: TEXT NOT NULL
     ```

2. **Dynamically Created Tables**:
   - Tables are created dynamically based on the configurations in `table_conf`
   - Each table corresponds to a Salesforce object
   - The schema of each table matches the fields specified in the SOQL query

## Security Considerations

1. **Authentication**:
   - Salesforce credentials are stored in the configuration file
   - Consider using environment variables or a secure credential store in production

2. **Data Protection**:
   - Sensitive data should be encrypted in transit and at rest
   - Implement proper access controls for the PostgreSQL database

3. **Error Handling**:
   - Failed jobs are logged and can be retried
   - Implement monitoring to detect and alert on synchronization failures

## Scalability

The architecture is designed to scale in several ways:

1. **Horizontal Scaling**:
   - Multiple worker processes can be deployed to handle increased load
   - Redis Queue supports distributed workers across multiple machines

2. **Batch Processing**:
   - Large datasets can be processed in batches to manage memory usage
   - Implement incremental synchronization for very large datasets

3. **Performance Optimization**:
   - Use database indexes for frequently queried fields
   - Implement caching for frequently accessed data
   - Optimize SOQL queries to retrieve only necessary fields

## Monitoring and Logging

1. **Logging**:
   - The application uses Python's logging module
   - Log level can be configured in `config/config.py`
   - Consider integrating with a centralized logging system in production

2. **Monitoring**:
   - Monitor Redis Queue for job failures and backlogs
   - Implement health checks for all components
   - Set up alerts for synchronization failures or performance issues

## Future Enhancements

1. **Web Interface**:
   - Add a web-based administration interface for managing synchronization configurations
   - Implement dashboards for monitoring synchronization status and performance

2. **Advanced Synchronization**:
   - Implement bidirectional synchronization
   - Add support for conflict resolution
   - Implement field mapping and data transformation

3. **Additional Data Sources**:
   - Extend the architecture to support additional data sources beyond Salesforce
   - Implement adapters for different data sources and destinations