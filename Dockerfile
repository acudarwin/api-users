FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY requirements_dev.txt .

RUN pip install -r requirements_dev.txt

ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "-b", ":8000", "--timeout", "3600", "src.main:app", "--reload"]