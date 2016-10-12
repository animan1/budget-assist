BIN = .virtualenv/bin
PIP = ${BIN}/pip
PYTHON = ${BIN}/python

virtualenv:
	virtualenv .virtualenv

reqs: pip
	${PIP} install -r requirements.txt

pip:
	${PIP} install --upgrade "pip>=6.0.6" wheel

quickstart: virtualenv reqs

shell:
	${PYTHON} manage.py shell
