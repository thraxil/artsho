REPO=thraxil
APP=artsho

include *.mk

deploy: ./ve/bin/python validate jenkins
	./ve/bin/fab deploy

travis_deploy: ./ve/bin/python validate jenkins
	./ve/bin/fab deploy -i artsho_rsa
