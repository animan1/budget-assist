virtualenv:
	virtualenv .virtualenv

reqs: pip
	.virtualenv/bin/pip install -r requirements.txt

pip:
	.virtualenv/bin/pip install --upgrade "pip>=6.0.6" wheel

quickstart: virtualenv reqs
