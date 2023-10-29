# Author: Mikita Zyhmantovich

def nsp(x, y):
    if x == 0 and y == 1 or x == 1 and y == 0:
        return 1
    elif x < 0 or y < 0:
        return 0
    else:
        return nsp(x-1, y) + nsp(x, y - 1)


print(nsp(3, 2))
