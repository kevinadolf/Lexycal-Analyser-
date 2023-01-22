# -*- coding: utf-8 -*-

import re # importando regular expressions 

class Buffer():
    def load_buffer():
        file = open('program.c', 'r') # programa em C
        code = file.readline() # pedaço de codigo

        buffer = []
        counter = 1

        # o tamanho do buffer pode ser modificado ao mudar o tamanho do contador
        while code != "": # enqnt nao for EOF, append pro vetor buffer
            buffer.append(code) #
            code = file.readline() # lendo proximo pedaço de codigo 
            counter += 1 # e conforme for lendo, aumenta-se o contador

            if counter == 10 or code == '':
                # Return a full buffer
                buffer = ''.join(buffer)
                counter = 1
                yield buffer

                # resetando o buffer
                buffer = []

        file.close()

#--------------------------------
class LexicalAnalyzer():
    def tokenize(self, code):
        rules = [ 
            ('MAIN', r'main'),          # main
            ('INT', r'int'),            # int inteiro
            ('IF', r'if'),              # if
            ('ELSE', r'else'),          # else
            ('WHILE', r'while'),        # while
            ('PRINT', r'print'),        # print
            ('LBRACKET', r'\('),        # (
            ('RBRACKET', r'\)'),        # )
            ('LBRACE', r'\{'),          # {
            ('RBRACE', r'\}'),          # }
            ('COMMA', r','),            # ,
            ('PCOMMA', r';'),           # ;
            ('EQ', r'=='),              # ==
            ('NE', r'!='),              # !=
            ('LE', r'<='),              # <=
            ('GE', r'>='),              # >=
            ('OR', r'\|\|'),            # ||
            ('AND', r'&&'),             # &&
            ('ATTR', r'\='),            # =
            ('LT', r'<'),               # <
            ('GT', r'>'),               # >
            ('PLUS', r'\+'),            # +
            ('MINUS', r'-'),            # -
            ('MULT', r'\*'),            # *
            ('DIV', r'\/'),             # /
            ('ID', r'[a-zA-Z]\w*'),     # IDENTIFIERS
            ('INTEGER_CONST', r'\d(\d)*'),          # int constante inteira
            ('MISMATCH', r'.'),         # outro caracter
        ]

        tokens_join = '|'.join('(?P<%s, %s>)' % x for x in rules)
        lin_start = 0 #começando pela linha zero

        # listas de cada uma das saidas
        token = []
        lexeme = []
        row = []
        column = []

        # It analyzes the code to find the lexemes and their respective Tokens
        for m in re.finditer(tokens_join, code):
            tipo_token = m.lastgroup
            lexema_token = m.group(tipo_token)

            if tipo_token == 'NEWLINE':
                lin_start = m.end()
                self.lin_num += 1
            elif tipo_token == 'SKIP':
                continue
            elif tipo_token == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (lexema_token, self.lin_num))
            else:
                    col = m.start() - lin_start
                    column.append(col)
                    token.append(tipo_token)
                    lexeme.append(lexema_token)
                    row.append(self.lin_num)
                    # To print information about a Token
                    print('Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'.format(tipo_token, lexema_token, self.lin_num, col))

        return token, lexeme, row, column

lin_num = 1
if __name__ == '__main__':
    Buffer = Buffer()
    Analyzer = LexicalAnalyzer()

    # Lists for every list returned list from the function tokenize
    token = []
    lexeme = []
    row = []
    column = []

    # Tokenize and reload of the buffer
    for i in Buffer.load_buffer():
        t, lex, lin, col = Analyzer.tokenize(i)
        token += t
        lexeme += lex
        row += lin
        column += col

    print('\nRecognize Tokens: ', token)