from abc import ABC, abstractmethod
from collections import deque

class Stack:
    def __init__(self):
        self._container = deque()

    def push(self, o):
        self._container.append(o)

    def pop(self):
        return self._container.pop()

    def peek(self):
        return self._container[-1]

    def __len__(self):
        return len(self._container)

    def __repr__(self):
        s = ", ".join([str(x) for x in self._container])
        return f"<Stack [{s}]>"

class Expression(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

class Constant(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __repr__(self):
        return f"<Constant {self.value}>"

class BinaryOperator(Expression):
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self):
        if self.op == "+":
            return self.lhs.evaluate() + self.rhs.evaluate()
        elif self.op == "-":
            return self.lhs.evaluate() - self.rhs.evaluate()
        elif self.op == "*":
            return self.lhs.evaluate() * self.rhs.evaluate()
        elif self.op == "/":
            return self.lhs.evaluate() / self.rhs.evaluate()

    def __repr__(self):
        return f"<BinaryOperator {self.lhs} {self.op} {self.rhs}>"

class UnaryOperator(Expression):
    def __init__(self, rhs, op):
        self.rhs = rhs
        self.op = op

    def evaluate(self):
        if self.op == "-":
            return -self.rhs.evaluate()

    def __repr__(self):
        return f"<UnaryOperator {self.op} {self.rhs}>"

class Calculation:
    def __init__(self):
        self._result_stack = Stack()
        self._operator_stack = Stack()

    def read_str(self, s):
        i = 0
        while i < len(s):
            ch = s[i]
            if ch.isdecimal():
                num, l = self._consume_number(s, i)
                self._result_stack.push(Constant(num))
                i += l - 1
            elif ch == " ":
                pass
            elif ch == "(":
                self._operator_stack.push("(")
            elif ch == ")":
                self._fold_parenthesis()
            elif ch in "+-*/":
                self._fold_operators(ch)
                self._operator_stack.push(ch)
            else:
                raise ValueError("Unknown input character: " + s[i])
            i += 1

        while len(self._operator_stack):
            if self._operator_stack.peek() == "(":
                raise ValueError("Unmatched left parenthesis")
            self._pop_operation()

        # print(self._result_stack, self._operator_stack)

    def get_result(self):
        return self._result_stack.pop().evaluate()

    def _consume_number(self, s, i):
        j = 0
        while i+j < len(s):
            if not s[i+j].isdecimal():
                break
            j += 1
        return (int(s[i:i+j]), j)

    def _precendence(self, ch):
        PRECEDENCE_MAP = {
            "+": 2,
            "-": 2,
            "*": 3,
            "/": 3,
            "(": -99,
            ")": 99,
        }
        return PRECEDENCE_MAP[ch]

    def _fold_parenthesis(self):
        while self._operator_stack.peek() != "(":
            try:
                self._pop_operation()
            except:
                raise ValueError("Unmatched right parenthesis")
        assert self._operator_stack.pop() == "("

    def _fold_operators(self, new_op):
        while len(self._operator_stack):
            op = self._operator_stack.peek()
            if op != "(" and self._precendence(op) >= self._precendence(new_op):
                self._pop_operation()
            else:
                break

    def _pop_operation(self):
        op = self._operator_stack.pop()
        rhs = self._result_stack.pop()
        if len(self._result_stack):
            lhs = self._result_stack.pop()
            self._result_stack.push(BinaryOperator(lhs, rhs, op))
        else:
            self._result_stack.push(UnaryOperator(rhs, op))


def main():
    user_input = input("Enter an expression: ")
    calc = Calculation()
    calc.read_str(user_input)
    print(calc.get_result())

if __name__ == "__main__":
    main()
