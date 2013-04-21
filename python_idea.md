## Pull request for language improvement proposal:

### Team:

- David Baird
- Ryan Reily
- Aaron Davis

### Intended Topic:

PEP 3104: Access to names in outer scopes
This PEP adds a new keyword in Python 3.x, nonlocal,
to refer to variables not in the local scope, but necessarily
at the global scope either. This changes brings Python closer
to true static nested scoping. Before this PEP, Python could
refer to a name in any enclosing scope, but only rebind a name
in the local scope or in the module-global scope.

Note: our three team members will probably work on different 
language proposals

### Sources (so far):

- http://www.python.org/dev/peps/pep-3104
- http://mail.python.org/pipermail/python-dev/2006-February/061568.html
- other threads in the python mailing list
- http://stackoverflow.com/questions/1261875/python-nonlocal-statement
- http://c2.com/cgi/wiki?DynamicScoping

### Code Example (from stackoverflow, link above):

```
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter
```

### TODO/Status of work

- [ ] Read email threads on this subject
- [ ] Research how this change is being used Python 3
- [ ] Collaborate with team on their papers
- [ ] Write rough draft
- [ ] Write final draft


