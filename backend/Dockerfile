FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD [ "fastapi", "run",  "./app/main.py", "--host", "0.0.0.0", "--port", "8181"]
# CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8181"] for prod
# http://127.0.0.1:8181/docs

# docker build . -t backend
# docker run -p 8181:8181 backend