# Install Webapp on edge VM

## Requirements

Create a `.env` file with the following content and fill the variables :

```bash
# custom secret to enable sessions in Flask
FLASK_SECRET_KEY=SecretKeyForFlaskSessions

# endpoint of the kafka broker
KAFKA_BOOTSTRAP_SERVERS=kafka-broker-0:9092
```

## Procedure

- Run `make up`
- Open VirtualBox and export the VM with name `prin-webapp`.
- Copy the VM file inside the Edge machine and run it