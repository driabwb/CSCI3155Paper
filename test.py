#!/bin/usr/python

# works in python 3 with the PEP implemented
# but not in python 2 without it
def make_counter_nonlocal():
    count = 0
    def counter1():
        nonlocal count
        count += 1
        return count
    return counter1()

# does not work, count is outside of the scope of counter2
def make_counter():
    count = 0
    def counter2():
        count += 1
        return count
    return counter2()

# works in python 2 or 3, for loops could already access
# variables outside of their scope
def make_counter_for():
    count = 0
    for i in range(5):
        count += 1
    return count

print("{}".format(make_counter_nonlocal()))
#print("{}".format(make_counter()))
print("{}".format(make_counter_for()))
