# app/schemas.py

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import date, datetime
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    medico = "médico"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str
    role: Role

class User(UserBase):
    id: int
    is_active: bool
    role: Role
    model_config = ConfigDict(from_attributes=True)

class UserStatusUpdate(BaseModel):
    is_active: bool

class PatientBase(BaseModel):
    numero_documento: str
    nombre_apellidos: str
    fecha_nacimiento: date
    edad: int = Field(..., gt=0)
    genero: str
    orientacion_sexual: str
    causa_deficiencia: str
    cat_fisica: str
    cat_psicosocial: str
    nivel_d1: int = Field(..., ge=0, le=100)
    nivel_d2: int = Field(..., ge=0, le=100)
    nivel_d3: int = Field(..., ge=0, le=100)
    nivel_d4: int = Field(..., ge=0, le=100)
    nivel_d5: int = Field(..., ge=0, le=100)
    nivel_d6: int = Field(..., ge=0, le=100)
    nivel_global: int = Field(..., ge=0, le=100)

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    owner_id: int
    is_active: bool = True
    prediction_profile: Optional[int] = None
    prediction_description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class PredictionInput(BaseModel):
    edad: int
    genero: str
    orientacion_sexual: str
    causa_deficiencia: str
    cat_fisica: str
    cat_psicosocial: str
    nivel_d1: int
    nivel_d2: int
    nivel_d3: int
    nivel_d4: int
    nivel_d5: int
    nivel_d6: int
    nivel_global: int
    model_config = ConfigDict(from_attributes=True)

class PredictionOutput(BaseModel):
    profile: int
    description: str


# ----------------------------------------------------------------------
# HU-07c: sugerencias de codigos CIF-IA
# ----------------------------------------------------------------------
class IcfStatus(str, Enum):
    sugerido = "sugerido"
    aceptado = "aceptado"
    editado = "editado"
    rechazado = "rechazado"


class IcfGenerateRequest(BaseModel):
    """Datos clinicos opcionales que escribe el medico. No admite nada mas (ni nombre ni documento)."""
    model_config = ConfigDict(extra="forbid")

    diag_cie: Optional[str] = Field(default=None, max_length=300)
    clinical_notes: Optional[str] = Field(default=None, max_length=2000)


class IcfDecision(BaseModel):
    """Decision del medico sobre un codigo. `editado` permite cambiar calificadores y, con codigo y titulo
    juntos, el codigo. `aceptado` y `rechazado` no cambian el contenido."""
    model_config = ConfigDict(extra="forbid")

    status: IcfStatus
    qualifier: Optional[int] = Field(default=None, ge=0, le=4)
    qualifier_cn: Optional[int] = Field(default=None, ge=0, le=9)
    qualifier_cl: Optional[int] = Field(default=None, ge=0, le=9)
    code: Optional[str] = Field(default=None, pattern=r"^[bsd][0-9]{3,5}$")
    title: Optional[str] = Field(default=None, min_length=1, max_length=300)


class IcfSuggestionItem(BaseModel):
    id: int
    component: str
    code: str
    title: str
    qualifier: Optional[int] = None
    qualifier_cn: Optional[int] = None
    qualifier_cl: Optional[int] = None
    justification: Optional[str] = None
    origin: str
    status: str
    original_code: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class IcfSuggestionSet(BaseModel):
    """Una generacion completa: los codigos agrupados por componente y los datos de la corrida."""
    patient_id: int
    batch_id: Optional[str] = None
    model: Optional[str] = None
    llm_used: bool = False
    created_at: Optional[datetime] = None
    latency_ms: Optional[int] = None  # solo en la respuesta de generar
    warnings: List[str] = Field(default_factory=list)  # solo en la respuesta de generar
    functions: List[IcfSuggestionItem] = Field(default_factory=list)
    structures: List[IcfSuggestionItem] = Field(default_factory=list)
    activities: List[IcfSuggestionItem] = Field(default_factory=list)