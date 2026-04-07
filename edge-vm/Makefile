SHELL = /bin/bash

.PHONY: up export

up:
	test -e .env || { echo "Create the .env file as documented in the README.md" ; exit 1; }
	test -e rootCA.crt || { echo "Copy the rootCA.crt file from the server" ; exit 1; }
	vagrant validate
	vagrant up

export:
	read -p "Should I export it to OVA (VM is stopped)? (y/n)" do_export_vm && \
		test "$$do_export_vm" = 'y' && \
		vagrant halt && \
		VBoxManage export prin-webapp --output='prin-webapp.ova' --ovf20 --manifest