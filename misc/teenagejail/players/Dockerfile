FROM ubuntu:20.04

RUN apt update && apt install -y python3

RUN /usr/sbin/useradd --no-create-home -u 1000 user

#works with os.setuid(1000) to make sure file is unreadable by the time user code is run
COPY teenagejail.py /
RUN chmod 600 /teenagejail.py

CMD python3 teenagejail.py
