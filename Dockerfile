FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Pre-download model into the image so runtime stays offline & instant
RUN python -c "from transformers import pipeline; pipeline('text-classification', model='unitary/toxic-bert')"

EXPOSE 9090

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090"]
