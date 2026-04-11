from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    ingredients = Column(Text, nullable=False)  # JSON string with ingredients
    steps = Column(Text)  # JSON string with steps
    tags = Column(Text)  # JSON array of tag strings
    photos = Column(Text)  # JSON array of photo URLs
    prep_time = Column(Integer)  # minutes
    cook_time = Column(Integer)  # minutes
    servings = Column(Integer)
    difficulty = Column(String)  # easy, medium, hard
    cuisine = Column(String)  # e.g., "Italian", "Asian"
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="recipes")
    categories = relationship(
        "Category", secondary="recipe_categories", back_populates="recipes"
    )
