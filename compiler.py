# Mohammad Hossein Haji Seyyed Soleyman / 98105687
# Mohammad Ali Mohammad Khani / 98102251
import re

start = 0
id_no = 9
letter = '[A-Za-z]'
digit = '[0-9]'
symbol = [';', ':', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']
whitespace = '[\n\r\t\v\f]'
keyword = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']


def get_next_token(code):
    global start
    end = start
    token_type = -1
    char = code[end]
    if re.match(letter, char):
        token_type = 'ID'
        end += 1
        while re.match(letter or digit, code[end]):
            end += 1
    elif char in symbol:
        token_type = 'SYMBOL'
        end += 1
        if code[end] == '=' and code[end] == code[end + 1]:
            end += 1
    elif re.match(digit, char):
        token_type = 'NUM'
        end += 1
        while re.match(digit, code[end]):
            end += 1
    elif re.match(whitespace, char):
        end += 1
        while re.match(whitespace, code[end]):
            end += 1
    elif char == '/':
        token_type = 'COMMENT'
        end += 1
        if code[end] == '/':
            end += 1
            while code[end] != '\n':
                end += 1
        elif code[end] == '*':
            end += 1
    else:
        end += 1
        start += 1
        return None

    token_string = code[start: end]

    if token_type == 'ID' and token_string in keyword:
        token_type = 'KEYWORD'

    start += len(token_string)
    if start == len(code):
        start = 0

    return token_type, token_string


def write_tokens_in_file(tokens, line_no):
    file = open('tokens.txt', 'a')
    if len(tokens) > 0:
        file.write(str(line_no) + '.\t')
    for token in tokens:
        file.write('(' + token[0] + ', ' + token[1] + ') ')
    if len(tokens) > 0:
        file.write('\n')
    file.close()


def create_symbol_table():
    file = open('symbol_table.txt', 'w')
    file.write('1.	if\n2.	else\n3.	void\n4.	int\n5.	repeat\n6.	break\n7.	until\n8.	return')
    file.close()


def add_to_symbol_table(identifier):
    pass


# else:
#     file = open


line_no = 0
create_symbol_table()
with open('input.txt') as file:
    for line in file:
        start = 0
        line_no += 1
        tokens = []
        while start != len(line) - 1:
            token = get_next_token(line)
            if (token is not None) and not (token[0] == 'COMMENT' or token[0] == 'WHITESPACE'):
                tokens.append(token)
                if token[0] == 'ID':
                    add_to_symbol_table(token[1])
        write_tokens_in_file(tokens, line_no)
