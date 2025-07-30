from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

# Importar todos los routers
from routes.auth_routes import router as auth_router
from routes.client_routes import router as client_router
from routes.category_routes import router as category_router
from routes.order_routes import router as order_router
from routes.inventory_routes import router as inventory_router
from routes.component_routes import router as component_router
from routes.user_type_routes import router as user_type_router
from routes.pipeline_routes import router as pipeline_router

# Configuración inicial
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Tienda de Componentes",
    description="API para gestión de tienda de componentes electrónicos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers con prefijos
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(client_router, prefix="/api/clients", tags=["Clientes"])
app.include_router(category_router, prefix="/api/categories", tags=["Categorías"])
app.include_router(order_router, prefix="/api/orders", tags=["Pedidos"])
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventario"])
app.include_router(component_router, prefix="/api/components", tags=["Componentes"])
app.include_router(user_type_router, prefix="/api/user-types", tags=["Tipos de Usuario"])
app.include_router(pipeline_router, prefix="/api/pipelines", tags=["Pipelines"])

@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Bienvenido a la API de Tienda de Componentes",
        "endpoints": {
            "documentación": "/docs",
            "autenticación": "/api/auth",
            "clientes": "/api/clients",
            "categorías": "/api/categories",
            "pedidos": "/api/orders",
            "inventario": "/api/inventory",
            "componentes": "/api/components",
            "pipelines": "/api/pipelines"
        }
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando aplicación...")
    # Aquí puedes agregar inicializaciones necesarias

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Apagando aplicación...")
    # Aquí puedes agregar limpieza necesaria