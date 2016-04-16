# encoding=utf8

import re

def tokenizer(input_program):
    current = 0
    tokens = []
    program_length = len(input_program)
    REGEX_WHITESPACE = re.compile(r"\s");
    REGEX_NUMBERS = re.compile(r"[0-9]");
    REGEX_LETTERS = re.compile(r"[a-z]", re.I);
    while current < program_length:
        char = input_program[current]
        if char == '(':
            tokens.append({
                'type': 'lparen',
                'value': '('
            })
            current = current+1
            continue
        if char == ')':
            tokens.append({
                'type': 'rparen',
                'value': ')'
            })
            current = current+1
            continue

        if re.match(REGEX_WHITESPACE, char):
            current = current+1
            continue

        if re.match(REGEX_NUMBERS, char):
            value = ''
            while re.match(REGEX_NUMBERS, char):
                value += char
                current = current+1
                char = input_program[current];

            tokens.append({
                'type': 'number',
                'value': value
            })
            continue

        if re.match(REGEX_LETTERS, char):
            value = ''
            while re.match(REGEX_LETTERS, char):
                value += char
                current = current+1
                char = input_program[current]

            tokens.append({
                'type': 'name',
                'value': value
            })

            current = current+1
            continue

        raise ValueError('I dont know what this character is: ' + char);
    return tokens
        
def parser(tokens):
    global current
    current = 0
    def walk():
        global current
        token = tokens[current]
        if token.get('type') == 'number':
            current = current + 1
            return {
                'type': 'NumberLiteral',
                'value': token.get('value')
            }
        if token.get('type') == 'lparen':
            current = current + 1
            token = tokens[current]
            node = {
                'type': 'CallExpression',
                'name': token.get('value'),
                'params': []
            }

            current = current + 1
            token = tokens[current]
            while token.get('type') != 'rparen':
                node['params'].append(walk());
                token = tokens[current]
            current = current + 1
            return node
        raise TypeError(token.get('type'))
    ast = {
        'type': 'Program',
        'body': []
    }
    token_length = len(tokens)
    while current < token_length:
        ast['body'].append(walk())
    return ast

def traverser(ast, visitor):
    def traverseArray(array, parent):
        for child in array:
            traverseNode(child, parent)
    
    def traverseNode(node, parent):
        method = visitor.get(node['type'])
        if method:
            method(node, parent)
        if node['type'] == 'Program':
            traverseArray(node['body'], node)
        elif node['type'] == 'CallExpression':
            traverseArray(node['params'], node)
        elif node['type'] == 'NumberLiteral':
            # do nothing
            0
        else:
            raise TypeError(node['type'])
    traverseNode(ast, None)

def transformer(ast):
    newAst = {
        'type': 'Program',
        'body': []
    }
    
    ast['_context'] = newAst.get('body')

    def NumberLiteralVisitor(node, parent):
        parent['_context'].append({
            'type': 'NumberLiteral',
            'value': node['value']
        })
    def CallExpressionVisitor(node, parent):
        expression = {
            'type': 'CallExpression',
            'callee': {
                'type': 'Identifier',
                'name': node['name']
            },
            'arguments': []
        }
        
        node['_context'] = expression['arguments']

        if parent.get('type') != 'CallExpression':
            expression = {
                'type': 'ExpressionStatement',
                'expression': expression
            }
        parent['_context'].append(expression)

    traverser( ast , {
        'NumberLiteral': NumberLiteralVisitor,
        'CallExpression': CallExpressionVisitor 
    })
    
    return newAst

def codeGenerator(node):
    if node['type'] == 'Program':
        return '\n'.join([code for code in map(codeGenerator, node['body'])])
    elif node['type'] == 'ExpressionStatement':
        return (
            codeGenerator(node['expression']) 
            +';'
            )
    elif node['type'] == 'CallExpression':
        return (
            codeGenerator(node['callee']) 
            +'('
            + ', '.join([code for code in map(codeGenerator, node['arguments'])])
            +')'
            )
    elif node['type'] == 'Identifier':
        return node['name']
    elif node['type'] == 'NumberLiteral':
        return node['value']
    else:
        raise TypeError(node['type'])

def compiler(input_program):
    tokens = tokenizer(input_program)
    ast    = parser(tokens)
    newAst = transformer(ast)
    output = codeGenerator(newAst)
    return output
