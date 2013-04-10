#!/bin/usr/python


def make_counter_nonlocal():
    count = 0
    def counter1():
        nonlocal count
        count += 1
        return count
    return counter1()

def make_counter():
    count = 0
    def counter2():
        count += 1
        return count
    return counter2()

def make_counter_for():
    count = 0
    for i in range(5):
        count += 1
    return count



print("{}".format(make_counter_nonlocal()))
#print("{}".format(make_counter()))
print("{}".format(make_counter_for()))
