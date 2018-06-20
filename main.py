#!/usr/bin/env python3

import ast
import parser
import emitter

import sys
import subprocess
import os

import pyparsing as pp


def tests():
	arr = [
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
		h, body, f = emitter.emit_program(tree)
		print('---\n' + body + '\n---')
		source = "\n\n".join([h, body, f])
		with open('output.py', 'w') as file:
			file.write(source)
		subprocess.run(['python3', 'output.py'], check=True)
		print()

def main():
	if sys.argv[1] == '--tests':
		tests()
	else:
		with open(sys.argv[1], 'r') as file:
			i = file.read()
			tree = parser.parse(i)
			h, body, f = emitter.emit_program(tree)
			source = "\n\n".join([h, body, f])
			with open('output.py', 'w') as file:
				file.write(source)
			subprocess.run(['python3', 'output.py'], check=True)


if __name__ == '__main__':
	main()
