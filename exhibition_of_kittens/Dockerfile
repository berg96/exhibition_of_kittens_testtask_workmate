FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN chmod +x entrypoint.sh
RUN chmod +x wait-for-it.sh
ENTRYPOINT ["/app/entrypoint.sh"]