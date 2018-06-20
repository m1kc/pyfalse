#!/usr/bin/env python3

import pyparsing as pp

import sys

# [$1=$[\%1\]?~[$1-f;!*]?]f:
def f(x):
	if x == 1:
		return 1
	else:
		return x * f(x - 1)


class Stack(object):
	def __init__(self):
		#super(Stack, self).__init__()
		self.stack = []

	def push(self, x):
		self.stack += [x]

	# Look at Nth element where N=0 is stack top.
	def look(self, n):
		return self.stack[-n-1]

	def pop(self):
		x = self.stack[-1]
		self.stack = self.stack[:-1]
		return x

	def pop2(self):
		b = self.pop()
		a = self.pop()
		return a, b

	def op(self, fn):
		self.push(fn(self.pop()))

	def op2(self, fn):
		self.push(fn(*self.pop2()))


class FalseState(object):
	def __init__(self):
		#super(FalseState, self).__init__()
		self.stack = Stack()

	def add(self): self.stack.op2(lambda a, b: a+b)
	def sub(self): self.stack.op2(lambda a, b: a-b)
	def mul(self): self.stack.op2(lambda a, b: a*b)
	def div(self): self.stack.op2(lambda a, b: a/b)
	def neg(self): self.stack.op(lambda a: -a)

	def eq(self): self.stack.op2(lambda a, b: a == b)
	def gt(self): self.stack.op2(lambda a, b: a > b)
	def land(self): self.stack.op2(lambda a, b: a and b)
	def lor(self): self.stack.op2(lambda a, b: a or b)
	def lneg(self): self.stack.op(lambda a: not a)

	def dup(self):
		self.stack.push(self.stack.look(0))

	def drop(self):
		self.stack.pop()

	def swap(self):
		a = self.stack.pop()
		b = self.stack.pop()
		self.stack.push(a)
		self.stack.push(b)

	def rot(self):
		c = self.stack.pop()
		b = self.stack.pop()
		a = self.stack.pop()
		self.stack.push(b)
		self.stack.push(c)
		self.stack.push(a)

	def pick(self):
		i = self.stack.pop()
		self.stack.push(self.stack.look(i))


def try_parse(value):
	try:
		return int(value), True
	except ValueError:
		return 0, False


def is_space(x):
	return (x in [' ', '\n', '\t'])


class FalseFunction(object):
	def __init__(self, source=""):
		#super(FalseFunction, self).__init__()
		self.source = source

	def run(self, state):
		in_number = False
		for op in self.source:
			n, ok = try_parse(op)
			if ok:
				if in_number:
					state.stack.push(state.stack.pop() * 10 + n)
				else:
					in_number = True
					state.stack.push(n)
			else:
				in_number = False
				if is_space(op): pass
				elif op == '+': state.add()
				elif op == '-': state.sub()
				elif op == '*': state.mul()
				elif op == '/': state.div()
				elif op == '_': state.neg()
				elif op == '=': state.eq()
				elif op == '>': state.gt()
				elif op == '&': state.land()
				elif op == '|': state.lor()
				elif op == '~': state.lneg()
				elif op == '$': state.dup()
				elif op == '%': state.drop()
				elif op == '\\': state.swap()
				elif op == '@': state.rot()
				elif (op == 'ø' or op == 'p'): state.pick()
				else: raise ValueError("Unknown operation: "+op)
		return


def run(s, print_stack=True):
	f = FalseState()
	main_fn = FalseFunction(s)
	main_fn.run(f)
	if print_stack:
		print(f.stack.stack)
	return f


def entry_point(argv):
	run('2 2 +')
	run('322 22 -')
	run('128 10 *')
	run('100 5 /')
	run('5 _')
	run('2 2 =')
	run('3 4 >')
	run('1 1 = 1 1 = &')
	run('1 1 = 1 2 = &')
	run('1 1 = 1 2 = |')
	run('1 1 = ~')
	run('0 1 $')
	run('0 1 %')
	run('0 1 2 \\')
	run('0 1 2 3 @')
	run('7 8 9 2 p')
	return 0


def target(*args):
	return entry_point, None

if __name__ == "__main__":
	entry_point(sys.argv)
