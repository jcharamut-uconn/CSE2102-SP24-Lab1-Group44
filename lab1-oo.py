from abc import ABC, abstractmethod
from collections import deque

class Expression(ABC):
    @staticmethod
    @abstractmethod
    def is_valid_char(c):
        pass

    @abstractmethod
    def consume(self, c):
        pass

class Number(Expression):
    def __init__(self, value=None):
        self._buf = ""
        self.value = value

    @staticmethod
    def is_valid_char(c):
        return c.isdecimal()

    def consume(self, c):
        if not self.is_valid_char(c):
            raise ValueError
        self._buf += c
        self.value = int(self._buf)

    def __repr__(self):
        return "<Number {}>".format(self.value)

class Operator(Expression):
    def __init__(self):
        self.op = None

    @staticmethod
    def is_valid_char(c):
        return c in "()+-*/"

    def consume(self, c):
        if not self.is_valid_char(c):
            raise ValueError
        assert self.op is None
        self.op = c

    def precedence(self):
        if self.op == "(":
            return 1
        elif self.op in "+-":
            return 2
        elif self.op in "*/":
            return 3
        elif self.op == ")":
            return 4
        else:
            raise ValueError("Invalid Operator: " + self.op)

    def apply(self, v1, v2):
        if self.op == "+":
            return Number(v1.value + v2.value)
        elif self.op == "-":
            return Number(v1.value - v2.value)
        elif self.op == "*":
            return Number(v1.value * v2.value)
        elif self.op == "/":
            return Number(v1.value / v2.value)

    def __repr__(self):
        return "<Operator '{}'>".format(self.op)


class Calculator:
    def tokenize_str(s):
        tokens = deque()
        token_in_progress = None
        i = 0
        while i < len(s):
            c = s[i]

            # if starting new token, find type
            if not token_in_progress:
                if Number.is_valid_char(c):
                    token_in_progress = Number()
                elif Operator.is_valid_char(c):
                    token_in_progress = Operator()
                elif c == " ":
                    # dont care about spaces
                    i += 1
                else:
                    raise ValueError("Invalid input char: " + c)

            # try consuming a character
            try:
                token_in_progress.consume(c)
                i += 1
            except ValueError:
                # if invalid for that token, move onto another
                tokens.append(token_in_progress)
                token_in_progress = None

        tokens.append(token_in_progress)
        return tokens

    def parse_tokens(tokens):
        output_stack = deque()
        operator_stack = deque()

        while len(tokens):
            tok = tokens.popleft()
            if isinstance(tok, Number):
                output_stack.append(tok)
            elif isinstance(tok, Operator):
                if tok.op == "(":
                    output_stack.append(tok)
                elif tok.op == ")":
                    while len(operator_stack) and operator_stack[-1].op != "(":
                        op = operator_stack.pop()
                        v2 = output_stack.pop()
                        v1 = output_stack.pop()
                        output_stack.append(op.apply(v1, v2))
                    operator_stack.pop()
                else:
                    while len(operator_stack) and operator_stack[-1].precedence() > tok.precedence():
                        op = operator_stack.pop()
                        v2 = output_stack.pop()
                        v1 = output_stack.pop()
                        output_stack.append(op.apply(v1, v2))
                    operator_stack.append(tok)
        while len(operator_stack):
            if operator_stack[-1].op == "(":
                raise RuntimeError("Mismatched Parentheses")
            op = operator_stack.pop()
            v2 = output_stack.pop()
            v1 = output_stack.pop()
            output_stack.append(op.apply(v1, v2))
        return output_stack


    def evaluate_str(s):
        print(f"input str: '{s}'")
        tokens = Calculator.tokenize_str(s)
        print(f"token queue: '{tokens}'")
        output = Calculator.parse_tokens(tokens)
        print(f"output stack: '{output}'")
        return output[0].value


def main():
    user_input = input("Enter an expression: ")
    print(Calculator.evaluate_str(user_input))


if __name__ == "__main__":
    main()
