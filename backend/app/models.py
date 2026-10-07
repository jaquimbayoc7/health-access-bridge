# app/models.py

from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="médico")

    # <--- CORRECCIÓN #1: Se añade la relación inversa
    # Esto permite acceder a user.patients para ver todos los pacientes de un usuario
    patients = relationship("Patient", back_populates="owner")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    numero_documento = Column(String, unique=True, index=True)
    nombre_apellidos = Column(String, index=True)
    fecha_nacimiento = Column(Date)
    edad = Column(Integer)
    genero = Column(String)
    orientacion_sexual = Column(String)
    causa_deficiencia = Column(String)
    cat_fisica = Column(String)
    cat_psicosocial = Column(String)
    nivel_d1 = Column(Integer)
    nivel_d2 = Column(Integer)
    nivel_d3 = Column(Integer)
    nivel_d4 = Column(Integer)
    nivel_d5 = Column(Integer)
    nivel_d6 = Column(Integer)
    nivel_global = Column(Integer)
    
    is_active = Column(Boolean, default=True)
    prediction_profile = Column(Integer, nullable=True)
    prediction_description = Column(String, nullable=True)

    # ======================================================================
    # CORRECCIÓN #2: ESTA ES LA SOLUCIÓN PRINCIPAL
    # Se añade la columna 'owner_id' como una clave foránea que apunta
    # a la columna 'id' de la tabla 'users'.
    # ======================================================================
    owner_id = Column(Integer, ForeignKey("users.id"))

    # <--- CORRECCIÓN #3: Se establece la relación
    # Esto permite acceder a patient.owner para ver el objeto User del médico dueño
    owner = relationship("User", back_populates="patients")


class IcfSuggestion(Base):
    """
    HU-07c: un codigo CIF-IA sugerido para un paciente y la decision del medico sobre el.
    Una generacion crea varias filas con el mismo `batch_id`; regenerar crea un lote nuevo y conserva
    los anteriores (trazabilidad: que sugirio la maquina y que aprobo el profesional).
    Columnas simples, compatibles con SQLite de los tests (no hay migraciones).
    """
    __tablename__ = "icf_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), index=True, nullable=False)
    batch_id = Column(String(36), index=True, nullable=False)
    position = Column(Integer, default=0)  # orden de relevancia dentro del componente

    component = Column(String(1), nullable=False)  # b, s o d
    code = Column(String(10), nullable=False)
    title = Column(String(300), nullable=False)
    qualifier = Column(Integer, nullable=True)  # 0-4 (en s: magnitud)
    qualifier_cn = Column(Integer, nullable=True)  # solo s: naturaleza, 8 por defecto
    qualifier_cl = Column(Integer, nullable=True)  # solo s: localizacion, 8 por defecto
    justification = Column(String(400), nullable=True)
    origin = Column(String(20), nullable=False, default="rules")  # llm, similarity o rules

    status = Column(String(12), nullable=False, default="sugerido")  # sugerido, aceptado, editado, rechazado
    original_code = Column(String(10), nullable=True)  # codigo sugerido, si el medico lo cambio al editar
    model = Column(String(80), nullable=True)  # modelo que genero la sugerencia (auditoria)

    diag_cie = Column(String(300), nullable=True)  # instantanea de entrada, opcional
    clinical_notes = Column(String(2000), nullable=True)  # instantanea de entrada, opcional

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    decided_at = Column(DateTime, nullable=True)
    decided_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)