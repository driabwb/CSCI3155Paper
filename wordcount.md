# CSCI 3155 Rough Draft

### Introduction

This paper discusses Python Enhancement Proposel (PEP) 3104: Access to names in outer scopes.

### What is the PEP?

### Why implement this PEP?

In Python, one can declare functions within functions, which gives the appearance of a nested lexical scope. However, before this PEP one could not actually modify variables not in the immediate local scope, which defied the inuition of many programmers who expected it. For instance, in this code, taken from the PEP proposal site: [1]

Here, a programmer used to nested lexical scoping would assume the ability to modify the score variable in the nested function. However, Python did not support this functionality until this PEP was implemented in Python 3.

### Community reaction

Since PEP 227, there has been talk in the community of addressing the issue of reassigning free variables within a nested scope. As Alman T. Goo writes in the Python-Dev mailing list:

In general, there was agreement that this quirk of the language was problematic, and many replies echoed this concern: "The lack of support for rebinding names in enclosing scopes is certainly a wart." [3]

Almann suggests the keyword "use" in this message quoted above, and in the course of the converstaion more are suggested as well, including "outer", "extern", "common", and many others.

In the discussion thread, there were fewer arguments against the new proposal than for it. One lines of the arguments against it seemed to be against nested scoping in general:

Other objections cite that there are not enough non-trivial use cases to warrent a new keyword, esspecailly considering there are already ways to work around the issue by using classes to declare a kind of namespace [4]. But despite the resistence to this proposal, at the end of the day it seemed to be a need that a critical mass of people could not let go of, as summerized by Guido in this quote:

### Conclusion

### Citations
