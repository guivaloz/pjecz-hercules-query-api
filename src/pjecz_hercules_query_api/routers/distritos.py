"""
Distritos
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from pjecz_hercules_query_api.core.authentication import UsuarioInDB, get_current_active_user
from pjecz_hercules_query_api.core.database import Session, get_session
from pjecz_hercules_query_api.core.pagination import CustomPage
from pjecz_hercules_query_api.core.validation import safe_clave, safe_string
from pjecz_hercules_query_api.models.distritos import Distrito
from pjecz_hercules_query_api.models.permisos import Permiso
from pjecz_hercules_query_api.schemas.distritos import DistritoOut

distritos = APIRouter(prefix="/distritos")


@distritos.get("", response_model=CustomPage[DistritoOut])
def distritos_paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)],
    clave: Annotated[str | None, Query()] = None,
    nombre: Annotated[str | None, Query()] = None,
    es_distrito: Annotated[bool | None, Query()] = None,
    es_jurisdiccional: Annotated[bool | None, Query()] = None,
):
    """Distritos paginado"""
    if current_user.permissions.get("DISTRITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    stmt = select(Distrito).where(Distrito.estatus == "A")
    if clave and (clave := safe_clave(clave)):
        stmt = stmt.where(Distrito.clave.ilike(f"%{clave}%"))
    if nombre and (nombre := safe_string(nombre)):
        stmt = stmt.where(Distrito.nombre.ilike(f"%{nombre}%"))
    if es_distrito is not None:
        stmt = stmt.where(Distrito.es_distrito == es_distrito)
    if es_jurisdiccional is not None:
        stmt = stmt.where(Distrito.es_jurisdiccional == es_jurisdiccional)
    stmt = stmt.order_by(Distrito.clave)
    return paginate(session, stmt)
