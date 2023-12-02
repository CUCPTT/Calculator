import re

# 定义正则表达式模式
patterns = [
    ('NUMBER', r'-?\d+(\.\d+)?'),  # 匹配整数、小数、负数
    ('ARITHMETIC_OP', r'\+|-|\*|/|%|\*\*|//'),  # 算术运算符
    ('LOGICAL_OP', r'&|\||~|\^|<<|>>'),  # 逻辑运算符
    ('FUNCTION', r'sin\(|cos\(|tan\(|ln\(|sqrt\('),  # 函数
    ('OTHER', r'\(|\)|\.|\s'),  # 其他标识符：括号、点、空格
]

# 构建正则表达式模式
regex_patterns = '|'.join('(?P<%s>%s)' % pair for pair in patterns)

# 进行词法分析
def lexer(input_string):
    tokens = []
    for match in re.finditer(regex_patterns, input_string):
        for name, value in match.groupdict().items():
            if value is not None and not (name == 'OTHER' and value == ' '):
                tokens.append((name, value))
                break  # 找到匹配的标记后立即停止

    # 将连续的 '*' 组合为 '**'
    combined_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i][1] == '*' and i + 1 < len(tokens) and tokens[i + 1][1] == '*':
            combined_tokens.append(('ARITHMETIC_OP', '**'))
            i += 2
        else:
            combined_tokens.append(tokens[i])
            i += 1

    # 输出标记序列（忽略空格）
    output_tokens = [token[1] for token in combined_tokens if token[0] != 'OTHER' or token[1] != ' ']

    return output_tokens

if __name__ == '__main__':

    # 示例输入
    input_string = "sin((1<<2) + 3**4)"

    # 执行词法分析
    tokens = lexer(input_string)
    print(tokens)
