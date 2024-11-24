from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String)
    birth_date = Column(String)
    arrival_date = Column(Date)
    is_admin = Column(Boolean)

    # relationships
    weights = relationship("Weights", back_populates="profile")
    training_logs = relationship("TrainingLog", back_populates="profile")
    location_use = relationship("LocationUse", back_populates="profile")
    fecals = relationship("Fecal", back_populates="profile")
    deep_cleans = relationship("DeepClean", back_populates="profile")
    daily_feed_and_cleans = relationship("DailyFeedAndClean", back_populates="profile")

class Weights(Base):
    __tablename__ = "weights"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    weight = Column(Float)
    date = Column(Date)
    
    # relationships
    profile = relationship("Profile", back_populates="weights")

class TrainingLog(Base):
    __tablename__ = "training_logs"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    animal_name = Column(String)
    activity = Column(String)
    progress_notes = Column(Text)
    date = Column(Date)
    
    # relationships
    profile = relationship("Profile", back_populates="training_logs")

class Fecal(Base):
    __tablename__ = "fecals"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    animal_name = Column(String)
    result = Column(String)
    notes = Column(Text)
    date = Column(Date)

    # relationships
    profile = relationship("Profile", back_populates="fecals")

class DeepClean(Base):
    __tablename__ = "deep_cleans"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    animal_name = Column(String)
    date = Column(Date)
    cleaner_name = Column(String)
    notes = Column(Text)

    # relationships
    profile = relationship("Profile", back_populates="deep_cleans")

class DailyFeedAndClean(Base):
    __tablename__ = "daily_feed_and_clean"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    animal_name = Column(String)
    date = Column(Date)
    prepped = Column(Boolean)
    fed = Column(Boolean)
    cleaned = Column(Boolean)
    leftovers = Column(Boolean)
    water = Column(Boolean)
    poop = Column(Boolean)
    notes = Column(String)
    staff_only = Column(Boolean)
    fed_by = Column(String)

    # relationships
    profile = relationship("Profile", back_populates="daily_feed_and_cleans")

class LocationUse(Base):
    __tablename__ = "location_use"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    animal_name = Column(String(255))
    classroom_use = Column(Boolean)
    touch_animal = Column(Boolean)
    stone_stage = Column(Boolean)
    parties = Column(Boolean)
    offsites = Column(Boolean)
    fireside = Column(Boolean)
    walkaround = Column(Boolean)
    camps = Column(Boolean)
    tours = Column(Boolean)
    display = Column(Boolean)
    use_notes = Column(Text)

    # relationships
    profile = relationship("Profile", back_populates="location_use")

