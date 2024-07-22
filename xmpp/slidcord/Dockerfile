FROM nicocool84/slidcord:master

USER root
RUN apt-get update && \
        apt-get install -y python3-nacl wget git && \
        pip install pynacl

# RUN rm -rf /venv/lib/python3.11/site-packages/slidge && \
#         git clone https://github.com/Doridian/slidge.git /tmp/slidge && \
#         git -C /tmp/slidge checkout 87feaec6b64c5c3f4d90d32f2e4370716cf66b42 && \
#         mv /tmp/slidge/slidge /venv/lib/python3.11/site-packages/slidge && \
#         rm -rf /tmp/slidge

USER slidge
