FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

RUN gcc test_file.c -o test_file

CMD ["python", "app.py"]