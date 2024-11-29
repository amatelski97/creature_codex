import asyncio
from fastapi import FastAPI
from app.routers import animal_profiles
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(animal_profiles.router)


@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Creature Codex API!"}


# Database initialization function
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Run initialization on startup
@app.on_event("startup")
async def on_startup():
    await init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
