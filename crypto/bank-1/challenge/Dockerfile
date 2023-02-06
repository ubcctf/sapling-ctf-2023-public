FROM gcr.io/kctf-docker/challenge@sha256:501458c0426acc3b5a74a661791271faf0dca6555b46bfb76f944d2558bd08d5
RUN apt update && apt install -y python3 python3-pip
RUN pip install pycryptodome

COPY --chown=user challenge.py /home/user/challenge.py
COPY --chown=user secrets.py /home/user/secrets.py

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"/home/user/challenge.py"