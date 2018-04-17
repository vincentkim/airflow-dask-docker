
from datetime import datetime
from airflow import DAG
import airflow
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'vincent',
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True
}

dag = DAG(
    'fibo_world',  schedule_interval="@once",
    default_args=args)


def print_fibo(**param):
    def fib(n):
            if n<2:
                    return n
            return fib(n-2) + fib(n-1)
    dum = fib(22)
    return dum

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)


for idx in range(30):
        hello_operator = PythonOperator(task_id='hello_task_%s' % idx, python_callable=print_fibo, dag=dag)
        dummy_operator >> hello_operator
