FROM python:3.14

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY api/ .

EXPOSE 5000

CMD ["python", "rotas_api/api_db.py"]