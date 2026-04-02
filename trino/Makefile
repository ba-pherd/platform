SHELL = /bin/bash

.PHONY: create-udf-package

create-udf-package:
	cd plugins/anonymization-udfs && ./mvnw clean install
	cp -r plugins/anonymization-udfs/target/trino-anonymization-udfs-1.0 docker/server/trino-anonymization-udfs-1.0