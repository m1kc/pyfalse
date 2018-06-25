def entry_point(argv):
	m = state.stack.pop()
	m()
	print(state.stack.stack)

def target(*args):
    return entry_point, None

if __name__ == "__main__":
	import sys
	entry_point(sys.argv)
