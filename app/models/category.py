from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.database import Base

# Таблица связи рецептов и категорий (many-to-many)
recipe_category = Table(
    'recipe_categories',
    Base.metadata,
    Column('recipe_id', ForeignKey('recipes.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True)
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String, default="#f97316")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="categories")
    recipes = relationship(
        "Recipe",
        secondary=recipe_category,
        back_populates="categories"
    )


# Обновляем модель User в user.py - нужно добавить categories relationship
# Это будет сделано отдельно
