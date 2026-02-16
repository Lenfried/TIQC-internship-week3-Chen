"""
Script to check if MySQL and MongoDB are running and accessible
"""
import socket
import subprocess
import sys
from config import MYSQL_HOST, MYSQL_PORT, MONGODB_HOST, MONGODB_PORT

def check_port(host, port, service_name):
    """Check if a port is open (service is running)"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def check_mysql_service():
    """Check if MySQL service is running on Windows"""
    try:
        result = subprocess.run(
            ['sc', 'query', 'MySQL'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return 'RUNNING' in result.stdout
    except:
        return False

def check_mongodb_service():
    """Check if MongoDB service is running on Windows"""
    try:
        result = subprocess.run(
            ['sc', 'query', 'MongoDB'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return 'RUNNING' in result.stdout
    except:
        # Try alternative service names
        try:
            result = subprocess.run(
                ['sc', 'query', 'MongoDB'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return 'RUNNING' in result.stdout
        except:
            return False

def main():
    print("=== Database Status Check ===\n")
    
    # Check MySQL
    print("Checking MySQL...")
    mysql_port_open = check_port(MYSQL_HOST, MYSQL_PORT, "MySQL")
    mysql_service_running = check_mysql_service()
    
    if mysql_port_open:
        print(f"[OK] MySQL is running on {MYSQL_HOST}:{MYSQL_PORT}")
    else:
        print(f"[X] MySQL is NOT running on {MYSQL_HOST}:{MYSQL_PORT}")
        print("\n  To start MySQL:")
        print("  1. Open Services (services.msc)")
        print("  2. Find 'MySQL' service")
        print("  3. Right-click and select 'Start'")
        print("\n  Or use PowerShell (as Administrator):")
        print("    Start-Service MySQL")
        print("\n  If MySQL is not installed:")
        print("    Download from: https://dev.mysql.com/downloads/mysql/")
        print("    Or use XAMPP: https://www.apachefriends.org/")
    
    print()
    
    # Check MongoDB
    print("Checking MongoDB...")
    mongodb_port_open = check_port(MONGODB_HOST, MONGODB_PORT, "MongoDB")
    mongodb_service_running = check_mongodb_service()
    
    if mongodb_port_open:
        print(f"[OK] MongoDB is running on {MONGODB_HOST}:{MONGODB_PORT}")
    else:
        print(f"[X] MongoDB is NOT running on {MONGODB_HOST}:{MONGODB_PORT}")
        print("\n  To start MongoDB:")
        print("  1. Open Services (services.msc)")
        print("  2. Find 'MongoDB' service")
        print("  3. Right-click and select 'Start'")
        print("\n  Or use PowerShell (as Administrator):")
        print("    Start-Service MongoDB")
        print("\n  If MongoDB is not installed:")
        print("    Download from: https://www.mongodb.com/try/download/community")
        print("    Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas")
    
    print("\n=== Summary ===")
    if mysql_port_open and mongodb_port_open:
        print("[OK] Both databases are running! You can proceed with:")
        print("  python setup_databases.py")
        print("  python seed_data.py")
        print("  python app.py")
    else:
        print("[X] Please start the required database services before proceeding.")
        print("\nQuick Start Guide:")
        print("1. Start MySQL service")
        print("2. Start MongoDB service")
        print("3. Run: python setup_databases.py")
        print("4. Run: python seed_data.py (optional)")
        print("5. Run: python app.py")

if __name__ == '__main__':
    main()
