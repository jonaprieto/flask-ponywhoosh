SHELL := /bin/bash


.PHONY : install
install:
	python setup.py install

.PHONY : test
test:
	python setup.py test
	python -m unittest test
	@echo "$@ succeeded!"

.PHONY : docs
docs:
	pip install sphinx
	cd docs && make html

.PHONY : TODO
TODO :
	find . -type d \( -path './.git' -o -path './dist' \) -prune -o -print \
	| xargs grep -I 'TODO' \
	| sort