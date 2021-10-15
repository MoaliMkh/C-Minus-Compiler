# Mohammad Hossein Haji Seyyed Soleyman / 98105687
# Mohammad Ali Mohammad Khani / 98102251
import re

line_no = 0
comment = False
comment_str = ''
comment_line = -1
start = 0
letter = '[A-Za-z]'
digit = '[0-9]'
symbol = [';', ':', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']
whitespace = '[\n\r\t\v\f]'
keyword = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
tokens_file_content = ''
errors_file_content = ''


def get_next_token(code):
    global start, comment, comment_line
    end = start
    token_type = -1
    char = code[end]
    if comment:
        token_type = 'COMMENT'
        while True:
            if char == '*':
                end += 1
                if code[end] == '/':
                    comment = False
                    break
            if code[end] == '\n' or end == len(code):
                break
    if re.match(letter, char):
        token_type = 'ID'
        end += 1
        while re.match(letter or digit, code[end]):
            end += 1
        if not (re.match(whitespace, code[end]) or code[end] in symbol or code[end] == ' '):
            end += 1
            token_type = 'Invalid input'
    elif char in symbol:
        token_type = 'SYMBOL'
        end += 1
        if code[end] == '=' and code[end] == code[end - 1]:
            end += 1
        elif char == '*' and code[end] == '/':
            end += 1
            token_type = 'Unmatched comment'
    elif re.match(digit, char):
        token_type = 'NUM'
        end += 1
        while re.match(digit, code[end]):
            end += 1
        if re.match(letter, code[end]):
            end += 1
            token_type = 'Invalid number'
        elif not (re.match(whitespace, code[end]) or code[end] in symbol or code[end] == ' '):
            end += 1
            token_type = 'Invalid input'
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
                        end += 1
                        break
                elif code[end] == '\n':
                    comment = True
                    comment_line = line_no
                    break
                else:
                    end += 1
        else:
            token_type = 'Invalid input'
    elif char == ' ':
        end += 1
        token_type = 'Space'
    elif not (re.match(letter or digit or whitespace, char) or char in symbol):
        end += 1
        token_type = 'Invalid input'

    token_string = code[start: end]

    if token_type == 'ID' and token_string in keyword:
        token_type = 'KEYWORD'

    start += len(token_string)
    if start == len(code):
        start = 0

    return token_type, token_string


def write_tokens(tokens, line_no):
    global tokens_file_content
    if len(tokens) > 0:
        tokens_file_content += str(line_no) + '.\t'
    for token in tokens:
        tokens_file_content += '(' + token[0] + ', ' + token[1] + ') '
    if len(tokens) > 0:
        tokens_file_content += '\n'


def create_symbol_table():
    file = open('symbol_table.txt', 'w')
    for x in range(0, 8):
        file.write(str(x + 1) + '.' + '\t' + keyword[x] + '\n')

    file.close()


def write_error(error_token):
    global errors_file_content
    if error_token[0] == 'Unclosed comment':
        errors_file_content += str(comment_line) + '.\t(' + error_token[1] + ', ' + error_token[0] + ')\n'
    else:
        errors_file_content += str(line_no) + '.\t(' + error_token[1] + ', ' + error_token[0] + ')\n'


def save_tokens():
    file = open('tokens.txt', 'w')
    file.write(tokens_file_content)
    file.close()


def save_errors():
    file = open('lexical_errors.txt', 'w')
    file.write(errors_file_content)
    file.close()


def save_symbol_table(identifiers):
    index = 1
    file = open('symbol_table.txt', 'w')
    for identifier in identifiers:
        file.write(str(index) + '.\t' + identifier + '\n')
        index += 1
    file.close()


identifiers = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
create_symbol_table()
file = open('input.txt', 'r')
for line in file:
    start = 0
    line_no += 1
    tokens = []
    while start != len(line) - 1:
        token = get_next_token(line)
        if token[0] == 'ID' or token[0] == 'KEYWORD' or token[0] == 'NUM' or token[0] == 'SYMBOL':
            tokens.append(token)
            if token[0] == 'ID' and not token[1] in identifiers:
                identifiers.append(token[1])
        elif token[0] == 'COMMENT' and comment:
            comment_str += token[1]
        elif not (token[0] == 'COMMENT' or token[0] == 'WHITESPACE' or token[0] == 'Space'):
            write_error(token)
    write_tokens(tokens, line_no)
file.close()

if comment:
    write_error(('Unclosed comment', comment_str[0: min(7, len(comment_str) - 1)] + '...'))

save_tokens()
save_errors()
save_symbol_table(identifiers)
