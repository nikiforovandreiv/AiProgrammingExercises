# 2 Python from the top-level
# 2.7 Exercises

# Exercise 1
def rotate_r(input_element):
    return input_element[-1:] + input_element[:-1]


# myString = "Hey"
# print(myString)
# print(rotate_r(myString))


# Exercise 2
def rotate_l(input_element):
    return input_element[1:] + input_element[0:1]


# myList = [1, 2, 3, 4]
# print(myList)
# print(rotate_l(myList))


# Exercise 4
def rotate_rx(input_element):
    input_element[:] = input_element[-1:] + input_element[:-1]


# myList = [1, 2, 3, 4]
# print(myList)
# rotate_rx(myList)
# print(myList)


# Exercise 5
# No, it's not possible to use function to change the string
# Strings are immutable in Python


# Exercise 6
def rotate_r2(input_element):
    return rotate_r(rotate_r(input_element))


# myString = "Thor"
# print(myString)
# print(rotate_r2(myString))


# Exercise 7
def rotate_rx2(input_element):
    rotate_rx(input_element)
    rotate_rx(input_element)


# myList = [1, 2, 3, 4]
# print(myList)
# rotate_rx2(myList)
# print(myList)


# Exercise 8
# myList = [1, 2, 3]
# myList = [myList, myList]
# rotate_rx(myList[1])
# print(myList)

# or

# myList = [[1, 2, 3], [1, 2, 3]]
# myList[0] = myList[1]
# rotate_rx(myList[1])
# print(myList)
