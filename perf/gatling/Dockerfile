FROM openjdk:11.0.10-jdk

COPY . /gatling
WORKDIR /gatling
RUN ./gradlew clean compileGatlingScala

ENTRYPOINT ["./entrypoint.sh"]
