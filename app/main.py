from fastapi import FastAPI
from app.core.middleware import setup_cors
from app.core.startup import register_startup, register_shutdown
from app.routers import animal_profiles, uploads, weights, deep_cleans


# Create FastAPI app
app = FastAPI(
    title="Creature Codex API",
    description="A modular API for managing animal profiles",
    version="1.0.0"
)

# Setup middleware
setup_cors(app)

# Include Routers
app.include_router(animal_profiles.router, prefix="/api/profiles", tags=["Animal Profiles"])
app.include_router(weights.router, prefix="/api/weights", tags=["Weights"])
app.include_router(deep_cleans.router, prefix="/api/deep_clean", tags=["Deep Cleans"])
# Register startup and shutdown events for database connection pool
@app.on_event("startup")
async def startup_event():
    """
    Initialize the database connection pool for Psycopg.
    """
    from app.database import db_pool
    await db_pool.open()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Close the database connection pool for Psycopg.
    """
    from app.database import db_pool
    await db_pool.close()

# Root route
@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Creature Codex API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    
