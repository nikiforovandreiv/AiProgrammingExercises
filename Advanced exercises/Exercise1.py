# author: Mikita Zyhmantovich
test_list = [1, 2, 3, 4]
test_string = "Mango"


def rev(itrbl):
    if not itrbl:
        return itrbl
    else:
        return itrbl[-1::] + rev(itrbl[:-1])


print(rev(test_string))
print(rev(test_list))
