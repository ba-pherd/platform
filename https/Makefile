SHELL = /bin/bash

CREATE_CRT_SCRIPT_PATH=./create-crt.sh

.PHONY: create-crt

create-crt:
	chmod +x ${CREATE_CRT_SCRIPT_PATH} && \
	${CREATE_CRT_SCRIPT_PATH}
	cp rootCA.crt ../trino/docker/server/rootCA.crt