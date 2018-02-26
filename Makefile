SHELL := /bin/bash

.PHONY: clean
clean:
	@rm -f example.sqlite
	@rm -Rf dist/
	@rm -Rf build/
	@rm -Rf indexes/
	@rm -Rf __pycache__/
	@rm -Rf ponywhoosh_indexes/
	@rm -Rf flask_ponywhoosh.egg-info
	@find . -name "*.pyc" -type f -delete

.PHONY : install-py2
install-py2:
	make clean
	python2.7 setup.py install

.PHONY : test-py2
test-py2:
	make install-py2
	python2.7 -m unittest test

.PHONY : install-py3
install-py3:
	make clean
	python3 setup.py install

.PHONY : test-py3
test-py3:
	make install-py3
	python3 -m unittest test

.PHONY : docs
docs:
	rm -d -Rf docs/src/_build
	rm -d -Rf docs/_sources
	rm -d -Rf docs/_static
	rm -f docs/*.html docs/*.js .buildinfo *.inv
	pip install sphinx
	cd docs/src && make html
	zip -vr docs/html.zip docs/src/_build/html -x "*.DS_Store"
	cp -R docs/src/_build/html/* docs/

.PHONY : TODO
TODO :
	find . -type d \( -path './.git' -o -path './dist' \) -prune -o -print \
	| xargs grep -I 'TODO' \
	| sort

.PHONY : README.rst
README.rst :
	pandoc --from=rst --to=rst --output=README.rst README.rst

.PHONY : deploy README.rst docs
deploy :
	pip install twine
	$(eval VERSION := $(shell bash -c 'read -p "Version: " pwd; echo $$pwd'))
	echo
	$(eval MSG := $(shell bash -c 'read -p "Comment: " pwd; echo $$pwd'))
	make clean
	git tag v$(VERSION)
	git commit -am "[ v$(VERSION) ] new version: $(MSG)"
	python setup.py build
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
	make clean
