# 🌺 BloomWatch - Sistema Inteligente de Monitoreo de Floración

**Sistema inteligente de monitoreo de floración de plantas** usando Django GIS, APIs meteorológicas, datos satelitales y modelos de IA con PyTorch.

## ⚡ Inicio Rápido (1 minuto)

```powershell
# 1. Clonar repositorio
git clone https://github.com/Miguelin04/BloomWatch.git
cd BloomWatch

# 2. Activar entorno virtual
.\virtual_311\Scripts\Activate.ps1

# 3. Ejecutar servidor
python manage.py runserver
```

**¡Eso es todo!** 🎉 El sistema se iniciará automáticamente en http://localhost:8000/

## 🚀 Características Principales

- **API REST completa** para gestión de plantas, ubicaciones y eventos de floración
- **Modelos de IA integrados** con PyTorch (U-Net para segmentación de floración)
- **Datos satelitales** de NASA MODIS, Landsat y PhenoCam Network
- **Sistema de autenticación** con tokens y permisos granulares
- **Panel de administración** completo con Django Admin
- **Documentación automática** de endpoints
- **Sistema de notificaciones** para usuarios

## 🛠️ Tecnologías Utilizadas

- **Django 5.2.7** - Framework web principal
- **Django REST Framework** - APIs REST
- **PyTorch** - Deep Learning y modelos de IA
- **SQLite/PostgreSQL** - Base de datos
- **NumPy/Pandas** - Procesamiento de datos
- **Pillow** - Procesamiento de imágenes

## 📦 Estructura del Proyecto

```
BloomWatch/
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
├── models/              # Modelos de PyTorch entrenados
│   └── best_model.pth   # Modelo U-Net para detección de floración
├── requirements.txt     # Dependencias Python
└── manage.py           # Comando Django
```

## 🔧 Instalación y Configuración

### 1. Crear entorno virtual
```bash
python -m venv virtual_311
virtual_311\Scripts\activate  # Windows
# source virtual_311/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
pip install torch torchvision  # Para modelos de IA
```

### 3. Crear base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear superusuario
```bash
python manage.py createsuperuser
```

### 5. Ejecutar servidor
```bash
python manage.py runserver
```

## 🤖 Modelo de IA Integrado

El sistema incluye un modelo U-Net entrenado para segmentación de floración:

- **Arquitectura:** U-Net (Encoder-Decoder con skip connections)
- **Entrada:** Imágenes RGB de 64x64 píxeles
- **Salida:** Máscaras de segmentación de floración
- **Parámetros:** 31M parámetros entrenados
- **Precisión:** Detección pixel por pixel de regiones florales

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

## 👨‍💻 Desarrollador

**Miguel Luna**  
📧 miguel.a.luna@unl.edu.ec  
🏛️ Universidad Nacional de Loja  
📍 Loja, Ecuador

## 📄 Licencia

Este proyecto está desarrollado para fines académicos y de investigación en la Universidad Nacional de Loja.