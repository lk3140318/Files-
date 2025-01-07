FROM python:3.9-slim

WORKDIR https://github.com/lk3140318/Files-/app
COPY . https://github.com/lk3140318/Files-/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
