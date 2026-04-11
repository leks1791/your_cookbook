import json
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship, reconstructor

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    ingredients = Column(Text, nullable=False)  # JSON string
    steps = Column(Text)  # JSON string
    tags = Column(Text)  # JSON string (was JSON array)
    photos = Column(Text)  # JSON string (was JSON array)
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

    @reconstructor
    def init_on_load(self):
        """Конвертируем JSON string в list при загрузке из БД"""
        self._tags_list = None
        self._photos_list = None

    @property
    def tags_list(self):
        """Получить tags как list"""
        if self._tags_list is None and self.tags:
            try:
                self._tags_list = json.loads(self.tags)
            except (json.JSONDecodeError, TypeError):
                self._tags_list = []
        return self._tags_list or []

    @tags_list.setter
    def tags_list(self, value):
        """Установить tags как list (автоматически сериализуется в JSON)"""
        if isinstance(value, list):
            self.tags = json.dumps(value)
            self._tags_list = value

    @property
    def photos_list(self):
        """Получить photos как list"""
        if self._photos_list is None and self.photos:
            try:
                self._photos_list = json.loads(self.photos)
            except (json.JSONDecodeError, TypeError):
                self._photos_list = []
        return self._photos_list or []

    @photos_list.setter
    def photos_list(self, value):
        """Установить photos как list (автоматически сериализуется в JSON)"""
        if isinstance(value, list):
            self.photos = json.dumps(value)
            self._photos_list = value

    def __setattr__(self, name, value):
        # Конвертируем list в JSON string для полей tags и photos при прямом присваивании
        if name in ("tags", "photos") and isinstance(value, list):
            value = json.dumps(value)
        super().__setattr__(name, value)
