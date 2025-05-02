# Salesforce Postgres Sync - API Documentation

This document provides detailed information about the APIs and interfaces available in the Salesforce Postgres Sync project. It serves as a reference for developers who want to use or extend the functionality of the system.

## Table of Contents

1. [Salesforce API](#salesforce-api)
2. [PostgreSQL API](#postgresql-api)
3. [Wrapper Functions](#wrapper-functions)
4. [Worker API](#worker-api)
5. [Utility Functions](#utility-functions)

## Salesforce API

The Salesforce API is implemented in `src/salesforce.py` and provides interfaces for interacting with Salesforce.

### SalesforceAPI Class

#### Constructor

```python
def __init__(self)
```

Initializes a new instance of the SalesforceAPI class and authenticates with Salesforce.

#### Methods

##### fetch_data

```python
def fetch_data(self, query: str) -> dict
```

Fetches data from Salesforce using the provided SOQL query.

**Parameters:**
- `query` (str): A valid SOQL query string

**Returns:**
- `dict`: A dictionary containing the query results with the following structure:
  ```
  {
    "totalSize": int,
    "done": bool,
    "records": list[dict]
  }
  ```

**Example:**
```python
salesforce = SalesforceAPI()
results = salesforce.fetch_data("SELECT Id, Name FROM Account LIMIT 10")
```

##### delete_records

```python
def delete_records(self, ids: list, object_name: str) -> None
```

Deletes records from Salesforce.

**Parameters:**
- `ids` (list): A list of Salesforce record IDs to delete
- `object_name` (str): The name of the Salesforce object (e.g., "Account")

**Example:**
```python
salesforce = SalesforceAPI()
salesforce.delete_records(["001XXXXXXXXXXXXXXX", "001YYYYYYYYYYYYYYY"], "Account")
```

## PostgreSQL API

The PostgreSQL API is implemented in `src/postgres.py` and provides interfaces for interacting with PostgreSQL.

### PostgreSQL Class

#### Constructor

```python
def __init__(self)
```

Initializes a new instance of the PostgreSQL class and establishes a connection to the PostgreSQL database.

#### Methods

##### fetch_table_queries

```python
def fetch_table_queries(self) -> list
```

Fetches table configurations from the `table_conf` table.

**Returns:**
- `list`: A list of tuples containing table names and queries

**Example:**
```python
postgres = PostgreSQL()
table_queries = postgres.fetch_table_queries()
# Returns: [("Account", "SELECT Id, Name FROM Account"), ...]
```

##### create_table

```python
def create_table(self, table_name: str) -> None
```

Creates a table in PostgreSQL if it doesn't already exist.

**Parameters:**
- `table_name` (str): The name of the table to create

**Example:**
```python
postgres = PostgreSQL()
postgres.create_table("Account")
```

##### insert_data

```python
def insert_data(self, table_name: str, records: list) -> None
```

Inserts records into a PostgreSQL table.

**Parameters:**
- `table_name` (str): The name of the table to insert data into
- `records` (list): A list of dictionaries containing the data to insert

**Example:**
```python
postgres = PostgreSQL()
records = [{"Id": "001XXXXXXXXXXXXXXX", "Name": "Test Account"}]
postgres.insert_data("Account", records)
```

##### close

```python
def close(self) -> None
```

Closes the PostgreSQL connection.

**Example:**
```python
postgres = PostgreSQL()
# ... perform operations ...
postgres.close()
```

## Wrapper Functions

Wrapper functions are implemented in `src/wrapper.py` and provide simplified interfaces to the core components.

### Functions

#### setup_postgres

```python
def setup_postgres() -> None
```

Sets up the PostgreSQL connection.

**Example:**
```python
from src.wrapper import setup_postgres
setup_postgres()
```

#### fetch_tables_wrapper

```python
def fetch_tables_wrapper() -> list
```

Fetches table configurations from PostgreSQL.

**Returns:**
- `list`: A list of tuples containing table names and queries

**Example:**
```python
from src.wrapper import fetch_tables_wrapper
table_queries = fetch_tables_wrapper()
```

#### create_table_wrapper

```python
def create_table_wrapper(table_name: str) -> None
```

Creates a table in PostgreSQL.

**Parameters:**
- `table_name` (str): The name of the table to create

**Example:**
```python
from src.wrapper import create_table_wrapper
create_table_wrapper("Account")
```

#### insert_data_wrapper

```python
def insert_data_wrapper(table_name: str, records: list) -> None
```

Inserts records into a PostgreSQL table.

**Parameters:**
- `table_name` (str): The name of the table to insert data into
- `records` (list): A list of dictionaries containing the data to insert

**Example:**
```python
from src.wrapper import insert_data_wrapper
records = [{"Id": "001XXXXXXXXXXXXXXX", "Name": "Test Account"}]
insert_data_wrapper("Account", records)
```

#### ids_wrapper

```python
def ids_wrapper(table_name: str) -> list
```

Retrieves IDs from a PostgreSQL table.

**Parameters:**
- `table_name` (str): The name of the table to retrieve IDs from

**Returns:**
- `list`: A list of IDs

**Example:**
```python
from src.wrapper import ids_wrapper
ids = ids_wrapper("Account")
```

#### close_postgres

```python
def close_postgres() -> None
```

Closes the PostgreSQL connection.

**Example:**
```python
from src.wrapper import close_postgres
close_postgres()
```

## Worker API

The Worker API is implemented in `src/worker.py` and provides functionality for managing Redis Queue workers.

### Functions

#### start_rq_worker

```python
def start_rq_worker() -> None
```

Starts a Redis Queue worker to process jobs.

**Example:**
```python
from src.worker import start_rq_worker
start_rq_worker()
```

## Utility Functions

Utility functions are implemented in `src/utils.py` and provide helper functionality.

### Functions

#### wait_for_job

```python
def wait_for_job(job) -> Any
```

Waits for a Redis Queue job to complete and returns its result.

**Parameters:**
- `job`: A Redis Queue job object

**Returns:**
- The result of the job

**Example:**
```python
from src.utils import wait_for_job
from redis import Redis
from rq import Queue

conn = Redis()
q = Queue(connection=conn)
job = q.enqueue(some_function)
result = wait_for_job(job)
```

## SQLAlchemy Models

The project uses SQLAlchemy ORM for model-based database operations. Models are defined in the `src/models/` directory.

### SObject_Metadata

Defined in `src/models/SObject_Metadata.py`, this model represents Salesforce object metadata.

### Fields_Metadata

Defined in `src/models/Fields_Metadata.py`, this model represents Salesforce field metadata.

## Configuration

Configuration is managed in `config/config.py` through the `Config` class, which provides access to application settings.

### Example

```python
from config.config import Config

# Access configuration values
salesforce_username = Config.SALESFORCE_USERNAME
postgres_host = Config.POSTGRES_HOST
```

## Error Handling

The application implements error handling throughout its components. When using the APIs, be prepared to handle the following exceptions:

- `SalesforceError`: Raised for Salesforce API errors
- `psycopg2.Error`: Raised for PostgreSQL errors
- `redis.RedisError`: Raised for Redis errors
- `Exception`: General exceptions for unexpected errors

## Best Practices

When using these APIs, follow these best practices:

1. **Resource Management**: Always close connections when done (e.g., `close_postgres()`)
2. **Error Handling**: Implement proper error handling around API calls
3. **Batch Processing**: Process large datasets in batches to manage memory usage
4. **Configuration**: Use the configuration system for settings rather than hardcoding values
5. **Testing**: Write tests for your code that uses these APIs