SHELL = /bin/bash

.PHONY: create-crt create-udf-package

up:
	test -e .env || { echo "Create the .env file as documented in the README.md" ; exit 1; }
	vagrant up
	printf "Test the VM. Should I export it to OVA? (y/n) "
	read do_export_vm && \
		test "$$do_export_vm" = 'y' && \
		VBoxManage export prin-webapp --output='prin-webapp.ova' --ovf20 --manifest