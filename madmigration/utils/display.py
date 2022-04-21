import imp
from utils.helpers import issue_url

class CMDDisplay:
    def display_reading_configurations(self):
        print(
            """
            Starting Engine and reading configuration from file
            """
        )

    def display_initializing_db_creation(self, source_database: str, dest_database: str):
        print(
            """
            
            """
        )

    def display_initializing_table_setup(self, old_table: str, new_table: str):
        print(
            """
            
            """
        )

    def display_begin_copying_data_from_old_db(self):
        print(
            """
            
            """
        )

    def display_finish_copy_data_from_old_db(self):
        print(
            """
            
            """
        )

    def display_interupted_copying_data_from_old_db(self):
        print(
            """
            
            """
        )

    def display_rollback_copying_data_from_db(self):
        print(
            """
            
            """
        )

    def display_configurations(self):
        print(
            """
            
            """
        )

    def display_database_does_not_exist(self):
        print(
            """
            
            """
        )

    def display_database_not_supported(self):
        print(
            f"""
            Database entered is not currently supported in Mad Migration

            feel free to open issues 👉'{issue_url()} to add support'
            """
        )

    def display_configuration_file_missing(self):
        print(
            f"""
            No Configuration file included in path

            Add mad_migration.yaml or mad_migration.json file to project path
            """
        )

    # def display_table_relationships(self):
    #     pass



cmd_diplay_utiltity = CMDDisplay()