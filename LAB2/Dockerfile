FROM ubuntu

RUN apt update && apt install -y iputils-ping python3 python3-venv python3-pip python3-dev build-essential

WORKDIR /app

COPY . .

RUN python3 -m venv venv

RUN ./venv/bin/pip install --upgrade pip

RUN ./venv/bin/pip install -r requirements.txt

ENTRYPOINT [ "./venv/bin/python", "app.py" ]