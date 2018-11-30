# coding: utf8
import json
import sys
import os.path
import traceback
import subprocess
import pindent
import funcs

from functools import wraps, partial
from keyword import iskeyword

if len(sys.argv) < 2:
    print(f"[-] Usage: {sys.argv[0]} <AST_JSON_file>")
    sys.exit(1)

fname = sys.argv[1]

if not os.path.exists(fname):
    print(f"[-] File {fname} not found!")
    sys.exit(2)

try:
    with open(fname) as f:
        data = json.load(f)
except:
    print(f"[-] Error parsing JSON file {fname}")
    sys.exit(3)

def quote(x):
    return x.replace('"','\\"')

def _(x):
    return x.replace("\r", "").replace("\n", "\\n").strip()

def inside_of(block):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwds):
            AST._LAST_BLOCK = block
            rst = fn(*args, **kwds)
            AST._LAST_BLOCK = None
            return rst
        return wrapper
    return decorator

def _binary_op(node, t, left="left", right="right"):
    lhs = AST.parse(node[left])
    rhs = AST.parse(node[right])
    return t.format(**locals())

class AST:
    _COMMENTS = {}
    _LAST_BLOCK = None
        
    def fix_comment_line(ln):
        l = len(ln)
        pos = 0
        while True and pos < l:
            if ln[pos] not in ["*", "/", " "]:
                break
            pos += 1
        return ln[pos:]
        
    def fix_variables(name):
        if name in ["_GET", "_POST", "_REQUEST"]:
            return "request.form"
        if name == "_SERVER":
            return "request.environ"
        if name == "this":
            return "self"
        if iskeyword(name):
            return f"{name}_"
        return name

    def fix_method(name):
        if name == "__construct":
            return "__init__"
        if name == "__destruct":
            return "__del__"
        return name

    def fix_constant(name):
        if name.upper() == "FALSE":
            return "False"
        if name.upper() == "TRUE":
            return "True"
        if name.upper() == "NULL":
            return "None"
        return name

    # ===========================================================

    def Expr_BitwiseNot(node):
        expr = AST.parse(node["expr"])
        return f"(1 << {expr}.bit_length()) - 1 - {expr}"

    Expr_Assign = partial(_binary_op, left="var", right="expr", t="{lhs} = {rhs}") 
    Expr_AssignRef = Expr_Assign
    Expr_AssignOp_Concat = partial(_binary_op, left="var", right="expr", t="{lhs} += {rhs}")
    Expr_AssignOp_Plus = partial(_binary_op, left="var", right="expr", t="{lhs} += {rhs}")
    Expr_AssignOp_Minus = partial(_binary_op, left="var", right="expr", t="{lhs} -= {rhs}")
    Expr_AssignOp_Mul = partial(_binary_op, left="var", right="expr", t="{lhs} *= {rhs}")
    Expr_AssignOp_BitwiseOr = partial(_binary_op, left="var", right="expr", t="{lhs} |= {rhs}")
    Expr_AssignOp_BitwiseXor = partial(_binary_op, left="var", right="expr", t="{lhs} ^= {rhs}")
    Expr_BinaryOp_BitwiseXor = partial(_binary_op, t="{lhs} ^ {rhs}")
    Expr_AssignOp_BitwiseOr = partial(_binary_op, left="var", right="expr", t="{lhs} |= {rhs}")
    Expr_AssignOp_BitwiseAnd = partial(_binary_op, left="var", right="expr", t="{lhs} &= {rhs}")
    Expr_BinaryOp_Concat = partial(_binary_op, t="{lhs} + {rhs}")
    Expr_BinaryOp_Mul = partial(_binary_op, t="{lhs} * {rhs}")
    Expr_BinaryOp_Mod = partial(_binary_op, t="{lhs} % {rhs}")
    Expr_BinaryOp_Div = partial(_binary_op, t="{lhs} / {rhs}")
    Expr_BinaryOp_Plus = partial(_binary_op, t="{lhs} + {rhs}")
    Expr_BinaryOp_Minus = partial(_binary_op, t="{lhs} - {rhs}")
    Expr_BinaryOp_BooleanOr = partial(_binary_op, t="{lhs} or {rhs}")
    Expr_BinaryOp_BooleanAnd = partial(_binary_op, t="{lhs} and {rhs}")
    Expr_BinaryOp_LogicalOr = partial(_binary_op, t="{lhs} or {rhs}")
    Expr_BinaryOp_LogicalXor = partial(_binary_op, t="bool({lhs}) != bool({rhs})")
    Expr_BinaryOp_LogicalAnd = partial(_binary_op, t="{lhs} and {rhs}")
    Expr_BinaryOp_Equal = partial(_binary_op, t="{lhs} == {rhs}")
    Expr_BinaryOp_NotEqual = partial(_binary_op, t="{lhs} != {rhs}")
    Expr_BinaryOp_Identical = partial(_binary_op, t="{lhs} == {rhs}")
    Expr_BinaryOp_NotIdentical = partial(_binary_op, t="{lhs} != {rhs}")
    Expr_BinaryOp_Greater = partial(_binary_op, t="{lhs} > {rhs}")
    Expr_BinaryOp_GreaterOrEqual = partial(_binary_op, t="{lhs} >= {rhs}")
    Expr_BinaryOp_Smaller = partial(_binary_op, t="{lhs} < {rhs}")
    Expr_BinaryOp_SmallerOrEqual = partial(_binary_op, t="{lhs} <= {rhs}")
    Expr_BinaryOp_BitwiseOr = partial(_binary_op, t="{lhs} | {rhs}")
    Expr_BinaryOp_BitwiseAnd = partial(_binary_op, t="{lhs} & {rhs}")
    Expr_BinaryOp_ShiftLeft = partial(_binary_op, t="{lhs} << {rhs}")
    Expr_BinaryOp_ShiftRight = partial(_binary_op, t="{lhs} >> {rhs}")
    Expr_AssignOp_Div = partial(_binary_op, left="var", right="expr", t="{lhs} /= {rhs}")
    Expr_AssignOp_ShiftLeft = partial(_binary_op, left="var", right="expr", t="{lhs} <<= {rhs}")
    Expr_AssignOp_ShiftRight = partial(_binary_op, left="var", right="expr", t="{lhs} >>= {rhs}")

    def Expr_ArrayDimFetch(node):
        var = AST.parse(node["var"])
        dim = AST.parse(node["dim"])
        if dim == None:
            dim = "-1"
        return f"{var}[{dim}]"

    def Expr_Variable(node):
        return AST.fix_variables(AST.parse(node["name"]).replace("\n", ""))
        
    def VarLikeIdentifier(node):
        return f"{node['name']}"

    def Scalar_LNumber(node):
        return f"{node['value']}"

    def Scalar_DNumber(node):
        return f"{node['value']}"

    def Expr_UnaryMinus(node):
        expr = AST.parse(node["expr"])
        return f"-{expr}" 

    def Scalar_String(node):
        value = quote(_(node["value"]))
        return f'"{value}"'
        
    def Expr_List(node):
        return AST.parse_children(node, "items", ", ")

    def Expr_StaticCall(node):
        args = AST.parse_children(node, "args", ", ")
        klass = AST.parse(node["class"]).strip()
        name = AST.parse(node["name"]).strip()
        return f"{klass}.{name}({args})"

    def Expr_ShellExec(node): #@@
        parts = AST.parse_children(node, "parts", " ")
        return f"import os; os.system('{parts}')"

    def Name_FullyQualified(node):
        parts = AST.parse_children(node, "parts", ".")
        return f"{parts}"

    Expr_StaticPropertyFetch = partial(_binary_op, left="class", right="name", t="{lhs}.{rhs}")
    Expr_Instanceof = partial(_binary_op, left="class", right="expr", 
        t="isinstance({rhs}, {lhs})")

    def Expr_PreInc(node):
        var = AST.parse(node["var"])
        return f"{var} += 1"

    def Expr_PreDec(node):
        var = AST.parse(node["var"])
        return f"{var} -= 1"

    def Expr_PostInc(node):
        var = AST.parse(node["var"])
        return f"{var} += 1"

    def Expr_PostDec(node):
        var = AST.parse(node["var"])
        return f"{var} -= 1"

    @inside_of("class")
    def Stmt_Class(node):
        # TODO: extends: null,
        # TODO: implements": [],
        name = AST.parse(node["name"]).strip()
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"class {name}:\n{stmts}\n# end class {name}\n"

    Stmt_Interface = Stmt_Class

    def Comment_Doc(node):
        if AST._COMMENTS.get(node["tokenPos"], None) is None:
            AST._COMMENTS[node["tokenPos"]] = True
            lines = [f"##// {AST.fix_comment_line(x)}" for x in node['text'].split("\n")]
            return "\n".join(lines)
        return None

    def Comment(node):
        return ""

    def Expr_Clone(node):
        expr = AST.parse(node['expr'])
        return f"{expr} # TODO: clone!"

    def Stmt_Continue(node):
        return "continue"

    def Stmt_Throw(node):
        return f"raise {AST.parse(node['expr'])}"

    @inside_of("def")
    def Stmt_Function(node):
        name = AST.parse(node["name"])
        params = AST.parse_children(node, "params", ", ")
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"def {name}({params}):\n{stmts}\n# end def {name}\n"
  
    def Expr_Closure(node):
        params = AST.parse_children(node, "params", ", ")
        stmts = AST.parse_children(node, "stmts", "; ")
        return f"lambda {params}: {stmts}"

    @inside_of("class_method")
    def Stmt_ClassMethod(node):
        name = AST.fix_method(AST.parse(node["name"]))
        params = AST.parse_children(node, "params", ", ")
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"def {name}({params}):\n{stmts}\n# end def {name}\n"

    def Param(node):
        # TODO: "variadic": false
        var = AST.parse(node["var"])
        default = AST.parse(node["default"])
        return f"{var} = {default}" 

    def Name(node):
        return ".".join(node["parts"])

    def Stmt_Property(node):
        return AST.parse_children(node, "props", ", ")

    def Stmt_PropertyProperty(node):
        name = AST.parse(node["name"])
        default = AST.parse(node["default"]) # TODO: check this!
        return f"{name} = {default}"

    def Stmt_Expression(node):
        return AST.parse(node["expr"])

    def Expr_Print(node):
        expr = AST.parse(node["expr"])
        return f"print({expr})"
        
    def Stmt_Use(node):
        uses = AST.parse_children(node, "uses")
        return "\n".join([f"exec(open({x}).read())({x})" for x in uses])

    def Expr_PropertyFetch(node):
        var = AST.parse(node["var"])
        name = AST.parse(node["name"])
        return f"{var}.{name}"
  
    def Stmt_Nop(node):
        return "pass"

    def Expr_Empty(node):
        expr = AST.parse(node["expr"])
        return f"({expr} is None)"
  
    def Expr_Isset(node):
        vars = AST.parse_children(node, "vars", ";")
        return f"""("{vars}" in  {{**globals(), **locals()}}) and ({vars} is not None)"""
    
    def Stmt_UseUse(node):
        return [AST.parse(node["name"])]

    def Stmt_InlineHTML(node):
        html = _(node["value"])
        return f'print(""" {html} """)'
  
    @inside_of("for")
    def Stmt_Foreach(node):
        value_var = AST.parse(node["valueVar"])
        expr = AST.parse(node["expr"])
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"for {value_var} in {expr}:\n{stmts}\n# end for"
     
    @inside_of("for")
    def Stmt_For(node):
        cond = AST.parse_children(node, "cond", ", ")
        init = AST.parse_children(node, "init", ", ")
        loop = AST.parse_children(node, "loop", ", ")
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"{init}\nwhile {cond}:\n{stmts}\n{loop}\n# end while"

    def Arg(node):
        return AST.parse(node["value"])

    def Const(node):
        name = AST.parse(node["name"])
        value = AST.parse(node["value"])
        return f"{name} = {value} # const"

    def Scalar_MagicConst_Dir(node):
        return "__DIR__"

    def Scalar_MagicConst_Line(node):
        return "0"

    def Scalar_MagicConst_Method(node):
        return "'__METHOD__'"

    def Scalar_MagicConst_Class(node):
        return "'__CLASS__'"

    def Scalar_MagicConst_Function(node):
        return "'__FUNCTION__'"

    def Expr_Include(node):
        expr = AST.parse(node["expr"]).strip()
        return f"php_include_file({expr})"

    def Expr_BooleanNot(node):
        expr = AST.parse(node["expr"])
        return f"(not {expr})"

    def Expr_FuncCall(node):
        args = AST.parse_children(node, "args")
        fn = AST.parse(node["name"]).strip()
        return funcs.to_python(fn, args)

    def Expr_ConstFetch(node):
        return AST.fix_constant(AST.parse(node["name"]))

    def Identifier(node):
        return node["name"]
 
    def Expr_ClassConstFetch(node):
        klass = AST.parse(node["class"])
        name = AST.parse(node["name"])
        return f"{klass}.{name}"

    def Scalar_EncapsedStringPart(node):
        value = _(node["value"])
        return f'"{value}"'

    def Scalar_Encapsed(node):
        return " + ".join([_(AST.parse(x)) for x in node["parts"]])

    def Stmt_Echo(node):
        expr = AST.parse_children(node, "exprs", ", ")
        return f'print({expr})'

    def Stmt_Static(node):
        vars = AST.parse_children(node, "vars", ", ")
        return f"{vars} #@@ TODO: static!"

    def Stmt_StaticVar(node):
        var = AST.parse(node["var"])
        default = AST.parse(node["default"])
        return f"{var} = {default}"

    def Expr_Exit(node):
        code = AST.parse(node["expr"])
        if isinstance(code, str):
            return f"print({code})\nsys.exit(0)" 
        return f"sys.exit({code or 0})"

    def Expr_MethodCall(node):
        var = AST.parse(node["var"])
        name = AST.parse(node["name"])
        args = AST.parse_children(node, "args", ", ")
        return f"{var}.{name}({args})"

    def Expr_New(node):
        klass = AST.parse(node["class"])
        args = AST.parse_children(node, "args", ", ")
        return f"{klass}({args})"

    @inside_of("if")
    def Stmt_If(node): 
        else_ = "" if node["else"] is None else AST.parse(node["else"])
        else_ = f"else:\n{else_}" if len(else_) != 0 else ""

        cond = AST.parse(node["cond"])
        stmts = AST.parse_children(node, "stmts", "\n")
        elseifs = AST.parse_children(node, "elseifs")
        return f"if {cond}:\n{stmts}\n{else_}\n# end if"

    def Stmt_Else(node):
        return AST.parse_children(node, "stmts", "\n")

    def Stmt_ElseIf(node):
        cond = AST.parse(node["cond"])
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"elif {cond}:\n{stmts}"
    
    @inside_of("try")
    def Stmt_TryCatch(node):
        finally_ = AST.parse_children(node, "finally", "\n")
        stmts = AST.parse_children(node, "stmts", "\n")
        catches = AST.parse_children(node, "catches", "\n")
        return f"try: \n{stmts}\n{catches}\n{finally_}\n# end try"

    def Stmt_Catch(node):
        types_ = AST.parse_children(node, "types", ",")
        vars = AST.parse(node["var"])
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"except {types_} as {vars}:\n{stmts}\n"
        
    def Stmt_HaltCompiler(node):
        return "# here goes code" #node["remaining"]

    def Scalar_MagicConst_File(node):
        return f"__file__"

    def Stmt_Return(node):
        expr = AST.parse(node["expr"])
        return f"return {expr}" 
    
    def Expr_Array(node): 
        vals = AST.parse_children(node, "items")
        
        if len(vals) == 0:
            return "[]"

        if vals[0].startswith("\xFF\xEE"):
            values = ", ".join([x[2:] for x in vals])
            return f"{{{values}}}"
        values = ", ".join(vals)
        return f"[{values}]"

    def Expr_ArrayItem(node):
        key = AST.parse(node["key"])
        value = AST.parse(node["value"])

        if key is None:
            return value
        return f"\xFF\xEE{key}: {value}"

    def Expr_Cast_Array(node):
        expr = AST.parse(node["expr"])
        return f"{expr}  ##@@ TODO: cast_array!"

    def Expr_Cast_Object(node):
        expr = AST.parse(node["expr"])
        return f"{expr}  ##@@ TODO: cast_object!"

    def Expr_Cast_Bool(node):
        expr = AST.parse(node["expr"])
        return f"bool({expr})"

    def Expr_Cast_Double(node):
        val = AST.parse(node["expr"])
        return f"double({val})"

    def Expr_ErrorSuppress(node):
        # TODO: wrap the expr in a Try block. 
        return AST.parse(node["expr"])

    def Stmt_Unset(node):
        vars = AST.parse_children(node, "vars")
        return "\n".join([f"{x} = None" for x in vars])

    def Expr_Cast_Array(node):
        expr = AST.parse(node["expr"])
        return f"str({expr})"
  
    @inside_of("switch")
    def Stmt_Switch(node):
        # TODO: clean this mess!
        var = AST.parse(node["cond"])
        kw = "if"
        out = []
        for i in node["cases"]:
            case = AST.parse(i["cond"])
            stmts = AST.parse_children(i, "stmts", "\n")
            
            condTxt = "else"
            if case is not None:
                condTxt = f"{kw} {var} == {case}"

            if len(stmts) != 0:
                out.append(f"{condTxt}:\n{stmts}")
            else:
                out.append(f"{condTxt} or \\")
                kw = ""
                continue

            if kw == "if" or kw == "":
                kw = "elif"
        out.append("# end if")
        return "\n".join(out)
        
    def Stmt_Case(node):
        return AST.parse(node)

    def Stmt_Break(node):
        return "break" if AST._LAST_BLOCK == "switch" else "pass"
            
    def Expr_Cast_Int(node):
        expr = AST.parse(node["expr"])
        return f"int({expr})"

    def Expr_Cast_String(node):
        expr = AST.parse(node["expr"])
        return f"str({expr})"
  
    def Stmt_Global(node):
        vars = AST.parse_children(node, "vars", ", ")
        return f"global {vars}"

    def Expr_Ternary(node):
        if_ = AST.parse(node["if"])
        cond = AST.parse(node["cond"])
        else_ = AST.parse(node["else"])
        return f"({if_} if {cond} else {else_})"

    def Stmt_While(node):
        cond = AST.parse(node["cond"])
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"while {cond}: \n {stmts} \n# end while"

    def Stmt_Do(node):
        cond = AST.parse(node["cond"])
        stmts = AST.parse_children(node, "stmts", "\n")
        return f"while True:\n{stmts}\nif {cond}: break\n# end if\n# end while"

    def Stmt_ClassConst(node):
        cs = AST.parse_children(node, "consts")
        return "\n".join([f"{x} # const" for x in cs])

    def parse(node):
        if node == None:
            return None

        if not (isinstance(node, list) or isinstance(node, dict)):
            return node

        try:
            # TODO: I'm not interested in parsing the comment nodes...
            # comments = ""
            # if ("attributes" in node) and ("comments" in node["attributes"]):
            #     out = [getattr(AST, x["nodeType"])(x) 
            #             for x in node["attributes"]["comments"]]
            #     out = [x for x in out if x != None]
            #     comments = ("\n" + "\n".join(out) + "\n").strip()
   
            # rs = getattr(AST, node["nodeType"])(node)
            # return f"{comments}{rs}"

            return getattr(AST, node["nodeType"])(node)
        except Exception as e:
            print(">> ", e, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print(json.dumps(node, sort_keys=True, indent=2, separators=(',', ': ')), file=sys.stderr)
            return ''

    def parse_children(node, name, delim=None):
        values = [AST.parse(x) for x in (node[name] or [])]

        if isinstance(delim, str):
            return delim.join([x for x in values if x is not None])
        return values

out = ["# coding: utf8\n"]
for node in data:
    out.append(AST.parse(node))
out.append("""
# GRUESOME PATCH: promote locals to global...
globals().update(locals())""")

print(pindent.reformat_string("\n".join(out), stepsize=2, tabsize=2, expandtabs=1))