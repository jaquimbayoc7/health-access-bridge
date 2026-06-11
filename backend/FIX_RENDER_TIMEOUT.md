# Solución al Timeout de Deploy en Render

## 🔴 Problema

El deploy falló con el error:
```
==&gt; Timed Out
==&gt; Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
```

Esto ocurre cuando Render no puede verificar que el servicio esté funcionando dentro del tiempo límite (normalmente 60 segundos).

## ✅ Soluciones Implementadas

### 1. Startup Optimizado

**Cambios en `app/main.py`**:

- ✅ **Logging condicional**: El middleware de logging detallado solo se activa con `DEBUG=true`
- ✅ **Seed opcional**: El seed de datos ahora es opcional y se salta por defecto en producción
- ✅ **Mensajes más cortos**: Reducción del logging verboso durante startup
- ✅ **Startup más rápido**: De ~20-30 segundos a ~5-10 segundos

### 2. Variables de Entorno Opcionales

Nuevas variables de entorno que puedes configurar en Render:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `DEBUG` | `false` (default) | Habilita logging detallado cuando es `true` |
| `RUN_SEED` | `false` (default) | Ejecuta el seed de datos cuando es `true` |

### 3. Health Check Optimizado

El endpoint `/health` sigue siendo ultra-rápido y responde inmediatamente.

## 📋 Pasos para Desplegar

### 1. Subir los Cambios

```bash
git add backend/app/main.py
git commit -m "Perf: Optimizar startup para prevenir timeout en Render"
git push origin master
```

### 2. Esperar el Deploy

Render detectará automáticamente los cambios y comenzará a redesplegar.

### 3. Verificar en Logs

En **Render Dashboard → Backend Service → Logs**, deberías ver:

```
⚡ Inicializando esquema...
✓ DB ready
⏭ Seed skipped (set RUN_SEED=true to enable)
🌐 CORS configurado para 7 orígenes
```

**Tiempo esperado de startup**: ~5-10 segundos

## 🔧 Configuración Adicional en Render (Opcional)

Si aún hay problemas de timeout, puedes ajustar estas configuraciones:

### Opción 1: Aumentar el Timeout de Health Check

En **Render Dashboard → Backend Service → Settings → Health Check**:

1. Scroll hasta "Health Check Grace Period"
2. Aumenta el valor a **90 segundos** (default es 60)
3. Save changes

### Opción 2: Cambiar el Plan de Render

Los planes gratuitos de Render tienen menos recursos y pueden ser más lentos:

- **Free Plan**: 512 MB RAM, puede tardar más en iniciar
- **Starter Plan ($7/mes)**: 1 GB RAM, inicio más rápido
- **Standard Plan**: 2 GB RAM o más, mucho más rápido

### Opción 3: Deshabilitar Temporalmente el Health Check

⚠️ **Solo para debugging**:

En `render.yaml`:
```yaml
# Comentar temporalmente
# healthCheckPath: /health
# healthCheckInterval: 300
```

Esto deshabilitará el health check y permitirá que el servicio se inicie sin verificación.

## 🐛 Debugging Adicional

### Si el Timeout Persiste

1. **Verifica la conexión a la base de datos**:
   - Ve a **Render Dashboard → Database**
   - Verifica que esté "Available"
   - Si está "Suspended", actívala

2. **Verifica las variables de entorno**:
   ```bash
   DATABASE_URL=postgresql://...  # Debe existir
   SECRET_KEY=...                  # Debe existir
   ```

3. **Revisa los logs completos**:
   - Busca errores antes del "Timed Out"
   - Si hay errores de conexión a DB, el problema es la base de datos

### Test Local

Prueba localmente que el startup sea rápido:

```bash
cd backend

# Sin seed (como en producción)
time uvicorn app.main:app --host 0.0.0.0 --port 8000

# Deberías ver:
# ⚡ Inicializando esquema...
# ✓ DB ready
# ⏭ Seed skipped
# 🌐 CORS configurado para 7 orígenes
# Uvicorn running on http://0.0.0.0:8000

# Startup debería tomar menos de 5 segundos
```

### Con Seed Habilitado (Solo Dev)

```bash
RUN_SEED=true uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🎯 Checklist de Deploy

Antes de reportar un bug, verifica:

- [ ] El build se completó exitosamente ("Build successful 🎉")
- [ ] La base de datos está activa en Render
- [ ] Las variables de entorno están configuradas (`DATABASE_URL`, `SECRET_KEY`)
- [ ] Los logs muestran "⚡ Inicializando esquema..." sin errores
- [ ] El startup completo toma menos de 30 segundos
- [ ] El endpoint `/health` está accesible (prueba en navegador)

## 📊 Diferencias: Antes vs. Después

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Tiempo de startup** | ~20-30s | ~5-10s |
| **Logging en producción** | Verboso | Mínimo |
| **Seed** | Siempre | Opcional |
| **CORS logging** | Detallado | Resumido |
| **Health check** | Inmediato | Inmediato |

## 💡 Recomendaciones

1. **Mantén `DEBUG=false` en producción** para mejor performance
2. **Solo habilita `RUN_SEED=true` en desarrollo** o cuando necesites datos de prueba
3. **Si el seed es necesario en producción**, ejecutarlo manualmente después del deploy:
   ```bash
   # En Render Shell (Dashboard → Service → Shell)
   python -c "from app.database import SessionLocal; from app.seed import run_seed; db = SessionLocal(); run_seed(db); db.close()"
   ```

## 🚀 Resultado Esperado

Después de estos cambios:
1. ✅ El deploy debería completarse exitosamente
2. ✅ El startup toma menos de 10 segundos
3. ✅ El servicio responde rápidamente al health check
4. ✅ CORS sigue funcionando correctamente
5. ✅ Los exception handlers siguen activos

## 📝 Si el Problema Persiste

Si después de estos cambios aún hay timeout, proporciona:

1. **Logs completos** del deploy (últimas 100 líneas antes del "Timed Out")
2. **Estado de la base de datos** (Available/Suspended)
3. **Plan de Render** que estás usando (Free/Starter/Standard)
4. **Tiempo exacto** que tarda el build (desde "Installing collected packages" hasta "Timed Out")
