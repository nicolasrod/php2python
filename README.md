PHP2Python
==========

Convert PHP code to Python running under CGI (beta).

Requirements
------------

- PHP 7 with Package PHP-Parser installed (https://github.com/nikic/PHP-Parser#quick-start)
- Python 3 with Package goto-statement installed (https://pypi.org/project/goto-statement/)


Converting WordPress source code to Python
------------------------------------------

In the folder ./wordpress-5.4 there's a copy of WP and its convertion with the tool:

```
$ python3 php2py.py --keep-ast ./wordpress-5.4
```

This produces \*.py files, the \*.ast (because --keep-ast is used) and if there's any error (which should be at the moment) \*.errors.txt files.

In order to run the converted files you need to specify the full path of the PHP compatibility library in the *PHP2PY_COMPAT* environmental variable:

````
$ cd ./wordpress-5.4
$ PHP2PY_COMPAT=$HOME/php_compat.py python3 index.py
````

There are a few things left to finish in order to get a complete working converting without having to edit to converted code. I was waiting to tackle those before publishing the code but I'm not having much spare time left these days.

Any PR's and/or comments are more than welcome.

Roadmap
-------

- [x] Complete implementation of AST nodes transformation.
- [ ] Address limitations of Python language (single expression lambdas, assigns in statements).
- [ ] Finish implementing all of the supporting PHP functions to run WordPress.
- [ ] Rearrange AST nodes to simplify conversion.
- [ ] Refactor converted code to output Flask/Django code instead. Required an overhaul of the
  import mechanism.
- [ ] Massive cleanup.


Licence
-------

Copyright Nicolás Rodriguez (nicolasrod@google.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


