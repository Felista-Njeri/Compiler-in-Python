# Compiler-in-Python
Lexer, Parser and intermediate code generation in Python 

lexer.py - Lexer/Scanner to tokenize the input string into different 
            token types such as keywords, identifiers, numbers etc. 

python_parser_icg.py - Parser implemented using the recursive descent parsing approach.
                        Tokens generated from the lexer are stored in token.json file.
                        The parser reads the json file and generates a parse tree.
                        Intermediate code generation generates Three address code from the parse tree output.

parser_icg_expressions.py - works for expressions only such as 6 * 4 - 7 
                         run the lexer to generate tokens then run parser_icg_expressions.py to generate parse tree
                         and Three address code

input_program.txt - contains the sample program

tokens.json - stores the output of the lexer.

grammar.txt - specifies the grammar