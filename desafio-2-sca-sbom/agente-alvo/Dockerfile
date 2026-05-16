FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY target/agente-bancario-1.0.0-baseline.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
