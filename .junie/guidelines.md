# Development Guidelines for Salesforce Postgres Sync

This document provides guidelines and instructions for developing and maintaining the Salesforce Postgres Sync project.

## Build/Configuration Instructions

### Prerequisites
- Python 3.9 or higher
- Salesforce CLI (for authentication)
- Docker and Docker Compose (optional, for containerized development)

### Setting Up the Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishalpatidar99/salesforce-postgres-sync.git
   cd salesforce-postgres-sync
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   - Edit `config/config.py` to set your Salesforce and PostgreSQL credentials
   - For Salesforce authentication, you can either:
     - Use username/password/security token (uncomment and fill in the relevant lines)
     - Use Salesforce CLI authentication (set `SALESFORCE_CLI_ORG_ALIAS` to your org alias)

4. **Set up the database infrastructure:**
   - Option 1: Use Docker Compose (recommended for development):
     ```bash
     docker-compose -f docker-composer.yml up -d
     ```
   - Option 2: Use existing PostgreSQL and Redis instances:
     - Ensure PostgreSQL and Redis are running
     - Update `config/config.py` with the correct connection details

5. **Initialize the PostgreSQL database:**
   - Create the `table_conf` table:
     ```sql
     CREATE TABLE IF NOT EXISTS table_conf (
         id SERIAL PRIMARY KEY,
         table_name VARCHAR(255) NOT NULL,
         query TEXT NOT NULL
     );
     ```
   - Insert configuration entries:
     ```sql
     INSERT INTO table_conf (table_name, query) VALUES ('Account', 'SELECT Id, Name FROM Account');
     ```

## Testing Information

### Running Tests

The project uses the Python `unittest` framework for testing. Tests are located in the `tests` directory.

To run all tests:
```bash
python -m unittest discover tests
```

To run a specific test file:
```bash
python -m unittest tests/test_postgres.py
```

### Writing Tests

1. **Create test files in the `tests` directory:**
   - Name test files with the prefix `test_`
   - Organize tests by module (e.g., `test_postgres.py`, `test_salesforce.py`)

2. **Use unittest and mocking:**
   - Extend `unittest.TestCase` for test classes
   - Use `unittest.mock` for mocking external dependencies
   - Example:
     ```python
     import unittest
     from unittest.mock import patch, MagicMock
     from src.postgres import PostgreSQL

     class TestPostgreSQL(unittest.TestCase):
         @patch('psycopg2.connect')
         def setUp(self, mock_connect):
             # Mock setup code
             ...
         
         def test_method(self):
             # Test code
             ...
     ```

3. **Run tests before committing changes**

### Test Coverage

To measure test coverage, install and use the `coverage` package:

```bash
pip install coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Generates HTML report in htmlcov/
```

## Additional Development Information

### Project Structure

- `config/`: Configuration files
- `src/`: Source code
  - `models/`: SQLAlchemy models
  - `Base.py`: SQLAlchemy base configuration
  - `postgres.py`: PostgreSQL interaction
  - `salesforce.py`: Salesforce API interaction
  - `worker.py`: Redis queue worker
  - `wrapper.py`: Wrapper functions for the main application
- `tests/`: Test files

### Code Style

- Follow PEP 8 guidelines for Python code
- Use docstrings for classes and methods (as seen in the existing code)
- Use type hints where appropriate

### Debugging

- The application uses Python's logging module
- Log level can be configured in `config/config.py`
- Logs are output to the console by default

### Working with Salesforce

- The application uses the `simple-salesforce` library for Salesforce API interactions
- Authentication is handled in the `SalesforceAPI` class in `src/salesforce.py`
- SOQL queries are defined in the `table_conf` table in PostgreSQL

### Working with PostgreSQL

- Direct database operations are handled by the `PostgreSQL` class in `src/postgres.py`
- SQLAlchemy ORM is set up in `src/Base.py` for model-based operations
- Models are defined in the `src/models/` directory

### Redis Queue

- The application uses Redis and RQ for job queuing
- The worker is started in `main.py`
- Jobs are enqueued in `main.py` and processed by the worker