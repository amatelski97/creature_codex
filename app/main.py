from fastapi import FastAPI
from app.core.middleware import setup_middleware
from app.core.config import settings
from app.core.startup import register_startup, register_shutdown
from app.routers import animal_profiles, uploads


# Create FastAPI app
app = FastAPI(
    title= "Creature Codex API",
    description = "a modular api for managing animal profiles",
    version = "1.0.0"
)

# Setup middleware
setup_middleware(app)



# Include Routers
app.include_router(animal_profiles.router, prefix="/api/profiles", tags=["Animal Profiles"])


# Register startup and shutdown events
register_startup(app)
register_shutdown(app)

# Root route

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Creature Codex API!"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

