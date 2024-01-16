"""
Author: Sergei Baginskii
"""

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
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"{self.name}({self.expr})"

    def ev(self, env):
        return self.op(self.expr.ev(env))

    def __eq__(self, other):
        if isinstance(other, Unop):
            return self.name == other.name and self.expr == other.expr
        return False

    def vs(self):
        return self.expr

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
    e_value = 3.1415926  # approximate so that there is no need to call math or numpy
    name = "exp"
    op = lambda self, x: Exp.e_value ** x

    def diff(self, name):
        return self.expr.diff(name) * Exp(self.expr)

    def simplify(self):
        expr = self.expr.simplify()
        if expr.vs() == []:
            expr = expr.ev({})

        if isinstance(expr, Con):
            return Con(Exp.e_value ** expr.val)

        return Exp(expr)


class Neg(Unop):
    name = "-"
    op = lambda self, x: -x

    def diff(self, name):
        return Neg(self.expr.diff(name))

    def simplify(self):
        expr = self.expr.simplify()
        if expr.vs() == []:
            expr = expr.ev({})

        if isinstance(expr, Con):
            return Con(-expr.val)

        return Neg(expr)


ex1 = Add(Mul(Con(2.5), Var("x1")), Var("x2"))
ex2 = Add(Con(2.5), Con(-2.5))
ex3 = Mul(Var("x1"), Con(1))
ex4 = Sub(Con(2.5), Con(1.0))
ex5 = Div(Var("x1"), Var("x2"))
ex6 = Neg(Var("x1"))
print(ex6.diff("x1").simplify())
