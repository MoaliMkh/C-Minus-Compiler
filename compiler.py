# Mohammad Hossein Haji Seyyed Soleyman / 98105687
# Mohammad Ali Mohammad Khani / 98102251

line_no = 0
first_error = True
comment = False
comment_str = ''
comment_line = -1
start = 0
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
          'w', 'x', 'y', 'z',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
          'W', 'X', 'Y', 'Z']
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']
whitespaces = ['\n', '\r', '\t', '\v', '\f']
keywords = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']


def get_next_token(code):
    global start, comment, comment_line
    end = start
    token_type = -1
    char = code[end]

    if comment:
        token_type = 'COMMENT'
        while True:
            if code[end] == '*':
                end += 1
                if code[end] == '/':
                    end += 1
                    comment = False
                    break
            if code[end] == '\n' or end == len(code):
                break
            end += 1
    else:
        if char in letters:
            token_type = 'ID'
            end += 1
            while code[end] in letters or code[end] in digits:
                end += 1
            if not (code[end] in whitespaces or code[end] in symbols or code[end] == ' '):
                end += 1
                token_type = 'Invalid input'

        elif char in symbols:
            token_type = 'SYMBOL'
            end += 1
            if char == '*':
                if code[end] == '/':
                    end += 1
                    token_type = 'Unmatched comment'
                elif not (code[end] in letters or code[end] in digits or code[end] in whitespaces or code[end] in symbols or code[end] == ' '):
                    end += 1
                    token_type = 'Invalid input'
            elif char == '=':
                if code[end] == '=':
                    end += 1
                elif not (code[end] in letters or code[end] in digits or code[end] in whitespaces
                          or code[end] in symbols or code[end] == ' ' or code[end] == '/'):
                    end += 1
                    token_type = 'Invalid input'

        elif char in digits:
            token_type = 'NUM'
            end += 1
            while code[end] in digits:
                end += 1
            if code[end] in letters:
                end += 1
                token_type = 'Invalid number'
            elif not (code[end] in whitespaces or code[end] in symbols or code[end] == ' '):
                end += 1
                token_type = 'Invalid input'

        elif char in whitespaces:
            token_type = 'WHITESPACE'
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

        elif not (char in letters or char in digits or char in whitespaces or char in symbols):
            end += 1
            token_type = 'Invalid input'

    token_string = code[start: end]

    if token_type == 'ID' and token_string in keywords:
        token_type = 'KEYWORD'

    start += len(token_string)
    if start == len(code):
        start = 0

    return token_type, token_string


def write_tokens(tokens, line_no, tokens_file_content):
    if len(tokens) > 0:
        tokens_file_content += str(line_no) + '.\t'
    for token in tokens:
        tokens_file_content += '(' + token[0] + ', ' + token[1] + ') '
    if len(tokens) > 0:
        tokens_file_content += '\n'
    return tokens_file_content


def create_symbol_table():
    file = open('symbol_table.txt', 'w')
    for x in range(0, 8):
        file.write(str(x + 1) + '.' + '\t' + keywords[x] + '\n')
    file.close()


def write_error(error_token, errors_file_content):
    global first_error
    if first_error:
        if error_token[0] == 'Unclosed comment':
            errors_file_content += str(comment_line) + '.\t(' + str(error_token[1]) + ', ' + str(error_token[0]) + ') \n'
        else:
            errors_file_content += str(line_no) + '.\t(' + str(error_token[1]) + ', ' + str(error_token[0]) + ') \n'
        first_error = False
    else:
        errors_file_content = errors_file_content[: -1] + '(' + str(error_token[1]) + ', ' + str(error_token[0]) + ') \n'
    return errors_file_content


def save_tokens(tokens_file_content):
    file = open('tokens.txt', 'w')
    file.write(tokens_file_content)
    file.close()


def save_errors(errors_file_content):
    file = open('lexical_errors.txt', 'w')
    if len(errors_file_content) > 0:
        file.write(errors_file_content)
    else:
        file.write('There is no lexical error.')
    file.close()


def save_symbol_table(identifiers):
    index = 1
    file = open('symbol_table.txt', 'w')
    for identifier in identifiers:
        file.write(str(index) + '.\t' + identifier + '\n')
        index += 1
    file.close()


tokens_file_content = ''
errors_file_content = ''
identifiers = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
create_symbol_table()
file = open('input.txt', 'r')
content = file.readlines()
file.close()

for line in content:
    start = 0
    first_error = True
    if line[-1] != '\n':
        line += '\n'
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
            errors_file_content = write_error(token, errors_file_content)
    tokens_file_content = write_tokens(tokens, line_no, tokens_file_content)

if comment:
    errors_file_content = write_error(('Unclosed comment', comment_str[0: min(7, len(comment_str))] + '...'), errors_file_content)

save_tokens(tokens_file_content)
save_errors(errors_file_content)
save_symbol_table(identifiers)