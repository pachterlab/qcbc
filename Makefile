.PHONY : clean build

clean:
	rm -rf build
	rm -rf dist
	rm -rf qcbc.egg-info
	rm -rf docs/_build
	rm -rf docs/api
	rm -rf .coverage

build:
	python setup.py sdist bdist_wheel

