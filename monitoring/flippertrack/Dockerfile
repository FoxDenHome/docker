FROM alpine:latest

RUN apk --no-cache add python3 py3-requests py3-prometheus-client py3-dateutil

COPY __main__.py /opt/flippertrack/__main__.py

ENTRYPOINT [ "/usr/bin/python3", "/opt/flippertrack" ]
