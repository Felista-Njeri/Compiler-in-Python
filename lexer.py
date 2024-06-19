import json
import re

# Token types
TOKEN_INT = "Integer"
TOKEN_FLOAT = "Float"
TOKEN_IDENTIFIER = "Identifier"
TOKEN_ASSIGNMENT_OPERATOR = "Assignment Operator"
TOKEN_ARITHMETIC_OPERATOR = "Arithmetic Operator"
TOKEN_LOGICAL_OPERATOR = "Logical Operator"
TOKEN_KEYWORD = "Keyword"
TOKEN_STRING = "String"
TOKEN_LEFT_PAREN = "Left Parenthesis"
TOKEN_RIGHT_PAREN = "Right Parenthesis"
TOKEN_LEFT_CURLYBRACE = "Left Curly Brace"
TOKEN_RIGHT_CURLYBRACE = "Right Curly Brace"
TOKEN_SYMBOL = "Symbol"
TOKEN_UNKNOWN = "Unknown"
TOKEN_EOF = "EOF"

# Keywords list
keywords = {"if", "else", "while", "for", "int", "char", "float", "main", "return", "printf", "void"}

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def to_dict(self):
        return {"Type": self.type, "Value": self.value}

# Function to check if a character is an operator
def is_operator(c):
    return c in "+-*/="

# Function to check if a string is a keyword
def is_keyword(s):
    return s in keywords

# Function to tokenize input string
def tokenize(input):
    tokens = []
    i = 0
    while i < len(input):
        if input[i].isspace():
            i += 1
            continue
        if input[i].isdigit():
            start = i
            while i < len(input) and (input[i].isdigit() or input[i] == '.'):
                i += 1
            value = input[start:i]
            type = TOKEN_INT if '.' not in value else TOKEN_FLOAT
            tokens.append(Token(type, value))
            continue
        if input[i] == '"':
            start = i
            i += 1
            while i < len(input) and input[i] != '"':
                i += 1
            if i < len(input):
                i += 1
            value = input[start:i]
            tokens.append(Token(TOKEN_STRING, value))
            continue
        if input[i].isalpha() or input[i] == '_':
            start = i
            while i < len(input) and (input[i].isalnum() or input[i] == '_'):
                i += 1
            value = input[start:i]
            type = TOKEN_KEYWORD if is_keyword(value) else TOKEN_IDENTIFIER
            tokens.append(Token(type, value))
            continue
        if is_operator(input[i]):
            if input[i] == '=' and i + 1 < len(input) and input[i + 1] == '=':
                tokens.append(Token(TOKEN_LOGICAL_OPERATOR, "=="))
                i += 2
            else:
                tokens.append(Token(TOKEN_ASSIGNMENT_OPERATOR if input[i] == '=' else TOKEN_ARITHMETIC_OPERATOR, input[i]))
                i += 1
            continue
        if input[i] == '(':
            tokens.append(Token(TOKEN_LEFT_PAREN, input[i]))
            i += 1
            continue
        if input[i] == ')':
            tokens.append(Token(TOKEN_RIGHT_PAREN, input[i]))
            i += 1
            continue
        if input[i] == '{':
            tokens.append(Token(TOKEN_LEFT_CURLYBRACE, input[i]))
            i += 1
            continue
        if input[i] == '}':
            tokens.append(Token(TOKEN_RIGHT_CURLYBRACE, input[i]))
            i += 1
            continue
        if input[i] in '<>':
            tokens.append(Token(TOKEN_LOGICAL_OPERATOR, input[i]))
            i += 1
            continue
        tokens.append(Token(TOKEN_SYMBOL, input[i]))
        i += 1
    tokens.append(Token(TOKEN_EOF, "EOF"))
    return tokens

# Function to print tokens
def print_tokens(tokens):
    for token in tokens:
        print(f"Type: {token.type}, Value: {token.value}")

# Function to write tokens to JSON file
def write_tokens_to_json(tokens, filename):
    tokens_dict_list = [token.to_dict() for token in tokens]
    with open(filename, 'w') as json_file:
        json.dump(tokens_dict_list, json_file, indent=4)

def main():
    # Read input from file
    with open("input_program.txt", "r") as file:
        input = file.read()

    # Tokenize input
    tokens = tokenize(input)

    # Print tokens
    print_tokens(tokens)

    # Write tokens to JSON file
    write_tokens_to_json(tokens, "tokens.json")

if __name__ == "__main__":
    main()
