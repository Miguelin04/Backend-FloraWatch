# 🔧 CONFIGURACIÓN RÁPIDA FLORAWATCH

## ⚡ Inicio Súper Rápido (1 minuto)

### **Solo necesitas hacer esto UNA VEZ:**

1. **Abrir PowerShell como Administrador** en la carpeta del proyecto
2. **Ejecutar el script de inicio:**
   ```powershell
   .\start_florawatch.ps1
   ```

¡Eso es todo! El sistema se iniciará automáticamente.

---

## 📋 Checklist de Verificación

### **Antes de ejecutar el script:**

- [ ] PostgreSQL 15 instalado y corriendo
- [ ] pgAdmin 4 instalado  
- [ ] Base de datos `florawatch_db` creada
- [ ] Usuario `florawatch_user` con password `flora123`
- [ ] Extensión PostGIS habilitada
- [ ] Puerto PostgreSQL: **5433** (no 5432)

### **Credenciales de acceso:**

#### **PostgreSQL:**
- **Superusuario**: `postgres` / `1234`  
- **Usuario app**: `florawatch_user` / `flora123`
- **Puerto**: `5433`

#### **Django Admin:**
- **Usuario**: `miguel`
- **Email**: `miguel.a.luna@unl.edu.ec`

---

## 🚨 Si algo falla:

### **1. Error "Python no encontrado"**
```powershell
# Activar manualmente el entorno
.\virtual_311\Scripts\Activate.ps1
```

### **2. Error PostgreSQL**
```powershell
# Verificar que PostgreSQL esté en puerto 5433
# Abrir pgAdmin y conectar con postgres/1234
```

### **3. Error GDAL**
```powershell
# Las variables se configuran automáticamente
# Si falla, ejecutar manualmente:
$env:GDAL_LIBRARY_PATH = "D:\ruta\completa\virtual_311\Lib\site-packages\osgeo\gdal.dll"
```

---

## 🌐 URLs Importantes

Una vez iniciado el servidor:

- **🏠 Inicio**: http://localhost:8000/
- **⚙️ Admin**: http://localhost:8000/admin/
- **📊 Estado APIs**: http://localhost:8000/api/status/
- **🌤️ Clima Madrid**: http://localhost:8000/api/weather/40.4168/-3.7038/
- **🌺 Análisis Floración**: http://localhost:8000/api/weather/40.4168/-3.7038/flowering-analysis/

---

## 🎯 Resultado Esperado

Si todo funciona correctamente, deberías ver:

```
🧪 INICIANDO PRUEBAS DE APIS FLORAWATCH
==================================================
✅ PostgreSQL conectado
✅ PostGIS activo  
✅ Clima actual obtenido
✅ NASA API respondió correctamente
🎯 Tasa de éxito: 100.0%
🎉 ¡Todas las APIs están funcionando correctamente!

🚀 INICIANDO SERVIDOR DJANGO...  
📍 URL: http://localhost:8000/
System check identified no issues (0 silenced).
Django version 5.2.7, using settings 'florawatch.settings'
Starting development server at http://127.0.0.1:8000/
```

---

**¡Tu sistema FloraWatch estará listo en menos de 1 minuto!** 🎉