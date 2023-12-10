import re

def lexer(input_string):

    input_string = input_string.replace(' ','')

    legal_chars = ['0','1','2','3','4','5','6','7','8','9','.','(',')','+','-','*','/','%','&','|','^','~','<','>','s','i','n','c','o','t','a','l','q','r']
    illegal_chars = []
    for char in input_string:
        if char not in legal_chars:
            illegal_chars.append(char)

    if illegal_chars:
        print("Error: Invalid character(s): {}".format(illegal_chars))
        return False
    
    tokens = []

    operators = {'+': 'arithmetic', '-': 'arithmetic', '*': 'arithmetic', '/': 'arithmetic', '%': 'arithmetic', '**': 'arithmetic', '//': 'arithmetic',
                 '&': 'logical', '|': 'logical', '~': 'logical', '^': 'logical', '<<': 'logical', '>>': 'logical'}
        
    # Regular expressions for matching patterns
    number_pattern = r'(\d+(\.\d+)?)'
    operator_pattern = r'(\*\*|//|<<|>>|[+\-*/%&|^~]|(?<!\d)-)'
    function_pattern = r'(sin\(|cos\(|tan\(|ln\(|sqrt\()'
    left_paren_pattern = r'(\()'
    right_paren_pattern = r'(\))'
    space_pattern = r'\s+'

    # Combined regular expression pattern
    combined_pattern = re.compile('|'.join([number_pattern, operator_pattern, function_pattern, left_paren_pattern, right_paren_pattern, space_pattern]))
    matches = combined_pattern.findall(input_string)
    
    for match in matches:

        token_type = ''

        if match[0]:  # Matched a number
            if '.' in match[0]:
                token_type = 'float'
            elif match[0].isdigit():
                token_type = 'integer'
            else:
                token_type = 'unsigned'
            tokens.append(('number',token_type,match[0]))

        elif match[2]:  # Matched an operator
            token_type = operators.get(match[2])
            tokens.append(('operator',token_type,match[2]))            

        elif match[3]:  # Matched a function
            token_type = 'function'
            tokens.append(('left',token_type,match[3]))  

        elif match[4]:  # Matched a left parenthesis
            token_type = ''
            tokens.append(('left',token_type,match[4]))  

        elif match[5]:  # Matched a right parenthesis
            token_type = ''
            tokens.append(('right',token_type,match[5]))  

    print(tokens)
    
    return tokens

#if __name__ == '__main__':
#    input_str = 'sin((1<<2) + -3**4)'
#    result = lexer(input_str)
