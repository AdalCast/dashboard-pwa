#!/usr/bin/env python3
"""
Script para verificar que todo está listo para el despliegue en EasyPanel
"""

import os
import sys
from pathlib import Path

def check_file(filename, description):
    """Verificar que un archivo existe"""
    if Path(filename).exists():
        print(f"✅ {description}: {filename}")
        return True
    else:
        print(f"❌ {description} NO encontrado: {filename}")
        return False

def check_env_variables():
    """Verificar que las variables de entorno estén configuradas"""
    print("\n📋 Verificando variables de entorno en .env:")
    
    if not Path('.env').exists():
        print("❌ Archivo .env no encontrado")
        return False
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'FLASK_SECRET_KEY']
    with open('.env', 'r') as f:
        content = f.read()
        
    all_found = True
    for var in required_vars:
        if var in content and not f"{var}=tu_" in content and not f"{var}=YOUR_" in content:
            print(f"✅ {var} configurado")
        else:
            print(f"❌ {var} NO configurado o usa valor por defecto")
            all_found = False
            
    return all_found

def check_icons():
    """Verificar que los iconos PWA existan"""
    print("\n🎨 Verificando iconos PWA:")
    
    icons = [
        'static/icons/icon-192x192.png',
        'static/icons/icon-512x512.png'
    ]
    
    all_found = True
    for icon in icons:
        if Path(icon).exists():
            size = Path(icon).stat().st_size
            print(f"✅ {icon} encontrado ({size} bytes)")
        else:
            print(f"❌ {icon} NO encontrado")
            all_found = False
            
    return all_found

def main():
    print("=" * 60)
    print("🚀 VERIFICACIÓN DE DESPLIEGUE EN EASYPANEL")
    print("=" * 60)
    
    print("\n📦 Verificando archivos necesarios:")
    checks = [
        ('Dockerfile', 'Dockerfile'),
        ('.dockerignore', 'Docker ignore'),
        ('requirements.txt', 'Requisitos de Python'),
        ('app.py', 'Aplicación principal'),
        ('.env', 'Variables de entorno'),
        ('static/js/sw.js', 'Service Worker'),
        ('static/css/style.css', 'Estilos CSS'),
    ]
    
    results = []
    for filename, description in checks:
        results.append(check_file(filename, description))
    
    # Verificar variables de entorno
    results.append(check_env_variables())
    
    # Verificar iconos
    icons_ok = check_icons()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    if all(results) and icons_ok:
        print("\n✅ ¡Todo listo para desplegar en EasyPanel!")
        print("\n📝 Próximos pasos:")
        print("   1. Sube tu código a un repositorio Git (GitHub/GitLab)")
        print("   2. Crea una nueva aplicación en EasyPanel")
        print("   3. Conecta tu repositorio")
        print("   4. Configura las variables de entorno")
        print("   5. ¡Despliega!")
        print("\n📖 Lee DEPLOYMENT.md para instrucciones detalladas")
        return 0
    else:
        print("\n⚠️  Hay problemas que debes resolver antes de desplegar:")
        
        if not all(results):
            print("\n🔧 Archivos o configuraciones faltantes")
            
        if not icons_ok:
            print("\n🎨 Iconos PWA faltantes:")
            print("   - Agrega icon-192x192.png e icon-512x512.png")
            print("   - Lee static/icons/README.md para más información")
            
        print("\n📖 Consulta DEPLOYMENT.md para más detalles")
        return 1

if __name__ == '__main__':
    sys.exit(main())
