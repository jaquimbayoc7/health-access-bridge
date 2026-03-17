# app/seed.py
# Script de seed para crear datos de prueba en los 3 ambientes (dev, qa, prod)
# Se ejecuta automáticamente en el startup de la app si no existen datos previos.

from sqlalchemy.orm import Session
from . import crud, schemas, models


# Usuarios de prueba por ambiente
SEED_USERS = [
    {
        "email": "administrador@salud.co",
        "password": "adminpassword",
        "full_name": "Administrador del Sistema",
        "role": schemas.Role.admin,
    },
    {
        "email": "medico1@salud.co",
        "password": "medico123",
        "full_name": "Dr. Carlos Martínez",
        "role": schemas.Role.medico,
    },
    {
        "email": "medico2@salud.co",
        "password": "medico123",
        "full_name": "Dra. Ana Lucía Gómez",
        "role": schemas.Role.medico,
    },
]

# Pacientes de prueba (se asignan al medico1)
SEED_PATIENTS = [
    {
        "numero_documento": "1001234567",
        "nombre_apellidos": "Juan Pérez García",
        "fecha_nacimiento": "1985-03-15",
        "edad": 41,
        "genero": "Masculino",
        "orientacion_sexual": "Heterosexual",
        "causa_deficiencia": "Accidente laboral",
        "cat_fisica": "Moderada",
        "cat_psicosocial": "Leve",
        "nivel_d1": 45,
        "nivel_d2": 30,
        "nivel_d3": 55,
        "nivel_d4": 40,
        "nivel_d5": 35,
        "nivel_d6": 50,
        "nivel_global": 42,
    },
    {
        "numero_documento": "1002345678",
        "nombre_apellidos": "María Fernanda López",
        "fecha_nacimiento": "1990-07-22",
        "edad": 35,
        "genero": "Femenino",
        "orientacion_sexual": "Heterosexual",
        "causa_deficiencia": "Enfermedad congénita",
        "cat_fisica": "Severa",
        "cat_psicosocial": "Moderada",
        "nivel_d1": 70,
        "nivel_d2": 65,
        "nivel_d3": 75,
        "nivel_d4": 60,
        "nivel_d5": 55,
        "nivel_d6": 80,
        "nivel_global": 67,
    },
    {
        "numero_documento": "1003456789",
        "nombre_apellidos": "Carlos Eduardo Ramírez",
        "fecha_nacimiento": "1978-11-03",
        "edad": 47,
        "genero": "Masculino",
        "orientacion_sexual": "Heterosexual",
        "causa_deficiencia": "Accidente de tránsito",
        "cat_fisica": "Leve",
        "cat_psicosocial": "Leve",
        "nivel_d1": 20,
        "nivel_d2": 15,
        "nivel_d3": 25,
        "nivel_d4": 10,
        "nivel_d5": 18,
        "nivel_d6": 22,
        "nivel_global": 18,
    },
    {
        "numero_documento": "1004567890",
        "nombre_apellidos": "Lucía Valentina Torres",
        "fecha_nacimiento": "1995-01-30",
        "edad": 31,
        "genero": "Femenino",
        "orientacion_sexual": "Bisexual",
        "causa_deficiencia": "Enfermedad degenerativa",
        "cat_fisica": "Moderada",
        "cat_psicosocial": "Severa",
        "nivel_d1": 50,
        "nivel_d2": 55,
        "nivel_d3": 60,
        "nivel_d4": 70,
        "nivel_d5": 65,
        "nivel_d6": 58,
        "nivel_global": 59,
    },
    {
        "numero_documento": "1005678901",
        "nombre_apellidos": "Andrés Felipe Morales",
        "fecha_nacimiento": "1982-09-18",
        "edad": 43,
        "genero": "Masculino",
        "orientacion_sexual": "Heterosexual",
        "causa_deficiencia": "Lesión deportiva",
        "cat_fisica": "Leve",
        "cat_psicosocial": "Ninguna",
        "nivel_d1": 15,
        "nivel_d2": 10,
        "nivel_d3": 20,
        "nivel_d4": 5,
        "nivel_d5": 12,
        "nivel_d6": 18,
        "nivel_global": 13,
    },
    {
        "numero_documento": "1006789012",
        "nombre_apellidos": "Diana Patricia Herrera",
        "fecha_nacimiento": "1988-05-12",
        "edad": 37,
        "genero": "Femenino",
        "orientacion_sexual": "Heterosexual",
        "causa_deficiencia": "Enfermedad autoinmune",
        "cat_fisica": "Severa",
        "cat_psicosocial": "Moderada",
        "nivel_d1": 75,
        "nivel_d2": 70,
        "nivel_d3": 80,
        "nivel_d4": 65,
        "nivel_d5": 60,
        "nivel_d6": 85,
        "nivel_global": 72,
    },
    {
        "numero_documento": "1007890123",
        "nombre_apellidos": "Santiago Alejandro Ruiz",
        "fecha_nacimiento": "2000-12-05",
        "edad": 25,
        "genero": "Masculino",
        "orientacion_sexual": "Homosexual",
        "causa_deficiencia": "Trauma craneoencefálico",
        "cat_fisica": "Moderada",
        "cat_psicosocial": "Severa",
        "nivel_d1": 55,
        "nivel_d2": 60,
        "nivel_d3": 50,
        "nivel_d4": 75,
        "nivel_d5": 70,
        "nivel_d6": 45,
        "nivel_global": 59,
    },
    {
        "numero_documento": "1008901234",
        "nombre_apellidos": "Valentina Sofía Castillo",
        "fecha_nacimiento": "1992-08-25",
        "edad": 33,
        "genero": "Femenino",
        "orientacion_sexual": "Heterosexual",
        "causa_deficiencia": "Accidente laboral",
        "cat_fisica": "Leve",
        "cat_psicosocial": "Moderada",
        "nivel_d1": 30,
        "nivel_d2": 35,
        "nivel_d3": 25,
        "nivel_d4": 40,
        "nivel_d5": 38,
        "nivel_d6": 28,
        "nivel_global": 33,
    },
    {
        "numero_documento": "1009012345",
        "nombre_apellidos": "Miguel Ángel Ortiz",
        "fecha_nacimiento": "1975-04-10",
        "edad": 50,
        "genero": "Masculino",
        "orientacion_sexual": "Heterosexual",
        "causa_deficiencia": "Enfermedad cardiovascular",
        "cat_fisica": "Severa",
        "cat_psicosocial": "Severa",
        "nivel_d1": 85,
        "nivel_d2": 80,
        "nivel_d3": 90,
        "nivel_d4": 78,
        "nivel_d5": 75,
        "nivel_d6": 88,
        "nivel_global": 83,
    },
    {
        "numero_documento": "1010123456",
        "nombre_apellidos": "Laura Camila Mendoza",
        "fecha_nacimiento": "1998-02-14",
        "edad": 28,
        "genero": "Femenino",
        "orientacion_sexual": "Heterosexual",
        "causa_deficiencia": "Parálisis cerebral",
        "cat_fisica": "Moderada",
        "cat_psicosocial": "Moderada",
        "nivel_d1": 48,
        "nivel_d2": 52,
        "nivel_d3": 45,
        "nivel_d4": 55,
        "nivel_d5": 50,
        "nivel_d6": 47,
        "nivel_global": 50,
    },
]


def run_seed(db: Session):
    """
    Ejecuta el seed de datos de prueba.
    Solo crea datos si no existen previamente (idempotente).
    Retorna un resumen de lo creado.
    """
    created_users = 0
    created_patients = 0

    # 1. Crear usuarios
    for user_data in SEED_USERS:
        existing = crud.get_user_by_email(db, email=user_data["email"])
        if not existing:
            user_in = schemas.UserCreate(
                email=user_data["email"],
                password=user_data["password"],
                full_name=user_data["full_name"],
                role=user_data["role"],
            )
            crud.create_user(db=db, user=user_in)
            created_users += 1
            print(f"  ✓ Usuario creado: {user_data['email']} ({user_data['role'].value})")
        else:
            print(f"  → Usuario ya existe: {user_data['email']}")

    # 2. Crear pacientes: primeros 5 → medico1, siguientes 5 → medico2
    from datetime import date
    assignments = [
        ("medico1@salud.co", SEED_PATIENTS[:5]),
        ("medico2@salud.co", SEED_PATIENTS[5:]),
    ]
    for email, patients in assignments:
        medico = crud.get_user_by_email(db, email=email)
        if medico:
            existing_patients = crud.get_patients_by_owner(db, owner_id=medico.id)
            if len(existing_patients) == 0:
                for p_data in patients:
                    patient_dict = p_data.copy()
                    patient_dict["fecha_nacimiento"] = date.fromisoformat(patient_dict["fecha_nacimiento"])
                    patient_in = schemas.PatientCreate(**patient_dict)
                    crud.create_user_patient(db=db, patient=patient_in, user_id=medico.id)
                    created_patients += 1
                    print(f"  ✓ Paciente creado para {email}: {p_data['nombre_apellidos']}")
            else:
                print(f"  → Pacientes ya existen para {email} ({len(existing_patients)} registros)")
        else:
            print(f"  ⚠ No se encontró {email} para asignar pacientes")

    print(f"\n  Seed completado: {created_users} usuarios, {created_patients} pacientes creados")
    return {"users_created": created_users, "patients_created": created_patients}
