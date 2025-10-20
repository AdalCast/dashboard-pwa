# ✅ CHECKLIST RÁPIDO - Despliegue en EasyPanel

## 📋 Antes de Desplegar

### 1. Archivos Necesarios (✅ Ya Creados)
- [x] `Dockerfile` - Para construir la imagen Docker
- [x] `.dockerignore` - Archivos a ignorar en Docker
- [x] `docker-compose.yml` - Para testing local
- [x] `.gitignore` - Archivos a ignorar en Git
- [x] `.env.example` - Ejemplo de variables de entorno
- [x] `DEPLOYMENT.md` - Guía completa de despliegue

### 2. Configuración (⚠️ Pendiente)
- [ ] **Crear iconos PWA** (icon-192x192.png y icon-512x512.png)
- [ ] **Generar nueva FLASK_SECRET_KEY** para producción
- [ ] **Subir código a repositorio Git** (GitHub/GitLab)

### 3. En EasyPanel (⚠️ Pendiente)
- [ ] Crear cuenta en [EasyPanel.io](https://easypanel.io)
- [ ] Crear nueva aplicación
- [ ] Conectar repositorio Git
- [ ] Configurar variables de entorno
- [ ] Configurar dominio con HTTPS
- [ ] Desplegar

---

## 🎯 Pasos Rápidos

### Paso 1: Generar Nueva Clave Secreta
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Guarda este valor para configurarlo en EasyPanel.

### Paso 2: Crear Iconos PWA
- Descarga o crea iconos de 192x192 y 512x512 píxeles
- Colócalos en `static/icons/`
- Usa [pwabuilder.com/imageGenerator](https://www.pwabuilder.com/imageGenerator)

### Paso 3: Subir a Git
```bash
git init
git add .
git commit -m "Preparar para despliegue en EasyPanel"
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

**⚠️ IMPORTANTE:** Asegúrate de que `.env` NO se suba (ya está en .gitignore)

### Paso 4: Configurar en EasyPanel

**Variables de Entorno:**
```
SUPABASE_URL=https://uioqfpkaslhgkqgkpmrk.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
FLASK_SECRET_KEY=[tu_nueva_clave_generada]
```

**Configuración de la App:**
- Build Method: Docker
- Port: 5000
- Auto Deploy: Enabled

### Paso 5: Verificar
- [ ] App funciona en el dominio
- [ ] HTTPS activo (candado verde)
- [ ] Service Worker registrado
- [ ] PWA instalable
- [ ] Modo offline funciona

---

## 🚀 Comando de Verificación

Ejecuta esto para verificar que todo está listo:

```bash
python check_deployment.py
```

o en Windows:
```bash
check_deployment.bat
```

---

## 📚 Recursos

- **Guía Completa:** Lee `DEPLOYMENT.md`
- **EasyPanel Docs:** [easypanel.io/docs](https://easypanel.io/docs)
- **PWA Checklist:** [web.dev/pwa-checklist](https://web.dev/pwa-checklist)

---

## 🆘 Problemas Comunes

### "App no inicia"
→ Verifica logs en EasyPanel
→ Revisa variables de entorno

### "PWA no se puede instalar"
→ Asegúrate de tener HTTPS
→ Verifica que existan los iconos
→ Limpia caché del navegador

### "Error de Supabase"
→ Verifica credenciales
→ Comprueba políticas RLS
→ Revisa que las tablas existan

---

**¿Listo para desplegar? 🚀**

Sigue la guía completa en `DEPLOYMENT.md` para instrucciones paso a paso.
