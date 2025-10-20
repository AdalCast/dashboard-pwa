from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta
import json
import uuid
from functools import wraps
import bcrypt
from werkzeug.security import check_password_hash

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
CORS(app)

# Configuración de Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Funciones híbridas de autenticación (bcrypt + Werkzeug)
def is_bcrypt_hash(password_hash):
    """Detecta si el hash es de tipo bcrypt"""
    return password_hash and password_hash.startswith('$2b$')

def hash_password(password):
    """Crear hash bcrypt de la contraseña (para nuevos usuarios)"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, stored_hash):
    """Verificar contraseña usando el método correcto según el tipo de hash"""
    if not stored_hash:
        return False
    
    if is_bcrypt_hash(stored_hash):
        # Es un hash bcrypt - usar bcrypt
        try:
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        except Exception as e:
            print(f"Error verificando bcrypt: {e}")
            return False
    else:
        # Es un hash Werkzeug - usar método Werkzeug
        try:
            return check_password_hash(stored_hash, password)
        except Exception as e:
            print(f"Error verificando Werkzeug: {e}")
            return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/transactions')
@login_required
def transactions():
    return render_template('transactions.html')

@app.route('/fixed-expenses')
@login_required
def fixed_expenses():
    return render_template('fixed_expenses.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/currency')
@login_required
def currency():
    return render_template('currency.html')

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Finanzas Personales",
        "short_name": "FinanzasPWA",
        "description": "Aplicación de gestión de finanzas personales",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#4f46e5",
        "icons": [
            {
                "src": "/static/icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/icon-512x512.png", 
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

# API Routes
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email y contraseña son requeridos'
            }), 400
        
        # Buscar usuario en la tabla Usuarios
        response = supabase.table('Usuarios').select('*').eq('correo', email).execute()
        
        if response.data and len(response.data) > 0:
            user = response.data[0]
            
            # Verificar que el usuario está activo
            if not user.get('activo', True):
                return jsonify({
                    'success': False,
                    'message': 'Usuario inactivo'
                }), 401
            
            # Verificar contraseña hash
            password_hash = user.get('password_hash')
            if password_hash:
                # Verificar contraseña con bcrypt
                if verify_password(password, password_hash):
                    # Contraseña correcta
                    session['user_id'] = user['id']
                    session['user_email'] = user['correo']
                    session['user_name'] = user.get('full_name', '')
                    
                    return jsonify({
                        'success': True,
                        'message': 'Inicio de sesión exitoso'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Contraseña incorrecta'
                    }), 401
            else:
                return jsonify({
                    'success': False,
                    'message': 'Usuario sin contraseña configurada'
                }), 401
        else:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 401
            
    except Exception as e:
        print(f"Error en login: {str(e)}")  # Para debug
        return jsonify({
            'success': False,
            'message': f'Error en el servidor: {str(e)}'
        }), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Sesión cerrada'})

@app.route('/api/dashboard-summary')
@login_required
def dashboard_summary():
    try:
        user_id = session['user_id']
        month = request.args.get('month')
        
        # Si no se especifica mes, usar el actual
        if not month:
            month = datetime.now().strftime('%Y-%m')
        
        # Obtener transacciones del mes especificado
        response = supabase.table('Transacciones').select('*').eq('usuario_id', user_id).gte('fecha', f'{month}-01').lt('fecha', f'{month}-32').execute()
        transactions = response.data
        
        # Calcular totales
        total_ingresos = sum(t['monto'] for t in transactions if t['tipo'] == 'ingreso')
        total_gastos = sum(abs(t['monto']) for t in transactions if t['tipo'] == 'gasto')
        balance = total_ingresos - total_gastos
        
        # Agrupar gastos por categoría
        gastos_por_categoria = {}
        for t in transactions:
            if t['tipo'] == 'gasto':
                categoria = t['categoria']
                gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0) + abs(t['monto'])
        
        # Últimas 10 transacciones del mes
        ultimas_transacciones = sorted(transactions, key=lambda x: x['fecha'], reverse=True)[:10]
        
        return jsonify({
            'total_ingresos': total_ingresos,
            'total_gastos': total_gastos,
            'balance': balance,
            'gastos_por_categoria': gastos_por_categoria,
            'ultimas_transacciones': ultimas_transacciones,
            'mes_seleccionado': month
        })
        
    except Exception as e:
        print(f"Error en dashboard: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions')
@login_required
def get_transactions():
    try:
        user_id = session['user_id']
        month = request.args.get('month')
        tipo = request.args.get('tipo')
        
        query = supabase.table('Transacciones').select('*').eq('usuario_id', user_id)
        
        if month:
            query = query.gte('fecha', f'{month}-01').lt('fecha', f'{month}-32')
        
        if tipo:
            query = query.eq('tipo', tipo)
            
        response = query.order('fecha', desc=True).execute()
        
        return jsonify(response.data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
@login_required
def add_transaction():
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        transaction_data = {
            'id': str(uuid.uuid4()),
            'usuario_id': user_id,
            'fecha': data['fecha'],
            'categoria': data['categoria'],
            'monto': int(float(data['monto'])),
            'descripcion': data['descripcion'],
            'tipo': data['tipo'],
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('Transacciones').insert(transaction_data).execute()
        
        return jsonify({
            'success': True,
            'message': 'Transacción agregada exitosamente',
            'data': response.data[0]
        })
        
    except Exception as e:
        print(f"Error en add_transaction: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/<transaction_id>', methods=['PUT'])
@login_required
def update_transaction(transaction_id):
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        # Verificar que la transacción pertenece al usuario
        check_response = supabase.table('Transacciones').select('*').eq('id', transaction_id).eq('usuario_id', user_id).execute()
        
        if not check_response.data:
            return jsonify({'error': 'Transacción no encontrada'}), 404
        
        update_data = {
            'fecha': data['fecha'],
            'categoria': data['categoria'],
            'monto': int(float(data['monto'])),
            'descripcion': data['descripcion'],
            'tipo': data['tipo']
        }
        
        response = supabase.table('Transacciones').update(update_data).eq('id', transaction_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Transacción actualizada exitosamente',
            'data': response.data[0]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/<transaction_id>', methods=['DELETE'])
@login_required
def delete_transaction(transaction_id):
    try:
        user_id = session['user_id']
        
        # Verificar que la transacción pertenece al usuario
        check_response = supabase.table('Transacciones').select('*').eq('id', transaction_id).eq('usuario_id', user_id).execute()
        
        if not check_response.data:
            return jsonify({'error': 'Transacción no encontrada'}), 404
        
        response = supabase.table('Transacciones').delete().eq('id', transaction_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Transacción eliminada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fixed-expenses')
@login_required
def get_fixed_expenses():
    try:
        user_id = session['user_id']
        # Buscar por teléfono ya que no hay usuario_id en esta tabla
        user_response = supabase.table('Usuarios').select('telefono').eq('id', user_id).execute()
        if not user_response.data:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        user_phone = user_response.data[0]['telefono']
        response = supabase.table('Gastos fijos').select('*').eq('teléfono', user_phone).order('día pago').execute()
        
        return jsonify(response.data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fixed-expenses', methods=['POST'])
@login_required
def add_fixed_expense():
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        # Obtener teléfono del usuario
        user_response = supabase.table('Usuarios').select('telefono').eq('id', user_id).execute()
        if not user_response.data:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        user_phone = user_response.data[0]['telefono']
        
        expense_data = {
            'id': str(uuid.uuid4()),
            'teléfono': user_phone,
            'día pago': int(data['dia_pago']),
            'categoría': data['categoria'],
            'monto': int(float(data['monto'])),
            'descripción': data['descripcion'],
            'frecuencia': data['frecuencia'],
            'tipo': 'gasto_fijo'
        }
        
        response = supabase.table('Gastos fijos').insert(expense_data).execute()
        
        return jsonify({
            'success': True,
            'message': 'Gasto fijo agregado exitosamente',
            'data': response.data[0]
        })
        
    except Exception as e:
        print(f"Error en add_fixed_expense: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/fixed-expenses/<expense_id>', methods=['PUT'])
@login_required
def update_fixed_expense(expense_id):
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        # Obtener teléfono del usuario
        user_response = supabase.table('Usuarios').select('telefono').eq('id', user_id).execute()
        if not user_response.data:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        user_phone = user_response.data[0]['telefono']
        
        # Verificar que el gasto fijo pertenece al usuario
        check_response = supabase.table('Gastos fijos').select('*').eq('id', expense_id).eq('teléfono', user_phone).execute()
        
        if not check_response.data:
            return jsonify({'error': 'Gasto fijo no encontrado'}), 404
        
        update_data = {
            'día pago': int(data['dia_pago']),
            'categoría': data['categoria'],
            'monto': int(float(data['monto'])),
            'descripción': data['descripcion'],
            'frecuencia': data['frecuencia']
        }
        
        response = supabase.table('Gastos fijos').update(update_data).eq('id', expense_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Gasto fijo actualizado exitosamente',
            'data': response.data[0]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fixed-expenses/<expense_id>', methods=['DELETE'])
@login_required
def delete_fixed_expense(expense_id):
    try:
        user_id = session['user_id']
        
        # Obtener teléfono del usuario
        user_response = supabase.table('Usuarios').select('telefono').eq('id', user_id).execute()
        if not user_response.data:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        user_phone = user_response.data[0]['telefono']
        
        # Verificar que el gasto fijo pertenece al usuario
        check_response = supabase.table('Gastos fijos').select('*').eq('id', expense_id).eq('teléfono', user_phone).execute()
        
        if not check_response.data:
            return jsonify({'error': 'Gasto fijo no encontrado'}), 404
        
        response = supabase.table('Gastos fijos').delete().eq('id', expense_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Gasto fijo eliminado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile')
@login_required
def get_profile():
    try:
        user_id = session['user_id']
        response = supabase.table('Usuarios').select('*').eq('id', user_id).execute()
        
        if response.data:
            return jsonify(response.data[0])
        else:
            return jsonify({'error': 'Perfil no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        update_data = {
            'full_name': data.get('full_name', ''),
            'telefono': data.get('telefono', ''),
            'reporte_diario': data.get('reporte_diario', True),
            'reporte_semanal': data.get('reporte_semanal', True),
            'reporte_mensual': data.get('reporte_mensual', True)
        }
        
        response = supabase.table('Usuarios').update(update_data).eq('id', user_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Perfil actualizado exitosamente',
            'data': response.data[0] if response.data else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta auxiliar para crear/actualizar contraseña (solo para desarrollo/testing)
@app.route('/api/update-password', methods=['POST'])
@login_required
def update_password():
    try:
        data = request.get_json()
        new_password = data.get('new_password')
        current_password = data.get('current_password')
        
        if not new_password:
            return jsonify({
                'success': False,
                'message': 'Nueva contraseña es requerida'
            }), 400
        
        user_id = session['user_id']
        
        # Obtener usuario actual
        response = supabase.table('Usuarios').select('*').eq('id', user_id).execute()
        
        if not response.data:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404
        
        user = response.data[0]
        
        # Si tiene contraseña actual, verificarla
        if user.get('password_hash') and current_password:
            if not verify_password(current_password, user['password_hash']):
                return jsonify({
                    'success': False,
                    'message': 'Contraseña actual incorrecta'
                }), 401
        
        # Crear hash de nueva contraseña
        new_password_hash = hash_password(new_password)
        
        # Actualizar en base de datos
        update_response = supabase.table('Usuarios').update({
            'password_hash': new_password_hash
        }).eq('id', user_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Contraseña actualizada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Función auxiliar para crear contraseña (solo para desarrollo)
@app.route('/api/create-user-password', methods=['POST'])
def create_user_password():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email y contraseña son requeridos'
            }), 400
        
        # Crear hash de contraseña
        password_hash = hash_password(password)
        
        # Actualizar usuario existente con contraseña
        response = supabase.table('Usuarios').update({
            'password_hash': password_hash
        }).eq('correo', email).execute()
        
        if response.data:
            return jsonify({
                'success': True,
                'message': f'Contraseña creada para {email}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
