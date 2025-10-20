# Finanzas PWA

Una aplicación web progresiva (PWA) para gestión de finanzas personales, desarrollada con Flask y diseñada para funcionar tanto online como offline.

## Características

- 📊 **Dashboard interactivo** con resumen financiero
- 💳 **Gestión de transacciones** con filtros y edición
- 📅 **Gastos fijos recurrentes**
- 👤 **Perfil de usuario** con preferencias personalizables
- 🔒 **Autenticación segura** con Supabase
- 📱 **PWA completa** - funciona offline y se puede instalar
- 🎨 **Diseño responsive** para móvil y escritorio

## Tecnologías

### Backend
- **Flask** - Framework web de Python
- **Supabase** - Base de datos y autenticación
- **python-dotenv** - Gestión de variables de entorno

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript vanilla** - Interactividad
- **Chart.js** - Gráficos interactivos
- **Service Worker** - Funcionalidad offline

## Instalación

### Requisitos previos
- Python 3.8 o superior
- Cuenta de Supabase configurada
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd DashboardPWA
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   - El archivo `.env` ya está configurado con las credenciales de Supabase
   - Opcionalmente, puedes cambiar `FLASK_SECRET_KEY` por una clave más segura

5. **Configurar la base de datos en Supabase**
   
   Ejecuta los siguientes scripts SQL en tu panel de Supabase:

   ```sql
   -- Tabla de usuarios
   CREATE TABLE usuarios (
       id UUID PRIMARY KEY DEFAULT auth.uid(),
       correo TEXT UNIQUE NOT NULL,
       telefono TEXT,
       reporte_diario BOOLEAN DEFAULT true,
       reporte_semanal BOOLEAN DEFAULT true,
       reporte_mensual BOOLEAN DEFAULT true,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );

   -- Tabla de transacciones
   CREATE TABLE transacciones (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
       fecha DATE NOT NULL,
       categoria TEXT NOT NULL,
       monto REAL NOT NULL,
       descripcion TEXT NOT NULL,
       tipo TEXT NOT NULL CHECK (tipo IN ('gasto', 'ingreso')),
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );

   -- Tabla de gastos fijos
   CREATE TABLE gastos_fijos (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
       dia_pago INTEGER NOT NULL CHECK (dia_pago >= 1 AND dia_pago <= 31),
       categoria TEXT NOT NULL,
       monto REAL NOT NULL,
       descripcion TEXT NOT NULL,
       frecuencia TEXT NOT NULL DEFAULT 'mensual',
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );

   -- Políticas de seguridad RLS
   ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
   ALTER TABLE transacciones ENABLE ROW LEVEL SECURITY;
   ALTER TABLE gastos_fijos ENABLE ROW LEVEL SECURITY;

   -- Políticas para usuarios
   CREATE POLICY "Los usuarios pueden ver su propio perfil" ON usuarios
       FOR SELECT USING (auth.uid() = id);
   
   CREATE POLICY "Los usuarios pueden actualizar su propio perfil" ON usuarios
       FOR UPDATE USING (auth.uid() = id);

   -- Políticas para transacciones
   CREATE POLICY "Los usuarios pueden ver sus propias transacciones" ON transacciones
       FOR SELECT USING (auth.uid() = usuario_id);
   
   CREATE POLICY "Los usuarios pueden insertar sus propias transacciones" ON transacciones
       FOR INSERT WITH CHECK (auth.uid() = usuario_id);
   
   CREATE POLICY "Los usuarios pueden actualizar sus propias transacciones" ON transacciones
       FOR UPDATE USING (auth.uid() = usuario_id);
   
   CREATE POLICY "Los usuarios pueden eliminar sus propias transacciones" ON transacciones
       FOR DELETE USING (auth.uid() = usuario_id);

   -- Políticas para gastos fijos
   CREATE POLICY "Los usuarios pueden ver sus propios gastos fijos" ON gastos_fijos
       FOR SELECT USING (auth.uid() = usuario_id);
   
   CREATE POLICY "Los usuarios pueden insertar sus propios gastos fijos" ON gastos_fijos
       FOR INSERT WITH CHECK (auth.uid() = usuario_id);
   
   CREATE POLICY "Los usuarios pueden actualizar sus propios gastos fijos" ON gastos_fijos
       FOR UPDATE USING (auth.uid() = usuario_id);
   
   CREATE POLICY "Los usuarios pueden eliminar sus propios gastos fijos" ON gastos_fijos
       FOR DELETE USING (auth.uid() = usuario_id);
   ```

6. **Agregar iconos de la PWA**
   - Coloca `icon-192x192.png` e `icon-512x512.png` en la carpeta `static/icons/`
   - Ver `static/icons/README.md` para más detalles

## Ejecución

### Desarrollo
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### Producción
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Uso

### Primera vez
1. Visita la aplicación en tu navegador
2. Inicia sesión con las credenciales de tu página de CV
3. Comienza a agregar tus transacciones y gastos fijos

### Características principales

#### Dashboard
- Resumen financiero del mes actual
- Gráfico de gastos por categoría
- Lista de transacciones recientes

#### Transacciones
- Agregar ingresos y gastos
- Editar transacciones existentes
- Filtrar por mes y tipo
- Eliminar transacciones con confirmación

#### Gastos Fijos
- Registrar gastos recurrentes
- Configurar día de pago y frecuencia
- Ver total de gastos mensuales

#### Perfil
- Actualizar información personal
- Configurar preferencias de reportes
- Gestionar cuenta

### PWA (Progressive Web App)
- **Instalación**: Usa el botón "Agregar a pantalla de inicio" en tu navegador móvil
- **Modo offline**: La aplicación funciona sin conexión con los datos guardados
- **Notificaciones**: (Funcionalidad lista para implementar reportes automáticos)

## Estructura del Proyecto

```
DashboardPWA/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── .env                  # Variables de entorno
├── static/
│   ├── css/
│   │   └── style.css     # Estilos principales
│   ├── js/
│   │   ├── app.js        # JavaScript principal
│   │   └── sw.js         # Service Worker
│   └── icons/            # Iconos de la PWA
├── templates/
│   ├── base.html         # Template base
│   ├── login.html        # Página de login
│   ├── dashboard.html    # Dashboard principal
│   ├── transactions.html # Gestión de transacciones
│   ├── fixed_expenses.html # Gastos fijos
│   └── profile.html      # Perfil de usuario
└── README.md            # Este archivo
```

## API Endpoints

### Autenticación
- `POST /api/login` - Iniciar sesión
- `POST /api/logout` - Cerrar sesión

### Dashboard
- `GET /api/dashboard-summary` - Resumen financiero

### Transacciones
- `GET /api/transactions` - Listar transacciones
- `POST /api/transactions` - Crear transacción
- `PUT /api/transactions/{id}` - Actualizar transacción
- `DELETE /api/transactions/{id}` - Eliminar transacción

### Gastos Fijos
- `GET /api/fixed-expenses` - Listar gastos fijos
- `POST /api/fixed-expenses` - Crear gasto fijo
- `PUT /api/fixed-expenses/{id}` - Actualizar gasto fijo
- `DELETE /api/fixed-expenses/{id}` - Eliminar gasto fijo

### Perfil
- `GET /api/profile` - Obtener perfil
- `PUT /api/profile` - Actualizar perfil

## Personalización

### Colores y tema
- Edita las variables CSS en `static/css/style.css`
- Los colores principales están definidos en `:root`

### Categorías
- Las categorías de gastos e ingresos están en los templates
- Puedes agregar o modificar categorías en `transactions.html`

### Reportes automáticos
- La funcionalidad está preparada en la base de datos
- Implementa la lógica de envío en el backend según tus necesidades

## Soporte

- **Navegadores**: Chrome, Firefox, Safari, Edge (versiones recientes)
- **Dispositivos**: Responsive design para móvil, tablet y escritorio
- **PWA**: Compatible con instalación en iOS y Android

## Seguridad

- ✅ Autenticación con Supabase
- ✅ Row Level Security (RLS) en base de datos
- ✅ Validación de sesiones en todas las rutas protegidas
- ✅ Protección CSRF implícita
- ✅ Variables de entorno para credenciales

## Licencia

Este proyecto es de código libre para uso personal y educativo.

---

¡Tu PWA de finanzas personales está lista para usar! 🚀