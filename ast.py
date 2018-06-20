class Opcode(object):
	def __init__(self, value):
		#super(Opcode, self).__init__()
		self.value = value
	def __str__(self):
		return "OP(" + self.value + ")"

class Number(object):
	def __init__(self, value):
		#super(Number, self).__init__()
		self.value = value
	def __str__(self):
		return "N(" + str(self.value) + ")"

class Varname(object):
	def __init__(self, value):
		#super(Varname, self).__init__()
		self.value = value
	def __str__(self):
		return "VAR(" + self.value + ")"

class String(object):
	def __init__(self, value):
		#super(String, self).__init__()
		self.value = value
	def __str__(self):
		return "STR('" + self.value + "')"

class Function(object):
	def __init__(self, value):
		#super(Function, self).__init__()
		self.value = value
	def __str__(self):
		ret = "FN("
		for i in self.value:
			ret += i.__str__()
			ret += " "
		ret = ret.strip()
		ret += ")"
		return ret
