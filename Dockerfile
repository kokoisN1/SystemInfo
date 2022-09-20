FROM python:3.8-slim-buster
ARG LISTEN_PORT=5000
ENV PORT=$LISTEN_PORT

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "SystemInfoApp", "run", "--host=0.0.0.0"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
