from pydantic import BaseModel, Field
from datetime import date

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    calories: float = Field(ge=1)
    proteins: float = Field(ge=0)
    fats: float = Field(ge=0)
    carbs: float = Field(ge=0)

class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    daily_target: int = Field(ge=0)
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    name: str
    password: str

class Product(BaseModel):
    product_id: int
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float

class User(BaseModel):
    user_id: int
    name: str
    daily_target: int

class MealCreate(BaseModel):
    user_name: str
    product_id: int
    grams: float
    date: date

class Meal(BaseModel):
    meal_id: int
    user_id: int
    product_id: int
    grams: float
    date: date
    model_config = {"from_attributes": True}
