# Salesforce Postgres Sync - Documentation

Welcome to the Salesforce Postgres Sync documentation. This documentation provides comprehensive information about the project, its features, architecture, APIs, and implementation plan.

## Documentation Index

### Overview
- [README](../README.md) - Project overview, features, prerequisites, and basic usage

### Detailed Documentation
- [Feature Documentation](feature_documentation.md) - Detailed information about the features and how to use them
- [API Documentation](api_documentation.md) - Reference for the APIs and interfaces available in the project
- [Architecture Documentation](architecture.md) - System overview, component descriptions, and design details
- [Implementation Plan](implementation_plan.md) - Project phases, milestones, tasks, and timeline

## Quick Start

To get started with the Salesforce Postgres Sync project:

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

4. **Set up the database infrastructure:**
   - Option 1: Use Docker Compose:
     ```bash
     docker-compose -f docker-composer.yml up -d
     ```
   - Option 2: Use existing PostgreSQL and Redis instances

5. **Initialize the PostgreSQL database:**
   - Create the `table_conf` table and insert configuration entries

6. **Run the application:**
   ```bash
   python main.py
   ```

## Documentation Structure

The documentation is organized to provide information at different levels of detail:

- **README.md**: Provides a high-level overview of the project, its features, and basic usage instructions.
- **Feature Documentation**: Describes each feature in detail, including how it works and how to use it.
- **API Documentation**: Provides a reference for the APIs and interfaces available in the project.
- **Architecture Documentation**: Explains the system's components, their interactions, and the overall design.
- **Implementation Plan**: Outlines the project phases, milestones, tasks, and timeline.

## Contributing to Documentation

If you'd like to contribute to the documentation:

1. Fork the repository
2. Make your changes
3. Submit a pull request

Please follow these guidelines when contributing:

- Use clear, concise language
- Include examples where appropriate
- Follow the existing documentation structure
- Update the documentation index if adding new files

## Getting Help

If you need help with the Salesforce Postgres Sync project:

- Check the documentation for information about your issue
- Look for examples in the code
- Open an issue on GitHub if you've found a bug or have a feature request