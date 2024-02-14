from abc import ABC, abstractmethod

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

class BinaryOperator(Expression):
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self):
        if self.op == "+":
            return lhs.evaluate() + rhs.evaluate()
        elif self.op == "-":
            return lhs.evaluate() - rhs.evaluate()
        elif self.op == "*":
            return lhs.evaluate() * rhs.evaluate()
        elif self.op == "/":
            return lhs.evaluate() / rhs.evaluate()

class UnaryOperator(Expression):
    def __init__(self, rhs, op):
        self.rhs = rhs
        self.op = op

    def evaluate(self):
        if self.op == "-":
            return -rhs.evaluate()

class Calculation:
    def __init__(self):
        pass


def main():
    user_input = input("Enter an expression: ")
    user_input = user_input.replace(" ", "")
    calc = Calculation()
    calc.read_str(user_input)
    print(calc.get_result())

if __name__ == "__main__":
    main()
