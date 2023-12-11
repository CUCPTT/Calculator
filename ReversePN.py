from math import cos, sin, log, sqrt, tan, pi

from lexicalAnalyse import lexer

def infix_to_postfix(tokens):
    output = []
    stack = []
    priority_table = {'+': 1, '-': 1, '*': 2, '/': 2, "%": 2, "//": 2, '**': 3, '|': 4, '^': 4, '&': 4, '<<': 4,
                      '>>': 4, "~": 4}
    def get_priority(operator):
        return priority_table.get(operator, 0)

    for token in tokens:
        token_type, _, token_value = token

        if token_type == 'number':
            output.append(token_value)
        elif token_type == 'left':
            if token_value.endswith('('):  # Check if it's a function call
                stack.append(('left', 'function', token_value))
            else:
                stack.append(token)
        elif token_type == 'right':
            while stack and stack[-1][0] != 'left':
                output.append(stack.pop()[2])
            if stack:
                left_type, left_subtype, left_value = stack.pop()
                if left_subtype == 'function':
                    output.append(left_value)
        elif token_type == 'operator':
            while stack and get_priority(stack[-1][2]) >= get_priority(token_value):
                output.append(stack.pop()[2])
            stack.append(token)

    while stack:
        output.append(stack.pop()[2])

    return output

def evaluate_postfix(postfix_expr):
    stack = []

    for token in postfix_expr:
        try:
            if token.lstrip('-').replace('.', '', 1).isdigit():
                # 修改此处以支持一元负号的情况
                stack.append(float(token))
            elif token in {'+', '-', '*', '/', '%', '//', '**', '|', '^', '&', '<<', '>>'}:
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = perform_operation1(operand1, operand2, token)
                stack.append(result)
            elif token.startswith(('sin(', 'cos(', 'ln(', 'sqrt(', 'tan(')):
                operand = stack.pop()
                result = perform_function(token, operand)
                stack.append(result)
            elif token in {'~'}:
                operand = stack.pop()
                result = perform_operation2(operand)
                stack.append(result)
        except (ValueError, ZeroDivisionError, ArithmeticError) as e:
            return f"Error: {e}"

    return stack[0] if stack else None


def perform_operation1(operand1, operand2, operator):
    try:
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise ZeroDivisionError("Division by zero")
            return operand1 / operand2
        elif operator == '%':
            return operand1 % operand2
        elif operator == '//':
            if operand2 == 0:
                raise ZeroDivisionError("Floor division by zero")
            return int(operand1 // operand2)
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
    except (ValueError, ZeroDivisionError, ArithmeticError) as e:
        raise ArithmeticError(f"Error in {operator} operation: {e}")

def perform_operation2(operand1):
    try:
        return ~int(operand1)
    except ValueError as e:
        raise ArithmeticError(f"Error in ~ operation: {e}")

def perform_function(func, operand):
    try:
        if func == 'sin(':
            return sin(operand)
        elif func == 'cos(':
            return cos(operand)
        elif func == 'ln(':
            if operand <= 0:
                raise ValueError("Logarithm of non-positive number")
            return log(operand)
        elif func == 'sqrt(':
            if operand < 0:
                raise ValueError("Square root of negative number")
            return sqrt(operand)
        elif func == 'tan(':
            if abs(operand % (2 * pi)) == pi / 2:
                raise ValueError("Tangent of pi/2 is undefined")
            return tan(operand)
    except (ValueError, ZeroDivisionError, ArithmeticError) as e:
        raise ArithmeticError(f"Error in {func} function: {e}")

if __name__ == '__main__':
    input_str = '-1+3'
    tokens = lexer(input_str)

    postfix_expr = infix_to_postfix(tokens)
    print(f"Postfix Expression: {postfix_expr}")

    result = evaluate_postfix(postfix_expr)
    print(f"Result: {result}")
