from fastapi import FastAPI
from app.routers import animal_profiles
from app.database import Base, engine
import sys
import os
from fastapi.middleware.cors import CORSMiddleware

# Debugging Information
print("sys.path:", sys.path)
print("Routers directory contents:", os.listdir(os.path.join(os.path.dirname(__file__), "routers")))

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # Add both variations
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(animal_profiles.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Creature Codex API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
