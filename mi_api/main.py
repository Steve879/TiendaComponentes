import uvicorn
import logging
from fastapi import FastAPI, Request
from routes.component_pipeline_routes import router as component_pipeline_router



from controllers.users import create_user, login
from models.users import User
from models.login import Login


from utils.security import validateuser, validateadmin


from routes.inventory_route import router as inventory_router  
from routes.component_route import router as component_router

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


app.include_router(inventory_router)
app.include_router(component_router)
app.include_router(component_pipeline_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
