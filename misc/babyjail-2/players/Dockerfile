FROM ubuntu:20.04

RUN apt update && apt install -y python3

RUN /usr/sbin/useradd --no-create-home -u 1000 user

#works with os.setuid(1000) to make sure file is unreadable by the time user code is run
COPY babyjail-2.py /
RUN chmod 600 /babyjail-2.py

CMD python3 babyjail-2.py
