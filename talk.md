## PEP 3104 - Access to Names in Outer Scopes

CSCI 3155 - Lightning Talk  

PEP 3104 - Access to Names in Outer Scopes  

David Baird -- Aaron Davis -- Ryan Riley  

## PEP Overview
* In Python 3, the ability to rebind (assign) names from the nearest enclosing scope was added
* In PEP 227, nested scoping was added to Python
* However, names from enclosing scopes could be refered to but not rebound

## Other Languages

* C/C++
    * No problem, nested scoping not allowed

* Scala
    * Already has the functionality of this PEP

* Python
    * ???

## Rationale
* Python supports nested scoping
* Most other languages that support nested scoping support rebinding of names from enclosing scopes
* Therefore this was confusing to programmers

## What already worked

This was legal before PEP 3104:

    def make_counter_print():
        count = 0
        def counter2():
            print(count)
        return counter2()

* We could access a variable outside the scope, just not modify it

## What already worked

This was legal before too:

    def make_counter_for():
        count = 0
        for i in range(5):
            count += 1
        return count

* This PEP mostly refers to functions declared within functions
* For-loops could already access outer scopes in Python2

## The Problem:

This was illegal before PEP 3104:

    def make_counter():
        count = 0
        def counter2():
            count += 1
            return count
        return counter2()

* This code does not work, count is outside of the scope of counter2
* In Python2, there was no way to access the name count from the inner scope
* In Python3, this can be done with the 'nonlocal' keyword


## Work-around Example
    
    class Namespace:
        pass

    def make_counter():
        ns = Namespace()
        ns.count = 0
        def counter2():
            ns.count += 1
            return count
        return counter2()

* Using a class as a namespace allowed one to work around this constraint

## Work-around didn't satisfy everybody

But many found the namespace solution inelegant:  
  

>I have also seen mention that the use
>of classes can mitigate this, but that seems, IMHO, heavy handed in cases
>when an elegant solution using a closure would suffice and be more
>appropriate--especially when Python already has nested lexical scopes.

> \- Almann T. Goo, Python Dev Mailing List

## Proposed Solutions

Two categories of proposed solutions:  

1. New syntax in outer scope
    * Scope Override Declaration (outer scope)

2. New syntax in inner scope
    * Outer Reference Expression
    * Rebinding Operator
    * Scope Override Declaration (inner scope)

## New syntax in outer scope

* New keyword for names in outer scopes
* Would allow references to these names to be visible in enclosed scopes
* Like JavaScript's 'var' keyword
* Other suggestions were 'my' and 'scope'

## Outer Scope Override Declaration Rejected
* Rejected because context-sensitive
* Moving a function could change its meaning depending on its enclosing scope(s)

## New Syntax in Inner Scope - Outer Reference Expression
* Names with the prepended . would refer to names bound in non-local scopes
* Possibly, multiple dots would indicate going out multiple levels of scope
* For example, .x or ..x
* Rejected because error-prone and confusing
* Concern that x and .x could refer to the same thing

## New Syntax in Inner Scope - Rebinding Operator
* Use := as a 'rebinding operator'
* This would allowing reassignment of a name without declaring it to be local
* Also rejected because confusing

## New Syntax in Inner Scope - Scope Override Declaration
* Create a new keyword which indicate the name is not being declared as local
* Many suggested keywords, including scoped, ref, outer, refer, share, and others
* This solution was adopted with keyword 'nonlocal' 

## The Implemented Solution

What it looks like:

    def make_counter_nonlocal():
        count = 0
        def counter1():
            nonlocal count
            count += 1
            return count
        return counter1()

* The keyword 'nonlocal' allows one to access the name from the enclosing scope
* This change has taken effect in Python3