#!/bin/bash

echo "========================================="
echo "   CONFIGURACION PWA FINANZAS PERSONALES"
echo "========================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    echo ""
    echo "Por favor instala Python3 desde https://python.org"
    exit 1
fi

echo "✅ Python3 detectado"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el entorno virtual"
        exit 1
    fi
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

echo ""

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "📋 Actualizando pip..."
python -m pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "📋 SIGUIENTES PASOS:"
echo ""
echo "1. Configura tu base de datos en Supabase usando los scripts SQL del README.md"
echo "2. Agrega los iconos en static/icons/ (ver static/icons/README.md)"
echo "3. Ejecuta: python app.py"
echo "4. Visita: http://localhost:5000"
echo ""
echo "🚀 ¡Tu PWA de finanzas está lista!"
echo ""