class NumStorage:
    def __init__(self):
        self.number = [0] * 100
        self.top = -1

class SymbolStorage:
    def __init__(self):
        self.symbol = [''] * 100
        self.top = -1

def init_operate_num(stack_num):
    stack_num.top = -1

def init_operate_symbol(stack_symbol):
    stack_symbol.top = -1

def in_num_storage(stack_num, num):
    stack_num.top += 1
    stack_num.number[stack_num.top] = num

def in_symbol_storage(stack_symbol, ch):
    stack_symbol.top += 1
    stack_symbol.symbol[stack_symbol.top] = ch

def read_num_storage(stack_num):
    return stack_num.number[stack_num.top]

def read_symbol_storage(stack_symbol):
    return stack_symbol.symbol[stack_symbol.top]

def get_num_data(stack_num):
    num = stack_num.number[stack_num.top]
    stack_num.top -= 1
    return num

def get_symbol(stack_symbol):
    symbol = stack_symbol.symbol[stack_symbol.top]
    stack_symbol.top -= 1
    return symbol

def judge_symbol_priority(ch):
    if ch == '(':
        return 1
    elif ch == '+' or ch == '-':
        return 2
    elif ch == '*' or ch == '/':
        return 3
    elif ch == ')':
        return 4

def math(v1, v2, c):
    if c == '+':
        return v1 + v2
    elif c == '-':
        return v1 - v2
    elif c == '*':
        return v1 * v2
    elif c == '/':
        return v1 / v2

def main():
    print("Enter the expression (no blank, no decimals): ")
    data = NumStorage()
    symbol = SymbolStorage()
    init_operate_num(data)
    init_operate_symbol(symbol)
    i = t = sum_val = 0
    v1 = v2 = 0
    c = ''
    i = t = sum_val = 0
    v = [''] * 100
    user_input = input()
    for i in range(len(user_input)):
        if i == 0 and user_input[i] == '-':
            v[t] = user_input[i]
            t += 1
        elif user_input[i] == '(' and i + 1 < len(user_input) and user_input[i + 1] == '-':
            i += 1
            v[t] = user_input[i]
            t += 1
            while i < len(user_input) and user_input[i] >= '0' and user_input[i] <= '9':
                v[t] = user_input[i]
                t += 1
                i += 1
            in_num_storage(data, int(''.join(v)))
            while t > 0:
                v[t] = ''
                t -= 1
            if i < len(user_input) and user_input[i] != ')':
                i -= 1
                in_symbol_storage(symbol, '(')
        elif i < len(user_input) and user_input[i] >= '0' and user_input[i] <= '9':
            while i < len(user_input) and user_input[i] >= '0' and user_input[i] <= '9':
                v[t] = user_input[i]
                t += 1
                i += 1
            in_num_storage(data, int(''.join(v)))
            while t > 0:
                v[t] = ''
                t -= 1
            i -= 1
        else:
            if symbol.top == -1:
                in_symbol_storage(symbol, user_input[i])
            elif judge_symbol_priority(user_input[i]) == 1:
                in_symbol_storage(symbol, user_input[i])
            elif judge_symbol_priority(user_input[i]) == 2:
                if judge_symbol_priority(read_symbol_storage(symbol)) == 1:
                    in_symbol_storage(symbol, user_input[i])
                elif judge_symbol_priority(read_symbol_storage(symbol)) == 2:
                    while symbol.top >= 0 and data.top >= 1:
                        v2 = get_num_data(data)
                        v1 = get_num_data(data)
                        sum_val = math(v1, v2, get_symbol(symbol))
                        in_num_storage(data, sum_val)
                    in_symbol_storage(symbol, user_input[i])
                elif judge_symbol_priority(read_symbol_storage(symbol)) == 3:
                    while symbol.top >= 0 and data.top >= 1:
                        v2 = get_num_data(data)
                        v1 = get_num_data(data)
                        sum_val = math(v1, v2, get_symbol(symbol))
                        in_num_storage(data, sum_val)
                    in_symbol_storage(symbol, user_input[i])

            elif judge_symbol_priority(user_input[i]) == 3:
                if judge_symbol_priority(read_symbol_storage(symbol)) == 1:
                    in_symbol_storage(symbol, user_input[i])
                elif judge_symbol_priority(read_symbol_storage(symbol)) == 2:
                    in_symbol_storage(symbol, user_input[i])
                elif judge_symbol_priority(read_symbol_storage(symbol)) == 3:
                    while symbol.top >= 0 and data.top >= 1:
                        v2 = get_num_data(data)
                        v1 = get_num_data(data)
                        sum_val = math(v1, v2, get_symbol(symbol))
                        in_num_storage(data, sum_val)
                    in_symbol_storage(symbol, user_input[i])
            elif judge_symbol_priority(user_input[i]) == 4:
                while symbol.top >= 0 and judge_symbol_priority(read_symbol_storage(symbol)) != 1:
                    v2 = get_num_data(data)
                    v1 = get_num_data(data)
                    sum_val = math(v1, v2, get_symbol(symbol))
                    in_num_storage(data, sum_val)
                get_symbol(symbol)
    while symbol.top != -1:
        v2 = get_num_data(data)
        v1 = get_num_data(data)
        sum_val = math(v1, v2, get_symbol(symbol))
        in_num_storage(data, sum_val)
    print("The result is: ", data.number[0])

main()
