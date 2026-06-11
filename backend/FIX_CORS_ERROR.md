# Solución al Error de CORS en Render

## 🔴 Problema Original

Al intentar crear un paciente desde el frontend de Render, se generaba el siguiente error:

```
Uncaught (in promise) Error: A listener indicated an asynchronous response by returning true, but the message channel closed before a response was received
Access to fetch at 'https://hab-backend-szj1.onrender.com/patients/' from origin 'https://hab-frontend.onrender.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
Failed to load resource: net::ERR_FAILED
```

## 🔍 Causa del Problema

Aunque CORS estaba configurado en el backend, cuando FastAPI lanzaba excepciones (errores de validación, autenticación, etc.), los headers de CORS no se incluían en la respuesta de error. Esto causaba que el navegador bloqueara la solicitud antes de que el frontend pudiera ver el error real.

## ✅ Soluciones Implementadas

### 1. Exception Handlers Personalizados

Se agregaron tres exception handlers que aseguran que los headers de CORS siempre estén presentes:

- **`http_exception_handler`**: Maneja excepciones HTTP (401, 403, 404, etc.)
- **`validation_exception_handler`**: Maneja errores de validación de requests (422)
- **`general_exception_handler`**: Maneja cualquier otra excepción no capturada (500)

Cada handler:
- Verifica el origen de la solicitud
- Agrega los headers de CORS apropiados si el origen está permitido
- Retorna la respuesta de error con los headers incluidos

### 2. Middleware de Logging

Se agregó un middleware personalizado que registra:
- Todas las requests entrantes (método, path, origen)
- El status code de cada respuesta
- Útil para debuggear problemas de CORS en tiempo real

### 3. Logging de Configuración en Startup

Al iniciar el servidor, ahora se muestra:
- La lista completa de orígenes permitidos
- Confirmación visual de la configuración de CORS

## 📋 Próximos Pasos

### 1. Desplegar los Cambios a Render

```bash
# Desde la raíz del proyecto
git add backend/app/main.py
git commit -m "Fix: Agregar exception handlers para CORS en errores"
git push origin main
```

### 2. Verificar los Logs en Render

Una vez desplegado, ve a Render Dashboard → tu servicio de backend → Logs y busca:

```
🌐 CONFIGURACIÓN DE CORS
Orígenes permitidos:
  ✓ https://hab-frontend.onrender.com
  ...
```

### 3. Probar la Creación de Pacientes

Intenta crear un paciente desde el frontend. Ahora deberías ver en los logs:

```
📨 POST /patients/ | Origin: https://hab-frontend.onrender.com
📤 POST /patients/ | Status: 201
```

### 4. Si Aún Hay Errores

Si aún ves errores, revisa los logs para identificar:

1. **Error 401 Unauthorized**: Problema con el token de autenticación
   - Verifica que el token JWT se esté enviando correctamente
   - Verifica que el token no haya expirado

2. **Error 422 Unprocessable Entity**: Problema con los datos enviados
   - Verifica que todos los campos requeridos estén presentes
   - Verifica que los tipos de datos sean correctos

3. **Error 500 Internal Server Error**: Error en el servidor
   - Revisa los logs para ver el error específico
   - Puede ser un problema con la base de datos o el modelo

## 🔧 Debugging Adicional

### Verificar Headers en el Navegador

1. Abre DevTools (F12)
2. Ve a la pestaña Network
3. Intenta crear un paciente
4. Click en la request fallida
5. Verifica:
   - **Request Headers**: ¿Se está enviando el `Authorization: Bearer <token>`?
   - **Response Headers**: ¿Están presentes los headers de CORS?

### Verificar Token JWT

El token debe tener el formato:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Si el token expiró o no es válido, necesitarás hacer login nuevamente.

### Verificar Datos del Paciente

El payload debe incluir todos los campos requeridos según el schema `PatientCreate`:

```json
{
  "nombre": "Juan",
  "apellidos": "Pérez",
  "cedula": "123456789",
  "edad": 30,
  "genero": "Masculino",
  // ... otros campos requeridos
}
```

## 📚 Archivos Modificados

- `backend/app/main.py`: Exception handlers y logging mejorado

## 🎯 Resultado Esperado

Después de estos cambios:
1. ✅ Las solicitudes desde el frontend de Render deberían funcionar correctamente
2. ✅ Los errores del backend deberían ser visibles en el frontend (no bloqueados por CORS)
3. ✅ Los logs del backend deberían mostrar información útil para debugging

## 💡 Notas Adicionales

- Los exception handlers NO ocultan los errores, solo aseguran que los headers de CORS estén presentes
- El logging es útil para producción pero puede generar muchos logs; considera desactivarlo o reducirlo si es necesario
- Si agregas nuevos orígenes (dominios), asegúrate de incluirlos en la variable `ALLOWED_ORIGINS` o en el array `_default_origins`
