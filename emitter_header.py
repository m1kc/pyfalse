class Stack(object):
	def __init__(self):
		#super(Stack, self).__init__()
		self.stack = []

	def push(self, x):
		self.stack += [x]

	def look(self, n):
		"""Look at Nth element where N=0 is stack top."""
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


def bool_to_int(x):
	if x == True:
		return 1
	return 0


def int_to_bool(x):
	if x == 1:
		return True
	return False


class FalseState(object):
	def __init__(self):
		#super(FalseState, self).__init__()
		self.stack = Stack()
		self.current_var = ''
		self.vars = {}

	def add(self): self.stack.op2(lambda a, b: a+b)
	def sub(self): self.stack.op2(lambda a, b: a-b)
	def mul(self): self.stack.op2(lambda a, b: a*b)
	def div(self): self.stack.op2(lambda a, b: a/b)
	def neg(self): self.stack.op(lambda a: -a)

	def eq(self): self.stack.op2(lambda a, b: bool_to_int(a == b))
	def gt(self): self.stack.op2(lambda a, b: bool_to_int(a > b))
	def land(self): self.stack.op2(lambda a, b: bool_to_int(int_to_bool(a) and int_to_bool(b)))
	def lor(self): self.stack.op2(lambda a, b: bool_to_int(int_to_bool(a) or int_to_bool(b)))
	def lneg(self): self.stack.op(lambda a: bool_to_int(not int_to_bool(a)))

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

	def setvar(self):
		self.vars[self.current_var] = self.stack.pop()

	def getvar(self):
		self.stack.push(self.vars[self.current_var])


state = FalseState()
