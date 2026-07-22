from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from database import Base

class Users(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    daily_target: Mapped[int]

class Products(Base):
    __tablename__ = 'products'
    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    calories: Mapped[float]
    proteins: Mapped[float]
    fats: Mapped[float]
    carbs: Mapped[float]

class Meals(Base):
    __tablename__ = 'meals'
    meal_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id'))
    grams: Mapped[float]
    date: Mapped[date]
    product: Mapped['Products'] = relationship()