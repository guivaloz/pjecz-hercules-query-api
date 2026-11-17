"""
Tests Init

Las pruebas consultan con requests una API en ejecución. Configure en el archivo .env:

    API_BASE_URL=prefijo.cadena_aleatoria
    API_KEY=http://127.0.0.1:8000
    TIMEOUT=10
    USUARIO_EMAIL=anonymous@server.com
"""

import os

from dotenv import load_dotenv

load_dotenv()
config = {
    "api_base_url": os.getenv("API_BASE_URL", "http://127.0.0.1:8000"),
    "api_key": os.getenv("API_KEY", ""),
    "timeout": int(os.getenv("TIMEOUT", "10")),
    "usuario_email": os.getenv("USUARIO_EMAIL", "anonymous@server.com"),
}
