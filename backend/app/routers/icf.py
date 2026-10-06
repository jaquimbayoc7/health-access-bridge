# app/routers/icf.py

from fastapi import APIRouter, Depends

from .. import dependencies, models
from ..services import icf_client

router = APIRouter(
    tags=["ICF"]
)


@router.get("/health")
def icf_health(
    current_user: models.User = Depends(dependencies.get_current_active_admin),
):
    """
    Diagnostico de la conexion con el servidor local de IA (HU-07).
    Solo administradores. No expone la URL ni el token del servidor.
    """
    return icf_client.check_health()
