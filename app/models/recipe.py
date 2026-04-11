from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    ingredients = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="recipes")
    categories = relationship(
        "Category", secondary="recipe_categories", back_populates="recipes"
    )
