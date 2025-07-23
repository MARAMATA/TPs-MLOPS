# quick_fix.py - Solution rapide pour corriger tous les problèmes
import os
import sys

def main():
    """Correction rapide de tous les problèmes"""
    print("🔧 Correction rapide des problèmes AWS RDS")
    print("=" * 50)
    
    # 1. Vérifier les fichiers existants
    files_to_check = [
        ("db/connexion.py", "Fichier de connexion"),
        ("setup_aws_database.py", "Script de setup AWS"),
        ("quick_aws_test.py", "Test rapide AWS")
    ]
    
    print("\n1. Vérification des fichiers...")
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} - MANQUANT")
    
    # 2. Vérifier les corrections nécessaires
    print("\n2. Vérification des corrections nécessaires...")
    
    corrections_needed = []
    
    # Vérifier le hostname dans setup_aws_database.py
    if os.path.exists("setup_aws_database.py"):
        with open("setup_aws_database.py", "r") as f:
            content = f.read()
            if "m2-dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com" in content:
                corrections_needed.append("Hostname incorrect dans setup_aws_database.py")
    
    # Vérifier l'import text() dans db/connexion.py
    if os.path.exists("db/connexion.py"):
        with open("db/connexion.py", "r") as f:
            content = f.read()
            if "from sqlalchemy import create_engine, text" not in content:
                corrections_needed.append("Import text() manquant dans db/connexion.py")
    
    if corrections_needed:
        print("❌ Corrections nécessaires:")
        for correction in corrections_needed:
            print(f"   - {correction}")
    else:
        print("✅ Tous les fichiers semblent corrects")
    
    # 3. Instructions
    print("\n3. Instructions pour corriger...")
    print("🔧 Remplacez les fichiers suivants par les versions corrigées:")
    print("   - db/connexion.py → Version corrigée avec text()")
    print("   - setup_aws_database.py → Version corrigée avec bon hostname")
    
    # 4. Test final
    print("\n4. Tests à effectuer après correction:")
    print("   python quick_aws_test.py")
    print("   python setup_aws_database.py")
    print("   python api/main.py")

if __name__ == "__main__":
    main()