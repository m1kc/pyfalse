def entry_point(argv):
	try:
		m = state.stack.pop().as_fn()
		m()
		print(state.stack.stack)
	except Exception as e:
		print(e)
	return 0


def target(*args):
    return entry_point, None

if __name__ == "__main__":
	import sys
	entry_point(sys.argv)
