David Baird
- What is the PEP working copy

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
