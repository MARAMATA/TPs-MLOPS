from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def print_hello():
    return 'Hello from Airflow!'

# Configuration par défaut du DAG
default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définition du DAG
dag = DAG(
    'example_dag',
    default_args=default_args,
    description='Un DAG d\'exemple simple',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example'],
)

# Tâche 1 : Commande bash
task1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

# Tâche 2 : Fonction Python
task2 = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag,
)

# Tâche 3 : Autre commande bash
task3 = BashOperator(
    task_id='print_working_directory',
    bash_command='pwd && ls -la',
    dag=dag,
)

# Définir les dépendances
task1 >> task2 >> task3
