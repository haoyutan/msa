all: dist uninstall install

dist: clean
	python setup.py sdist

uninstall:
	-pip uninstall -y MSA-Framework

install: dist
	pip install dist/*.tar.gz

clean:
	rm -rf dist/*.tar.gz
