FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY ./ /app

WORKDIR /app/planner

EXPOSE 8080

CMD ["python", "main.py"]