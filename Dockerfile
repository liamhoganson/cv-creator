FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
# Upgrade pip and install setuptools before installing requirements
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]