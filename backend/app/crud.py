# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas, auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    # <--- CORRECCIÓN CLAVE: Ahora 'user.role' viene del schema y funcionará
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role.value  # Usamos .value para obtener el string del Enum
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_activity(db: Session, user_id: int, is_active: bool):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.is_active = is_active
        db.commit()
        db.refresh(db_user)
    return db_user

def activate_all_users(db: Session):
    """Activa todos los usuarios inactivos en el sistema."""
    users = db.query(models.User).filter(models.User.is_active == False).all()
    count = 0
    for user in users:
        user.is_active = True
        count += 1
    db.commit()
    return count

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def get_all_patients(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Patient).filter(models.Patient.is_active == True)
    if search:
        term = f"%{search}%"
        query = query.filter(
            models.Patient.nombre_apellidos.ilike(term) |
            models.Patient.numero_documento.ilike(term)
        )
    return query.offset(skip).limit(limit).all()

def get_patients_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Patient).filter(
        models.Patient.owner_id == owner_id,
        models.Patient.is_active == True
    )
    if search:
        term = f"%{search}%"
        query = query.filter(
            models.Patient.nombre_apellidos.ilike(term) |
            models.Patient.numero_documento.ilike(term)
        )
    return query.offset(skip).limit(limit).all()

def create_user_patient(db: Session, patient: schemas.PatientCreate, user_id: int):
    """
    Crea un nuevo paciente en la base de datos.
    Maneja errores de integridad (duplicados, etc.)
    """
    try:
        db_patient = models.Patient(**patient.model_dump(), owner_id=user_id)
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    except Exception as e:
        db.rollback()
        print(f"❌ Error en create_user_patient: {type(e).__name__}: {str(e)}")
        raise

def update_patient(db: Session, db_patient: models.Patient, patient_update: schemas.PatientUpdate):
    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db_patient.is_active = False
        db.commit()
        db.refresh(db_patient)
    return db_patient

def update_patient_prediction(db: Session, patient_id: int, profile: int, description: str):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db_patient.prediction_profile = profile
        db_patient.prediction_description = description
        db.commit()
        db.refresh(db_patient)
    return db_patient