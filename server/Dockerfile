FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# mount /app/src for hot refreshes when developing locally
COPY src /app/src
VOLUME /app/src

WORKDIR /app/src
EXPOSE 5000
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000" ]
