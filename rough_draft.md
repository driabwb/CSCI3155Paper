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

This was a compeletely unexpected result for many developers. A programmer used to nested lexical scoping would assume the ability to modify the score variable in the nested function. However, Python did not support this functionality until this PEP was implemented in Python 3. 
Although there are other ways of accessing the outer variables, they are not simple or direct. Python touts itself as being easy to read and ituitive, so in keeping these attributes a new resolution was needed. 

This PEP proposes a new keyword, 'nonlocal', to solve the scoping issue. The keyword acts as a override for searching the local scope only, saying that if the variable is not declared in this scope, look to the next outer scopes. Several other approaches to repair the problem, as well as other keywords, were proposed. The override solution was selected because it provided a clearer meaning and did not have the potential to break existing code. Among the other proposed keywords were global and outer. These two were less favorable because they either already had another meaning, as in the case of global, or were a commonly used variable name, as with outer. Nonlocal, while a little cumbersome, provided a good solution because it is very clear; it says exactly what it is doing. Thus, nonlocal was chosen as the proposed solution [1].

The added functionality was also important to the full implementation of closures in Python. Closures are generally associated with functional programming as they are basically a referencing environment that allows for higher-order functions. Although Python technically has supprted closures since version 2.2, the addition of the 'nonlocal' keyword makes them explicit. [8]

There were two main categories of solutions to this problem, those that suggested new syntax similar to JavaScript or Perl, where a name is bound (outer scope) s, and those that suggested new syntax where the name is used (inner scope) [1]. This PEP eventually went the way of the new syntax in the inner scope, primarily because the first method would cause function definitions to become context sensitive depending on what names are bound in an outer scope. In other words, situations could arise where the exact same line of code could produce different results based on the previous binding and could be a source of confusion. 

### Community reaction

Since PEP 227, there has been talk in the community of addressing the issue of reassigning free variables within a nested scope. As Almann T. Goo writes in the Python-Dev mailing list:


>My rationale is that with the advent of PEP 227 <http://www.python.org/peps/pep-0227.html>, Python has proper  
>nested lexical scopes, but can have undesirable behavior (especially with new developers) when a user makes  
>wants to make an assignment to a free variable within a nested function." [2]


In general, there was agreement that this quirk of the language was problematic, and many replies echoed this concern: "The lack of support for rebinding names in enclosing scopes is certainly a wart." [3]

Almann suggested the keyword "use" in this message quoted above, and in the course of the conversation more are suggested as well, including "outer", "extern", "common", and many others.There was considerable support for not adding a keyword and simply "abusing" the use of the global keyword whenever the situation arose. [5]

In the discussion thread, there were fewer arguments against the new proposal than for it. Most of the arguments against it were really just arguments against nested scoping in general, citing the lack of need for multiple levels of nested scopes. For example:


>Introducing these two new keywords is equivalent to encouraging nested scope use.  Right now nested scope use  
>is "limited" or "fraught with gotchas".  Adding the 'use' and 'scope' keywords to label levels of scopes for  
>name resolution will only encourage users to write closures which could have written better or not written  
>at all... [4]

Arguments against nested lexical scoping did not really seem to gain traction. Since PEP 227, Python has allowed for statically nested scopes and there was no movement remove such support. [1] 
Many were quick to point this out in their responses, stating that to Python already allowed nested scopes, so the access to outer variables was necessary for consistency:

>...your argument is more of an argument against PEP 227 than what I am >proposing. Again, today's Python already allows a developer to have deep >nested scopes. [2]

Other objections cite that there are not enough non-trivial use cases to warrant a new keyword, especially considering there are already ways to work around the issue by using classes or namespaces or simply wrapping the value in a mutable object like a list. [4] This word-around is displayed in the following code taken from the PEP proposal site: [1]

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
Despite the resistance to this proposal, there was a critical mass of people could simply not let go of the inconsistency created by the lack of functionality, as summarized by Guido in this quote:


>I think the needs are actually pretty simple. Python currently doesn't allow assignment to variables in an outer  
>non-global scope, and people have shown by their behavior that they cannot get used to this (otherwise the debate  
>would have fizzled by now). [5]


Once the PEP was actually implemented, there were complaints regarding inability to reassign a value at the time of declaration of the nonlocal variable. A second line or a comma separating the declaration from the reassignment was needed. For example,`nonlocal x += 1` fails with a syntax error but `nonlocal x; x+1` works. The first statment is clearer to the reader that it is incrementing a nonlocal variable. There was some dispute over whether or not this should be corrected. However, this just turned out to be a bug that is currently being patched. [6] 

The bug is in the grammar of the PEP which attempts to allow for multiple declarations with a single use of nonlocal, eg. `nonlocal a, b = c, d = 1` [6] The potential patch fixes this by simplifying to grammar for both nonlocal and global declarations to allow for this form of short-hand reassignment. [6]


### Conclusion
PEP 3104 was indeed accepted into the Python language for all versions of Python 3. Why did this PEP succeed where others fail? Based on the community feedback, it appears that there was a discrepancy between many programmers' intuition in cases where nested scope is employed and the actual functionality of the Python language. Resolving such discrepencies is philosophically important to Python, which states as a guiding principle 
>Explicit is better than implicit [7]

Also, the only real debate regarding the PEP was really a debate about nested scoping. Since statically nested scopes were already integregated, it was decided that full implementation was preferable to partial.  
PEP 3104 allows for that nested scope intuition to be realized in practice by using the 'nonlocal' keyword. Although other solutions were proposed, such as using a new := operator or using a <function name>.nonlocal style syntax, this solution remained the most elegant and Pythonic in the eyes of the community.

### Citations
[1] K. Yee. (2009, January 19). PEP 3104 -- Access to Names in Outer Scopes [Online]. Available: http://www.python.org/dev/peps/pep-3104/

[2] A. Goo. (2006, February 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061568.html

[3] J. Hylton. (2006, Februray 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061602.html

[4] J. Carlson. (2006, February 21). [Python-Dev] PEP for Better Control of Nested Lexical Scopes [Online]. Available: http://mail.python.org/pipermail/python-dev/2006-February/061577.html

[5] G. van Rossum. (2006, July 5). [Python-Dev] Explicit Lexical Scoping (pre-PEP?) [Online}. Available: http://mail.python.org/pipermail/python-dev/2006-July/066991.html

[6] B. Peterson (2008, October 23). Python Issue 4199 -- add shorthand global and nonlocal statements [Online]. Available: http://bugs.python.org/issue4199

[7] T. Peters. (2004, August 19). PEP 20 -- The Zen of Python [Online]. Available: http://www.python.org/dev/peps/pep-0020/

[8] Anonymous(2013, April 8). Python syntax and semantics [Online]. Available: http://en.wikipedia.org/wiki/Python_syntax_and_semantics#Closures


