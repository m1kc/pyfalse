import ast

import sys

import pyparsing as pp


def parse(s):
	code = pp.Forward()
	opcode = pp.Or([
		pp.Literal('+'),
		pp.Literal('-'),
		pp.Literal('*'),
		pp.Literal('/'),
		pp.Literal('_'),

		pp.Literal('='),
		pp.Literal('>'),
		pp.Literal('&'),
		pp.Literal('|'),
		pp.Literal('~'),

		pp.Literal('$'),
		pp.Literal('%'),
		pp.Literal('\\'),
		pp.Literal('@'),
		pp.Literal('ø'), pp.Literal('p'),

		pp.Literal(':'),
		pp.Literal(';'),

		pp.Literal('!'),
		pp.Literal('?'),
		pp.Literal('#'),
	]).setParseAction(lambda toks: ast.Opcode(toks[0]))
	number = (
		pp.Word('1234567890')
		.setParseAction(lambda toks: ast.Number(int(toks[0])))
	)
	str_def = (
		(pp.Literal('"') + pp.SkipTo(pp.Literal('"'), include=True))
		.setParseAction(lambda toks: ast.String(toks[1]))
	)
	varname = (
		pp.Word('qwertyuiopasdfghjklzxcvbnm', exact=1)
		.setParseAction(lambda toks: ast.Varname(toks[0]))
	)
	fn_def = pp.Suppress(pp.Literal('[')) + code + pp.Suppress(pp.Literal(']'))
	expr = pp.Or([opcode, number, varname, str_def, fn_def])
	atom = pp.Or([expr])
	code << pp.ZeroOrMore(atom)
	code.setParseAction(lambda toks: ast.Function(toks))
	return code.parseString(s)[0]
