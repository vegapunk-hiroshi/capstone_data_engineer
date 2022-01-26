from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    truncate_sql = """
    TRUNCATE TABLE {};
    """
    
    insert_sql = """
    INSERT INTO {} {};
    """

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id = "redshift",
                 table = "",
                 truncate_data = False,
                 sql_query = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.truncate_data = truncate_data
        self.sql_query = sql_query

    def execute(self, context):
        self.log.info(f"Delete existing data: {self.truncate_data}.")
        self.log.info(f"Started execution of LoadFactOperator on {self.table}")
        
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
       
        if self.truncate_data:
            redshift_hook.run(LoadFactOperator.truncate_sql.format(self.table))
        
        redshift_hook.run(LoadFactOperator.insert_sql.format(self.table, self.sql_query))
        
        self.log.info(f"Completed insertion of LoadFactOperator on {self.table}")
        