from typing import Any

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger

from app.api import api_router
from app.config import settings, setup_app_logging
from app import __version__ as api_version
from model import __version__ as model_version

# setup logging as early as possible
setup_app_logging(config=settings)


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

root_router = APIRouter()

# Cuerpo de la respuesta en la raíz
@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html lang='es'><head><meta charset='utf-8'>"
        "<title>Bankchurn API</title>"
        "<style>"
        "body{margin:0;min-height:100vh;display:flex;align-items:center;"
        "justify-content:center;font-family:Arial,Helvetica,sans-serif;"
        "background:linear-gradient(135deg,#1b1035,#4b2a7b);color:#f4f1fa;}"
        ".card{max-width:640px;margin:24px;padding:40px;border-radius:16px;"
        "background:rgba(255,255,255,0.08);"
        "box-shadow:0 10px 30px rgba(0,0,0,0.35);}"
        "h1{margin-top:0;font-size:28px;}"
        "p,li{line-height:1.5;color:#d9d2ea;}"
        "code{background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;}"
        ".btn{display:inline-block;margin-top:8px;padding:10px 18px;"
        "border-radius:8px;background:#f2b134;color:#1b1035;"
        "font-weight:bold;text-decoration:none;}"
        "footer{margin-top:28px;font-size:12px;color:#b8acd6;}"
        "</style></head>"
        "<body><div class='card'>"
        "<h1>Welcome to the new API - Julian Castañeda MIAD CICLO 6 - Despliegue de Soluciones de Analytics</h1>"
        "<p>Predicción de abandono de clientes bancarios con un modelo de "
        "random forest, servido en un contenedor Docker en Railway con "
        "despliegue continuo desde GitHub.</p>"
        "<ul><li><code>POST /api/v1/predict</code>: predicción de abandono "
        "para uno o varios clientes.</li></ul>"
        f"<p>Versión de la API: {api_version} · "
        f"Versión del modelo: {model_version}</p>"
        "Check the docs: <a class='btn' href='/docs'>here</a>"
        "<footer>Despliegue de soluciones analíticas · MIAD · "
        "Universidad de los Andes</footer>"
        "</div></body></html>"
    )

    return HTMLResponse(content=body)


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    # ejecución del servidor - host para ejecutar en servidor 
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
