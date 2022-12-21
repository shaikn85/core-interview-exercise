FROM python:alpine
WORKDIR /app
COPY app.py /app
COPY input.json /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["python", "app.py"]
