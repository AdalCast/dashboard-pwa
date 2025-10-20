@echo off
echo =========================================
echo   CONFIGURACION PWA FINANZAS PERSONALES
echo =========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo.
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error al crear el entorno virtual
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual ya existe
)

echo.

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo 📋 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error al instalar dependencias
    pause
    exit /b 1
)

echo.
echo ✅ ¡Instalación completada!
echo.
echo 📋 SIGUIENTES PASOS:
echo.
echo 1. Configura tu base de datos en Supabase usando los scripts SQL del README.md
echo 2. Agrega los iconos en static/icons/ (ver static/icons/README.md)
echo 3. Ejecuta: python app.py
echo 4. Visita: http://localhost:5000
echo.
echo 🚀 ¡Tu PWA de finanzas está lista!
echo.
pause