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
        if code[end] == '=' and code[end] == code[end - 1]:
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
            while True:
                if code[end] == '*':
                    end += 1
                    if code[end] == '/':
                        break
                elif code[end] == '\n':
                    break
                else:
                    end += 1
    elif char == ' ':
        end += 1
        token_type = 'Space'
    elif not (re.match(letter or digit or whitespace, char) or char in symbol):
        end += 1
        token_type = 'Invalid Input'

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
    file.write('1.\tif\n2.\telse\n3.\tvoid\n4.\tint\n5.\trepeat\n6.\tbreak\n7.\tuntil\n8.\treturn')
    file.close()


def add_to_symbol_table(identifier):
    file = open('symbol_table.txt', 'a')
    line_number = 0
    for line in file:
        line_number += 1
        if identifier in line:
            pass
        else:
            file.write(str(line_number + 1) + "." + "\t" + identifier + "\n")


# else:
#     file = open

def write_error(invalid_char):
    file = open('lexical_errors.txt', 'a')
    file.write(str(line_no) + '.\t(' + invalid_char + ', Invalid Input)\n')


line_no = 0
create_symbol_table()
with open('input.txt') as file:
    for line in file:
        start = 0
        line_no += 1
        tokens = []
        while start != len(line) - 1:
            token = get_next_token(line)
            if token[0] == 'Invalid Input':
                write_error(token[1])
            elif not (token[0] == 'COMMENT' or token[0] == 'WHITESPACE' or token[0] == 'Space'):
                tokens.append(token)
                if token[0] == 'ID':
                    add_to_symbol_table(token[1])

        write_tokens_in_file(tokens, line_no)
