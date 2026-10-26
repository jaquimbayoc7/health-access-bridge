# app/routers/analytics.py
"""HU-08 — Dashboard de analisis: estadisticas agregadas, sin datos identificables."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import dependencies, models
from ..services import analytics

router = APIRouter()


@router.get("/summary")
def get_summary(
    genero: Optional[str] = None,
    edad_min: Optional[int] = Query(None, ge=0, le=120),
    edad_max: Optional[int] = Query(None, ge=0, le=120),
    causa: Optional[str] = None,
    perfil: Optional[int] = Query(None, ge=0, le=9),
    owner_id: Optional[int] = Query(None, description="Solo administrador: limita el resumen a un médico"),
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user),
):
    """Resumen agregado de los pacientes del usuario (todos, si es administrador).

    Solo conteos y promedios: no devuelve nombre, documento ni otros datos identificables."""
    if edad_min is not None and edad_max is not None and edad_min > edad_max:
        raise HTTPException(status_code=422, detail="edad_min no puede ser mayor que edad_max")
    if owner_id is not None and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo el administrador puede filtrar por médico")
    return analytics.build_summary(
        db, current_user, genero=genero, edad_min=edad_min, edad_max=edad_max, causa=causa, perfil=perfil, owner_id=owner_id
    )


@router.get("/filters")
def get_filters(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user),
):
    """Valores disponibles para los filtros del dashboard."""
    return analytics.filter_options(db, current_user)
