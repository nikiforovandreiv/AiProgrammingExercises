# Author Oleksii Kalashnikov
# Implementation of the missing trials
from z3 import *

def unique(s, xs):
    m = s.model()
    for x in xs:
        s.push()
        s.add(x != m.eval(x, model_completion=True))
        if s.check() == sat:
            return False
        s.pop()
    return True

def trial1():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 & ~r2
    sign2 = r1 != r2

    s = Solver()

    s.add(sign1 != sign2)

    return s
    
def trial2():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 | r2
    sign2 = ~r1

    cond  = sign1 == sign2

    s = Solver()
    s.add(cond)

    return s

def trial3():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = ~r1 | r2
    sign2 = r1

    cond  = sign1 == sign2

    s = Solver()
    s.add(cond)

    return s



def trial4():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 & r2
    sign2 = sign1

    cond1 = r1 == sign1
    cond2 = r2 != sign2

    s = Solver()
    s.add(cond1, cond2)

    return s

def trial5():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 | r2
    sign2 = r1

    cond1 = r1 == sign1
    cond2 = r2 != sign2

    s = Solver()
    s.add(cond1, cond2)

    return s

def trial6():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 == r2
    sign2 = r1

    cond1 = r1 == sign1
    cond2 = r2 != sign2

    s = Solver()
    s.add(cond1, cond2)

    return s

def trial7():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 != r2
    sign2 = r1

    cond1 = r1 == sign1
    cond2 = r2 != sign2

    s = Solver()
    s.add(cond1, cond2)

    return s


def trial8():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign2 = ~r2
    sign1 = ~r1 & ~r2

    cond1 = r1 == sign1
    cond2 = r2 != sign2

    s = Solver()
    s.add(cond1, cond2)

    return s
    
def trial9():
    r1, r2, r3 = Bools("r1 r2 r3")
    # ri True means there is a lady in room i
    # ri False --> tiger!
    # one_lady = (r1 & ~r2 & ~r3) | (~r1 & r2 & ~r3) | (~r1 & ~r2 & r3)
    one_lady = Sum([If(r, 1, 0) for r in [r1, r2, r3]]) == 1
    
    sign1 = ~r1
    sign2 = r2
    sign3 = ~r2

    # one_sign = (sign1 & ~sign2 & ~sign3) | (~sign1 & sign2 & ~sign3) | (~sign1 & ~sign2 & sign3) | (~sign1 & ~sign2 & ~sign3)
    one_sign = Sum([If(sign, 1, 0) for sign in [sign1, sign2, sign3]]) <= 1
    
    s = Solver()
    s.add(one_lady)
    s.add(one_sign)

    return s

def trial10():
    r1, r2, r3 = Bools("r1 r2 r3")
    # ri True means there is a lady in room i
    # ri False --> tiger!
    # one_lady = (r1 & ~r2 & ~r3) | (~r1 & r2 & ~r3) | (~r1 & ~r2 & r3)
    one_lady = Sum([If(r, 1, 0) for r in [r1, r2, r3]]) == 1
    sign1 = ~r2
    sign2 = ~r2
    sign3 = ~r1

    # A sign with a lady says the truth
    lady_sign_truth = If(r1, sign1, If(r2, sign2, sign3))

    # At least one of the other two signs is false
    one_false_sign = ~sign1 | ~sign2 | ~sign3
    s = Solver()
    s.add(one_lady)
    s.add(one_false_sign)
    s.add(lady_sign_truth)

    return s




def trial11():
    r1, r2, r3 = Ints("r1 r2 r3")
    # ri = 0, if tiger in room i
    #      1, if lady in room i
    #      2, if room i is empty
    rs = [r1, r2, r3]
    range_cond = [(0 <= r) & (r <= 2) for r in rs]
    distinct_cond = Distinct(rs)

    sign1 = r3 == 2
    sign2 = r1 == 0
    sign3 = r3 == 2
    signs = [sign1, sign2, sign3]
    
    sign_cond = [Implies(rs[i] == 0, ~signs[i]) & \
                 Implies(rs[i] == 1, signs[i]) for i in range(3)]

    s = Solver()
    s.add(range_cond)
    s.add(distinct_cond)
    s.add(sign_cond)

    return s

def trial12():
    r1, r2, r3, r4, r5, r6, r7, r8, r9 = Ints("r1 r2 r3 r4 r5 r6 r7 r8 r9")
    rs = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
    # rs[i] = 0, if tiger in room i+1
    #         1, if lady in room i+1
    #         2, if room i is empty i+1
    range_cond = [(0 <= r) & (r <= 2) for r in rs]
    one_lady = Sum([If(r == 1, 1, 0) for r in rs]) == 1
    
    signs1 = (rs[0] == 1) | (rs[2] == 1) | (rs[4] == 1) | (rs[6]== 1) | (rs[8] == 1)
    signs2 = rs[1] == 2
    signs7 = rs[0] != 1
    
    signs4 = ~signs1
    signs5 = signs4 | signs2
    signs7 = rs[0] != 1
    signs3 = signs5 | ~signs7
    signs6 = ~signs3

    signs8 = (rs[7] == 0) & (rs[8] == 2)
    signs9 = (rs[8] == 0) & ~signs6
    signs = [signs1 , signs2, signs3, signs4, signs5, signs6, signs7, signs8, signs9]
    sign_cond = [Implies(rs[i] == 0, ~signs[i]) & \
                 Implies(rs[i] == 1, signs[i]) for i in range(9)]
    cond1 = rs[7] != 2
    # cond2 = rs[7] != 1
    # If room 8 is empty lady could be in multiple different rooms, if it not lady is awlays in the 7th room
    s = Solver()
    s.add(range_cond)
    s.add(one_lady)
    s.add(sign_cond)
    s.add(cond1)
    
    return s

if __name__ == "__main__":
    s = trial12()
    print(s.check())
    print(s.model())
    
