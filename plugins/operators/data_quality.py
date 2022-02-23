from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    
    check_no_data = """
    SELECT COUNT(*)
    FROM {} 
    """
    type_check = """
    SELECT {}
    FROM {}
    LIMIT 1
    """

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id = "redshift",
                 table = {},
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table

    def execute(self, context):

        self.log.info("Started checking data quality")
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        errors = []
        
        for tb in self.table.keys():
            sql_query = DataQualityOperator.check_no_data.format(tb)
            records = redshift_hook.get_records(sql_query)[0]
            record = records[0]
            self.log.info(f"Number of record of {tb} table: {record}")

            if record < 0:
                errors.append(tb)
        
        for tb_name, ls in self.table.items():
            sql_query = DataQualityOperator.type_check.format(ls[0], tb_name)
            record = redshift_hook.get_records(sql_query)[0]
            cell = record[0]
            self.log.info(f" record type check: the cell is {cell}")
            if ls[1] == 'str':
                if type(cell) is str:
                    self.log.info(f"The column '{ls[0]}' of '{tb_name}' table is string type. Data check passed. ")
                else:
                    self.log.info(f"The column '{ls[0]}' of '{tb_name}' table is not string type. Data check unpassed. ")
        
            elif ls[1] == 'int':
                if type(cell) is int:
                    self.log.info(f"The column '{ls[0]}' of '{tb_name}' table is int type. Data check passed. ")
                else:
                    self.log.info(f"The column '{ls[0]}' of '{tb_name}' table is not int type. Data check unpassed. ")
            else:
                self.log.info(f"The column '{ls[0]}' of '{tb_name}' table has failed data check.")


        if len(errors) > 0:
            for e in errors:
                self.log.info(f"Error at {e}")
                raise ValueError("Couldn't pass data quality check ")

        self.log.info(f"Passed the data quality tests per table")
