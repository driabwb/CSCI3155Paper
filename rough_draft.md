# CSCI3155 Paper: PEP 3104 (Rough Draft)

## David Baird, Aaron Davis, Ryan Riley

### The Proposal

This paper discusses Python Enhancement Proposal (PEP) 3104, access to names in outer scopes. In Python, one can declare functions within functions which gives the syntactic appearance of a nested, lexical scope. Before PEP 3104, one could access variables outside the immediate local scope but not modify them. This lack of functionality was counter-intuitive to programmers accustomed to using nested scopes. The following code, taken from the PEP proposal site, illustrates the problem: [1]

~~~~~
def make_scoreboard(frame, score=0):
    label = Label(frame)
    label.pack()
    for i in [-10, -1, 1, 10]:
        def increment(step=i):
            score = score + step  # fails with UnboundLocalError
            label['text'] = score
        button = Button(frame, text='%+d' % i, command=increment)
        button.pack()
    return label
~~~~~

The error on line 6 was a completely unexpected result for many developers. A programmer accustomed to nested, lexical scoping would assume the ability to modify the score variable in the nested function. Python, however, did not support this functionality until the PEP was implemented in Python 3. Previously, one would have to wrap a variable in a class, namespace, or mutable object to be able to modify it from an inner scope. Below is an example of such a work-around:

~~~~
class Namespace:
    pass

def make_scoreboard(frame, score=0):
    ns = Namespace()
    ns.score = 0
    label = Label(frame)
    label.pack()
    for i in [-10, -1, 1, 10]:
        def increment(step=i):
            ns.score = ns.score + step
            label['text'] = ns.score
        button = Button(frame, text='%+d' % i, command=increment)
        button.pack()
    return label
~~~~

The extra code required by the example obscures the actual workings of the program to a potential reader. Because Python touts itself as being easy to read and ituitive, a more elegant solution was needed.

This PEP proposed a new keyword, 'nonlocal', to solve the scoping issue. The keyword acts as an override for searching the local scope only, allowing the program to look to outerscopes if the variable in question is not locally bound. Several other approaches to repair the problem, as well as other keywords, were proposed. The override solution was selected because it provided a clearer meaning and did not have the potential to break existing code. Among the other proposed keywords were global and outer. 'Global' was rejected to avoid any confusion with its already established usage and outer was rejected because it was a commonly used variable. 'Nonlocal', while somewhat cumbersome, provided a good solution because it clearly and succinctly conveys its purpose. After much debate, nonlocal was chosen as the solution [1].

The added functionality was also important to the full implementation of closures in Python. Closures are pieces of code that have associated data environments. This data environment is typically a table of references to the free variables (nonlocal) available to the related code. Closures allow for higher-order functions and are required for currying, making them extremely important to functional-style programmers. Although Python has technically supported closures since version 2.2, the addition of the 'nonlocal' keyword makes them explicit. [8] For many, this explicit implementation of closures was the primary motivation in pushing for the development of this PEP. For imperative style programmers, the added functionality was erroneus as closures are not commonly used. 

There were two main categories of propsed solutions to the problem raised by the PEP definition: new syntax in the outer scope, similar to the 'var' of JavaScript, or new syntax in the inner scope [1]. The outer scope solution would entail a new keyword such as 'var, 'my', or 'scope', which would indicate that this name could be rebound in scopes inside the current one. This PEP eventually went the way of the new syntax in the inner scope, primarily because the first method would cause function definitions to become context sensitive depending on what names are bound in an outer scope. In other words, situations could arise where the exact same line of code could produce different results based on the previous binding and could be a source of confusion.

### Community discussion

Since PEP 227, there has been talk in the community of addressing the issue of reassigning free variables within a nested scope. As Almann T. Goo writes in the Python-Dev mailing list:


>My rationale is that with the advent of PEP 227 <http://www.python.org/peps/pep-0227.html>, Python has proper  
>nested lexical scopes, but can have undesirable behavior (especially with new developers) when a user makes  
>wants to make an assignment to a free variable within a nested function." [2]


In general, there was agreement that this quirk of the language was problematic, and many replies echoed this concern: "The lack of support for rebinding names in enclosing scopes is certainly a wart." [3]

Goo suggested the keyword "use" in the message quoted above, and in the course of the conversation many more keywords were suggested including "outer", "extern", "common", and others. There was considerable support for not adding a keyword and simply "abusing" the use of the global keyword whenever the situation arose. [5]

In the discussion threads, there were fewer arguments against the new proposal than for it. Most of the arguments against it were really arguing against nested scoping in general, citing the lack of need for multiple levels of nested scopes. For example:

>Introducing these two new keywords is equivalent to encouraging nested scope use. Right now nested scope use  
>is "limited" or "fraught with gotchas". Adding the 'use' and 'scope' keywords to label levels of scopes for  
>name resolution will only encourage users to write closures which could have written better or not written  
>at all... [4]

Arguments against nested lexical scoping did not really seem to gain traction. Python has allowed for statically nested scopes since PEP 227 and there was no movement remove such support. [1] Many were quick to point this out in their responses, stating that to Python already allowed nested scopes, so the access to outer variables was necessary for consistency:

>...your argument is more of an argument against PEP 227 than what I am proposing.
>Again, today's Python already allows a developer to have deep nested scopes. [2]

Other objections cite that there are not enough non-trivial use cases to warrant a new keyword, especially considering there are already ways to work around the issue by using classes as namespaces or simply wrapping the value in a mutable object like a list. [4]

However, despite the resistance to this proposal, there was a critical mass of people could simply not let go of the inconsistency created by the lack of functionality, as summarized by Guido in this quote:

>I think the needs are actually pretty simple. Python currently doesn't allow assignment to variables in an outer  
>non-global scope, and people have shown by their behavior that they cannot get used to this (otherwise the debate  
>would have fizzled by now). [5]


Once the PEP was actually implemented, there were complaints regarding inability to reassign a value at the time of declaration of the nonlocal variable. A second line or a comma separating the declaration from the reassignment was needed. For example, "nonlocal x += 1" fails with a syntax error but "nonlocal x; x+=1" works. The first statment is clearer to the reader that it is incrementing a nonlocal variable. There was some dispute over whether or not this should be corrected. However, it turned out that this was just a bug in the language implementation. The syntax "nonlocal x += 1" was intended to be correct. Thus far, the bug is still not fixed. [6]

The bug is in the grammar of the PEP which attempts to allow for multiple declarations with a single use of nonlocal, eg. "nonlocal a, b = c, d = 1" [6] The potential patch fixes this by simplifying to grammar for both nonlocal and global declarations to allow for this form of short-hand reassignment. [6]


### Conclusion
PEP 3104 was accepted into the Python language for all versions of Python 3. Why did this PEP succeed where others fail? Based on the community feedback, it appears that there was a discrepancy between many programmers' intuition in cases where nested scope is employed and the actual functionality of the Python language. Resolving such discrepencies is philosophically important to Python, which states as a guiding principle :

>Explicit is better than implicit [7]

Also, the only real debate regarding the PEP was really a debate about nested scoping. Since statically nested scopes were already integregated, it was decided that full implementation was preferable to partial. PEP 3104 allows for that nested scope intuition to be realized in practice by using the "nonlocal" keyword. Although other solutions were proposed, such as using a new := operator or using a <function name>.nonlocal style syntax, this solution remained the most elegant and Pythonic in the eyes of the community.

### Citations
[1] K. Yee. (2009, January 19). PEP 3104 -- Access to Names in Outer Scopes [Online]. Available: http://www.python.org/dev/peps/pep-3104/

[2] A. Goo. (2006, February 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061568.html

[3] J. Hylton. (2006, Februray 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061602.html

[4] J. Carlson. (2006, February 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061577.html

[5] G. van Rossum. (2006, July 5). [Python-Dev] Explicit Lexical Scoping (pre-PEP?) [Online}. Available: http://mail.python.org/pipermail/python-dev/2006-July/066991.html

[6] B. Peterson (2008, October 23). Python Issue 4199 -- add shorthand global and nonlocal statements [Online]. Available: http://bugs.python.org/issue4199

[7] T. Peters. (2004, August 19). PEP 20 -- The Zen of Python [Online]. Available: http://www.python.org/dev/peps/pep-0020/

[8] Anonymous(2013, April 8). Python syntax and semantics [Online]. Available: http://en.wikipedia.org/wiki/Python_syntax_and_semantics#Closures


