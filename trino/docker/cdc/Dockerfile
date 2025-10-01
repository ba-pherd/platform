FROM openjdk:11.0.14-jdk

ARG TRINO_VERSION

WORKDIR /cdc

RUN <<EOF
    apt update

    # Trino CLI
    wget -O trino https://github.com/trinodb/trino/releases/download/${TRINO_VERSION}/trino-cli-${TRINO_VERSION}
    chmod +x trino
    apt install -y less
EOF

ENV TRINO_ENDPOINT="http://trino:8080"
ENV FLUSH_DELAY_SECONDS=15

VOLUME /cdc/data

ENTRYPOINT ["bash", "-c", "./scripts/init.sh && ./scripts/cdc.sh"]