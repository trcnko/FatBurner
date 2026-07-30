# 🍰 FatBurner — Умный трекер питания и КБЖУ

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white)
![Security](https://img.shields.io/badge/Security-Bcrypt%20Hashing-228B22)

**FatBurner** — полноценное production-ready веб-приложение для ведения дневника питания, расчёта КБЖУ и конструирования собственных рецептов с автоматическим пересчётом калорийности на 100 грамм.

🌐 **Live Demo:** [https://fat-burner.ru](https://fat-burner.ru)

---

## ✨ Ключевые возможности

- 🔐 **Безопасная аутентификация** — регистрация и вход по никнейму и паролю. Пароли надежно хешируются алгоритмом **bcrypt** (через `passlib`).
- 🍪 **Бесшовные сессии (Cookies)** — интеграция с `streamlit-extras` CookieManager. Авторизация сохраняется в браузере на 365 дней, пользователь не вылетает из профиля при обновлении страницы.
- 📝 **Дневник питания** — детальный отчёт за день: съедено / осталось / цель + разбивка по БЖУ.
- 🗑️ **Полноценный CRUD** — создание и безопасное удаление записей о приёмах пищи.
- 🍕 **База продуктов** — добавление новых продуктов с КБЖУ на 100 г.
- 🥘 **Конструктор рецептов** — умный калькулятор: суммирует КБЖУ всех ингредиентов и сохраняет готовое блюдо в базу с пересчётом на 100 г.
- 🧪 **Тестирование (Pytest)** — unit-тесты для проверки корректности API-эндпоинтов и бизнес-логики.
- 🎨 **Дизайн в палитре Pantone 2026** — кастомный CSS, эмодзи-навигация и тёплая эстетика интерфейса, выходящая за рамки стандартных виджетов Streamlit.

---

## Локальный запуск

### 1. Клонировать репозиторий
git clone https://github.com/trcnko/FatBurner.git && cd FatBurner

### 2. Создать .env в корне
cat > .env << EOF
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_db
EOF

### 3. Поднять все сервисы
docker-compose up --build

### 4. Запустить тесты (внутри контейнера backend)
docker-compose exec backend pytest -v