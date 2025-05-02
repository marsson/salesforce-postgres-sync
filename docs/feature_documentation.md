# Salesforce Postgres Sync - Feature Documentation

This document provides detailed information about the features available in the Salesforce Postgres Sync project, including how they work and how to use them.

## Table of Contents

1. [Data Synchronization](#data-synchronization)
2. [Table Configuration Management](#table-configuration-management)
3. [Asynchronous Processing](#asynchronous-processing)
4. [Error Handling and Retry Mechanisms](#error-handling-and-retry-mechanisms)
5. [Salesforce Authentication Options](#salesforce-authentication-options)
6. [Containerized Development](#containerized-development)

## Data Synchronization

### Overview

The core feature of the Salesforce Postgres Sync project is the ability to synchronize data between Salesforce and PostgreSQL databases. The synchronization process fetches data from Salesforce based on configured queries and stores it in corresponding PostgreSQL tables.

### How It Works

1. The application reads synchronization configurations from the `table_conf` table in PostgreSQL.
2. For each configuration, it fetches data from Salesforce using the specified SOQL query.
3. It creates or verifies the corresponding table in PostgreSQL.
4. It inserts the fetched data into the PostgreSQL table.
5. Optionally, it can delete the processed records from Salesforce (disabled by default).

### Usage

To use the data synchronization feature:

1. Ensure your Salesforce and PostgreSQL credentials are configured in `config/config.py`.
2. Set up the `table_conf` table in PostgreSQL with your desired synchronization configurations.
3. Run the application:
   ```bash
   python main.py
   ```

### Example Configuration

To synchronize Account data from Salesforce to PostgreSQL:

1. Insert a configuration into the `table_conf` table:
   ```sql
   INSERT INTO table_conf (table_name, query) 
   VALUES ('Account', 'SELECT Id, Name, Industry, Type FROM Account');
   ```

2. Run the application to synchronize the data.

### Customization Options

- **Field Selection**: Modify the SOQL query in the `table_conf` table to select specific fields.
- **Filtering**: Add WHERE clauses to the SOQL query to filter the data being synchronized.
- **Sorting**: Add ORDER BY clauses to the SOQL query to control the order of data retrieval.
- **Limiting**: Add LIMIT clauses to the SOQL query to control the amount of data retrieved.

## Table Configuration Management

### Overview

The Table Configuration Management feature allows you to define which Salesforce objects and fields should be synchronized to PostgreSQL. Configurations are stored in the `table_conf` table in PostgreSQL.

### How It Works

1. The `table_conf` table stores configurations with the following columns:
   - `id`: A unique identifier for the configuration
   - `table_name`: The name of the Salesforce object and corresponding PostgreSQL table
   - `query`: The SOQL query used to fetch data from Salesforce

2. When the application runs, it reads these configurations and processes each one.

### Usage

To manage table configurations:

1. Create the `table_conf` table if it doesn't exist:
   ```sql
   CREATE TABLE IF NOT EXISTS table_conf (
       id SERIAL PRIMARY KEY,
       table_name VARCHAR(255) NOT NULL,
       query TEXT NOT NULL
   );
   ```

2. Insert configurations for the Salesforce objects you want to synchronize:
   ```sql
   INSERT INTO table_conf (table_name, query) 
   VALUES ('Account', 'SELECT Id, Name FROM Account');
   
   INSERT INTO table_conf (table_name, query) 
   VALUES ('Contact', 'SELECT Id, FirstName, LastName, Email FROM Contact');
   ```

3. Update existing configurations as needed:
   ```sql
   UPDATE table_conf 
   SET query = 'SELECT Id, Name, Industry, Type FROM Account'
   WHERE table_name = 'Account';
   ```

4. Delete configurations you no longer need:
   ```sql
   DELETE FROM table_conf 
   WHERE table_name = 'Contact';
   ```

### Best Practices

- Start with a small subset of fields to ensure the synchronization works as expected.
- Use WHERE clauses to limit the amount of data being synchronized, especially for large objects.
- Consider the relationships between objects when defining synchronization order.
- Regularly review and update your configurations as your data needs change.

## Asynchronous Processing

### Overview

The Asynchronous Processing feature uses Redis Queue (RQ) to process synchronization jobs asynchronously. This allows for better scalability, fault tolerance, and performance.

### How It Works

1. The application enqueues jobs for various operations (fetching data, creating tables, inserting data).
2. Redis Queue workers process these jobs asynchronously.
3. The application can wait for job completion when necessary or continue processing other tasks.

### Usage

The asynchronous processing is built into the application and requires no special configuration beyond setting up Redis. However, you can customize the behavior:

1. Configure Redis connection details in `config/config.py`:
   ```python
   REDIS_HOST = 'localhost'
   REDIS_PORT = 6379
   REDIS_PASSWORD = None
   QUEUE_NAME = 'salesforce_postgres_sync'
   ```

2. Start additional workers for better performance:
   ```bash
   python -c "from src.worker import start_rq_worker; start_rq_worker()"
   ```

### Benefits

- **Scalability**: Multiple workers can process jobs in parallel.
- **Fault Tolerance**: Failed jobs can be retried automatically.
- **Resource Management**: Long-running tasks don't block the main application.
- **Monitoring**: Job status and progress can be monitored.

## Error Handling and Retry Mechanisms

### Overview

The Error Handling and Retry Mechanisms feature ensures that synchronization operations are resilient to transient failures and provides clear error reporting.

### How It Works

1. The application implements error handling at multiple levels:
   - API-level error handling for Salesforce and PostgreSQL operations
   - Job-level error handling for Redis Queue jobs
   - Application-level error handling for the main workflow

2. Retry mechanisms are implemented for operations that may fail due to transient issues:
   - Salesforce API calls with rate limiting
   - Database connections with network issues
   - Redis operations with temporary unavailability

### Usage

Error handling is built into the application, but you can customize logging and monitoring:

1. Configure logging level in `config/config.py`:
   ```python
   LOG_LEVEL = logging.INFO  # or logging.DEBUG, logging.WARNING, etc.
   ```

2. Implement additional monitoring by checking job status and logs.

### Error Types and Handling

- **Salesforce API Errors**: Handled with retries for rate limiting and authentication issues.
- **PostgreSQL Errors**: Handled with connection retries and transaction management.
- **Redis Errors**: Handled with connection retries and job requeuing.
- **General Exceptions**: Logged with detailed information for troubleshooting.

## Salesforce Authentication Options

### Overview

The Salesforce Authentication Options feature provides multiple ways to authenticate with Salesforce, allowing for flexibility in different environments.

### Authentication Methods

1. **Username/Password/Security Token**:
   - Provide your Salesforce username, password, and security token in `config/config.py`.
   - Simple to set up but requires storing credentials in the configuration file.

2. **Salesforce CLI Authentication**:
   - Use Salesforce CLI to authenticate and store the session.
   - More secure as it doesn't require storing credentials in the configuration file.
   - Useful for development environments.

### Configuration

Configure authentication in `config/config.py`:

```python
# Option 1: Username/Password/Security Token
SALESFORCE_USERNAME = 'your_username@example.com'
SALESFORCE_PASSWORD = 'your_password'
SALESFORCE_SECURITY_TOKEN = 'your_security_token'

# Option 2: Salesforce CLI
SALESFORCE_CLI_ORG_ALIAS = 'your_org_alias'
```

### Best Practices

- Use environment variables for credentials in production environments.
- Rotate security tokens regularly.
- Use Salesforce CLI authentication for development to avoid storing credentials.
- Implement proper access controls for configuration files containing credentials.

## Containerized Development

### Overview

The Containerized Development feature provides a Docker-based development environment for the project, ensuring consistency across different development machines and simplifying setup.

### How It Works

1. The project includes a `docker-composer.yml` file that defines services for:
   - PostgreSQL database
   - Redis queue
   - Python application

2. Docker Compose manages these services and their dependencies.

### Usage

To use the containerized development environment:

1. Ensure Docker and Docker Compose are installed on your system.

2. Start the environment:
   ```bash
   docker-compose -f docker-composer.yml up -d
   ```

3. Access the services:
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

4. Stop the environment when done:
   ```bash
   docker-compose -f docker-composer.yml down
   ```

### Benefits

- **Consistency**: Ensures all developers work with the same environment.
- **Isolation**: Keeps development dependencies separate from the host system.
- **Simplicity**: Simplifies setup and configuration of required services.
- **Portability**: Works the same way across different operating systems.

### Customization

You can customize the Docker environment by editing the `docker-composer.yml` file:

- Change port mappings to avoid conflicts with existing services.
- Modify resource allocations for containers.
- Add additional services as needed.
- Configure persistent volumes for data storage.