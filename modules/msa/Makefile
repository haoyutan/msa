all: dist install

dist: clean
	python setup.py sdist

uninstall:
	yes | pip uninstall MSA-Framework

install: dist
	pip install dist/*.tar.gz

clean:
	rm -rf dist/*.tar.gz
