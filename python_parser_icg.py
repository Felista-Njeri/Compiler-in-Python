#parser and icg code for the language in "input_program.txt"

import json

class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children else []
        self.leaf = leaf

def parse(tokens):
    token_iter = iter(tokens) 
    current_token = next(token_iter, None)

    def error(message):
        raise Exception(f"Syntax error: {message}")

    def match(expected_type, expected_value=None):
        nonlocal current_token
        if current_token is None:
            error(f"Unexpected end of input, expected {expected_type} {'with value ' + expected_value if expected_value else ''}")
        if current_token['Type'] == expected_type and (expected_value is None or current_token['Value'] == expected_value):
            matched_token = current_token
            current_token = next(token_iter, None)
            return matched_token
        else:
            error(f"Expected {expected_type} {'with value ' + expected_value if expected_value else ''}, but got {current_token['Type']} with value {current_token['Value']}")

    def program():
        function_node = function()
        return Node('program', [function_node])

    def function():
        match('Keyword', 'int')
        match('Keyword', 'main')
        match('Left Parenthesis', '(')
        params_node = params()
        match('Right Parenthesis', ')')
        match('Left Curly Brace', '{')
        statements_node = statements()
        return_node = return_statement()
        match('Right Curly Brace', '}')
        return Node('function', [params_node, statements_node, return_node])

    def params():
        children = []
        while current_token and current_token['Value'] != ')':
            children.append(Node('param', leaf=match('Keyword', 'int')['Value']))
            children.append(Node('identifier', leaf=match('Identifier')['Value']))
            if current_token and current_token['Value'] == ',':
                match('Symbol', ',')
        return Node('params', children)

    def statements():
        children = []
        while current_token and current_token['Value'] not in ('return', '}'):
            if current_token['Value'] == 'if':
                children.append(if_statement())
            elif current_token['Type'] == 'Keyword' and current_token['Value'] == 'int':
                children.append(declaration())
            else:
                children.append(assignment())
        return Node('statements', children)

    def declaration():
        children = []
        children.append(Node('type', leaf=match('Keyword', 'int')['Value']))
        children.append(Node('identifier', leaf=match('Identifier')['Value']))
        match('Symbol', ';')
        return Node('declaration', children)

    def if_statement():
        children = []
        children.append(Node('if', leaf=match('Keyword', 'if')['Value']))
        match('Left Parenthesis', '(')
        children.append(condition())
        match('Right Parenthesis', ')')
        match('Left Curly Brace', '{')
        children.append(statements())
        match('Right Curly Brace', '}')
        return Node('if_statement', children)

    def condition():
        children = []
        children.append(Node('identifier', leaf=match('Identifier')['Value']))
        children.append(Node('operator', leaf=match('Logical Operator')['Value']))
        children.append(Node('identifier', leaf=match('Identifier')['Value']))
        return Node('condition', children)

    def assignment():
        children = []
        children.append(Node('identifier', leaf=match('Identifier')['Value']))
        children.append(Node('operator', leaf=match('Assignment Operator')['Value']))
        children.append(expression())
        match('Symbol', ';')
        return Node('assignment', children)

    def expression():
        node = term()
        while current_token and current_token['Type'] == 'Arithmetic Operator' and current_token['Value'] in ('+', '-'):
            op = Node('operator', leaf=match('Arithmetic Operator')['Value'])
            node = Node('expression', [node, op, term()])
        return node

    def term():
        node = factor()
        while current_token and current_token['Type'] == 'Arithmetic Operator' and current_token['Value'] in ('*', '/'):
            op = Node('operator', leaf=match('Arithmetic Operator')['Value'])
            node = Node('term', [node, op, factor()])
        return node

    def factor():
        if current_token['Type'] == 'Integer':
            return Node('integer', leaf=match('Integer')['Value'])
        elif current_token['Type'] == 'Identifier':
            return Node('identifier', leaf=match('Identifier')['Value'])
        elif current_token['Value'] == '(':
            match('Left Parenthesis', '(')
            node = expression()
            match('Right Parenthesis', ')')
            return node
        else:
            error(f"Unexpected token: {current_token['Type']} with value {current_token['Value']}")

    def return_statement():
        children = []
        children.append(Node('return', leaf=match('Keyword', 'return')['Value']))
        children.append(expression())
        match('Symbol', ';')
        return Node('return_statement', children)

    return program()

def print_tree(node, level=0):
    print('  ' * level + node.type, end='')
    if node.leaf is not None:
        print(' (' + node.leaf + ')')
    else:
        print()
    for child in node.children:
        print_tree(child, level + 1)

class TACInstruction:
    def __init__(self, operation, arg1=None, arg2=None, result=None):
        self.operation = operation
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        if self.arg2 is not None:
            return f"{self.result} = {self.arg1} {self.operation} {self.arg2}"
        elif self.arg1 is not None:
            return f"{self.result} = {self.operation} {self.arg1}"
        else:
            return f"{self.operation} {self.result}"

class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0

    def new_temp(self):
        temp_name = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_name

    def generate(self, node):
        if node.type == 'program':
            for child in node.children:
                self.generate(child)
        elif node.type == 'function':
            for child in node.children:
                self.generate(child)
        elif node.type == 'statements':
            for child in node.children:
                self.generate(child)
        elif node.type == 'declaration':
            # Declarations don't generate TAC directly
            pass
        elif node.type == 'if_statement':
            cond_result = self.generate(node.children[1])
            true_label = self.new_temp()
            end_label = self.new_temp()
            self.instructions.append(TACInstruction('IF', cond_result, 'GOTO', true_label))
            self.instructions.append(TACInstruction('GOTO', None, None, end_label))
            self.instructions.append(TACInstruction('LABEL', None, None, true_label))
            for stmt in node.children[2].children:
                self.generate(stmt)
            self.instructions.append(TACInstruction('LABEL', None, None, end_label))
        elif node.type == 'condition':
            left = self.generate(node.children[0])
            op = node.children[1].leaf
            right = self.generate(node.children[2])
            result = self.new_temp()
            self.instructions.append(TACInstruction(op, left, right, result))
            return result
        elif node.type == 'assignment':
            expr_result = self.generate(node.children[2])
            self.instructions.append(TACInstruction('=', expr_result, None, node.children[0].leaf))
        elif node.type == 'expression' or node.type == 'term':
            return self.generate_expression(node)
        elif node.type == 'return_statement':
            expr_result = self.generate(node.children[1])
            self.instructions.append(TACInstruction('RETURN', expr_result))
        elif node.type == 'identifier':
            return node.leaf
        elif node.type == 'integer':
            return node.leaf
        elif node.type == 'param':
            return node.leaf
        elif node.type == 'if':
            return node.leaf

    def generate_expression(self, node):
        if len(node.children) == 3:
            left = self.generate(node.children[0])
            op = node.children[1].leaf
            right = self.generate(node.children[2])
            result = self.new_temp()
            self.instructions.append(TACInstruction(op, left, right, result))
            return result
        else:
            return self.generate(node.children[0])

def print_TAC(instructions):
    for instr in instructions:
        print(instr)

with open('tokens.json', 'r') as f:
    tokens = json.load(f)

parse_tree = parse(tokens)
print_tree(parse_tree)

tac_generator = TACGenerator()
tac_generator.generate(parse_tree)
print("\nThree-address Code (TAC):")
print_TAC(tac_generator.instructions)
