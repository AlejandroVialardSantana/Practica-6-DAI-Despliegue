# Dockerfile
FROM python:3.11-alpine

WORKDIR /e-commerce
COPY . /e-commerce
RUN pip install -r requirements.txt

# Recolecta archivos estáticos
RUN python manage.py collectstatic --noinput

# Ejecuta Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "Ecommerce.wsgi:application"]