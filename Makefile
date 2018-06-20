all:
	env PYTHONPATH=./pypy:./virtualenv/lib/python3.6/site-packages pypy ./pypy/rpython/translator/goal/translate.py main.py

clone:
	hg clone https://bitbucket.org/pypy/pypy
