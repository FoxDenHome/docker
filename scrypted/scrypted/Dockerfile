FROM ghcr.io/koush/scrypted:latest

COPY monitor.py /monitor.py

ENTRYPOINT [ "/monitor.py", "npm", "--prefix", "/server", "exec", "scrypted-serve" ]
