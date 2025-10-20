@echo off
echo 🚀 Iniciando PWA Finanzas Personales...
echo.

REM Verificar si el entorno virtual existe
if not exist "venv" (
    echo ❌ Error: Entorno virtual no encontrado
    echo.
    echo Ejecuta setup.bat primero para configurar el proyecto
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar si Flask está instalado
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Flask no está instalado
    echo.
    echo Ejecuta setup.bat primero para instalar las dependencias
    pause
    exit /b 1
)

echo ✅ Iniciando servidor Flask...
echo.
echo 🌐 La aplicación estará disponible en: http://localhost:5000
echo 🛑 Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar la aplicación
python app.py