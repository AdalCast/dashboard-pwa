#!/usr/bin/env python3
"""
Script para crear contraseñas hash para usuarios existentes
Uso: python create_password.py
"""

import sys
import os
from dotenv import load_dotenv
from supabase import create_client
import bcrypt

# Cargar variables de entorno
load_dotenv()

def hash_password(password):
    """Crear hash seguro de la contraseña"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def main():
    # Configurar Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: Variables de entorno SUPABASE_URL y SUPABASE_KEY no están configuradas")
        return
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("🔐 Configurador de Contraseñas PWA Finanzas")
    print("=" * 50)
    
    try:
        # Listar usuarios existentes
        response = supabase.table('Usuarios').select('id, correo, password_hash').execute()
        
        if not response.data:
            print("❌ No se encontraron usuarios en la base de datos")
            return
        
        print("\n📋 Usuarios existentes:")
        for i, user in enumerate(response.data, 1):
            has_password = "✅ Sí" if user.get('password_hash') else "❌ No"
            print(f"  {i}. {user['correo']} - Contraseña: {has_password}")
        
        print("\n¿Qué quieres hacer?")
        print("1. Configurar contraseña para un usuario específico")
        print("2. Configurar contraseña para todos los usuarios sin contraseña")
        print("3. Salir")
        
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == "1":
            email = input("\nIngresa el email del usuario: ").strip()
            password = input("Ingresa la nueva contraseña: ").strip()
            
            if not email or not password:
                print("❌ Email y contraseña son requeridos")
                return
            
            # Crear hash
            password_hash = hash_password(password)
            
            # Actualizar usuario
            update_response = supabase.table('Usuarios').update({
                'password_hash': password_hash
            }).eq('correo', email).execute()
            
            if update_response.data:
                print(f"✅ Contraseña configurada exitosamente para {email}")
            else:
                print(f"❌ Usuario {email} no encontrado")
        
        elif choice == "2":
            default_password = input("\nIngresa la contraseña por defecto para todos: ").strip()
            
            if not default_password:
                print("❌ Contraseña es requerida")
                return
            
            # Crear hash
            password_hash = hash_password(default_password)
            
            # Actualizar usuarios sin contraseña
            users_updated = 0
            for user in response.data:
                if not user.get('password_hash'):
                    update_response = supabase.table('Usuarios').update({
                        'password_hash': password_hash
                    }).eq('id', user['id']).execute()
                    
                    if update_response.data:
                        users_updated += 1
                        print(f"✅ Contraseña configurada para {user['correo']}")
            
            print(f"\n🎉 Se configuraron contraseñas para {users_updated} usuarios")
        
        elif choice == "3":
            print("👋 ¡Hasta luego!")
            return
        
        else:
            print("❌ Opción inválida")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()