from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Products, Users, Meals
from schemas import ProductCreate, Product, UserCreate, Meal, MealCreate
from datetime import date

app = FastAPI()

def calculate_nutrition(meals, daily_target):
    cpfc = {}

    cpfc['ККалории'] = 0
    cpfc['Белки'] = 0
    cpfc['Жиры'] = 0
    cpfc['Углеводы'] = 0

    history_list = []
    for meal in meals:
        cpfc['ККалории'] += meal.product.calories * meal.grams * 0.01
        cpfc['Белки'] += meal.product.proteins * meal.grams * 0.01
        cpfc['Жиры'] += meal.product.fats * meal.grams * 0.01
        cpfc['Углеводы'] += meal.product.carbs * meal.grams * 0.01

        meal_calories = round(meal.product.calories * meal.grams * 0.01)
        meal_proteins = round(meal.product.proteins * meal.grams * 0.01, 1)
        meal_fats = round(meal.product.fats * meal.grams * 0.01, 1)
        meal_carbs = round(meal.product.carbs * meal.grams * 0.01, 1)

        history_list.append({
            'Продукт': meal.product.name,
            'Калории, ккал': meal_calories,
            'Белки, г': meal_proteins,
            'Жиры, г': meal_fats,
            'Углеводы, г': meal_carbs
        })

    remains = daily_target - cpfc['ККалории']

    return cpfc, history_list, remains

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return {'status': 'ok'}


@app.post('/products')
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    db_product = Products(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get('/products', response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Products).all()
    return products


@app.post('/users')
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.name == user_in.name).first()
    if user:
        raise HTTPException(status_code=400, detail='Этот ник уже занят')
    db_user = Users(**user_in.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/meals", response_model=Meal)
def create_meal(meal_in: MealCreate, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.name == meal_in.user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    product = db.query(Products).filter(Products.product_id == meal_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    db_meal = Meals(user_id=user.user_id,
                    **meal_in.model_dump())
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


@app.get('/users/{name}/stats')
def get_user_stats(name: str, date_query: date, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meals = db.query(Meals).join(Products).filter(Meals.user_id == user.user_id,
                                          Meals.date == date_query
                                          ).all()

    total_eaten, meals_history, remains = calculate_nutrition(meals, user.daily_target)

    return {
        'user_name': user.name,
        'date': date_query,
        'daily_target': user.daily_target,
        'total_eaten': total_eaten,
        'remains': remains,
        'meals_history': meals_history
    }


@app.delete('/meals/{meal_id}')
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meals).filter(Meals.meal_id == meal_id).first()

    if not meal:
        raise HTTPException(status_code=404, detail='Приём пищи не найден')

    db.delete(meal)
    db.commit()

    return {'message': 'Приём пищи успешно удалён'}