import unittest
from unittest.mock import patch, MagicMock
from src.postgres import PostgreSQL

class TestPostgreSQL(unittest.TestCase):
    @patch('psycopg2.connect')
    def setUp(self, mock_connect):
        # Mock the database connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        
        # Create PostgreSQL instance
        self.postgres = PostgreSQL()
    
    def test_fetch_table_queries(self):
        # Set up mock return value
        expected_result = [('table1', 'SELECT * FROM table1'), ('table2', 'SELECT * FROM table2')]
        self.mock_cursor.fetchall.return_value = expected_result
        
        # Call the method
        result = self.postgres.fetch_table_queries()
        
        # Assert the method was called correctly
        self.mock_cursor.execute.assert_called_once_with("SELECT table_name, query FROM table_conf;")
        
        # Assert the result is as expected
        self.assertEqual(result, expected_result)
    
    def test_create_table(self):
        # Call the method
        self.postgres.create_table('test_table')
        
        # Assert the execute method was called with the correct SQL
        self.mock_cursor.execute.assert_called_once()
        self.assertTrue('CREATE TABLE IF NOT EXISTS test_table' in self.mock_cursor.execute.call_args[0][0])
        
        # Assert commit was called
        self.mock_connection.commit.assert_called_once()
    
    def test_insert_data(self):
        # Set up test data
        table_name = 'test_table'
        records = [{'Id': '001'}, {'Id': '002'}]
        
        # Call the method
        self.postgres.insert_data(table_name, records)
        
        # Assert execute was called twice (once for each record)
        self.assertEqual(self.mock_cursor.execute.call_count, 2)
        
        # Assert commit was called
        self.mock_connection.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()