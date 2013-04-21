David Baird
- What is the PEP working copy


In Python, one can declare functions within functions, which gives the appearance of a nested lexical scope. However, before PEP 3104 one could not modify variables outside the immediate local scope which defies the inuition of many programmers. For instance, in this code, taken from the PEP proposal site: [1]

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

Here, a programmer used to nested lexical scoping would assume the ability to modify the score variable in the nested function; however, Python did not support this functionality until this PEP was implemented in Python 3.  

The PEP proposes a new keyword 'nonlocal' to solve the scoping issue.  The keyword acts as a override for searching the local scope only, saying that the variable is not declared in this scope look in outer scopes.  Several other approaches to repair the problem as well as other keywords were purposed.  The override solution was selected because it provided a clearer meaning and did not have the potential to break existing code.  Among the other proposed keywords are global and outer. These two were less favourable because they either had other meaning, as in the case of global, or were a commonly used variable name, as with outer.  Nonlocal, while a little cumbersome, provided a good solution because it is very clear; it says exactly what it is doing. Thus, nonlocal was chosen as the proposed solution.




# ignore this stuff.
~~~~~
def a:
  x = 1
  def b:
    x += 1
  b()
~~~~~
~~~~~
def b:
  x += 1
def a:
  x = 1
  b()
~~~~~
