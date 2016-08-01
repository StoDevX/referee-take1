(from http://docs.python-guide.org/en/latest/writing/structure/#test-suite)

> To give the individual tests import context, create a tests/context.py file:

>     import os
>     import sys
>     sys.path.insert(0, os.path.abspath('..'))
>
>     import sample

> Then, within the individual test modules, import the module like so:

>     from .context import sample

> This will always work as expected, regardless of installation method.
