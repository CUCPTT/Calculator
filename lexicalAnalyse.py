import re

valid_words = [
    'sin(', 'cos(', 'tan(', 'ln(', 'sqrt(',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '.', '(', ')', '+', '-', '*', '/', '%', '&', '|', '^', '~', '<', '>',
    '**','<<','>>'
]

def split_string(expression):
    # 使用正则表达式进行匹配，按照规则分割字符串
    pattern = r'(sin\(|cos\(|tan\(|ln\(|sqrt\(|\*\*|<<|>>|.)'
    # 找到所有匹配的子串
    substrings = re.findall(pattern, expression)
    # 过滤空字符串
    substrings = [substr for substr in substrings if substr.strip()]
    return substrings

def is_illegal_char(char):
    if char in valid_words:
        return False
    else:
        return True

def lexer(input_string):
    input_string = input_string.replace(' ', '')
    result = split_string(input_string)

    illegal_chars = []
    for char in result:
        if is_illegal_char(char):
            illegal_chars.append(char)

    if illegal_chars:
        print("Error: Invalid character(s): {}".format(illegal_chars))
        return False

    tokens = []

    operators = {'+': 'arithmetic', '-': 'arithmetic', '*': 'arithmetic', '/': 'arithmetic', '%': 'arithmetic', '**': 'arithmetic', '//': 'arithmetic',
                 '&': 'logical', '|': 'logical', '~': 'logical', '^': 'logical', '<<': 'logical', '>>': 'logical'}

    # 正则表达式模式
    number_pattern = r'(-?\d+(\.\d+)?)'  # 修改正则表达式以允许负号作为数字的一部分
    operator_pattern = r'(\*\*|//|<<|>>|[+\-*/%&|^~]|(?<!\d)-)'
    function_pattern = r'(sin\(|cos\(|tan\(|ln\(|sqrt\()'
    left_paren_pattern = r'(\()'
    right_paren_pattern = r'(\))'
    space_pattern = r'\s+'

    # 组合正则表达式模式
    combined_pattern = re.compile('|'.join([number_pattern, operator_pattern, function_pattern, left_paren_pattern, right_paren_pattern, space_pattern]))
    matches = combined_pattern.findall(input_string)

    for match in matches:

        token_type = ''

        if match[0]:  # 匹配到数字
            if '.' in match[0]:
                token_type = 'float'
            else:
                token_type = 'integer'
            tokens.append(('number', token_type, match[0]))

        elif match[2]:  # 匹配到运算符
            token_type = operators.get(match[2])
            tokens.append(('operator', token_type, match[2]))

        elif match[3]:  # 匹配到函数
            token_type = 'function'
            tokens.append(('left', token_type, match[3]))

        elif match[4]:  # 匹配到左括号
            token_type = ''
            tokens.append(('left', token_type, match[4]))

        elif match[5]:  # 匹配到右括号
            token_type = ''
            tokens.append(('right', token_type, match[5]))

    # 修正负数的表示
    corrected_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i][0] == 'number' and tokens[i][2][0] == '-' and i + 1 < len(tokens) and tokens[i + 1][0] == 'number':
            corrected_tokens.append(('number', tokens[i][1], tokens[i][2]))
            corrected_tokens.append(('operator', 'arithmetic', '-'))
            corrected_tokens.append(('number', tokens[i + 1][1], tokens[i + 1][2]))
            i += 2
        else:
            corrected_tokens.append(tokens[i])
            i += 1

    print(corrected_tokens)
    return corrected_tokens

if __name__ == '__main__':
    #input_str = '-63.54 - 9'
    input_str = 'sin((1<<2) + -3.3**4)'
    result = lexer(input_str)
