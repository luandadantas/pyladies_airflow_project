from datetime import datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow import DAG


with DAG(
    'hello_world_dag',
    description='DAG para testar o Airflow',
    start_date=datetime(2025, 3, 15),
    schedule_interval='@daily',
    catchup=False
) as dag:

    start_dummy_task = DummyOperator(
        task_id='start_dummy_task',
    )

    print_1_task = BashOperator(
        task_id='imprime_oi_mundo_com_bash_operator',
        bash_command='echo "Hello World! (bash operator)"',
    )

    def print_hello():
        print("Hello World! (python operator)")

    print_2_task = PythonOperator(
        task_id='imprime_oi_mundo_com_python_operator',
        python_callable=print_hello,
    )

start_dummy_task >> print_1_task >> print_2_task
