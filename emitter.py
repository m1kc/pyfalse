import ast

def readfile(filename):
	with open(filename, 'r') as content_file:
		return content_file.read()

def indent(s):
	ret = []
	for ss in s.split('\n'):
		ret += ['  '+ss]
	return '\n'.join(ret)


def emit_program(el):
	return readfile('emitter_header.py'), emit(el), readfile('emitter_footer.py')

def emit(el):
	if isinstance(el, ast.Function):
		ret = 'def fn():\n'
		for x in el.value:
			ret += indent(emit(x))
			ret += '\n'
		ret += 'state.stack.push(fn)'
		return ret
	if isinstance(el, ast.Number):
		return f'state.stack.push({el.value})'
	if isinstance(el, ast.Opcode):
		return emit_opcode(el.value)
	if isinstance(el, ast.String):
		return f"print({el.value.__repr__()})"
	if isinstance(el, ast.Varname):
		return f"current_var = {el.value.__repr__()}"
	print(el)
	raise ValueError('Unknown AST node type')

def emit_opcode(op):
	if op == '+': return 'state.add()'
	elif op == '-': return 'state.sub()'
	elif op == '*': return 'state.mul()'
	elif op == '/': return 'state.div()'
	elif op == '_': return 'state.neg()'

	elif op == '=': return 'state.eq()'
	elif op == '>': return 'state.gt()'
	elif op == '&': return 'state.land()'
	elif op == '|': return 'state.lor()'
	elif op == '~': return 'state.lneg()'

	elif op == '$': return 'state.dup()'
	elif op == '%': return 'state.drop()'
	elif op == '\\': return 'state.swap()'
	elif op == '@': return 'state.rot()'
	elif (op == 'ø' or op == 'p'): return 'state.pick()'

	elif op == ':': return 'state.setvar()'
	elif op == ';': return 'state.getvar()'

	elif op == '!': return 'fn = state.stack.pop()\nfn()'
	elif op == '?': return 'fn = state.stack.pop()\ncond = state.stack.pop()\nif cond == 1:\n  fn()'
	elif op == '#': return '''fn = state.stack.pop()
cond = state.stack.pop()
while True:
  cond()
  if state.stack.pop() == 1:
    fn()
  else:
    break'''

	else: raise ValueError("Unknown operation: "+op)
