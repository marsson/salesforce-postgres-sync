import logging
import os
import threading
import concurrent.futures
from config.config import Config
from src.salesforce import SalesforceAPI
from redis import Redis
from src.worker import start_rq_worker
from src.wrapper import (
    setup_postgres,
    fetch_tables_wrapper,
    create_table_wrapper,
    insert_data_wrapper,
    ids_wrapper,
    close_postgres
) 
from rq import Queue
from src.utils import wait_for_job


def setup_logging():
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    setup_logging()
    setup_postgres()
    salesforce = SalesforceAPI()

    conn = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,  password=Config.REDIS_PASSWORD
)
    q = Queue(name=Config.QUEUE_NAME, connection=conn)

    # fetching data of conf table from postgres to query data from salesforce
    table_queries_job = q.enqueue(fetch_tables_wrapper)
    table_queries = wait_for_job(table_queries_job)


    # TODO: Modify this loop to work with table_name and filter instead of query
    # TODO: Add a step to check if metadata exists for the object and retrieve it if needed
    # TODO: Add a step to generate a query from the metadata and filter
    for table_name, query in table_queries:
        # TODO: This will change to table_name, filter once the schema is updated

        # TODO: Check if metadata exists for this object
        # TODO: If not, retrieve and store the metadata

        # TODO: Generate a query from the metadata and filter
        # TODO: This will replace the direct use of the query from table_conf

        # fetching data from salesforce using its instance
        query_records_job = q.enqueue(salesforce.fetch_data, query)
        query_records = wait_for_job(query_records_job)

        # TODO: Modify table creation to use the object metadata
        # creating table in postgres data in order to save it saperately
        create_table_job = q.enqueue(create_table_wrapper, table_name)

        # TODO: Modify data insertion to include all fields from the records
        # inserting data in respective table
        insert_data_job = q.enqueue(insert_data_wrapper, table_name, query_records["records"])

        # getting list of ids from saved data on postgres
        get_ids_job = q.enqueue(ids_wrapper, table_name)
        ids = wait_for_job(get_ids_job)

        # deleting data from salesforce NEVER UNLESS SPECIFIED
        #q.enqueue(salesforce.delete_records, ids, table_name)

    # closing postgres connection
    close_postgres()


if __name__ == "__main__":
    # Add this environment variable to avoid the fork() issue on macOS
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    with concurrent.futures.ProcessPoolExecutor() as executor:
        print("starting workers")
        executor.submit(start_rq_worker)
        main()
