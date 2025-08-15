import os
import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.component_pipeline_routes import router as component_pipeline_router
from routes.inventory_route import router as inventory_router
from routes.component_route import router as component_router

from controllers.users import create_user, login
from models.users import User
from models.login import Login
from utils.security import validateuser, validateadmin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes para desarrollo; restringe en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# --- Preflight global para OPTIONS ---
@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return JSONResponse(content={}, status_code=200)


# --- Rutas de prueba y salud ---
@app.get("/")
def read_root():
    return {"status": "healthy", "version": "0.0.0", "service": "Tienda_de_Componentes-api"}

@app.get("/health")
def health_check():
    try:
        return {
            "status": "healthy",
            "timestamp": "2025-08-02",
            "service": "mi_api",
            "environment": "production"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/ready")
def readiness_check():
    try:
        from utils.mongodb import test_connection
        db_status = test_connection()
        return {
            "status": "ready" if db_status else "not_ready",
            "database": "connected" if db_status else "disconnected",
            "service": "mi_api"
        }
    except Exception as e:
        return {"status": "not_ready", "error": str(e)}


# --- Rutas de usuarios ---
@app.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login")
async def login_access(l: Login) -> dict:
    return await login(l)

@app.get("/exampleadmin")
@validateadmin
async def example_admin(request: Request):
    return {
        "message": "This is an example admin endpoint.",
        "admin": request.state.admin
    }

@app.get("/exampleuser")
@validateuser
async def example_user(request: Request):
    return {
        "message": "This is an example user endpoint.",
        "email": request.state.email
    }

# --- Incluyendo routers ---
app.include_router(inventory_router)
app.include_router(component_router)
app.include_router(component_pipeline_router)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
