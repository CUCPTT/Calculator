from math import cos, sin,log, sqrt, tan
from lexicalAnalyse import lexer

def infix_to_postfix(tokens):
    output = []
    stack = []
    priority_table = {'+': 1, '-': 1, '*': 2, '/': 2,"%":2,"//":2, '**': 3, '|':4,'^':4,'&':4,'<<':4,'>>':4,"~":4}
    def get_priority(operator):
        return priority_table.get(operator, 0)

    for token in tokens:
        token_type, _, token_value = token

        if token_type == 'number':
            output.append(token_value)
        elif token_type == 'left':
            if token_value.endswith('('):  # 判断是否以 '(' 结尾，以确定是函数调用
                stack.append(('left', 'function', token_value))  # 将函数调用的左括号入栈
            else:
                stack.append(token)  # 普通左括号入栈
        elif token_type == 'right':
            while stack and stack[-1][0] != 'left':
                output.append(stack.pop()[2])
            if stack:
                left_type, left_subtype, left_value = stack.pop()
                if left_subtype == 'function':
                    # 如果是函数调用的右括号，将函数调用的左括号也加入后缀表达式
                    output.append(left_value)
            # 注意：这里不再直接使用 stack.pop()，因为上面已经可能执行过一次 pop 了
        elif token_type == 'operator':
            while stack and get_priority(stack[-1][2]) >= get_priority(token_value):
                output.append(stack.pop()[2])
            stack.append(token)

    while stack:
        output.append(stack.pop()[2])

    return output

# if __name__ == '__main__':
#     input_str = 'sin(1<<2 + 3**4)'
#     tokens = lexer(input_str)
#     postfix_expr = infix_to_postfix(tokens)
#     print(postfix_expr)

def evaluate_postfix(postfix_expr):
    stack = []

    for token in postfix_expr:
        if token.isdigit():
            stack.append(float(token))
        elif token in {'+', '-', '*', '/', '%', '//', '**', '|', '^', '&', '<<', '>>'}:
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = perform_operation1(operand1, operand2, token)
            stack.append(result)
        elif token.startswith(('sin(', 'cos(', 'ln(', 'sqrt(','tan(')):
            operand = stack.pop()
            result = perform_function(token, operand)
            stack.append(result)
        elif token in {'~'}:
            operand = stack.pop()
            result = perform_operation2(operand)
            stack.append(result)

    return stack[0] if stack else None

def perform_operation1(operand1, operand2, operator):
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        return operand1 / operand2
    elif operator == '%':
        return operand1 % operand2
    elif operator == '//':
        return operand1 // operand2
    elif operator == '**':
        return operand1 ** operand2
    elif operator == '|':
        return int(operand1) | int(operand2)
    elif operator == '^':
        return int(operand1) ^ int(operand2)
    elif operator == '&':
        return int(operand1) & int(operand2)
    elif operator == '<<':
        return int(operand1) << int(operand2)
    elif operator == '>>':
        return int(operand1) >> int(operand2)

def perform_operation2(operand1):
    return ~int(operand1)

def perform_function(func, operand):
    if func == 'sin(':
        return sin(operand)
    elif func == 'cos(':
        return cos(operand)
    elif func == 'ln(':
        return log(operand)
    elif func == 'sqrt(':
        return sqrt(operand)
    elif func == 'tan(':
        return tan(operand)

def RPN(tokens):
    RPN = infix_to_postfix(tokens)
    result = evaluate_postfix(RPN)
    return RPN, result

# if __name__ == '__main__':
#     input_str = '~1'
#     tokens = lexer(input_str)

#     postfix_expr = infix_to_postfix(tokens)
#     print(f"Postfix Expression: {postfix_expr}")

#     result = evaluate_postfix(postfix_expr)
#     print(f"Result: {result}")

# sin(1<<2 + 3**4)
# sin(3)**2 + cos(3)**2
# 3 + 4 * 2 / (1 - 5)
