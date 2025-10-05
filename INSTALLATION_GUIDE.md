# 🌺 FloraWatch Backend

Sistema de monitoreo inteligente de floración de plantas usando Django, PostGIS, y APIs meteorológicas/satelitales.

## 📋 Índice

- [🚀 Instalación Rápida](#-instalación-rápida)
- [📦 Requisitos del Sistema](#-requisitos-del-sistema)
- [⚙️ Configuración](#️-configuración)
- [🌐 APIs Disponibles](#-apis-disponibles)
- [🧪 Pruebas](#-pruebas)
- [📊 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔧 Troubleshooting](#-troubleshooting)

---

## 🚀 Instalación Rápida

### **1. Clonar el repositorio**
```bash
git clone https://github.com/Miguelin04/FloraWatch.git
cd FloraWatch/florewatchbackend
```

### **2. Activar entorno virtual**
```powershell
.\virtual_311\Scripts\Activate.ps1
```

### **3. Configurar variables de entorno**
```powershell
$env:GDAL_LIBRARY_PATH = "D:\ruta\completa\virtual_311\Lib\site-packages\osgeo\gdal.dll"
$env:GDAL_DATA = "D:\ruta\completa\virtual_311\Lib\site-packages\osgeo\data"
$env:DB_PORT = "5433"
```

### **4. Iniciar servidor**
```powershell
python manage.py runserver
```

### **5. Probar API**
Visita: `http://localhost:8000/api/status/`

---

## 📦 Requisitos del Sistema

### **Software Necesario:**
- ✅ **Python 3.11.9** (incluido en `virtual_311/`)
- ✅ **PostgreSQL 15** con PostGIS
- ✅ **pgAdmin 4** (para gestión de BD)

### **APIs Externas:**
- ✅ **NASA API Key**: `CDhaFiZI9T8ZbfcKcw0lUpEwdj9iF88h9ujznu9h`
- ✅ **OpenWeatherMap API Key**: `774e34e3b37ec7f9d61e7df5dc31cf8c`

### **Paquetes Python Incluidos:**
```
Django==5.2.7
djangorestframework==3.15.2
djangorestframework-gis==1.0
psycopg2-binary==2.9.10
python-dotenv==1.0.1
django-cors-headers==4.5.0
requests==2.32.3
GDAL==3.8.4 (wheel precompilado)
```

---

## ⚙️ Configuración

### **1. Base de Datos PostgreSQL**

#### **Credenciales por defecto:**
```env
DB_NAME=florawatch_db
DB_USER=florawatch_user
DB_PASSWORD=flora123
DB_HOST=localhost
DB_PORT=5433
```

#### **Crear extensión PostGIS (una sola vez):**
```sql
-- Conectar como superusuario 'postgres' (password: 1234)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Dar permisos al usuario de la aplicación
GRANT ALL PRIVILEGES ON DATABASE florawatch_db TO florawatch_user;
GRANT ALL ON SCHEMA public TO florawatch_user;
```

### **2. Variables de Entorno (.env)**

El archivo `.env` ya está configurado con:
```env
# APIs externas
NASA_API_KEY=CDhaFiZI9T8ZbfcKcw0lUpEwdj9iF88h9ujznu9h
OPENWEATHERMAP_API_KEY=774e34e3b37ec7f9d61e7df5dc31cf8c

# Base de datos
DB_PORT=5433
```

### **3. Migraciones de Base de Datos**
```powershell
python manage.py makemigrations
python manage.py migrate
```

### **4. Crear Superusuario**
```powershell
python manage.py createsuperuser
# Usuario: miguel
# Email: miguel.a.luna@unl.edu.ec
```

---

## 🌐 APIs Disponibles

### **Estado del Sistema**
```
GET /api/status/
```
Respuesta:
```json
{
  "timestamp": "2025-10-04T18:12:10.734545",
  "apis": {
    "openweathermap": {"status": "active"},
    "nasa": {"status": "configured"}
  },
  "services": {
    "database": "active",
    "gdal": "active", 
    "postgis": "active"
  }
}
```

### **APIs Meteorológicas**
```
GET /api/weather/{lat}/{lon}/                    # Clima actual
GET /api/weather/{lat}/{lon}/forecast/           # Pronóstico
GET /api/weather/{lat}/{lon}/flowering-analysis/ # Análisis floración
```

**Ejemplo Madrid:**
```
GET /api/weather/40.4168/-3.7038/flowering-analysis/
```

Respuesta:
```json
{
  "location": {"lat": 40.4168, "lon": -3.7038, "city": "Madrid"},
  "current_conditions": {
    "temperature": 21.16,
    "humidity": 52,
    "description": "cielo claro"
  },
  "flowering_analysis": {
    "temperature_favorable": true,
    "humidity_favorable": true, 
    "overall_score": 100,
    "recommendation": "Condiciones excelentes para floración"
  }
}
```

### **APIs Satelitales**
```
GET /api/satellite/{lat}/{lon}/     # Datos NASA
GET /api/analysis/{lat}/{lon}/      # Análisis combinado
```

### **Panel de Administración**
```
http://localhost:8000/admin/
```

---

## 🧪 Pruebas

### **Script de Pruebas Automáticas**
```powershell
python test_apis.py
```

**Resultados esperados:**
```
🧪 INICIANDO PRUEBAS DE APIS FLORAWATCH
==================================================
🗄️  PROBANDO CONEXIÓN A BASE DE DATOS...
✅ PostgreSQL conectado
✅ PostGIS activo
🌤️  PROBANDO OPENWEATHERMAP API...
✅ Clima actual obtenido
✅ Análisis de floración completado
🛰️  PROBANDO NASA API...
✅ NASA API respondió correctamente
==================================================
🎯 Tasa de éxito: 100.0%
🎉 ¡Todas las APIs están funcionando correctamente!
```

### **Prueba Manual GDAL**
```powershell
python test_gdal.py
```

---

## 📊 Estructura del Proyecto

```
florewatchbackend/
├── 📁 virtual_311/           # Entorno Python 3.11 + GDAL
├── 📁 florawatch/           # Configuración Django
├── 📁 accounts/             # Gestión usuarios
├── 📁 plants/               # Modelos plantas y ubicaciones
├── 📁 satellite_data/       # Datos satelitales
├── 📁 predictions/          # Predicciones IA
├── 📄 weather_service.py    # Servicio OpenWeatherMap
├── 📄 api_views.py          # Vistas API externas
├── 📄 api_urls.py           # URLs API externas  
├── 📄 test_apis.py          # Pruebas automáticas
├── 📄 test_gdal.py          # Prueba GDAL
├── 📄 .env                  # Variables entorno
├── 📄 requirements.txt      # Dependencias Python
└── 📄 manage.py            # Gestor Django
```

### **Modelos de Datos Principales**

#### **PlantSpecies** - Especies de plantas
- `name`: Nombre común
- `scientific_name`: Nombre científico  
- `plant_type`: Tipo (árbol, arbusto, flor, etc.)
- `typical_flowering_months`: Meses de floración

#### **Location** - Ubicaciones geográficas  
- `name`: Nombre del lugar
- `coordinates`: Campo PostGIS (Point)
- `latitude/longitude`: Coordenadas tradicionales
- `country`: País

#### **FloweringEvent** - Eventos de floración
- `detection_date`: Fecha detección
- `flowering_stage`: Etapa (capullo, temprana, máxima, etc.)
- `detection_method`: Método (visual, satelital, IA)
- `confidence_score`: Nivel de confianza (0-1)

---

## 🔧 Troubleshooting

### **Error: "Python no encontrado"**
```powershell
# Activar entorno virtual
.\virtual_311\Scripts\Activate.ps1
```

### **Error: "GDAL library not found"**
```powershell
# Configurar variables GDAL
$env:GDAL_LIBRARY_PATH = "D:\ruta\completa\virtual_311\Lib\site-packages\osgeo\gdal.dll"
$env:GDAL_DATA = "D:\ruta\completa\virtual_311\Lib\site-packages\osgeo\data"
```

### **Error: "PostGIS extension not found"**
```sql
-- En pgAdmin como usuario 'postgres':
CREATE EXTENSION IF NOT EXISTS postgis;
```

### **Error: "Port 5432 connection refused"**
```powershell
# PostgreSQL está en puerto 5433
$env:DB_PORT = "5433"
```

### **Error: "Authentication credentials not provided"**
Ya solucionado - las APIs son públicas (sin autenticación).

---

## 🎯 Estado del Proyecto

### ✅ **Completamente Funcional:**
- Django Backend con GIS
- PostgreSQL + PostGIS  
- GDAL 3.8.4 geoespacial
- OpenWeatherMap API integrada
- NASA API integrada
- Análisis de condiciones de floración
- Panel de administración
- APIs RESTful públicas

### 🔜 **Próximos Pasos:**
- Frontend React/Vue
- Modelos de IA para detección automática
- Dashboard de visualización
- Aplicación móvil

---

## 📞 Soporte

- **Desarrollador**: Miguel Luna
- **Email**: miguel.a.luna@unl.edu.ec
- **Proyecto**: FloraWatch - Sistema de Monitoreo de Floración

---

🌺 **¡FloraWatch está listo para monitorear la floración del mundo!** 🌍