FROM nicocool84/slidcord:master

USER root
RUN apt-get update && \
        apt-get install -y python3-nacl wget && \
        pip install pynacl

RUN rm -f /venv/lib/python3.11/site-packages/slidge/db/avatar.py && \
        wget https://raw.githubusercontent.com/Doridian/slidge/73a67b506815f1bc1013d161cd2932ec2c151183/slidge/db/avatar.py -O /venv/lib/python3.11/site-packages/slidge/db/avatar.py

USER slidge
