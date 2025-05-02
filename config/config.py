# config/config.py
import logging


class Config:
    #SALESFORCE_USERNAME = "your-username-password"
    #SALESFORCE_PASSWORD = "your-salesforce-password"
    #SALESFORCE_SECURITY_TOKEN = "your-salesforce-sercurity-token"
    SALESFORCE_CLI_ORG_ALIAS = "marsson"

    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = "5432"
    POSTGRES_DB = "devdb"
    POSTGRES_USER = "devuser"
    POSTGRES_PASSWORD = "devpass"

    REDIS_HOST = "localhost"
    REDIS_PORT = "6379"
    REDIS_PASSWORD = "myStrongPassword"

    QUEUE_NAME = "salesforce-postgres-sync"
    LOG_LEVEL = logging.INFO
