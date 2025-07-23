# dns_troubleshooting.py - Diagnostic DNS pour AWS RDS
import socket
import subprocess
import platform
import time

# Configuration
AWS_HOST = "m2-dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com"
BACKUP_HOST = "m2dsia-mlops.cfuik82swe2y.eu-central-1.rds.amazonaws.com"  # Nom alternatif possible

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"🔍 {title}")
    print(f"{'='*70}")

def test_basic_connectivity():
    """Test basic internet connectivity"""
    print_header("1. Test Connectivité Internet")
    
    test_hosts = [
        ("Google DNS", "8.8.8.8"),
        ("Cloudflare DNS", "1.1.1.1"),
        ("Google", "google.com"),
        ("AWS", "aws.amazon.com")
    ]
    
    for name, host in test_hosts:
        try:
            if host.replace('.', '').isdigit():  # IP address
                socket.create_connection((host, 53), timeout=5)
            else:  # Domain name
                socket.gethostbyname(host)
            print(f"✅ {name}: OK")
        except Exception as e:
            print(f"❌ {name}: FAILED - {e}")

def test_dns_servers():
    """Test DNS server configuration"""
    print_header("2. Configuration DNS")
    
    try:
        # Get DNS configuration on macOS
        result = subprocess.run(
            ["scutil", "--dns"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            print("📋 Configuration DNS détectée:")
            lines = result.stdout.split('\n')
            for line in lines[:20]:  # First 20 lines
                if 'nameserver' in line.lower():
                    print(f"   {line.strip()}")
        else:
            print("⚠️  Impossible de récupérer la configuration DNS")
            
    except Exception as e:
        print(f"❌ Erreur DNS config: {e}")

def test_nslookup():
    """Test nslookup command"""
    print_header("3. Test nslookup")
    
    hosts_to_test = [
        AWS_HOST,
        BACKUP_HOST,
        "eu-central-1.rds.amazonaws.com"
    ]
    
    for host in hosts_to_test:
        try:
            result = subprocess.run(
                ["nslookup", host], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            print(f"\n📍 nslookup {host}:")
            if result.returncode == 0:
                print(f"✅ Résolution OK")
                print(f"   Résultat: {result.stdout.strip()}")
            else:
                print(f"❌ Échec de résolution")
                print(f"   Erreur: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"❌ nslookup {host}: {e}")

def test_dig():
    """Test dig command"""
    print_header("4. Test dig (DNS détaillé)")
    
    try:
        result = subprocess.run(
            ["dig", AWS_HOST], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ dig réussi:")
            print(f"   {result.stdout}")
        else:
            print(f"❌ dig échoué: {result.stderr}")
            
    except FileNotFoundError:
        print("⚠️  Commande 'dig' non trouvée (normal sur macOS)")
    except Exception as e:
        print(f"❌ dig erreur: {e}")

def test_ping():
    """Test ping command"""
    print_header("5. Test ping")
    
    hosts_to_ping = [
        AWS_HOST,
        BACKUP_HOST,
        "aws.amazon.com"
    ]
    
    for host in hosts_to_ping:
        try:
            result = subprocess.run(
                ["ping", "-c", "3", host], 
                capture_output=True, 
                text=True, 
                timeout=15
            )
            
            if result.returncode == 0:
                print(f"✅ ping {host}: OK")
                # Extract average time
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'avg' in line:
                        print(f"   {line.strip()}")
                        break
            else:
                print(f"❌ ping {host}: FAILED")
                print(f"   Erreur: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"❌ ping {host}: {e}")

def test_alternative_hosts():
    """Test alternative AWS RDS hostnames"""
    print_header("6. Test Noms d'Hôtes Alternatifs")
    
    alternative_hosts = [
        "m2dsia-mlops.cfuik82swe2y.eu-central-1.rds.amazonaws.com",
        "m2-dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com",
        "m2dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com"
    ]
    
    for host in alternative_hosts:
        try:
            ip = socket.gethostbyname(host)
            print(f"✅ {host} -> {ip}")
        except Exception as e:
            print(f"❌ {host}: {e}")

def test_manual_dns():
    """Test with manual DNS servers"""
    print_header("7. Test avec DNS Publics")
    
    # This would require modifying system DNS, which is complex
    # Instead, we'll use socket with different approaches
    
    print("💡 Suggestion: Essayer de changer temporairement vos DNS")
    print("   1. Aller dans Préférences Système > Réseau")
    print("   2. Sélectionner votre connexion")
    print("   3. Cliquer sur 'Avancé' > 'DNS'")
    print("   4. Ajouter: 8.8.8.8 et 1.1.1.1")
    print("   5. Relancer le test")

def check_vpn_proxy():
    """Check for VPN or proxy"""
    print_header("8. Vérification VPN/Proxy")
    
    try:
        # Check for common VPN processes
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        vpn_keywords = ["openvpn", "cisco", "nordvpn", "expressvpn", "tunnelblick"]
        vpn_found = False
        
        for keyword in vpn_keywords:
            if keyword in result.stdout.lower():
                print(f"⚠️  VPN détecté: {keyword}")
                vpn_found = True
        
        if not vpn_found:
            print("✅ Aucun VPN détecté")
            
    except Exception as e:
        print(f"❌ Erreur vérification VPN: {e}")

def provide_solutions():
    """Provide solutions"""
    print_header("💡 SOLUTIONS POSSIBLES")
    
    print("🔧 Solution 1: Vérifier la Connexion Internet")
    print("   - Tester avec: ping google.com")
    print("   - Redémarrer le WiFi")
    print("   - Changer de réseau")
    
    print("\n🔧 Solution 2: Changer les DNS")
    print("   - Préférences Système > Réseau > Avancé > DNS")
    print("   - Ajouter: 8.8.8.8, 1.1.1.1")
    print("   - Ou utiliser: 208.67.222.222, 208.67.220.220")
    
    print("\n🔧 Solution 3: Vérifier le Nom d'Hôte AWS")
    print("   - Le nom d'hôte AWS RDS pourrait être incorrect")
    print("   - Vérifier dans AWS Console > RDS > Instances")
    print("   - Copier l'endpoint exact")
    
    print("\n🔧 Solution 4: Désactiver VPN/Proxy")
    print("   - Déconnecter temporairement le VPN")
    print("   - Désactiver les proxies")
    
    print("\n🔧 Solution 5: Utiliser SQLite en attendant")
    print("   - python switch_database.py --database sqlite")
    print("   - python setup_local_database.py")
    print("   - python api/main.py")
    
    print("\n🔧 Solution 6: Utiliser IP directement")
    print("   - Si vous obtenez l'IP de l'instance RDS")
    print("   - Remplacer le hostname par l'IP dans connexion.py")

def main():
    """Main diagnostic function"""
    print_header("DIAGNOSTIC DNS AWS RDS")
    print(f"🖥️  Système: {platform.system()} {platform.release()}")
    print(f"🎯 Cible: {AWS_HOST}")
    print(f"⏰ Heure: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run diagnostics
    test_basic_connectivity()
    test_dns_servers()
    test_nslookup()
    test_dig()
    test_ping()
    test_alternative_hosts()
    test_manual_dns()
    check_vpn_proxy()
    provide_solutions()
    
    print_header("🎯 PROCHAINES ÉTAPES")
    print("1. Suivre les solutions proposées ci-dessus")
    print("2. Relancer: python quick_aws_test.py")
    print("3. Si ça marche pas: python switch_database.py --database sqlite")
    print("4. Continuer avec SQLite pour le moment")

if __name__ == "__main__":
    main()