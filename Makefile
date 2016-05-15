.PHONY: run test

run:
	python run.py
	
test:
	nosetests --with-coverage --cover-inclusive --cover-package=wallebot  wallebot
