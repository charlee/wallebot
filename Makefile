.PHONY: run test

run:
	python run.py
	
test:
	nosetests -s --with-coverage --cover-inclusive --cover-package=wallebot  wallebot
