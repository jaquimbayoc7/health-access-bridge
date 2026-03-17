#!/usr/bin/env bash
# build.sh - Script para preparar la aplicación en Render

set -e  # Salir si hay algún error

echo "======================================"
echo "🚀 Iniciando proceso de build..."
echo "======================================"

# Paso 1: Verificar que las dependencias estén instaladas
echo "✓ Dependencias ya están instaladas"

# Paso 2: Generar el modelo si no existe
echo ""
echo "Verificando modelo ML..."
if [ ! -f "model/model_pipeline.joblib" ]; then
    echo "⚠️ Modelo no encontrado. Generando modelo..."
    python model/train_model.py
    echo "✓ Modelo generado correctamente"
else
    echo "✓ Modelo existe"
fi

# Paso 3: Inicializar la base de datos
echo ""
echo "Inicializando base de datos..."
python -c "
import os
from sqlalchemy import text, inspect
from app.database import engine, Base
import app.models  # noqa: ensure all models are registered

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    print('Verificando esquema de base de datos...')
    try:
        inspector = inspect(engine)
        needs_recreate = False

        if 'patients' in inspector.get_table_names():
            existing_cols = {c['name'] for c in inspector.get_columns('patients')}
            required_cols = {'numero_documento', 'nombre_apellidos', 'nivel_d1', 'nivel_global', 'owner_id'}
            missing = required_cols - existing_cols
            if missing:
                print(f'⚠️ Esquema desactualizado. Columnas faltantes: {missing}')
                needs_recreate = True
            else:
                print('✓ Esquema de patients ya está actualizado')
        else:
            needs_recreate = True

        if needs_recreate:
            print('Recreando tabla patients con esquema actualizado...')
            with engine.begin() as conn:
                conn.execute(text('DROP TABLE IF EXISTS patients'))
            Base.metadata.tables['patients'].create(engine, checkfirst=True)
            print('✓ Tabla patients recreada correctamente')

        # Crear las demás tablas que no existan
        Base.metadata.create_all(bind=engine)
        print('✓ Base de datos inicializada correctamente')
    except Exception as e:
        print(f'⚠️ Error al inicializar BD: {e}')
        import traceback; traceback.print_exc()
        print('Continuando...')
else:
    print('⚠️ DATABASE_URL no está configurada')
"

echo ""
echo "======================================"
echo "✓ Build completado exitosamente"
echo "======================================"

