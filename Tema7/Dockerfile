FROM python:3.11

RUN ls -l /bin/sh || echo "sh not found :("
RUN which sh || echo "sh not found anywhere"
RUN ls -l /bin/bash || echo "bash not found"
RUN apt-get update && apt-get install -y bash dash && ln -sf /bin/dash /bin/sh


COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "hr_system.wsgi:application", "--bind", "127.0.0.1:8000"]