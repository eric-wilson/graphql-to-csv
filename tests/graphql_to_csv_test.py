import os
import unittest

from graphql_to_csv.main import GraphQLtoCSV
from pathlib import Path


class TestGraphQL(unittest.TestCase):

    def test_to_csv(self):
        graphql = GraphQLtoCSV()
        graphql_file_path = os.path.join(
            Path(__file__).parent, "files", "test1.graphql"
        )

        output_file_path = os.path.join(
            Path(__file__).parent, ".output", "test1.csv"
        )
        graphql.to_csv(graphql_file_path, output_file_path)

        file_exists = os.path.exists(output_file_path)  
        self.assertEqual(True, file_exists)
