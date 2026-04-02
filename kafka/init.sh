#!/bin/bash

echo "Configuring topic devprin.patients"
/opt/kafka/bin/kafka-topics.sh --create \
    --if-not-exists \
    --topic "devprin.patients" \
    --replication-factor=1 \
    --bootstrap-server kafka-broker-0:9094

echo "Configuring topic devprin.mir-results"
/opt/kafka/bin/kafka-topics.sh --create \
    --if-not-exists \
    --topic "devprin.mir-results" \
    --replication-factor=1 \
    --bootstrap-server kafka-broker-0:9094

echo "Configuring topic devprin.task.trigger"
/opt/kafka/bin/kafka-topics.sh --create \
    --if-not-exists \
    --topic "devprin.task.trigger" \
    --replication-factor=1 \
    --bootstrap-server kafka-broker-0:9094

userGroups=("test-group1" "test-group2")

for group in ${userGroups[@]}
do
    topicName="devprin.${group}.task.result"
    echo "Configuring topic ${topicName}"
    /opt/kafka/bin/kafka-topics.sh --create \
        --if-not-exists \
        --topic "${topicName}" \
        --replication-factor=1 \
        --bootstrap-server kafka-broker-0:9094
    /opt/kafka/bin/kafka-configs.sh --entity-type topics \
        --entity-name "${topicName}" \
        --alter --add-config retention.ms="$(($TOPIC__TASK_RESULT__RETENTION_SECONDS * 1000))" \
        --bootstrap-server kafka-broker-0:9094    
done
