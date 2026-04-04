SHELL = /bin/bash

.PHONY: up

up:
	test -e .env || { echo "Create the .env file as documented in the README.md" ; exit 1; }
	test -e rootCA.crt || { echo "Copy the rootCA.crt file from the server" ; exit 1; }
	vagrant validate
	vagrant up
	printf "Test the VM. Should I export it to OVA? (y/n) "
	read do_export_vm && \
		test "$$do_export_vm" = 'y' && \
		vagrant halt && \
		VBoxManage export prin-webapp --output='prin-webapp.ova' --ovf20 --manifest