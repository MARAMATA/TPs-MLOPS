#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les DAGs sont syntaxiquement corrects
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire dags au path
dags_dir = Path(__file__).parent / "dags"
sys.path.insert(0, str(dags_dir))

def test_dag_import(dag_file):
    """Tester l'import d'un DAG"""
    try:
        module_name = dag_file.stem
        __import__(module_name)
        print(f"✅ {dag_file.name} - Import réussi")
        return True
    except Exception as e:
        print(f"❌ {dag_file.name} - Erreur: {e}")
        return False

def main():
    """Tester tous les DAGs"""
    print("🧪 Test de tous les DAGs ML/IA")
    print("=" * 40)
    
    dag_files = list(dags_dir.glob("*.py"))
    dag_files = [f for f in dag_files if not f.name.startswith("__")]
    
    if not dag_files:
        print("❌ Aucun DAG trouvé dans le répertoire dags/")
        return False
    
    success_count = 0
    for dag_file in dag_files:
        if test_dag_import(dag_file):
            success_count += 1
    
    print("\n📊 Résultats:")
    print(f"✅ DAGs valides: {success_count}/{len(dag_files)}")
    
    if success_count == len(dag_files):
        print("🎉 Tous les DAGs sont prêts!")
        return True
    else:
        print("⚠️ Certains DAGs ont des problèmes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
