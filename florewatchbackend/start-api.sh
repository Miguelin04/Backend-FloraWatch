# Para poder ejecutar este script, asegúrate de tener Python 3.10 instalado y accesible desde la línea de comandos y ejecutar chmod +x start-api.sh
#!/bin/bash

# salir si hay un error
set -e  

# nombre del entorno
ENV_NAME="virtual_311"

# crear entorno si no existe
if [ ! -d "$ENV_NAME" ]; then
    echo "🔹 Creando entorno virtual con Python 3.10..."
    python3.10 -m venv $ENV_NAME
fi

# activar entorno
echo "🔹 Activando entorno virtual..."

# Verificar si el sistema es Windows (asumiendo que $ENV_NAME contiene el path al entorno)
if [ -d "$ENV_NAME/Scripts" ]; then
    # CMD/PowerShell
    source $ENV_NAME/Scripts/activate
elif [ -d "$ENV_NAME/bin" ]; then
    # Linux o macOS
    source $ENV_NAME/bin/activate
else
    echo "❌ Error: No se encontró el script de activación del entorno virtual en las rutas estándar (bin/ o Scripts/)."
fi

# instalar dependencias si requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "🔹 Instalando dependencias de requirements.txt..."
    pip install -r requirements.txt
else
    echo "🔹 Instalando Django..."
    pip install django
fi

# correr migraciones (opcional si es proyecto nuevo)
echo "🔹 Aplicando migraciones..."
python manage.py migrate || echo "⚠️ No se encontró manage.py, saltando migraciones..."

# levantar servidor
echo "🚀 Levantando Django API en http://127.0.0.1:8000 ..."
python manage.py runserver
