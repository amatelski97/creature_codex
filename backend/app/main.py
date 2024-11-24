from fastapi import FastAPI
from app.database import Base, engine
from app.models import Profile, Weights, TrainingLog, Fecal, DeepClean, DailyFeedAndClean, LocationUse
from app.routers import profiles, weights, training_logs, fecals, deep_cleans, daily_feed_and_cleans, location_use

#initialize FastAPI app
app=FastAPI()

# create all tables in the database
Base.metadata.create_all(bind=engine)

# include routers
app.include_router(profiles.router)
app.include_router(weights.router)
app.include_router(training_logs.router)
app.include_router(fecals.router)
app.include_router(deep_cleans.router)
app.include_router(daily_feed_and_cleans.router)
app.include_router(location_use.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Creature Codex API!"}


