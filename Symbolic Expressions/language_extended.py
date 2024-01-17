"""
Author: Sergei Baginskii
"""

import math

class Expr:
    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Con(other)
        return Add(self, other)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Con(other)
        return Sub(self, other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Con(other)
        return Mul(self, other)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Con(other)
        return Div(self, other)

    def __neg__(self):
        return Neg(self)

    def simplify(self):
        return self


class Con(Expr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"{self.val}"

    def __eq__(self, other):
        if isinstance(other, Con):
            return self.val == other.val
        return False

    def ev(self, env):
        return self

    def diff(self, name):
        return Con(0)

    def vs(self):
        return []


class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"

    def ev(self, env):
        return Con(env[self.name])

    def diff(self, name):
        return Con(1 if self.name == name else 0)

    def __eq__(self, other):
        if isinstance(other, Var):
            return self.name == other.name
        return False

    def vs(self):
        return [self.name]


class Unop(Expr):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return f"{self.name}({self.arg})"

    def ev(self, env):
        return self.op(self.arg.ev(env))

    def __eq__(self, other):
        if isinstance(other, Unop):
            return self.name == other.name and self.arg == other.arg
        return False

    def vs(self):
        return self.arg.vs()

class BinOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.name} {self.right})"

    def ev(self, env):
        return self.op(self.left.ev(env), self.right.ev(env))

    def __eq__(self, other):
        if isinstance(other, BinOp):
            return self.name == other.name and self.left == other.left and self.right == other.right
        return False

    def vs(self):
        return self.left.vs() + self.right.vs()


class Add(BinOp):
    name = "+"
    op = lambda self, x, y: x + y

    def diff(self, name):
        return self.left.diff(name) + self.right.diff(name)

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if left.vs() == []:
            left = left.ev({})
        if right.vs() == []:
            right = right.ev({})

        if isinstance(left, Con) and isinstance(right, Con):
            return Con(left.val + right.val)

        if left == Con(0):
            return right

        if right == Con(0):
            return left

        return left + right


class Sub(BinOp):
    name = "-"
    op = lambda self, x, y: x - y

    def diff(self, name):
        return self.left.diff(name) - self.right.diff(name)

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if left.vs() == []:
            left = left.ev({})
        if right.vs() == []:
            right = right.ev({})

        if isinstance(left, Con) and isinstance(right, Con):
            return Con(left.val - right.val)

        if left == Con(0):
            return right

        if right == Con(0):
            return left

        if left == right:
            return Con(0)

        return left - right


class Mul(BinOp):
    name = "*"
    op = lambda self, x, y: x * y

    def diff(self, name):
        f = self.left
        f1 = f.diff(name)
        g = self.right
        g1 = g.diff(name)

        return f1 * g + f * g1

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if left.vs() == []:
            left = left.ev({})
        if right.vs() == []:
            right = right.ev({})

        if isinstance(left, Con) and isinstance(right, Con):
            return Con(left.val * right.val)

        if left == Con(0) or right == Con(0):
            return Con(0)

        if left == Con(1):
            return right

        if right == Con(1):
            return left

        return left * right


class Div(BinOp):
    name = "/"
    op = lambda self, x, y: x / y

    def diff(self, name):
        f = self.left
        f1 = f.diff(name)
        g = self.right
        g1 = g.diff(name)

        return (g * f1 - f * g1) / (g * g)

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if left.vs() == []:
            left = left.ev({})
        if right.vs() == []:
            right = right.ev({})

        if isinstance(left, Con) and isinstance(right, Con):
            return Con(left.val / right.val)

        if left == Con(0) and right != Con(0):
            return Con(0)

        if right == Con(0):
            raise ZeroDivisionError

        if right == Con(1):
            return left

        return left / right


class Exp(Unop):
    name = "exp"
    op = lambda self, x: Exp(x)

    def diff(self, name):
        if self.arg.diff(name) != 0:  # exponent is dependent of the variable
            return Exp(self.arg)
        else:  # not dependent
            return 0

    def simplify(self):
        expr = self.arg.simplify()
        if expr.vs() == []:
            expr = expr.ev({})

        if isinstance(expr, Con):
            return Con(math.exp(expr.val))

        return Exp(expr)


class Neg(Unop):
    name = "-"
    op = lambda self, x: -x

    def __init__(self, arg):
        super().__init__(arg)
        self.original_expr = self.arg

    def diff(self, name):
        return Neg(self.arg.diff(name))

    def simplify(self):
        expr = self.arg.simplify()
        if expr.vs() == []:
            expr = expr.ev({})

        if isinstance(expr, Con):
            return Con(-expr.val)

        if isinstance(expr, Neg):
            return self.original_expr.original_expr

        return Neg(expr)


env = {"x": 5}
test1 = Con(1) / (Exp(-Var("x")) + Con(1))

test2 = (Exp(Var("x")) - Exp(-Var("x")))/(Exp(Var("x")) + Exp(-Var("x")))


print(f"First example in a string form: {test1.simplify()}")
print(f"First example calculated {test1.ev(env).simplify()}")
print(f"First example differentiated {test1.diff('x').simplify()}")
print("\n")
print(f"Second example in a string form: {test2.simplify()}")
print(f"Second example calculated {test2.ev(env).simplify()}")
print(f"Second example differentiated {test2.diff('x').simplify()}")