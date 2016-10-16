REPO=thraxil
APP=artsho

include *.mk

deploy: ./ve/bin/python check jenkins
	./ve/bin/fab deploy

travis_deploy: ./ve/bin/python check jenkins
	./ve/bin/fab deploy -i artsho_rsa

all: flake8 test
