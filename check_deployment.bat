@echo off
echo ========================================
echo   VERIFICACION PARA DESPLIEGUE
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist "venv" (
    call venv\Scripts\activate.bat
)

REM Ejecutar el script de verificación
python check_deployment.py

echo.
pause
