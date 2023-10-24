test_string = "Thor"
test_list = [1, 2, 3, 4]
test_list2 = [5, 6, 7, 8]


def rotate_r(itrbl):  # exercise 1,3: Mikita Zyhmantovich, Andrei Nikiforov, Vladyslav Chornyi
    return itrbl[-1::] + itrbl[:-1]


def rotate_l(itrbl):  # exercise 2,3: Mikita Zyhmantovich, Andrei Nikiforov, Vladyslav Chornyi
    return itrbl[1:] + itrbl[0:1:]


def rotate_rx(itrbl):  # exercise 4: Mikita Zyhmantovich, Andrei Nikiforov, Vladyslav Chornyi
    itrbl[:] = itrbl[-1::] + itrbl[:-1]

# exercise 5 No, it's not possible to use function to change the string
# because strings are immutable in Python


def rotate_r2(itrbl):  # exercise 6: Mikita Zyhmantovich, Andrei Nikiforov
    return rotate_r(rotate_r(itrbl))


def rotate_rx2(itrbl):  # exercise 7: Mikita Zyhmantovich, Andrei Nikiforov
    rotate_rx(itrbl)
    rotate_rx(itrbl)

print("Test: exercise 1")
print(rotate_r(test_list))  # test excercise 1
print("Test: exercise 3")
print(rotate_r(test_string))  # test excercise 3

print("Test: exercise 2")
print(rotate_l(test_list))  # test excercise 2
print("Test: exercise 3")
print(rotate_l(test_string))  # test excercise 3

print("Test: exercise 4")
rotate_rx(test_list2)  # test exercise 4
print(test_list2)

print("Test: exercise 6")
print(rotate_r2(test_string))  # test excercise 6

test_list2 = [5, 6, 7, 8]  # test exercise 7
rotate_rx2(test_list2)
print("Test: exercise 7")
print(test_list2)

# --------------------------

print("Test: exercise 8")
l_aux = [1, 2, 3] # exercise 8 Mikita Zyhmantovich
l = [l_aux, l_aux]
print(l)
rotate_rx(l[1])
print(l)
