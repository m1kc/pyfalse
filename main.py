#!/usr/bin/env python3

import ast
import parser
import emitter_py3
import emitter_rpy

import sys
import subprocess
import os

import pyparsing as pp


def tests():
	arr = [
		'',
		'2 2+',
		'322 22 -',
		'128 10 *',
		'100 5 /',
		'5 _',
		'2 2 =',
		'3 4 >',
		'1 1 = 1 1 = &',
		'1 1 = 1 2 = &',
		'1 1 = 1 2 = |',
		'1 1 = ~',
		'0 1 $',
		'0 1 %',
		'0 1 2 \\',
		'0 1 2 3 @',
		'7 8 9 2 p',
		'"hello"',
		'["hello"]',
		'["hello"]["world"][2 2+]',
		'5 z :',
		'[$1=$[\\%1\\]?~[$1-f;!*]?]f:',
		'[$1=$[\\%1\\]?~[$1-f;!*]?]f:  5 f;!',
		'0[$5=~]["hello"1+]#'
	]
	for i in arr:
		print("=>", i)
		tree = parser.parse(i)
		print("=>", tree)
		# h, body, f = emitter_py3.emit_program(tree)
		h, body, f = emitter_rpy.emit_program(tree)
		source = "\n\n".join([h, body, f])
		print('---\n' + body + '\n---')
		with open('output.py', 'w') as file:
			file.write(source)
		# subprocess.run(['python3', 'output.py'], check=True)
		print('Compiling...')
		subprocess.run([
			'env',
			'PYTHONPATH=./pypy:/home/m1kc/work/Still-experimental/pypy-false/virtualenv/lib/python3.6/site-packages',
			'pypy',
			'./pypy/rpython/translator/goal/translate.py',
			'output.py',
		], check=True)
		print('Running...')
		subprocess.run(['./output-c'], check=True)
		print('exited')
		print()


def main():
	if sys.argv[1] == '--tests':
		tests()
	else:
		with open(sys.argv[1], 'r') as file:
			i = file.read()
			tree = parser.parse(i)
			# h, body, f = emitter_py3.emit_program(tree)
			h, body, f = emitter_rpy.emit_program(tree)
			source = "\n\n".join([h, body, f])
			with open('output.py', 'w') as file:
				file.write(source)
			subprocess.run(['python3', 'output.py'], check=True)


if __name__ == '__main__':
	main()
