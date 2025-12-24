from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html

from backend.routes.actions_router import router as actions_router
from backend.routes.connexion_router import router as connexion_router
from backend.routes.users_profiles_routes import router as users_profiles_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines
    allow_credentials=True,                   # Important pour les cookies HttpOnly
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/redoc", include_in_schema=False)
async def redoc():
    return get_redoc_html(openapi_url="/openapi.json", title="My API ReDoc")


app.include_router(actions_router)
app.include_router(connexion_router)
app.include_router(users_profiles_routes)
