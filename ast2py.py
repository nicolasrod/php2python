# coding: utf8

import json
import sys
import os.path
import traceback
import pindent
import ast
import argparse
import uuid
import re

from php_compat import PHP_FUNCTIONS
from functools import partial
from keyword import iskeyword

# TODO: s = '$a $b' => interpolate different types, do convertion!
# TODO: handle \\ namespaces in class names (php_is_callable for example). manually sometimes...


def _(x):
    return x.replace('\r', ' ').replace('\n', '\\n').strip()


def __(x):
    return re.sub('\n+', '\\n', x)


#  TODO: this is super inefficient. fix it!
def join_keys(vals):
    if not hasattr(join_keys, 'expr'):
        join_keys.expr = re.compile('{([^}]+)}, {([^}]+)}')

    while True:
        r = join_keys.expr.subn(r'{\1, \2}', vals)
        vals = r[0]

        if r[1] == 0:
            break
    return vals


def is_valid_code(src):
    try:
        ast.parse(src.replace('\x00', ''))
    except:
        return False, traceback.format_exc()
    return True, None


def quote(x):
    x = x.replace("\\", "\\\\").replace('"', '\\"')
    if len(x.split('\n')) > 3:
        return f'"""{x}"""'
    x = x.replace('\n', '\\n').replace('\r', '\\r')
    return f'"{x}"'


def fix_interface(implements):
    return ''.join([x.strip() for x in implements.split(',')])


def remove_both_ends(ln, chars=(',', ' ')):
    l = len(ln)
    s = 0
    while s < l:
        if ln[s] not in chars:
            break
        s += 1
    l -= 1
    while l > 0:
        if ln[l] not in chars:
            break
        l -= 1
    return ln[s:l + 1]


def get_only_varname(var):
    varname, *_ = var.split('[')
    return varname


_php_globals = {
    '_GET': 'PHP_REQUEST',
    '_POST': 'PHP_POST',
    '_REQUEST': 'PHP_REQUEST',
    'GLOBALS': 'PHP_GLOBALS',
    '_SERVER': 'PHP_SERVER',
    '_COOKIE': 'PHP_COOKIE',
    '_FILES': 'PHP_FILES',
    '_SESSION': 'PHP_SESSION',
    '_ENV': 'PHP_ENV',
    'this': 'self'
}

fix_comment_line = partial(remove_both_ends, chars=('*', '/', ' ', '\t'))


class AST:
    def __init__(self):
        self.comments = {}
        self.frames = []
        self.pre_code = []
        self.post_code = []
        self.namespace = []
        self.globals = []
        self.parents = []
        self.last_namespace = None
        self.static_vars = {}
        self.channel_data = None

    def push_namespace(self, name):
        self.last_name = name

    def add_namespace(self, name):
        if self.last_namespace is not None:
            return '.'.join([self.last_namespace, name])
        else:
            return name

    def pop_namespace(self):
        self.last_name = None

    def push_param_init(self, name, value):
        if self.channel_data is None:
            self.channel_data = []

        if value is not None:
            self.channel_data.append(
                f'if {name} is None:\n{name} = {value}\n# end if')

    def pop_params_init(self):
        if self.channel_data is None:
            return ''
        param_init = '\n'.join(self.channel_data)
        self.channel_data = None
        return param_init

    def get_parent(self, level=1):
        try:
            return self.parents[-1 * (level + 1)]
        except:
            return None

    def push_code(self, code, is_pre=False):
        if is_pre:
            self.pre_code.append(code)
        else:
            self.post_code.append(code)

    def pop_code(self, is_pre=False):
        if is_pre:
            code = '\n'.join(self.pre_code)
            self.pre_code = []
        else:
            code = '\n'.join(self.post_code)
            self.post_code = []
        return code

    def decorator_goto(self, node):
        goto_nodes = self.get_nodes_of_type(node, 'Stmt_Goto')
        return '@with_goto' if len(list(goto_nodes)) != 0 else ''

    def get_nodes_of_type(self, node, name=('Expr_Assign', 'Expr_AssignRef')):
        if isinstance(node, list):
            for dst in node:
                yield from self.get_nodes_of_type(dst, name)

        if node is None:
            return

        if 'nodeType' not in node:
            return

        name = [name] if isinstance(name, str) else name

        for i in name:
            if node['nodeType'] == i:
                yield node

        for item in node.keys():
            dst = node.get(item)

            if isinstance(dst, (dict, list)):
                yield from self.get_nodes_of_type(dst, name)

    def get_global_access_for(self, node):
        _vars = []
        tmp = _php_globals.values()
        for assign in self.get_nodes_of_type(node):
            varname = get_only_varname(self.parse(assign['var']))

            if varname in tmp:
                if varname not in _vars:
                    _vars.append(varname)

        return f"global {', '.join(_vars)}" if _vars else ''

    def with_docs(self, node, res):
        docs = self.parse_docs(node)

        if len(docs.strip()) != 0:
            docs = '\n\n' + docs

        if not isinstance(res, list):
            return f'{docs}{res}\n'

        res = '\n'.join(res)
        return f'{docs}{res}\n'

    def fix_assign_cond(self, node, name='cond', join_char='\n', var_tag='var', assign_tag=None):
        if node[name] is None:
            return '', '', ''

        if assign_tag is None:
            assign_tag = ('Expr_Assign', 'Expr_AssignRef', 'Expr_PostInc', 'Expr_PostDec'
                          'Expr_AssignOp_Concat', 'Expr_PreInc', 'Expr_PreDec')  # TODO: assign could be pre or post expr!

        if isinstance(node[name], list):
            cond = self.parse_children(node, name, ', ')
        else:
            cond = self.parse(node[name])

        exprs = cond
        assigns = []

        for n in self.get_nodes_of_type(node[name], assign_tag):
            assign = self.parse(n)
            var = self.parse(n[var_tag])
            cond = cond.replace(assign, var)
            exprs = exprs.replace(f'{var} = ', '').replace(
                f'{var} -= ', '').replace(f'{var} += ', '')
            assigns.append(assign)

        if join_char is None:
            return cond, assigns, exprs
        else:
            return cond, join_char.join(assigns), exprs

    def _binary_op(self, node, t, left='left', right='right'):
        lhs = self.parse(node[left])
        rhs = self.parse(node[right])
        return t.format(**locals())

    @staticmethod
    def pass_if_empty(data):
        if len(data.strip()) == 0:
            return 'pass'
        return data

    def is_inside_block(self):
        return len(self.frames) != 0

    def is_last_block(self, block):
        if len(self.frames) == 0:
            return False

        last_block = self.frames[-1].lower().strip()
        if isinstance(block, list):
            return last_block in [x.lower.strip() for x in block]
        return last_block == block.lower().strip()

    def is_inside_of_any(self, block):
        if len(self.frames) == 0:
            return False

        if isinstance(block, list):
            blocks = [x.lower().strip() for x in block]
            for frame in self.frames:
                if frame.lower().strip() in blocks:
                    return True
            return False
        return block.lower().strip() in [
            x.lower().strip() for x in self.frames
        ]

    def is_inside_of_Expr(self):
        if len(self.frames) == 0:
            return False

        return any([x.startswith('Expr_') for x in self.frames[:-1]])

    def fix_variables(self, name):
        # if '[' in name:
        #    return name

        if name in _php_globals:
            return _php_globals[name]

        if iskeyword(name) or name.lower() in ['end', 'open', 'file', 'len', 'self']:
            return f'{name}_'

        wns = self.add_namespace(name)
        if wns in self.static_vars:
            return wns
        return f'{name}_'

    def fix_property(self, name):
        if iskeyword(name) or name.lower() in ['end', 'open', 'file', 'len', 'self']:
            return f'{name}_'

        wns = self.add_namespace(name)
        if wns in self.static_vars:
            return wns
        return f'{name}'

    @staticmethod
    def fix_method(name):
        name = name.lower().strip()
        if name == '__construct':
            return '__init__'
        if name == '__destruct':
            return '__del__'
        if iskeyword(name):
            return f'{name}_'
        return name

    @staticmethod
    def fix_constant(name):
        tmp = name.lower().strip()
        if tmp == 'false':
            return 'False'
        if tmp == 'true':
            return 'True'
        if tmp == 'null':
            return 'None'
        return name

    def Expr_BitwiseNot(self, node):
        expr = self.parse(node['expr'])
        return f'(1 << ({expr}).bit_length()) - 1 - {expr}'

    def Expr_Assign(self, node):
        lhs = self.parse(node['var'])

        if self.is_inside_of_any(['Stmt_If', 'Stmt_Else']):
            rhs, assigns, _ = self.fix_assign_cond(node, 'expr')
        else:
            rhs = self.parse(node['expr'])

        return f'{lhs} = {rhs}'

    def Expr_AssignRef(self, node):
        return self._binary_op(node, '{lhs} = {rhs}', 'var', 'expr')

    def Expr_AssignOp_Concat(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} += {rhs}')

    def Expr_AssignOp_Plus(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} += {rhs}')

    def Expr_AssignOp_Minus(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} -= {rhs}')

    def Expr_AssignOp_Mul(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} *= {rhs}')

    def Expr_AssignOp_Mod(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} %= {rhs}')

    def Expr_AssignOp_BitwiseOr(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} |= {rhs}')

    def Expr_AssignOp_BitwiseXor(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} ^= {rhs}')

    def Expr_BinaryOp_BitwiseXor(self, node):
        return self._binary_op(node, t='{lhs} ^ {rhs}')

    def Expr_AssignOp_BitwiseAnd(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} &= {rhs}')

    def Expr_BinaryOp_Concat(self, node):
        return self._binary_op(node, t='{lhs} + {rhs}')

    def Expr_BinaryOp_Mul(self, node):
        return self._binary_op(node, t='{lhs} * {rhs}')

    def Expr_BinaryOp_Mod(self, node):
        return self._binary_op(node, t='{lhs} % {rhs}')

    def Expr_BinaryOp_Div(self, node):
        return self._binary_op(node, t='{lhs} / {rhs}')

    def Expr_BinaryOp_Plus(self, node):
        return self._binary_op(node, t='{lhs} + {rhs}')

    def Expr_BinaryOp_Pow(self, node):
        return self._binary_op(node, t='{lhs} ^ {rhs}')

    def Expr_BinaryOp_Minus(self, node):
        return self._binary_op(node, t='{lhs} - {rhs}')

    def Expr_BinaryOp_BooleanOr(self, node):
        return self._binary_op(node, t='{lhs} or {rhs}')

    def Expr_BinaryOp_BooleanAnd(self, node):
        return self._binary_op(node, t='{lhs} and {rhs}')

    def Expr_BinaryOp_LogicalOr(self, node):
        return self._binary_op(node, t='{lhs} or {rhs}')

    def Expr_BinaryOp_LogicalXor(self, node):
        return self._binary_op(node, t='bool({lhs}) != bool({rhs})')

    def Expr_BinaryOp_LogicalAnd(self, node):
        return self._binary_op(node, t='{lhs} and {rhs}')

    def Expr_BinaryOp_Equal(self, node):
        return self._binary_op(node, t='{lhs} == {rhs}')

    def Expr_BinaryOp_NotEqual(self, node):
        return self._binary_op(node, t='{lhs} != {rhs}')

    def Expr_BinaryOp_Identical(self, node):
        return self._binary_op(node, t='{lhs} == {rhs}')

    def Expr_BinaryOp_NotIdentical(self, node):
        return self._binary_op(node, t='{lhs} != {rhs}')

    def Expr_BinaryOp_Greater(self, node):
        return self._binary_op(node, t='{lhs} > {rhs}')

    def Expr_BinaryOp_GreaterOrEqual(self, node):
        return self._binary_op(node, t='{lhs} >= {rhs}')

    def Expr_BinaryOp_Smaller(self, node):
        return self._binary_op(node, t='{lhs} < {rhs}')

    def Expr_BinaryOp_SmallerOrEqual(self, node):
        return self._binary_op(node, t='{lhs} <= {rhs}')

    def Expr_BinaryOp_BitwiseOr(self, node):
        return self._binary_op(node, t='{lhs} | {rhs}')

    def Expr_BinaryOp_BitwiseAnd(self, node):
        return self._binary_op(node, t='{lhs} & {rhs}')

    def Expr_BinaryOp_ShiftLeft(self, node):
        return self._binary_op(node, t='{lhs} << {rhs}')

    def Expr_BinaryOp_ShiftRight(self, node):
        return self._binary_op(node, t='{lhs} >> {rhs}')

    def Expr_BinaryOp_Coalesce(self, node):
        return self._binary_op(node,
                               t='({lhs} if {lhs} is not None else {rhs})')

    def Expr_AssignOp_Div(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} /= {rhs}')

    def Expr_AssignOp_ShiftLeft(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} <<= {rhs}')

    def Expr_AssignOp_ShiftRight(self, node):
        return self._binary_op(node,
                               left='var',
                               right='expr',
                               t='{lhs} >>= {rhs}')

    def Expr_BinaryOp_Spaceship(self, node):
        return self._binary_op(
            node, t='(0 if {lhs} == {rhs} else 1 if {lhs} > {rhs} else -1)')

    def Expr_ArrayDimFetch(self, node):
        var = self.parse(node['var'])
        dim = self.parse(node['dim'])
        return f'{var}[{dim or -1}]'

    def Stmt_Const(self, node):
        return self.parse_children(node, 'consts', '\n')

    def Stmt_TraitUse(self, node):  #  TODO: check this!
        return ''

    def Stmt_Declare(self, node):  #  TODO: check this!
        return ''

    def Expr_Variable(self, node):
        return self.fix_variables(self.parse(node['name']).replace('\n', ''))

    def VarLikeIdentifier(self, node):
        name = self.fix_property(node['name'])
        return f'{name}'

    def Scalar_LNumber(self, node):
        val = node['value']
        return f'{val}'

    def Scalar_DNumber(self, node):
        return self.Scalar_LNumber(node)

    def Expr_UnaryMinus(self, node):
        expr = self.parse(node['expr'])
        return f'-{expr}'

    def Expr_UnaryPlus(self, node):
        expr = self.parse(node['expr'])
        return f'+{expr}'

    def Scalar_String(self, node):
        return quote(node['value'])

    def Expr_List(self, node):
        return self.parse_children(node, 'items', ', ')

    def Expr_StaticCall(self, node):
        args = self.parse_children(node, 'args', ', ')
        klass = self.parse(node['class']).strip()
        name = self.fix_method(self.parse(node['name']).strip())

        if klass == "parent":
            klass = "super()"

        return f'{klass}.{name}({args})'

    def Expr_ShellExec(self, node):
        cmd = quote(self.parse_children(node, 'parts', ' '))
        return f'php_exec({cmd})'

    def Name_FullyQualified(self, node):
        name = self.parse_children(node, 'parts', '.')
        return f'{name}'

    def Expr_StaticPropertyFetch(self, node):
        return self._binary_op(node,
                               left='class',
                               right='name',
                               t='{lhs}.{rhs}')

    def Expr_Instanceof(self, node):
        lhs = quote(self.parse(node['class']))
        rhs = self.parse(node['expr'])
        return f'type({rhs}).__name__ == {lhs}'

    def _pre_post_varname(self, node):
        return

    def Expr_PreInc(self, node):
        var = self.parse(node['var'])

        if not self.is_inside_of_Expr():
            return f'{var} += 1'
        else:
            self.push_code(f'{var} += 1', True)
            return f'{var}'

    def Expr_PreDec(self, node):
        var = self.parse(node['var'])

        if not self.is_inside_of_Expr():
            return f'{var} -= 1'
        else:
            self.push_code(f'{var} -= 1', True)
            return f'{var}'

    def Expr_PostInc(self, node):
        var = self.parse(node['var'])

        if not self.is_inside_of_Expr():
            return f'{var} += 1'
        else:
            self.push_code(f'{var} += 1')
            return f'{var}'

    def Expr_PostDec(self, node):
        var = self.parse(node['var'])

        if not self.is_inside_of_Expr():
            return f'{var} -= 1'
        else:
            self.push_code(f'{var} -= 1')
            return f'{var}'

    def Expr_Yield(self, node):
        k = self.parse(node['key'])
        v = self.parse(node['value'])

        if k is None:
            return f'yield from php_yield({v})'
        return f'yield from php_yield({{ {k}: {v} }})'

    def Expr_YieldForm(self, node):
        # TODO: finish this node!
        k = self.parse(node['key'])
        v = self.parse(node['value'])

        if k is None:
            return f'yield from php_yield({v})'
        return f'yield from php_yield({{ {k}: {v} }})'

    def Stmt_Namespace(self, node):
        name = self.parse(node['name']).replace('.', '_')
        qname = quote(name)
        self.push_namespace(name)
        stmts = self.parse_children(node, 'stmts', '\n')
        self.pop_namespace()

        if node['name'] is None:
            #  Global namespace
            return f'{stmts}\n'

        return self.with_docs(
            node, f'''
if not php_defined({qname}):
    class {name}:
        pass
    # end class
# end if

class {name}({name}):
    _namespace__ = {qname}

    {stmts}
# end class''')

    def Stmt_Class(self, node):
        extends = ''
        implements = ''

        if 'extends' in node and node['extends'] is not None:
            extends = self.parse_children(node, 'extends', ', ')

        if 'implements' in node and node['implements'] is not None:
            implements = fix_interface(
                self.parse_children(node, 'implements', ', '))

        supers = remove_both_ends(','.join([extends, implements]))
        name = self.parse(node['name'])
        self.push_namespace(name)
        stmts = self.pass_if_empty(self.parse_children(node, 'stmts', '\n'))
        self.pop_namespace()
        return self.with_docs(
            node, f'''
class {name}({supers}):
    {stmts}
# end class {name}
''')

    def Comment_Doc(self, node):
        if self.comments.get(node['tokenPos'], None) is None:
            self.comments[node['tokenPos']] = True
            lines = [
                f'#// {fix_comment_line(x)}' for x in node['text'].split('\n')
                if len(x.strip())
            ]
            return '\n'.join(lines)
        return None

    def Stmt_Interface(self, node):
        return self.Stmt_Class(node)

    def Stmt_Trait(self, node):
        return self.Stmt_Class(node)

    def Comment(self, node):
        return self.Comment_Doc(node)

    def Expr_Clone(self, node):
        expr = self.parse(node['expr'])
        return f'copy.deepcopy({expr})'

    def Stmt_Continue(self, node):
        return 'continue'

    def Stmt_Throw(self, node):
        expr = self.parse(node['expr'])
        return f'raise {expr}'

    def Stmt_Goto(self, node):
        name = self.parse(node['name'])
        return f'goto .{name}'

    def Stmt_Label(self, node):
        name = self.parse(node['name'])
        return f'label .{name}'

    def Stmt_Finally(self, node):
        stmts = self.parse_children(node, 'stmts', '\n')
        return '''finally:
        {stmts}'''

    def Stmt_Function(self, node):
        name = self.parse(node['name'])

        self.push_namespace(name)
        params = self.parse_children(node, 'params', ', ').replace(' = ', '=')
        self.pop_namespace()

        stmts = self.pass_if_empty(self.parse_children(node, 'stmts', '\n'))

        if params.find('*') == -1:
            params = remove_both_ends(params + ', *_args_')

        return self.with_docs(
            node, f'''
{self.decorator_goto(node)}
def {name}({params}):
    {self.pop_params_init()}
    {self.get_global_access_for(node['stmts'])}
    {stmts}
# end def {name}
'''.replace('\n\n', '\n'))

    def Expr_Closure(self, node):
        # TODO: add default values in the lambda
        params = self.parse_children(node, 'params', ', ')
        stmts = self.parse_children(node, 'stmts', '\n').strip()
        global_access = self.get_global_access_for(node['stmts'])

        if len(node['stmts']) < 2:
            if stmts.lower().startswith("return "):
                stmts = stmts[6:]
            return f'(lambda {params}: {stmts})'

        closure_id = str(uuid.uuid4()).replace('-', '')[:8]
        name = f'_closure_{closure_id}'
        self.push_code(
            f'''
def {name}({params}):
    {self.pop_params_init()}
    {global_access}
    {stmts}
# end def {name}''', True)
        return f'(lambda *args, **kwargs: {name}(*args, **kwargs))'

    def Stmt_ClassMethod(self, node):
        name = self.fix_method(self.parse(node['name']))
        self.push_namespace(name)
        params = remove_both_ends(
            'self, ' + self.parse_children(node, 'params', ', ').replace(' = ', '='))
        stmts = self.pass_if_empty(self.parse_children(node, 'stmts', '\n'))
        self.pop_namespace()
        global_access = self.get_global_access_for(node['stmts'])
        decorators = '\n'.join([
            '@classmethod' if node['flags'] == 9 else '',
            self.decorator_goto(node)
        ])
        return self.with_docs(
            node, f'''
{decorators}
def {name}({params}):
    {self.pop_params_init()}
    {global_access}
    {stmts}
# end def {name}
''')

    def Param(self, node):
        var = self.parse(node['var'])
        if node['variadic']:
            return f'*{var}'

        default = self.parse(node['default'])

        if node['default'] is not None and node['default']['nodeType'].startswith('Expr_'):
            self.push_param_init(var, default)
            return f'{var}=None'
        return f'{var}={default}'

    def Name(self, node):
        return '.'.join(node['parts'])

    def Stmt_Property(self, node):
        return self.with_docs(node, self.parse_children(node, 'props', ', '))

    def Stmt_PropertyProperty(self, node):
        name = self.parse(node['name'])
        default = 'Array()' if node['default'] is None else self.parse(
            node['default'])
        return f'{name} = {default}'

    def Stmt_Expression(self, node):
        return self.with_docs(node, self.parse(node['expr']))

    def Expr_Print(self, node):
        expr = self.parse(node['expr'])
        return self.with_docs(node, f'php_print({expr})')

    def Stmt_Use(self, node):
        #  TODO: include class if not defined instead!
        uses = self.parse_children(node, 'uses')
        return self.with_docs(node, '\n'.join(uses))

    def Expr_PropertyFetch(self, node):
        var = self.parse(node['var'])
        name = self.fix_property(self.parse(node['name']))
        return f'{var}.{name}'

    def Stmt_Nop(self, node):
        return 'pass' if self.is_inside_block() else ''

    def Expr_Empty(self, node):
        expr = self.parse(node['expr'])
        return f'php_empty(lambda : {expr})'

    def Expr_Eval(self, node):
        expr = self.parse(node['expr'])
        return self.with_docs(node,
                              f'''exec(compile({expr}, 'string', 'exec')''')

    def Expr_Isset(self, node):
        _vars = self.parse_children(node, 'vars')
        expr = ' and '.join(
            [f'php_isset(lambda : {v})' for v in _vars if v is not None])
        return f'({expr})'

    def Stmt_UseUse(self, node):
        #  TODO: maybe a load class hook here??
        klass_var = node['name']['parts'][-1]
        klass = self.parse(node['name'])
        alias = node['alias']
        qklass = quote(klass)

        if alias is None:
            return f'{klass_var} = php_new_class({qklass}, lambda *args, **kwargs: {klass}(*args, **kwargs))'
        return f'{alias} = php_new_class({qklass}, lambda *args, **kwargs: {klass}(*args, **kwargs))'

    def Stmt_InlineHTML(self, node):
        val = quote(node['value'])
        return self.with_docs(node, f'php_print({val})')

    def Stmt_Foreach(self, node):
        kvs = remove_both_ends(','.join([
            self.parse(node['keyVar']) or '',
            self.parse(node['valueVar']) or ''
        ]))
        expr = self.parse(node['expr'])
        stmts = self.pass_if_empty(self.parse_children(node, 'stmts', '\n'))
        return self.with_docs(
            node, f'''
for {kvs} in {expr}:
    {stmts}
# end for
''')

    def Stmt_For(self, node):
        cond, assigns, _ = self.fix_assign_cond(node)
        cond = 'True' if len(cond.strip()) == 0 else cond

        init = self.parse_children(node, 'init', '\n ')
        loop = self.parse_children(node, 'loop', ', ')
        stmts = self.parse_children(node, 'stmts', '\n')
        return self.with_docs(
            node, f'''
{init}
while {cond}:
    {assigns}
    {stmts}
    {loop}
# end while
''')

    def Arg(self, node):
        return self.parse(node['value'])

    def Const(self, node):
        name = self.parse(node['name'])
        val = self.parse(node['value'])
        return f'{name} = {val}'

    def Scalar_MagicConst_Dir(self, node):
        return '__DIR__'

    def Scalar_MagicConst_Line(self, node):
        return '0'

    def Scalar_MagicConst_Method(self, node):
        return '__METHOD__'

    def Scalar_MagicConst_Class(self, node):
        return '__CLASS__'

    def Scalar_MagicConst_Function(self, node):
        return '__FUNCTION__'

    def Scalar_MagicConst_Namespace(self, node):
        return '_namespace__'

    def Expr_ArrowFunction(self, node):
        raise Exception('Not Implemented yet!')

    def Expr_AssignOp_Coalesce(self, node):
        raise Exception('Not Implemented yet!')

    def Expr_AssignOp_Pow(self, node):
        raise Exception('Not Implemented yet!')

    def Expr_Cast_Unset(self, node):
        raise Exception('Not Implemented yet!')

    def Expr_ClosureUse(self, node):
        raise Exception('Not Implemented yet!')

    def NullableType(self, node):
        raise Exception('Not Implemented yet!')

    def Name_Relative(self, node):
        raise Exception('Not Implemented yet!')

    def Scalar_MagicConst_Trait(self, node):
        raise Exception('Not Implemented yet!')

    def Stmt_ClassLike(self, node):
        raise Exception('Not Implemented yet!')

    def Stmt_TraitUseAdaptation_Alias(self, node):
        raise Exception('Not Implemented yet!')

    def Stmt_TraitUseAdaptation_Precedence(self, node):
        raise Exception('Not Implemented yet!')

    def UnionType(self, node):
        raise Exception('Not Implemented yet!')

    def Expr_Include(self, node):
        expr = self.parse(node['expr']).strip()
        once = int(node["type"]) == 4
        return self.with_docs(node, f'php_include_file({expr}, once={once})')

    def Expr_BooleanNot(self, node):
        expr = self.parse(node['expr'])
        return f'(not {expr})'

    def Expr_FuncCall(self, node):
        args = self.parse_children(node, 'args', ', ')
        fn = self.parse(node['name']).strip()

        if fn.lower() == 'get_locals':
            fn = 'php_get_locals(locals(), inspect.currentframe()   .f_code.co_varnames)'
        if fn.lower() == 'compact':
            fn = 'php_compact'
            args = args.replace('",', '_",')
            args = re.sub('"$', '_"', args)
        else:
            fn = f'php_{fn}' if fn in PHP_FUNCTIONS else fn

        return f'{fn}({args})'

    def Expr_ConstFetch(self, node):
        return self.fix_constant(self.parse(node['name']))

    def Identifier(self, node):
        return node['name']

    def Expr_ClassConstFetch(self, node):
        klass = self.parse(node['class'])
        name = self.fix_property(self.parse(node['name']))
        return f'{klass}.{name}'

    def Scalar_EncapsedStringPart(self, node):
        val = _(quote(node['value']))
        return f'{val}'

    # TODO: change for f'{variable}'
    # TODO: take into account parts' type!
    def Scalar_Encapsed(self, node):
        return ' + '.join([f'str({_(self.parse(x))})' for x in node['parts']])

    def Stmt_Echo(self, node):
        expr = self.parse_children(node, 'exprs', ', ')
        return self.with_docs(node, f'php_print({expr})')

    def Stmt_Static(self, node):
        _vars = self.parse_children(node, 'vars', '\n ')
        return f'{_vars}'

    def Stmt_StaticVar(self, node):
        name = self.parse(node['var'])
        self.static_vars[self.add_namespace(name)] = True
        var = self.parse(node['var'])
        def_ = self.parse(node['default'])
        return f'{var} = {def_}'

    def Expr_Exit(self, node):
        code = self.parse(node['expr']) or 0

        if isinstance(code, str):
            return self.with_docs(node, f'php_print({code})\nphp_exit()')
        return self.with_docs(node, f'php_exit({code})')

    def Expr_MethodCall(self, node):
        var = self.parse(node['var'])
        name = self.fix_method(self.parse(node['name']))
        args = self.parse_children(node, 'args', ', ')
        return f'{var}.{name}({args})'

    def Expr_New(self, node):
        klass = self.parse(node['class'])
        args = self.parse_children(node, 'args', ', ')
        is_variable = len(
            list(self.get_nodes_of_type(node['class'], 'Expr_Variable'))) != 0

        if is_variable:
            return f'php_new_class({klass}, lambda : {{**locals(), **globals()}}[{klass}]({args}))'

        qklass = quote(klass)
        return f'php_new_class({qklass}, lambda : {klass}({args}))'

    def Stmt_If(self, node):
        stmts = self.pass_if_empty(self.parse_children(node, 'stmts', '\n'))
        elseifs = self.parse_children(node, 'elseifs', '\n')
        else_ = '' if node['else'] is None else self.parse(node['else'])
        else_ = f'else:\n{else_}' if len(else_) != 0 else ''
        cond, assigns, _ = self.fix_assign_cond(node)
        return self.with_docs(
            node, f'''
{assigns}
if {cond}:
    {stmts}
{elseifs}
{else_}
# end if''')

    def Stmt_Else(self, node):
        return self.parse_children(node, 'stmts', '\n')

    def Stmt_ElseIf(self, node):
        _, assigns, exprs = self.fix_assign_cond(node)
        stmts = self.parse_children(node, 'stmts', '\n')
        return self.with_docs(node, f'elif {exprs}:\n{assigns}\n{stmts}')

    def Stmt_TryCatch(self, node):
        finally_ = self.parse_children(node, 'finally', '\n')
        stmts = self.pass_if_empty(self.parse_children(node, 'stmts', '\n'))
        catches = self.parse_children(node, 'catches', '\n')
        return self.with_docs(
            node, f'try: \n{stmts}\n{catches}\n{finally_}\n# end try')

    def Stmt_Catch(self, node):
        types_ = self.parse_children(node, 'types', ',')
        vars = self.parse(node['var'])
        stmts = self.pass_if_empty(self.parse_children(node, 'stmts', '\n'))
        return f'except {types_} as {vars}:\n{stmts}\n'

    def Stmt_HaltCompiler(self, node):
        # TODO: Finish this node!
        return f'''# here goes code: {node['remaining']}'''

    def Scalar_MagicConst_File(self, node):
        return '__FILE__'

    def Stmt_Return(self, node):
        expr, assigns, _ = self.fix_assign_cond(node, name='expr')

        if self.is_inside_of_any('Expr_Closure'):
            return f'return {expr}'

        if self.is_inside_of_any(['Stmt_Function', 'Stmt_ClassMethod']):
            return self.with_docs(node, f'{assigns}\nreturn {expr}')

        retval = f'php_set_include_retval({expr})' if len(expr) > 0 else ''
        return self.with_docs(node, f'{assigns}\n{retval}\nsys.exit(-1)')

    def Expr_Array(self, node):
        vals = self.parse_children(node, 'items')

        if len(vals) == 0:
            return 'Array()'

        values = join_keys(', '.join(vals))
        return f'Array({values})'

    def Expr_ArrayItem(self, node):
        key = self.parse(node['key'])
        value = self.parse(node['value'])

        if key is None:
            return value
        return f'{{{key}: {value}}}'

    def Expr_Cast_Array(self, node):
        expr = self.parse(node['expr'])
        return f'{expr}'

    def Expr_Cast_Object(self, node):
        expr = self.parse(node['expr'])
        return f'{expr}'

    def Expr_Cast_Bool(self, node):
        expr = self.parse(node['expr'])
        return f'php_bool({expr})'

    def Expr_Cast_Double(self, node):
        expr = self.parse(node['expr'])
        return f'php_float({expr})'

    def Expr_Cast_Int(self, node):
        expr = self.parse(node['expr'])
        return f'php_int({expr})'

    def Expr_Cast_String(self, node):
        expr = self.parse(node['expr'])
        return f'php_str({expr})'

    def Expr_ErrorSuppress(self, node):
        expr = self.parse(node['expr'])
        return f'php_no_error(lambda: {expr})'

    def Stmt_Unset(self, node):
        _vars = self.parse_children(node, 'vars')
        return '\n'.join([f'{x} = None' for x in _vars])

    def Stmt_Switch(self, node):
        var = self.parse(node['cond'])
        out = [f'for case in Switch({var}):']

        for i in node['cases']:
            case = self.parse(i['cond'])
            out.append(f'''if case({case or ''}):''')
            out.append(
                self.pass_if_empty(self.parse_children(i, 'stmts', '\n')))
            out.append('# end if')
        out.append('# end for')

        return self.with_docs(node, '\n'.join(out))

    def Stmt_Case(self, node):
        return self.parse(node)

    def Stmt_Break(self, node):
        return 'break'

    def Stmt_Global(self, node):
        _vars = self.parse_children(node, 'vars')
        varnames = '\nglobal '.join(_vars)
        qvarnames = ','.join([quote(x) for x in _vars])
        self.globals.extend(_vars)
        return self.with_docs(
            node, '\n'.join([
                f'global {varnames}', '', f'php_check_if_defined({qvarnames})'
            ]))

    def Expr_Ternary(self, node):
        cond = self.parse(node['cond'])
        else_var, else_assign, else_value = self.fix_assign_cond(node,
                                                                 name='else')
        if_var, if_assign, if_value = self.fix_assign_cond(node, name='if')

        if len(if_value) == 0:
            if_value = cond

        if len(if_assign) == 0 and len(else_assign) == 0:
            #  1 if 2 == 1 else 2
            return f'{if_value} if {cond} else {else_value}'
        elif len(if_assign) != 0 and len(else_assign) == 0:
            # sep = 1 if 2 == 1 else 2
            return f'{if_assign} if {cond} else {else_value}'
        elif len(if_assign) != 0 and len(else_assign) != 0:
            # sep = 1 if 2 == 1 else sep = 2
            # check if and else are the same variable, else turn into an if!
            if if_var == else_var:
                # sep = 1 if 2 == 1 else 2
                return f'{if_assign} if {cond} else {else_value}'
            else:
                return f'if {cond}:\n{if_assign}\nelse:\n{else_assign}\n# end if'

        return f'{if_value} if {cond} else {else_assign}'

    def Stmt_While(self, node):
        cond, assigns, _ = self.fix_assign_cond(node)
        stmts = self.pass_if_empty(self.parse_children(node, 'stmts', '\n'))
        return self.with_docs(
            node, f'''
while True:
    {assigns}
    if not ({cond}):
        break
    # end if
    {stmts}
# end while''')

    def Stmt_Do(self, node):
        stmts = self.parse_children(node, 'stmts', '\n')
        cond, assigns, _ = self.fix_assign_cond(node)
        return self.with_docs(
            node, f'''
while True:
    {stmts}
    {assigns}
    if {cond}:
        break
    # end if
# end while''')

    def Stmt_ClassConst(self, node):
        return '\n'.join([f'{x}' for x in self.parse_children(node, 'consts')])

    def parse_docs(self, node):
        comments = ''

        if ('attributes' in node) and ('comments' in node['attributes']):
            out = [
                getattr(self, x['nodeType'])(x)
                for x in node['attributes']['comments']
            ]
            out = [x for x in out if x is not None]
            comments = ('\n' + '\n'.join(out) + '\n').strip()

            if len(comments) != 0:
                comments += '\n'

        return comments

    def parse(self, node):
        if node is None:
            return None

        if not isinstance(node, (list, dict)):
            return node

        if len(node) == 0:
            return ''

        self.frames.append(node['nodeType'])
        self.parents.append(node)
        r = getattr(self, node['nodeType'])(node)
        self.parents.pop()

        pre_code = ''
        post_code = ''

        if len(self.frames) > 0 and self.frames[-1].startswith('Stmt_'):
            pre_code = self.pop_code(True).strip()
            if len(pre_code) > 0:
                pre_code += '\n'

            post_code = self.pop_code().strip()
            if len(post_code) > 0:
                post_code = f'\n{post_code}'

        self.frames.pop()
        code = '\n'.join(r) if isinstance(r, list) else r
        return f'{pre_code}{code}{post_code}'.strip()

    def parse_children(self, node, name, delim=None):
        if name not in node or node[name] is None:
            return ''

        if isinstance(node[name], list):
            r = [
                x for x in [self.parse(i) for i in node[name]] if x is not None
            ]

            if not isinstance(delim, str):
                return r

            if isinstance(r, list):
                return delim.join(r)
        return self.parse(node[name])


#  TODO: use simple templates for the conversion
def parse_ast(fname):
    try:
        with open(fname) as f:
            data = json.load(f)
    except:
        print(f'[-] Error parsing AST file {fname}')
        sys.exit(3)

    out = [
        '''#!/usr/bin/env python3
# coding: utf-8

if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if

'''
    ]

    parser = AST()

    for node in data:
        parsed = parser.parse(node)
        pcode = parser.pop_code()

        if parsed is not None:
            out.append(pcode)
            out.append(parsed)

    out.append('')
    src, errs = pindent.reformat_string(__('\n'.join(out)),
                                        stepsize=4,
                                        tabsize=4,
                                        expandtabs=1)
    valid, syn = is_valid_code(src)

    if len(errs) != 0 or syn is not None:
        with open(f'{os.path.splitext(fname)[0]}.errors.txt', 'w') as f:
            f.write(errs)
            f.write(syn or '')

    return src


def main():
    parser = argparse.ArgumentParser(
        description='Convert AST files to Python Code')
    parser.add_argument('ast_file', type=str)
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args()

    if not os.path.exists(args.ast_file):
        print(f'[-] File {args.ast_file} not found!')
        sys.exit(2)

    print(parse_ast(args.ast_file))


if __name__ == '__main__':
    main()
