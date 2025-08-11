FROM python:3.12-alpine
WORKDIR /app
COPY . /app
RUN apk add --no-cache ffmpeg
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["python", "./main.py"]
