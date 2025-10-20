# 🚀 Guía de Despliegue en EasyPanel

Esta guía te ayudará a desplegar tu PWA de Finanzas Personales en EasyPanel.

## 📋 Requisitos Previos

1. **Cuenta en EasyPanel** ([https://easypanel.io](https://easypanel.io))
2. **Repositorio Git** (GitHub, GitLab o Bitbucket)
3. **Credenciales de Supabase** (ya las tienes en tu archivo `.env`)

## 🔐 Variables de Entorno Necesarias

En EasyPanel deberás configurar estas variables de entorno:

```
SUPABASE_URL=https://uioqfpkaslhgkqgkpmrk.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVpb3FmcGthc2xoZ2txZ2twbXJrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5MDcwMjIsImV4cCI6MjA3MzQ4MzAyMn0.uLP5Ov5XFZSj9_Akhp058uE1iBQ7jd_S5QrXv-pAYd4
FLASK_SECRET_KEY=tu_clave_secreta_muy_segura_aqui_12345
```

**⚠️ IMPORTANTE:** Cambia `FLASK_SECRET_KEY` por una clave más segura en producción.

## 📝 Pasos para Desplegar

### 1. Preparar el Repositorio Git

```bash
# Inicializar git si aún no lo has hecho
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparar aplicación para despliegue en EasyPanel"

# Conectar con tu repositorio remoto
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git

# Subir los cambios
git push -u origin main
```

**⚠️ NOTA:** Asegúrate de que el archivo `.env` NO se suba al repositorio (está en `.gitignore`).

### 2. Crear Aplicación en EasyPanel

1. **Inicia sesión** en tu panel de EasyPanel
2. **Crea un nuevo proyecto** o selecciona uno existente
3. **Agrega un nuevo servicio** > Selecciona "App"
4. **Configura el servicio:**

   - **Name:** `finanzas-pwa` (o el nombre que prefieras)
   - **Source:** Conecta tu repositorio de Git
   - **Branch:** `main` (o la rama que uses)
   - **Build Method:** Docker
   - **Port:** `5000`

### 3. Configurar Variables de Entorno

En la sección de "Environment Variables" de EasyPanel, agrega:

| Variable | Valor |
|----------|-------|
| `SUPABASE_URL` | Tu URL de Supabase |
| `SUPABASE_KEY` | Tu clave de Supabase |
| `FLASK_SECRET_KEY` | Una clave secreta fuerte (genera una nueva) |

**Generar una clave secreta fuerte:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Configurar Dominio y HTTPS

1. En EasyPanel, ve a la sección **"Domains"**
2. Agrega tu dominio personalizado o usa el subdominio proporcionado
3. EasyPanel configurará automáticamente el certificado SSL (HTTPS)

**Ejemplo de dominio:**
- `finanzas.tudominio.com` (personalizado)
- `finanzas-pwa.easypanel.host` (subdominio gratuito)

### 5. Configurar PWA para Producción

Asegúrate de que tu dominio esté configurado con **HTTPS** (obligatorio para PWA).

### 6. Desplegar

1. **Guarda la configuración** en EasyPanel
2. **Haz clic en "Deploy"**
3. EasyPanel construirá la imagen Docker y desplegará tu aplicación
4. Espera a que el estado cambie a **"Running"**

### 7. Verificar el Despliegue

Visita tu dominio y verifica:

- ✅ La aplicación carga correctamente
- ✅ El login funciona
- ✅ Puedes ver el dashboard
- ✅ HTTPS está activo (candado en el navegador)
- ✅ La PWA se puede instalar (ícono de instalación en la barra de direcciones)

## 🔧 Configuración Adicional para PWA

### 1. Verificar Service Worker

En las DevTools del navegador:
1. Abre **Application** > **Service Workers**
2. Verifica que el Service Worker esté registrado
3. Prueba el modo offline

### 2. Verificar Manifest

En las DevTools:
1. Abre **Application** > **Manifest**
2. Verifica que todos los campos estén correctos
3. Comprueba que los iconos se carguen

### 3. Actualizar URLs en el Código (Si es necesario)

Si usas un dominio personalizado, actualiza las referencias en:

**`static/js/app.js`** - Línea donde se define la base URL (si aplica)

## 📱 Instalar la PWA

### En Android:
1. Abre la app en Chrome
2. Toca el menú (3 puntos)
3. Selecciona "Instalar aplicación" o "Agregar a pantalla de inicio"

### En iOS:
1. Abre la app en Safari
2. Toca el ícono de compartir
3. Selecciona "Agregar a pantalla de inicio"

### En Desktop:
1. Abre la app en Chrome/Edge
2. Verás un ícono de instalación en la barra de direcciones
3. Haz clic en "Instalar"

## 🔄 Actualizar la Aplicación

Para desplegar cambios:

```bash
# Hacer cambios en el código
git add .
git commit -m "Descripción de los cambios"
git push

# EasyPanel detectará los cambios y re-desplegará automáticamente
```

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica los logs en EasyPanel
- Asegúrate de que las variables de entorno estén configuradas correctamente
- Verifica que el puerto 5000 esté expuesto en el Dockerfile

### El Service Worker no se registra
- Asegúrate de que HTTPS esté activo
- Limpia la caché del navegador
- Verifica que `sw.js` esté accesible en `/static/js/sw.js`

### Error de conexión con Supabase
- Verifica que las credenciales de Supabase sean correctas
- Comprueba que las tablas estén creadas en Supabase
- Revisa las políticas RLS en Supabase

### La PWA no se puede instalar
- Verifica que HTTPS esté activo
- Comprueba que el `manifest.json` sea válido
- Asegúrate de tener iconos en `/static/icons/`

## 📊 Monitoreo

EasyPanel proporciona:
- **Logs en tiempo real**
- **Métricas de CPU y memoria**
- **Estado del servicio**
- **Reinicio automático** si la app falla

## 🔒 Seguridad en Producción

✅ **Ya implementado:**
- HTTPS automático
- Variables de entorno seguras
- Autenticación con Supabase
- RLS en base de datos

🔐 **Recomendaciones adicionales:**
1. Cambia `FLASK_SECRET_KEY` regularmente
2. Habilita 2FA en tu cuenta de Supabase
3. Configura backups automáticos en Supabase
4. Revisa los logs regularmente

## 🎯 Checklist de Despliegue

- [ ] Repositorio Git configurado
- [ ] Dockerfile creado
- [ ] Variables de entorno configuradas en EasyPanel
- [ ] Dominio configurado con HTTPS
- [ ] Aplicación desplegada y funcionando
- [ ] Service Worker registrado
- [ ] PWA instalable
- [ ] Modo offline funcional
- [ ] Base de datos Supabase conectada
- [ ] Iconos PWA configurados

## 🌟 Siguiente Nivel

### Optimizaciones:
- Configurar CDN para assets estáticos
- Implementar rate limiting
- Agregar analytics (Google Analytics, etc.)
- Configurar notificaciones push

### Características adicionales:
- Exportar datos a CSV/PDF
- Gráficos más avanzados
- Categorías personalizables
- Recordatorios de pagos

---

## 📚 Recursos Adicionales

- [Documentación de EasyPanel](https://easypanel.io/docs)
- [Guía de PWA de Google](https://web.dev/progressive-web-apps/)
- [Documentación de Supabase](https://supabase.com/docs)
- [Documentación de Flask](https://flask.palletsprojects.com/)

---

¡Tu PWA de Finanzas Personales está lista para producción! 🚀💰

Para cualquier duda, revisa los logs en EasyPanel o consulta la documentación oficial.
