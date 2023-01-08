FROM ubuntu:jammy
WORKDIR /
RUN apt update && apt upgrade -y
RUN apt install python3-pip -y
RUN mkdir -p /infrared/data/configs/
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000

CMD 'python3' 'main.py'