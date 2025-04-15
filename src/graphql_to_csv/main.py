from graphql import parse, build_schema, GraphQLSchema
from graphql.type import GraphQLObjectType, GraphQLInputObjectType
import csv
import os


class GraphQLtoCSV:
    def __init__(self):
        pass

    def to_csv(self, graphql_path: str, output_file: str) -> str:
        """
        To Csv
            Args:
                graphql_path (str): path to a graphql file
                output_file (str): path to a cvs file
        """

        # Write to CSV
        if not output_file:
            raise ValueError("Output file path is required")

        if not output_file.endswith(".csv"):
            raise ValueError("Output file must have a .csv extension")

        # Load the GraphQL schema file
        schema: GraphQLSchema = self.__build_schema(graphql_path)

        rows = self.__build_rows(schema=schema)

        directory = os.path.dirname(output_file)

        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "Type",
                "Field",
                "Field Type",
                "Is Required",
                "Is List",
                "Description",
                "Mapped To",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        print("✅ Mapping spreadsheet created: graphql_schema_mapping.csv")

        return output_file

    def __build_schema(self, graphql_path: str) -> GraphQLSchema:
        """
        Build Schema
            Args:
                graphql_path (str): path to a graphql file
        """

        self.__validate_inputs(graphql_path)

        with open(graphql_path, "r", encoding="utf-8") as file:
            schema_text = file.read()

        schema_ast = parse(schema_text)
        schema = build_schema(schema_text)

        return schema

    def __build_rows(self, schema: GraphQLSchema) -> list:
        """
        Build Rows
            Args:
                schema (GraphQLSchema): graphql schema
        """

        rows = []

        for type_name, gql_type in schema.type_map.items():
            if type_name.startswith("__") or type_name in [
                "Query",
                "Mutation",
                "Subscription",
            ]:
                continue  # skip introspection and root types
            if isinstance(gql_type, (GraphQLObjectType, GraphQLInputObjectType)):
                for field_name, field in gql_type.fields.items():
                    field_type = field.type
                    is_required = False
                    is_list = False

                    # Traverse type wrappers
                    while hasattr(field_type, "of_type"):
                        if str(type(field_type)).endswith("NonNullType"):
                            is_required = True
                        if str(type(field_type)).endswith("ListType"):
                            is_list = True
                        field_type = field_type.of_type

                    rows.append(
                        {
                            "Type": type_name,
                            "Field": field_name,
                            "Field Type": str(field_type),
                            "Is Required": is_required,
                            "Is List": is_list,
                            "Description": field.description or "",
                            "Mapped To": "",
                        }
                    )

        # for type_name, type_obj in schema.type_map.items():
        #     if not hasattr(type_obj, "fields"):
        #         continue

        #     for field_name, field_obj in type_obj.fields.items():
        #         row = {
        #             "Type": type_name,
        #             "Field": field_name,
        #             "Field Type": str(field_obj.type),
        #             "Is Required": str(field_obj.type).endswith("!"),
        #             "Is List": str(field_obj.type).startswith("["),
        #             "Description": field_obj.description or "",
        #             "Mapped To": "",
        #         }
        #         rows.append(row)

        return rows

    def __validate_inputs(self, graphql_path: str) -> None:

        if not graphql_path.endswith(".graphql"):
            raise ValueError("GraphQL file must have a .graphql extension")

        if not os.path.exists(graphql_path):
            raise FileNotFoundError(f"GraphQL file not found: {graphql_path}")


def main():
    q_to_csv = GraphQLtoCSV()


if __name__ == "__main__":
    main()
