# from jinja2 import Template
# template = Template('Hello {{ name }}!')
# template.render(name='John Doe')


# return f"{klass}.{name}({args})"

X = """
if not php_defined({qname}):
    class {name}:
        pass
    # end class
# end if

class {name}({name}):
    __NAMESPACE__ = {qname}

    {stmts}
# end class"""

Y = f"""
if not php_defined({name}):
    class {name}:
        pass
    # end class
# end if

class {name}({name}):
    __NAMESPACE__ = {qname}

    {stmts}
# end class"""
