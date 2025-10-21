version: '3.9'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: hr_db
      POSTGRES_USER: hr_user
      POSTGRES_PASSWORD: hr_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn hr_system.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

volumes:
  postgres_data: