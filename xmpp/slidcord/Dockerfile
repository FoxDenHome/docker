FROM nicocool84/slidcord:master

USER root
RUN apt-get update && \
        apt-get install -y python3-nacl wget && \
        pip install pynacl

RUN rm -f /venv/lib/python3.11/site-packages/slidge/db/avatar.py /venv/lib/python3.11/site-packages/slidge/db/meta.py && \
        wget https://raw.githubusercontent.com/Doridian/slidge/87feaec6b64c5c3f4d90d32f2e4370716cf66b42/slidge/db/avatar.py -O /venv/lib/python3.11/site-packages/slidge/db/avatar.py && \
        wget https://raw.githubusercontent.com/Doridian/slidge/87feaec6b64c5c3f4d90d32f2e4370716cf66b42/slidge/db/meta.py -O /venv/lib/python3.11/site-packages/slidge/db/meta.py

USER slidge
