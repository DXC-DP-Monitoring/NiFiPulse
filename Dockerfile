FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary

CMD ["python", "load_star_schema.py"]
