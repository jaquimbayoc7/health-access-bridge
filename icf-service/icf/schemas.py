"""Contratos de entrada y salida del motor de sugerencia (HU-07b).

La entrada NO admite nombre, documento ni orientacion sexual: `extra="forbid"` rechaza cualquier campo
no previsto, de modo que un dato identificable no puede llegar al servicio por descuido.
"""
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

HAB_DOMAIN_KEYS = ("D1", "D2", "D3", "D4", "D5", "D6")


class PatientContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    age: int = Field(ge=0, le=120)
    gender: Optional[str] = Field(default=None, max_length=40)
    cause: Optional[str] = Field(default=None, max_length=120)
    cat_fisica: Optional[str] = Field(default=None, max_length=40)
    cat_psicosocial: Optional[str] = Field(default=None, max_length=40)
    levels: Dict[str, int] = Field(default_factory=dict)
    prediction_description: Optional[str] = Field(default=None, max_length=200)
    diag_cie: Optional[str] = Field(default=None, max_length=300)
    clinical_notes: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("levels")
    @classmethod
    def _check_levels(cls, value: Dict[str, int]) -> Dict[str, int]:
        for key, level in value.items():
            if key not in HAB_DOMAIN_KEYS:
                raise ValueError(f"dominio desconocido: {key}")
            if not 0 <= level <= 100:
                raise ValueError(f"nivel fuera de rango 0-100 en {key}: {level}")
        return value


class SuggestedCode(BaseModel):
    code: str
    title: str  # siempre del catalogo, nunca del LLM
    qualifier: Optional[int] = None  # 0-4; en estructuras (s) es la magnitud
    qualifier_cn: Optional[int] = None  # solo s: naturaleza del cambio (8 = no especificada)
    qualifier_cl: Optional[int] = None  # solo s: localizacion (8 = no especificada)
    justification: str
    origin: str  # "llm", "rules" o "similarity"


class SuggestionResult(BaseModel):
    applicable: bool
    message: Optional[str] = None
    model: str
    llm_used: bool = False  # True solo si el LLM respondio un JSON valido y se uso
    llm_error: Optional[str] = None
    latency_ms: int = 0
    timings: Dict[str, int] = Field(default_factory=dict)  # ms por etapa: embed, search, llm
    llm_stats: Dict[str, int] = Field(default_factory=dict)  # tokens y duraciones que reporta Ollama
    functions: List[SuggestedCode] = Field(default_factory=list)
    structures: List[SuggestedCode] = Field(default_factory=list)
    activities: List[SuggestedCode] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
