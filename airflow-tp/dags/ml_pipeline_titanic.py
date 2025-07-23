"""
DAG Airflow - Pipeline ML Simple
Version simplifiée sans dépendances externes
"""

from datetime import datetime, timedelta
import json
import logging
import random

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Configuration par défaut
default_args = {
    'owner': 'data_scientist',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# Définition du DAG
dag = DAG(
    'ml_pipeline_titanic_simple',
    default_args=default_args,
    description='Pipeline ML simplifié - Demo Titanic',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['machine-learning', 'demo', 'titanic'],
)

def setup_environment():
    """Vérifier l'environnement (version simplifiée)"""
    import sys
    import os
    
    logging.info("🔧 Vérification de l'environnement...")
    logging.info(f"🐍 Python version: {sys.version}")
    logging.info(f"📁 Working directory: {os.getcwd()}")
    logging.info(f"👤 User: {os.getenv('USER', 'unknown')}")
    
    # Créer un répertoire simple
    os.makedirs('/tmp/simple_ml', exist_ok=True)
    
    logging.info("✅ Environnement configuré avec succès")
    return {"status": "success", "python_version": sys.version}

def simulate_data_loading():
    """Simuler le chargement de données"""
    logging.info("📊 Simulation du chargement des données Titanic...")
    
    # Simuler des statistiques du dataset Titanic
    simulated_stats = {
        "total_passengers": 891,
        "survivors": 342,
        "survival_rate": 0.384,
        "features": ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"],
        "missing_values": {"Age": 177, "Cabin": 687, "Embarked": 2}
    }
    
    # Sauvegarder les stats
    with open('/tmp/simple_ml/data_stats.json', 'w') as f:
        json.dump(simulated_stats, f, indent=2)
    
    logging.info(f"✅ Données simulées: {simulated_stats['total_passengers']} passagers")
    logging.info(f"🎯 Taux de survie: {simulated_stats['survival_rate']:.1%}")
    
    return simulated_stats

def simulate_preprocessing():
    """Simuler le preprocessing"""
    logging.info("🔧 Simulation du preprocessing...")
    
    preprocessing_steps = [
        "Nettoyage des valeurs manquantes",
        "Encodage des variables catégorielles", 
        "Normalisation des features numériques",
        "Création de nouvelles features",
        "Division train/test"
    ]
    
    for i, step in enumerate(preprocessing_steps, 1):
        logging.info(f"   {i}. {step}")
    
    # Simuler des résultats de preprocessing
    results = {
        "original_features": 12,
        "processed_features": 15,
        "train_samples": 712,
        "test_samples": 179,
        "preprocessing_time": "2.3 seconds"
    }
    
    with open('/tmp/simple_ml/preprocessing_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    logging.info(f"✅ Preprocessing terminé: {results['processed_features']} features")
    return results

def simulate_model_training():
    """Simuler l'entraînement de modèles"""
    logging.info("🤖 Simulation de l'entraînement de modèles...")
    
    models = ["Random Forest", "Logistic Regression", "SVM", "Gradient Boosting"]
    results = {}
    
    best_model = None
    best_accuracy = 0
    
    for model in models:
        # Simuler des scores réalistes
        accuracy = round(random.uniform(0.75, 0.85), 3)
        cv_score = round(random.uniform(0.72, 0.82), 3)
        
        results[model] = {
            "accuracy": accuracy,
            "cv_score": cv_score,
            "training_time": f"{random.uniform(5, 30):.1f}s"
        }
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
        
        logging.info(f"📈 {model}: Accuracy={accuracy:.3f}, CV={cv_score:.3f}")
    
    # Résultats finaux
    final_results = {
        "best_model": best_model,
        "best_accuracy": best_accuracy,
        "all_models": results,
        "total_training_time": "45.2 seconds"
    }
    
    with open('/tmp/simple_ml/model_results.json', 'w') as f:
        json.dump(final_results, f, indent=2)
    
    logging.info(f"🏆 Meilleur modèle: {best_model} (Accuracy: {best_accuracy:.3f})")
    return final_results

def simulate_evaluation():
    """Simuler l'évaluation du modèle"""
    logging.info("📊 Simulation de l'évaluation du modèle...")
    
    # Simuler des métriques d'évaluation
    evaluation_results = {
        "accuracy": 0.821,
        "precision": 0.814,
        "recall": 0.785,
        "f1_score": 0.799,
        "auc_score": 0.873,
        "confusion_matrix": [[105, 12], [15, 47]],
        "top_features": [
            ["Sex_encoded", 0.298],
            ["Fare", 0.234],
            ["Age", 0.156],
            ["Pclass", 0.142],
            ["Title_encoded", 0.098]
        ]
    }
    
    with open('/tmp/simple_ml/evaluation_results.json', 'w') as f:
        json.dump(evaluation_results, f, indent=2)
    
    logging.info(f"🎯 Accuracy finale: {evaluation_results['accuracy']:.3f}")
    logging.info(f"🏅 AUC Score: {evaluation_results['auc_score']:.3f}")
    
    return evaluation_results

def generate_final_report():
    """Générer le rapport final"""
    logging.info("📋 Génération du rapport final...")
    
    # Charger tous les résultats
    with open('/tmp/simple_ml/data_stats.json', 'r') as f:
        data_stats = json.load(f)
    
    with open('/tmp/simple_ml/model_results.json', 'r') as f:
        model_results = json.load(f)
        
    with open('/tmp/simple_ml/evaluation_results.json', 'r') as f:
        evaluation_results = json.load(f)
    
    # Créer le rapport complet
    final_report = {
        "pipeline_execution": {
            "date": datetime.now().isoformat(),
            "status": "SUCCESS",
            "duration": "78.5 seconds"
        },
        "data_summary": data_stats,
        "model_summary": {
            "best_model": model_results["best_model"],
            "final_accuracy": evaluation_results["accuracy"],
            "auc_score": evaluation_results["auc_score"]
        },
        "recommendations": [
            "Le modèle est prêt pour la production",
            "Monitorer les performances sur de nouvelles données",
            "Considérer la ré-entraînement mensuel"
        ]
    }
    
    with open('/tmp/simple_ml/FINAL_REPORT.json', 'w') as f:
        json.dump(final_report, f, indent=2)
    
    logging.info("🎉 Rapport final généré avec succès!")
    logging.info(f"🏆 Modèle final: {final_report['model_summary']['best_model']}")
    logging.info(f"🎯 Performance: {final_report['model_summary']['final_accuracy']:.1%}")
    
    return final_report

# Définition des tâches
task_setup = PythonOperator(
    task_id='setup_environment',
    python_callable=setup_environment,
    dag=dag,
)

task_data = PythonOperator(
    task_id='load_data',
    python_callable=simulate_data_loading,
    dag=dag,
)

task_preprocess = PythonOperator(
    task_id='preprocess_data',
    python_callable=simulate_preprocessing,
    dag=dag,
)

task_train = PythonOperator(
    task_id='train_models',
    python_callable=simulate_model_training,
    dag=dag,
)

task_evaluate = PythonOperator(
    task_id='evaluate_model',
    python_callable=simulate_evaluation,
    dag=dag,
)

task_report = PythonOperator(
    task_id='generate_report',
    python_callable=generate_final_report,
    dag=dag,
)

task_cleanup = BashOperator(
    task_id='cleanup_success',
    bash_command='echo "🎉 Pipeline ML simplifié terminé avec succès! Vérifiez /tmp/simple_ml/"',
    dag=dag,
)

# Définir les dépendances
task_setup >> task_data >> task_preprocess >> task_train >> task_evaluate >> task_report >> task_cleanup