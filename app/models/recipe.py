import json

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship, reconstructor

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    ingredients = Column(Text, nullable=False)
    steps = Column(Text)
    tags = Column(Text)
    photos = Column(Text)
    prep_time = Column(Integer)
    cook_time = Column(Integer)
    servings = Column(Integer)
    difficulty = Column(String)
    cuisine = Column(String)
    notes = Column(Text)
    visibility = Column(String, nullable=False, default="private")
    publication_status = Column(String, nullable=False, default="draft")
    is_admin_recipe = Column(Boolean, nullable=False, default=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    original_recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="recipes", foreign_keys=[user_id])
    categories = relationship(
        "Category", secondary="recipe_categories", back_populates="recipes"
    )
    original_recipe = relationship("Recipe", remote_side=[id], uselist=False)

    @reconstructor
    def init_on_load(self):
        self._tags_list = None
        self._photos_list = None

    @property
    def tags_list(self):
        if self._tags_list is None and self.tags:
            try:
                self._tags_list = json.loads(self.tags)
            except (json.JSONDecodeError, TypeError):
                self._tags_list = []
        return self._tags_list or []

    @tags_list.setter
    def tags_list(self, value):
        if isinstance(value, list):
            self.tags = json.dumps(value)
            self._tags_list = value

    @property
    def photos_list(self):
        if self._photos_list is None and self.photos:
            try:
                self._photos_list = json.loads(self.photos)
            except (json.JSONDecodeError, TypeError):
                self._photos_list = []
        return self._photos_list or []

    @photos_list.setter
    def photos_list(self, value):
        if isinstance(value, list):
            self.photos = json.dumps(value)
            self._photos_list = value

    def __setattr__(self, name, value):
        if name in ("tags", "photos") and isinstance(value, list):
            value = json.dumps(value)
        super().__setattr__(name, value)
