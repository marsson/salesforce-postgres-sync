import logging
from config.config import Config
from simple_salesforce import Salesforce
from src.SalesforceFunctions import get_sf_auth_and_instance


class SalesforceAPI:
    def __init__(self):
        """
        Constructor method to initialize Salesforce instance and logger.
        """
        self.sf = self.get_salesforce_instance()  # Initialize Salesforce instance
        self.logger = logging.getLogger(__name__)

    def get_salesforce_instance(self):
        """
        Method to authenticate and initialize Salesforce instance.
        Returns:
            Salesforce instance.
        """
        try:
            #session_id, instance = SalesforceLogin(
            #    username=Config.SALESFORCE_USERNAME,
            #    password=Config.SALESFORCE_PASSWORD,
            #    security_token=Config.SALESFORCE_SECURITY_TOKEN,
            #)
            #print(
            #    f"INFO: initiated Salesforce instance with {Config.SALESFORCE_USERNAME}"
            #)
            #return Salesforce(instance=instance, session_id=session_id)
            session_id, instance = get_sf_auth_and_instance(Config.SALESFORCE_CLI_ORG_ALIAS)
            print(f"INFO: initiated Salesforce instance with cli:{Config.SALESFORCE_CLI_ORG_ALIAS}")
            print(f"INFO: initiated Salesforce instance :{instance}")
            filtered_instance = instance.removeprefix("https://")
            return Salesforce(instance=filtered_instance, session_id=session_id)

        except Exception as e:
            print(f"Error while initiating Salesforce instance: {str(e)}")

    def fetch_data(self, query):
        """
        Method to fetch data from Salesforce using a SOQL query.
        Args:
            query (str): SOQL query to fetch data.
        Returns:
            Query result containing fetched data.
        """
        try:
            # TODO: Modify this method to accept an object name and filter instead of a full query
            # TODO: Use the object metadata to dynamically generate a query with all fields
            query_records = self.sf.query_all(query)
            self.logger.info("Fetched data from Salesforce")
            return query_records
        except Exception as e:
            self.logger.error(f"Error while fetching data from Salesforce: {str(e)}")

    def generate_query_from_metadata(self, object_name, filter_clause=None):
        """
        TODO: Implement this method to generate a SOQL query from object metadata

        Args:
            object_name (str): Name of the Salesforce object
            filter_clause (str, optional): WHERE clause to filter the query

        Returns:
            str: A SOQL query string with all fields from the object metadata
        """
        # TODO: Retrieve object metadata if not already cached
        # TODO: Extract all queryable field names from the metadata
        # TODO: Generate a SOQL query with all fields
        # TODO: Add the filter clause if provided
        pass

    def delete_records(self, record_ids, table_name):
        """
        Method to delete records from Salesforce.
        Args:
            record_ids (list): List of record IDs to be deleted.
            table_name (str): Name of the Salesforce object from which records are to be deleted.
        """
        try:
            self.delete_associated_records(record_ids, ["Entitlement", "Case", "Opportunity"])

            for id in record_ids:
                self.sf.__getattr__(table_name).delete(id)
            self.logger.info("Deleted data from Salesforce")
        except Exception as e:
            self.logger.error(f"Error while deleting data from Salesforce: {str(e)}")

    def fetch_object_metadata(self, sObject_api_name: str):
        """
        Method to fetch metadata for a Salesforce object.
        Args:
            sObject_api_name (str): API name of the Salesforce object
        Returns:
            dict: Object metadata schema
        """
        try:
            schema = getattr(self.sf, sObject_api_name).describe()
            self.logger.info(f"Getting Describe from object {sObject_api_name}")
            return schema
        except Exception as e:
            self.logger.error(f"Error while fetching schema from salesforce object: {str(e)}")
            raise  # Re-raise the exception after logging
