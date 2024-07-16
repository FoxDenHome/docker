FROM nicocool84/slidcord:master

USER root
RUN apt-get update && \
        apt-get install -y python3-nacl && \
        pip install pynacl
USER slidge
