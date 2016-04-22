import super_tiny_compiler
program = "(add 2 (subtract 4 2))"
expectedOutput = "add(2, subtract(4, 2));"

expectedTokens = [
  { 'type': 'lparen',  'value': '('        },
  { 'type': 'name',   'value': 'add'      },
  { 'type': 'number', 'value': '2'        },
  { 'type': 'lparen',  'value': '('        },
  { 'type': 'name',   'value': 'subtract' },
  { 'type': 'number', 'value': '4'        },
  { 'type': 'number', 'value': '2'        },
  { 'type': 'rparen',  'value': ')'        },
  { 'type': 'rparen',  'value': ')'        }
];

expectedAst = {
  'type': 'Program',
  'body': [{
    'type': 'CallExpression',
    'name': 'add',
    'params': [{
      'type': 'NumberLiteral',
      'value': '2'
    }, {
      'type': 'CallExpression',
      'name': 'subtract',
      'params': [{
        'type': 'NumberLiteral',
        'value': '4'
      }, {
        'type': 'NumberLiteral',
        'value': '2'
      }]
    }]
  }]
};

expectedTransformedAst = {
  'type': 'Program',
  'body': [{
    'type': 'ExpressionStatement',
    'expression': {
      'type': 'CallExpression',
      'callee': {
        'type': 'Identifier',
        'name': 'add'
      },
      'arguments': [{
        'type': 'NumberLiteral',
        'value': '2'
      }, {
        'type': 'CallExpression',
        'callee': {
          'type': 'Identifier',
          'name': 'subtract'
        },
        'arguments': [{
          'type': 'NumberLiteral',
          'value': '4'
        }, {
          'type': 'NumberLiteral',
          'value': '2'
        }]
      }]
    }
  }]
};

from pprint import pprint

newTokens = super_tiny_compiler.tokenizer(program)
newAst = super_tiny_compiler.parser(newTokens)
newTransformedAst = super_tiny_compiler.transformer(newAst)
newCodeGenerator = super_tiny_compiler.codeGenerator(newTransformedAst)
newOutput = super_tiny_compiler.compiler(program)


assert (newTokens == expectedTokens), 'Tokenizer should turn `program` string into `tokens` array';
assert (newAst == expectedAst), 'Parser should turn `tokens` array into `ast`';
assert (newTransformedAst == expectedTransformedAst), 'Transformer should turn `ast` into a `newAst`';
assert (newCodeGenerator == expectedOutput), 'Code Generator should turn `newAst` into `output` string';
assert (newOutput == expectedOutput), 'Compiler should turn `program` into `output`';

