FROM amazoncorretto:23-headless

WORKDIR /data
USER 1000:1000
ENTRYPOINT [ "java" "-Xmx8G" "-Xms8G" "-jar" "server.jar" "nogui" ]
