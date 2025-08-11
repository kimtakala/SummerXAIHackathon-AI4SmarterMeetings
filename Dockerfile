FROM python:3.9.19-alpine
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["python", "./main.py"]
