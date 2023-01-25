FROM python:3.10.5
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev postgresql-client

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

ENV DATABASE_URL=postgres://obpqcmkostelfn:00cd6aab1ebe7440393401606db253d489239e82f177c4ace13b1a417c1be792@ec2-3-218-171-44.compute-1.amazonaws.com:5432/d7mtuekngs9rcb

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]