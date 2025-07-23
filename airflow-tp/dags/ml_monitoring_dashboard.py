"""
DAG de Monitoring - Supervise tous les pipelines ML/IA
"""

from datetime import datetime, timedelta
import json
import logging
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'ml_ops_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'ml_monitoring_dashboard',
    default_args=default_args,
    description='Dashboard de monitoring pour tous les pipelines ML/IA',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=['monitoring', 'dashboard', 'ml-ops'],
)

def check_pipeline_health():
    """Vérifier la santé de tous les pipelines"""
    logging.info("🔍 Vérification de la santé des pipelines...")
    
    pipelines = {
        'ml_pipeline': '/tmp/ml_pipeline',
        'ai_pipeline': '/tmp/ai_pipeline', 
        'cv_pipeline': '/tmp/cv_pipeline'
    }
    
    health_status = {}
    
    for pipeline_name, pipeline_path in pipelines.items():
        try:
            path = Path(pipeline_path)
            if path.exists():
                files = list(path.glob('*.json'))
                health_status[pipeline_name] = {
                    'status': 'healthy',
                    'files_count': len(files),
                    'last_modified': max([f.stat().st_mtime for f in files]) if files else 0
                }
            else:
                health_status[pipeline_name] = {
                    'status': 'not_found',
                    'files_count': 0,
                    'last_modified': 0
                }
        except Exception as e:
            health_status[pipeline_name] = {
                'status': 'error',
                'error': str(e),
                'files_count': 0,
                'last_modified': 0
            }
    
    # Sauvegarder le rapport de santé
    with open('/tmp/ml_health_report.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'pipelines': health_status
        }, f, indent=2)
    
    # Log du statut
    for pipeline, status in health_status.items():
        logging.info(f"📊 {pipeline}: {status['status']}")
    
    return health_status

def generate_summary_report():
    """Générer un rapport de synthèse"""
    logging.info("📋 Génération du rapport de synthèse...")
    
    summary = {
        'report_date': datetime.now().isoformat(),
        'pipelines_summary': {},
        'recommendations': []
    }
    
    # Collecter les données de chaque pipeline
    pipelines_data = {}
    
    # ML Pipeline
    try:
        ml_path = Path('/tmp/ml_pipeline/final_report.json')
        if ml_path.exists():
            with open(ml_path, 'r') as f:
                pipelines_data['ml_pipeline'] = json.load(f)
    except:
        pass
    
    # AI Pipeline  
    try:
        ai_path = Path('/tmp/ai_pipeline/ai_insights.json')
        if ai_path.exists():
            with open(ai_path, 'r') as f:
                pipelines_data['ai_pipeline'] = json.load(f)
    except:
        pass
    
    # CV Pipeline
    try:
        cv_path = Path('/tmp/cv_pipeline/results/image_analysis.json')
        if cv_path.exists():
            with open(cv_path, 'r') as f:
                pipelines_data['cv_pipeline'] = json.load(f)
    except:
        pass
    
    summary['pipelines_summary'] = pipelines_data
    
    # Recommandations générales
    if len(pipelines_data) == 0:
        summary['recommendations'].append("Aucun pipeline n'a encore été exécuté")
    elif len(pipelines_data) < 3:
        summary['recommendations'].append("Certains pipelines n'ont pas encore été exécutés")
    else:
        summary['recommendations'].append("Tous les pipelines sont opérationnels")
    
    # Sauvegarder le rapport de synthèse
    with open('/tmp/ml_summary_report.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    logging.info(f"📊 Rapport de synthèse généré: {len(pipelines_data)} pipelines analysés")
    
    return summary

# Tâches de monitoring
task_health_check = PythonOperator(
    task_id='check_pipeline_health',
    python_callable=check_pipeline_health,
    dag=dag,
)

task_summary_report = PythonOperator(
    task_id='generate_summary_report',
    python_callable=generate_summary_report,
    dag=dag,
)

task_monitoring_complete = BashOperator(
    task_id='monitoring_complete',
    bash_command='echo "📊 Monitoring terminé. Rapports disponibles dans /tmp/"',
    dag=dag,
)

# Définir les dépendances
task_health_check >> task_summary_report >> task_monitoring_complete
