"""
Usuarios-Roles
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from pjecz_hercules_query_api.core.authentication import UsuarioInDB, get_current_active_user
from pjecz_hercules_query_api.core.database import Session, get_session
from pjecz_hercules_query_api.core.pagination import CustomPage
from pjecz_hercules_query_api.core.validation import safe_email, safe_string
from pjecz_hercules_query_api.models.permisos import Permiso
from pjecz_hercules_query_api.models.roles import Rol
from pjecz_hercules_query_api.models.usuarios import Usuario
from pjecz_hercules_query_api.models.usuarios_roles import UsuarioRol
from pjecz_hercules_query_api.schemas.usuarios_roles import UsuarioRolOut

usuarios_roles = APIRouter(prefix="/usuarios_roles")


@usuarios_roles.get("", response_model=CustomPage[UsuarioRolOut])
def usuarios_roles_paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)],
    usuario_email: Annotated[str | None, Query()] = None,
    rol_nombre: Annotated[str | None, Query()] = None,
):
    """Usuarios-Roles paginado"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    stmt = select(UsuarioRol).where(UsuarioRol.estatus == "A")
    if usuario_email and (usuario_email := safe_email(usuario_email)):
        stmt = stmt.join(UsuarioRol.usuario).where(Usuario.email == usuario_email)
    if rol_nombre and (rol_nombre := safe_string(rol_nombre)):
        stmt = stmt.join(UsuarioRol.rol).where(Rol.nombre.ilike(f"%{rol_nombre}%"))
    stmt = stmt.order_by(UsuarioRol.id)
    return paginate(session, stmt)
