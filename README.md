# 🌺 FloraWatch Backend

**Sistema inteligente de monitoreo de floración de plantas** usando Django GIS, APIs meteorológicas y datos satelitales.

## ⚡ Inicio Rápido (1 minuto)

```powershell
# 1. Clonar repositorio
git clone https://github.com/Miguelin04/FloraWatch.git
cd FloraWatch/florewatchbackend

# 2. Ejecutar script de inicio
.\start_florawatch.ps1
```

**¡Eso es todo!** 🎉 El sistema se iniciará automáticamente en http://localhost:8000/

## 🚀 Características Principales

- **API REST completa** para gestión de plantas, ubicaciones y eventos de floración
- **Modelos de IA integrados** (Random Forest, LSTM, Isolation Forest)
- **Datos satelitales** de NASA MODIS, Landsat y PhenoCam Network
- **Sistema de autenticación** con tokens y permisos granulares
- **Panel de administración** completo con Django Admin
- **Documentación automática** de endpoints
- **Sistema de notificaciones** para usuarios

## 🛠️ Tecnologías Utilizadas

- **Django 5.2.7** - Framework web principal
- **Django REST Framework** - APIs REST
- **SQLite/PostgreSQL** - Base de datos
- **Scikit-learn** - Machine Learning
- **TensorFlow** - Deep Learning (LSTM)
- **NumPy/Pandas** - Procesamiento de datos
- **Pillow** - Procesamiento de imágenes

## 📦 Estructura del Proyecto

```
florewatchbackend/
├── florawatch/          # Configuración principal
│   ├── settings.py      # Configuraciones Django
│   ├── urls.py          # URLs principales
│   ├── views.py         # Vista de inicio
│   └── health_urls.py   # Health checks
├── plants/              # App de plantas
│   ├── models.py        # Modelos de plantas y floración
│   ├── views.py         # APIs de plantas
│   ├── admin.py         # Admin de plantas
│   └── urls.py          # URLs de plantas
├── satellite_data/      # App de datos satelitales
│   ├── models.py        # Modelos de datos satelitales
│   ├── views.py         # APIs de datos satelitales
│   └── admin.py         # Admin satelital
├── predictions/         # App de predicciones IA
│   ├── models.py        # Modelos de IA y predicciones
│   ├── views.py         # APIs de predicciones
│   └── admin.py         # Admin de IA
├── accounts/            # App de usuarios
│   ├── models.py        # Modelos de usuario y perfiles
│   ├── views.py         # APIs de usuarios
│   └── admin.py         # Admin de usuarios
├── requirements.txt     # Dependencias Python
├── .env                 # Variables de entorno
└── manage.py           # Comando Django
```

## 🔧 Instalación y Configuración

### 1. Crear entorno virtual
```bash
python -m venv virtual
virtual\Scripts\activate  # Windows
# source virtual/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Copiar `.env` y configurar:
```bash
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
NASA_API_KEY=tu-clave-nasa-aqui
```

### 4. Crear base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Cargar datos de ejemplo
```bash
python setup_initial_data.py
```

### 7. Ejecutar servidor
```bash
python manage.py runserver
```

## 🌐 Endpoints API

### Base URL: `http://127.0.0.1:8000/`

### 🔐 Autenticación
- `POST /api/auth/token/` - Obtener token de autenticación
- `GET /api/auth/` - Session-based auth

### 🌱 Plantas
- `GET /api/plants/species/` - Listar especies
- `POST /api/plants/species/` - Crear especie
- `GET /api/plants/locations/` - Listar ubicaciones
- `GET /api/plants/monitors/` - Monitores de plantas
- `GET /api/plants/flowering-events/` - Eventos de floración

### 🛰️ Datos Satelitales
- `GET /api/satellite/sources/` - Fuentes de datos
- `GET /api/satellite/collections/` - Colecciones de datos
- `GET /api/satellite/ndvi/{location_id}/` - Datos NDVI
- `POST /api/satellite/fetch-satellite-data/` - Obtener datos

### 🤖 Predicciones IA
- `GET /api/predictions/models/` - Modelos de IA
- `POST /api/predictions/predict/flowering/` - Predecir floración
- `POST /api/predictions/detect/current/` - Detectar floración actual
- `POST /api/predictions/train-model/` - Entrenar modelo

### 👤 Usuarios
- `POST /api/accounts/register/` - Registrar usuario
- `GET /api/accounts/profile/` - Perfil actual
- `GET /api/accounts/dashboard/` - Dashboard usuario

## 🔍 Panel de Administración

Accede a `http://127.0.0.1:8000/admin/` con las credenciales de superusuario para:

- Gestionar especies de plantas y ubicaciones
- Ver eventos de floración detectados
- Administrar modelos de IA y sesiones de predicción
- Gestionar usuarios y perfiles
- Configurar fuentes de datos satelitales

## 📊 Modelos de Datos Principales

### Plants App
- **PlantSpecies**: Especies de plantas monitoreadas
- **Location**: Ubicaciones geográficas
- **PlantMonitor**: Instancias específicas de plantas
- **FloweringEvent**: Eventos de floración detectados

### Predictions App
- **AIModel**: Modelos de IA entrenados
- **PredictionSession**: Sesiones de predicción
- **FloweringPrediction**: Predicciones específicas
- **TrainingDataset**: Datasets de entrenamiento

### Satellite Data App
- **SatelliteDataSource**: Fuentes de datos (NASA, Landsat)
- **SatelliteDataCollection**: Colecciones de datos
- **SatelliteDataPoint**: Puntos individuales de datos
- **WeatherData**: Datos meteorológicos

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Crear datos de prueba
python setup_initial_data.py
```

## 🚀 Producción

Para despliegue en producción:

1. Cambiar `DEBUG = False` en settings.py
2. Configurar base de datos PostgreSQL
3. Configurar servidor web (Nginx + Gunicorn)
4. Configurar variables de entorno de producción
5. Ejecutar `python manage.py collectstatic`

## 👨‍💻 Desarrollador

**Miguel Luna**  
📧 miguel.a.luna@unl.edu.ec  
🏛️ Universidad Nacional de Loja  
📍 Loja, Ecuador

## 📄 Licencia

Este proyecto está desarrollado para fines académicos y de investigación en la Universidad Nacional de Loja.

---

## 🔄 Integración con Frontend

Este backend está diseñado para trabajar con cualquier frontend que consuma APIs REST. La configuración CORS permite conexiones desde:

- `http://localhost:3000` (React/Next.js)
- `http://localhost:8080` (Vue.js)
- Otros puertos configurables

### Ejemplo de uso desde JavaScript:

```javascript
// Obtener token de autenticación
const response = await fetch('http://127.0.0.1:8000/api/auth/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'miguel', password: 'tu-password' })
});
const { token } = await response.json();

// Hacer predicción de floración
const prediction = await fetch('http://127.0.0.1:8000/api/predictions/predict/flowering/', {
    method: 'POST',
    headers: { 
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json' 
    },
    body: JSON.stringify({ location_id: 1, plant_species_id: 1 })
});
```