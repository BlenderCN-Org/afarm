SHELL=/bin/bash

#Macros
DEPS=""
NAME="animal-farm"
NAME_SHORT="afarm"
VERSION=0.0.1a1

PYTHON=python

SETUP_MASTER=setup_master.py
SETUP_CLIENT=setup_client.py
SETUP_SLAVE=setup_slave.py
SETUP=setup.py

#Dependencies

install-deps :
	pip3 install -U pip wheel #Standard items.
	pip3 install -Ur requirements.txt

reinstall-deps : clean-deps install-deps

list-deps :
	pip3 list

delete-deps :
	pip3 uninstall -r requirements.txt

clean-deps :
	pip3 freeze | xargs pip uninstall -y

#Distribute

build-master :
	${PYTHON} ${SETUP_MASTER} build

deb-master :
	mv ${SETUP_MASTER} ${SETUP}

	$(PYTHON) ${SETUP} --command-packages=stdeb.command sdist_dsc

	mv ${SETUP} ${SETUP_MASTER}

	cd deb_dist/animal-farm-${VERSION}; debuild

build-clean :
	rm -rf deb_dist dist animal-farm-${VERSION}.tar.gz MANIFEST
