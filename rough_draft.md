# CSCI3155 Paper: PEP 3104 (Rough Draft)

## David Baird, Aaron Davis, Ryan Riley

### What and Why

This paper discusses Python Enhancement Proposal (PEP) 3104: Access to names in outer scopes. In Python, one can declare functions within functions, which gives the appearance of a nested lexical scope. However, before this PEP one could not actually modify variables not in the immediate local scope, which defied the intuition of many programmers who expected it. For instance, in this code, taken from the PEP proposal site: [1]

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

Here, a programmer used to nested lexical scoping would assume the ability to modify the score variable in the nested function. However, Python did not support this functionality until this PEP was implemented in Python 3.

This PEP proposes a new keyword, 'nonlocal', to solve the scoping issue. The keyword acts as a override for searching the local scope only, saying that if the variable is not declared in this scope, look to the next outer scopes. Several other approaches to repair the problem, as well as other keywords, were purposed. The override solution was selected because it provided a clearer meaning and did not have the potential to break existing code. Among the other proposed keywords were global and outer. These two were less favorable because they either already had another meaning, as in the case of global, or were a commonly used variable name, as with outer. Nonlocal, while a little cumbersome, provided a good solution because it is very clear; it says exactly what it is doing. Thus, nonlocal was chosen as the proposed solution [1].

There were two main categories of solutions to this problem, those that suggested new syntax where a name is bound (outer scope), and those that suggested new syntax where the name is used (inner scope) [1]. This PEP eventually went the way of the new syntax in the inner scope, primarily because the first method would cause function definitions to become context sensitive depending on what names are bound in an outer scope.

### Community reaction

Since PEP 227, there has been talk in the community of addressing the issue of reassigning free variables within a nested scope. As Almann T. Goo writes in the Python-Dev mailing list:


>My rationale is that with the advent of PEP 227 <http://www.python.org/peps/pep-0227.html>, Python has proper  
>nested lexical scopes, but can have undesirable behavior (especially with new developers) when a user makes  
>wants to make an assignment to a free variable within a nested function." [2]


In general, there was agreement that this quirk of the language was problematic, and many replies echoed this concern: "The lack of support for rebinding names in enclosing scopes is certainly a wart." [3]

Almann suggests the keyword "use" in this message quoted above, and in the course of the conversation more are suggested as well, including "outer", "extern", "common", and many others.

In the discussion thread, there were fewer arguments against the new proposal than for it. One lines of the arguments against it seemed to be against nested scoping in general:


>Introducing these two new keywords is equivalent to encouraging nested scope use.  Right now nested scope use  
>is "limited" or "fraught with gotchas".  Adding the 'use' and 'scope' keywords to label levels of scopes for  
>name resolution will only encourage users to write closures which could have written better or not written  
>at all... [4]


Other objections cite that there are not enough non-trivial use cases to warrent a new keyword, especially considering there are already ways to work around the issue by using classes to declare a kind of namespace [4]. But despite the resistance to this proposal, at the end of the day it seemed to be a need that a critical mass of people could not let go of, as summarized by Guido in this quote:


>I think the needs are actually pretty simple. Python currently doesn't allow assignment to variables in an outer  
>non-global scope, and people have shown by their behavior that they cannot get used to this (otherwise the debate  
>would have fizzled by now). [5]


- [ ] Insert here maybe some rationale about why the current solution is best?

### Conclusion

PEP 3104 was indeed accepted into the Python language for all versions of Python 3. Why did this PEP succeed where others fail? Based on the community feedback, it appears that there was a discrepancy between many programmers' intuition in cases where nested scope is employed, and the actual functionality of the Python language. This allows for that nested scope intuition to be realized in practice by using the 'nonlocal' keyword. Although other solutions were proposed, such as using a new := operator or using a <function name>.nonlocal style syntax, this solution remained the most elegant and Pythonic in the eyes of the community.

### Citations
[1] K. Yee. (2009, January 19). PEP 3104 -- Access to Names in Outer Scopes [Online]. Available: http://www.python.org/dev/peps/pep-3104/

[2] A. Goo. (2006, February 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061568.html

[3] J. Hylton. (2006, Februray 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061602.html

[4] J. Carlson. (2006, February 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061577.html

[5] G. van Rossum. (2006, July 5). [Python-Dev] Explicit Lexical Scoping (pre-PEP?) [Online}. Available: http://mail.python.org/pipermail/python-dev/2006-July/066991.html
