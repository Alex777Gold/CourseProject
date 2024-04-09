FROM python:3.9

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2-binary django_extensions

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV DATABASE_URL=postgres://postgres:1@db:5432/CourseProject


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
