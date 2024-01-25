FROM python:3.11.6-bullseye

WORKDIR /app
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8001

CMD [ "python3", "./main.py" ]