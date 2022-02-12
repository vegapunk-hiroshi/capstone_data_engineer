from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

from operators import (StagingOperator, LoadFactOperator,LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries
from create_tables import CreateTable

from os import environ
from datetime import datetime, timedelta

# Redshift credentials
# scanx_hiroshi/scanxHiroshi79

AWS_KEY = environ.get('AWS_KEY')
AWS_SECRET = environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2021, 1, 1),
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup' : False
}

dag = DAG('CAPSTONE_ETL_AUTOMATION',
          default_args=default_args,
          description='Load and transform data in Redshift by Airflow',
#           schedule_interval='0 * * * *',
          schedule_interval='@hourly',
          catchup=False)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


c = CreateTable()
create_tables = PostgresOperator(    
    task_id='create_table',
    dag=dag,
    sql= c.create_tables(),
    postgres_conn_id='redshift'
)

staging = StagingOperator(
    task_id='staging_log',
    dag=dag,
    redshift_conn_id = 'redshift',
    aws_credentials='aws_credentials',
    table='staging_cleansed_logs',
    s3_bucket='scx-hiroshi',
    s3_key='auto_classify_jobs_concatenated.csv',
    json_path='s3://scx-hiroshi/auto_classify_jobs_concatenated.csv'
)

load_fact_table = LoadFactOperator(
    task_id='load_fact_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    table ='auto_classification_logs',
    truncate_data=False,
    sql_query=SqlQueries.autoclassifcation_logs_table_insert
)

load_users_dimension_table = LoadDimensionOperator(
    task_id='load_users_dim_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    table='users',
    truncate_data=True,
    sql_query=SqlQueries.users_table_insert
)

load_projects_dimension_table = LoadDimensionOperator(
    task_id='load_projects_dim_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    table='projects',
    truncate_data=True,
    sql_query=SqlQueries.projects_table_insert
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='load_time_dim_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    table='time',
    truncate_data=True,
    sql_query=SqlQueries.time_table_insert
)

run_quality_checks = DataQualityOperator(
    task_id='data_quality_checks',
    dag=dag,
    table=['auto_classification_logs', 'users', 'projects', 'time']
)

end_operator = DummyOperator(
    task_id='stop_execution',  
    dag=dag
)


start_operator >> create_tables

create_tables >> staging

staging >> load_fact_table

load_fact_table >> load_users_dimension_table
load_fact_table >> load_projects_dimension_table
load_fact_table >> load_time_dimension_table


load_users_dimension_table >> run_quality_checks
load_projects_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks


run_quality_checks >>  end_operator
