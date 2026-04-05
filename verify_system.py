#!/usr/bin/env python3
"""
Script de verificación del sistema SportBot.
Verifica que todos los componentes estén funcionando correctamente.
"""
import os
import sys

def check_environment():
    """Verificar entorno y dependencias"""
    print("\n" + "="*80)
    print("1. VERIFICANDO ENTORNO")
    print("="*80)
    
    # Python version
    print(f"\n✓ Python: {sys.version.split()[0]}")
    
    # Check required packages
    required = [
        'django', 'rest_framework', 'psycopg2', 
        'pandas', 'numpy', 'sklearn', 'xgboost', 'joblib'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - FALTA")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Paquetes faltantes: {', '.join(missing)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    return True


def check_files():
    """Verificar archivos necesarios"""
    print("\n" + "="*80)
    print("2. VERIFICANDO ARCHIVOS")
    print("="*80)
    
    required_files = [
        'manage.py',
        'config/settings.py',
        'apps/predictions/models.py',
        'apps/calculators/registry.py',
        'apps/models_ml/ensemble.py',
        'requirements.txt',
        '.env.example'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - FALTA")
            all_exist = False
    
    return all_exist


def check_ml_models():
    """Verificar modelos ML"""
    print("\n" + "="*80)
    print("3. VERIFICANDO MODELOS ML")
    print("="*80)
    
    models_dir = 'ml_models'
    required_models = [
        'lasso_model.pkl',
        'xgboost_model.pkl',
        'linear_model.pkl',
        'random_forest.pkl'
    ]
    
    if not os.path.exists(models_dir):
        print(f"\n✗ Directorio {models_dir}/ no existe")
        print("Ejecuta: mkdir ml_models")
        return False
    
    all_exist = True
    for model in required_models:
        path = os.path.join(models_dir, model)
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024
            print(f"✓ {model} ({size:.1f} KB)")
        else:
            print(f"✗ {model} - FALTA")
            all_exist = False
    
    if not all_exist:
        print("\n❌ Modelos faltantes")
        print("Ejecuta: python train_models.py")
    
    return all_exist


def check_calculators():
    """Verificar calculadoras de gematria"""
    print("\n" + "="*80)
    print("4. VERIFICANDO CALCULADORAS")
    print("="*80)
    
    try:
        from apps.calculators.registry import CalculatorRegistry
        
        calculators = CalculatorRegistry.list_calculator_names()
        count = len(calculators)
        
        print(f"\n✓ {count} calculadoras registradas:")
        for i, calc in enumerate(sorted(calculators), 1):
            print(f"   {i:2d}. {calc}")
        
        if count < 20:
            print(f"\n⚠️  Solo {count} calculadoras (objetivo: 35+)")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def check_database():
    """Verificar conexión a base de datos"""
    print("\n" + "="*80)
    print("5. VERIFICANDO BASE DE DATOS")
    print("="*80)
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        import django
        django.setup()
        
        from django.db import connection
        
        # Test connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("\n✓ Conexión a PostgreSQL exitosa")
            
            # Check tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cursor.fetchall()
            print(f"✓ {len(tables)} tablas encontradas")
            
            return True
        
    except Exception as e:
        print(f"\n✗ Error de conexión: {e}")
        print("\nSolución:")
        print("1. Verifica que PostgreSQL esté corriendo")
        print("2. Crea la base de datos: createdb sports_prediction_db")
        print("3. Ejecuta migraciones: python manage.py migrate")
        return False


def check_django_setup():
    """Verificar setup de Django"""
    print("\n" + "="*80)
    print("6. VERIFICANDO DJANGO")
    print("="*80)
    
    try:
        # Check if migrations exist
        migrations_dir = 'apps/predictions/migrations'
        if os.path.exists(migrations_dir):
            files = [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py']
            print(f"✓ {len(files)} archivos de migración encontrados")
        else:
            print("✗ Directorio de migraciones no existe")
            print("Ejecuta: python manage.py makemigrations")
            return False
        
        # Check .env file
        if os.path.exists('.env'):
            print("✓ Archivo .env configurado")
        else:
            print("⚠️  Archivo .env no existe")
            print("Ejecuta: cp .env.example .env")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Ejecutar todas las verificaciones"""
    print("\n" + "="*80)
    print("VERIFICACIÓN DEL SISTEMA SPORTBOT")
    print("="*80)
    
    results = {
        'Entorno': check_environment(),
        'Archivos': check_files(),
        'Modelos ML': check_ml_models(),
        'Calculadoras': check_calculators(),
        'Base de Datos': check_database(),
        'Django': check_django_setup(),
    }
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN")
    print("="*80)
    
    for component, status in results.items():
        icon = "✓" if status else "✗"
        print(f"{icon} {component}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n" + "="*80)
        print("🎉 ¡SISTEMA LISTO!")
        print("="*80)
        print("\nPuedes iniciar el servidor:")
        print("  python manage.py runserver")
        print("\nY hacer tu primera predicción:")
        print('  curl -X POST http://localhost:8000/api/predictions/predict/ \\')
        print('    -H "Content-Type: application/json" \\')
        print('    -d \'{"team1": "Lakers", "team2": "Celtics", "sport": "NBA"}\'')
    else:
        print("\n" + "="*80)
        print("❌ FALTAN COMPONENTES")
        print("="*80)
        print("\nRevisa los errores arriba y sigue las soluciones sugeridas.")
        print("Consulta QUICKSTART.md para más ayuda.")
    
    print("\n")


if __name__ == '__main__':
    main()
