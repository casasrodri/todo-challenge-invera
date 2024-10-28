FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . .
RUN python manage.py migrate
RUN python create_superuser.py

EXPOSE 8000

CMD [ "gunicorn", "--bind", "0.0.0.0:8000",  "app.wsgi:application"]

