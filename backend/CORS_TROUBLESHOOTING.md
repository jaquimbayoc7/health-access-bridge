# Troubleshooting CORS - Lista de Verificación

## ✅ Verificaciones Previas al Deploy

### 1. Verificar Variables de Entorno en Render

En Render Dashboard → Backend Service → Environment:

```bash
# Esta variable debería existir (opcional, ya hay defaults)
ALLOWED_ORIGINS=https://hab-frontend.onrender.com,https://hab-frontend-dev.onrender.com
```

**Nota**: Los orígenes ya están hardcodeados en el código, así que esta variable es opcional.

### 2. Verificar el Frontend `.env`

Asegúrate de que el frontend tenga configurada la variable:

```bash
VITE_API_BASE_URL=https://hab-backend-szj1.onrender.com
```

## 🔍 Después del Deploy - Verificar Logs

### Paso 1: Ver Logs del Backend

En Render Dashboard → Backend Service → Logs, deberías ver al inicio:

```
====================================================================
🌐 CONFIGURACIÓN DE CORS
====================================================================
Orígenes permitidos:
  ✓ http://localhost:3000
  ✓ http://localhost:5173
  ✓ http://localhost:8080
  ✓ https://hab-frontend.onrender.com
  ✓ https://hab-frontend-dev.onrender.com
  ✓ https://hab-frontend-qa.onrender.com
  ✓ https://e1bb997f-a232-4850-a558-28c9f9aba95b.lovableproject.com
====================================================================
```

### Paso 2: Intentar Crear un Paciente

Al hacer una solicitud, deberías ver en los logs:

```
📨 POST /patients/ | Origin: https://hab-frontend.onrender.com
📤 POST /patients/ | Status: 201
```

## 🚨 Errores Comunes y Soluciones

### Error 401 - Unauthorized

**Síntoma**: 
```
📨 POST /patients/ | Origin: https://hab-frontend.onrender.com
📤 POST /patients/ | Status: 401
```

**Causa**: Token de autenticación inválido o expirado

**Solución**:
1. Abre DevTools (F12) → Network
2. Click en la request fallida
3. Verifica en "Request Headers" que exista:
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
4. Si no está o está mal formado:
   - Cierra sesión en el frontend
   - Vuelve a iniciar sesión
   - Intenta crear el paciente nuevamente

### Error 422 - Validation Error

**Síntoma**:
```
📨 POST /patients/ | Origin: https://hab-frontend.onrender.com
📤 POST /patients/ | Status: 422
```

**Causa**: Datos inválidos en el payload

**Solución**:
1. Abre DevTools (F12) → Network
2. Click en la request fallida
3. Ve a "Response" y verifica qué campo está fallando
4. Ejemplo de respuesta:
   ```json
   {
     "detail": [
       {
         "loc": ["body", "edad"],
         "msg": "field required",
         "type": "value_error.missing"
       }
     ]
   }
   ```

### Error 500 - Internal Server Error

**Síntoma**:
```
📨 POST /patients/ | Origin: https://hab-frontend.onrender.com
❌ Error no manejado: DatabaseError: ...
📤 POST /patients/ | Status: 500
```

**Causa**: Error interno del servidor (base de datos, código, etc.)

**Solución**:
1. Revisa los logs completos del backend en Render
2. Busca el mensaje de error específico después de "❌ Error no manejado"
3. Posibles causas:
   - **Database connection error**: La base de datos no está disponible
   - **Constraint violation**: Datos duplicados (ej: cédula ya existe)
   - **Missing field**: Falta un campo requerido en el modelo

## 🔧 Verificaciones en el Navegador

### Test Manual de CORS

1. Abre DevTools (F12) → Console
2. Ejecuta este código:

```javascript
fetch('https://hab-backend-szj1.onrender.com/health', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
  .then(r => r.json())
  .then(data => console.log('✅ Backend alcanzable:', data))
  .catch(err => console.error('❌ Error:', err));
```

**Resultado esperado**:
```
✅ Backend alcanzable: { status: "ok" }
```

### Test de Autenticación

```javascript
const token = localStorage.getItem('authToken');
console.log('Token:', token ? '✅ Presente' : '❌ Faltante');
console.log('Token válido?', token && token.startsWith('eyJ') ? '✅ Formato correcto' : '❌ Formato incorrecto');
```

## 📊 Headers Esperados en Respuestas

Cuando hagas una solicitud desde el frontend, la respuesta del backend debería incluir:

```
Access-Control-Allow-Origin: https://hab-frontend.onrender.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
Access-Control-Allow-Headers: *
```

Para verificar en DevTools:
1. Network tab
2. Click en la request
3. Ve a "Response Headers"
4. Busca los headers `Access-Control-*`

## 🎯 Checklist Final

Antes de reportar un bug, verifica:

- [ ] Backend está corriendo (https://hab-backend-szj1.onrender.com/health devuelve `{"status":"ok"}`)
- [ ] Frontend tiene la variable `VITE_API_BASE_URL` correcta
- [ ] Token de autenticación está presente en localStorage
- [ ] Token de autenticación se está enviando en las requests (`Authorization` header)
- [ ] Los datos del formulario están completos y son válidos
- [ ] Los logs del backend muestran la configuración de CORS correcta
- [ ] Las requests aparecen en los logs del backend

## 📝 Información para Reportar Bugs

Si después de todas estas verificaciones el problema persiste, reporta:

1. **Logs del backend** (últimas 50 líneas)
2. **Screenshot de DevTools** mostrando:
   - Network tab con la request fallida
   - Request Headers
   - Response Headers (si hay)
3. **Console errors** (si hay)
4. **Datos exactos** que estás intentando enviar (sin información sensible)
