from abc import ABC, abstractmethod

class Storage(ABC):
    def __init__(self):
        self._data = [None] * 100
        self._top = -1

    def push(self, item):
        self._top += 1
        self._data[self._top] = item

    def peek(self):
        return self._data[self._top]

    def pop(self):
        v = self._data[self._top]
        self._top -= 1
        return v

    def __len__(self):
        return self._top + 1

class NumStorage(Storage):
    pass

class SymbolStorage(Storage):
    def math(self, left, right):
        c = self.pop()
        if c == '+':
            return left + right
        elif c == '-':
            return left - right
        elif c == '*':
            return left * right
        elif c == '/':
            return left / right

    def priority(self):
        return SymbolStorage.priority(self.peek())

    @classmethod
    def priority(ch):
        if ch == '(':
            return 1
        elif ch == '+' or ch == '-':
            return 2
        elif ch == '*' or ch == '/':
            return 3
        elif ch == ')':
            return 4

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
    number_stack = NumStorage()
    operator_stack = SymbolStorage()
    user_input = input("Enter the expression (no blank, no decimals): ")

    v = [""] * 100
    t = 0
    for i in range(len(user_input)):
        if i == 0 and user_input[i] == '-':
            v[t] = user_input[i]
            t += 1
        elif user_input[i] == '(' and i + 1 < len(user_input) and user_input[i + 1] == '-':
            i += 1
            buf = ""
            v[t] = user_input[i]
            t += 1
            while i < len(user_input) and user_input[i].isdecimal():
                v[t] = user_input[i]
                t += 1
                i += 1
            number_stack.push(int(''.join(v)))
            while t > 0:
                v[t] = ''
                t -= 1
            if i < len(user_input) and user_input[i] != ')':
                i -= 1
                operator_stack.push('(')
        elif i < len(user_input) and user_input[i].isdecimal():
            while i < len(user_input) and user_input[i].isdecimal():
                v[t] = user_input[i]
                t += 1
                i += 1
            number_stack.push(int(''.join(v)))
            while t > 0:
                v[t] = ''
                t -= 1
            i -= 1
        else:
            if len(operator_stack) == 0:
                operator_stack.push(user_input[i])
            elif judge_symbol_priority(user_input[i]) == 1:
                operator_stack.push(user_input[i])
            elif judge_symbol_priority(user_input[i]) == 2:
                if judge_symbol_priority(operator_stack.peek()) == 1:
                    operator_stack.push(user_input[i])
                elif judge_symbol_priority(operator_stack.peek()) == 2:
                    while operator_stack._top >= 0 and number_stack._top >= 1:
                        v2 = number_stack.pop()
                        v1 = number_stack.pop()
                        sum_val = math(v1, v2, operator_stack.pop())
                        number_stack.push(sum_val)
                    operator_stack.push(user_input[i])
                elif judge_symbol_priority(operator_stack.peek()) == 3:
                    while operator_stack._top >= 0 and number_stack._top >= 1:
                        v2 = number_stack.pop()
                        v1 = number_stack.pop()
                        sum_val = math(v1, v2, operator_stack.pop())
                        number_stack.push(sum_val)
                    operator_stack.push(user_input[i])

            elif judge_symbol_priority(user_input[i]) == 3:
                if judge_symbol_priority(operator_stack.peek()) == 1:
                    operator_stack.push(user_input[i])
                elif judge_symbol_priority(operator_stack.peek()) == 2:
                    operator_stack.push(user_input[i])
                elif judge_symbol_priority(operator_stack.peek()) == 3:
                    while operator_stack._top >= 0 and number_stack._top >= 1:
                        v2 = number_stack.pop()
                        v1 = number_stack.pop()
                        sum_val = math(v1, v2, operator_stack.pop())
                        number_stack.push(sum_val)
                    operator_stack.push(user_input[i])
            elif judge_symbol_priority(user_input[i]) == 4:
                while operator_stack._top >= 0 and judge_symbol_priority(operator_stack.peek()) != 1:
                    v2 = number_stack.pop()
                    v1 = number_stack.pop()
                    sum_val = math(v1, v2, operator_stack.pop())
                    number_stack.push(sum_val)
                operator_stack.pop()
    while len(operator_stack) > 0:
        v2 = number_stack.pop()
        v1 = number_stack.pop()
        sum_val = math(v1, v2, operator_stack.pop())
        number_stack.push(sum_val)
    print("The result is: ", number_stack.peek())


if __name__ == "__main__":
    main()

