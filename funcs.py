def to_python(fn, args):
    if f"php_{fn}" in globals():
        return globals()[f"php_{fn}"](*args)
    return f"""{fn}({",".join(args)})"""

# =================================================================

def php_file_exists(p1):
    return f"os.path.exists({p1})"

def php_dirname(p1, p2=1): #@@
    return f"os.path.dirname({p1})"

def php_sprintf(p1, *args): #@@ 
    return f'{p1} % ({", ".join(args)})'

def php_strtolower(p1):
    return f"{p1}.lower()"

def php_strtoupper(p1):
    return f"{p1}.upper()"

def php_count(p1, p2=0): #@@
    return f"len({p1})"

def php_trim(p1, p2=None): #@@
    return f"{p1}.strip()"

def php_replace(p1, p2, p3):
    return f"{p3}.replace({p1}, {p2})"
    
def php_strpos(p1, p2, p3=None): #@@
    return f"{p1}.find({p2})"

def php_define(p1, p2):
    return f"""{p1.replace("'", '').replace('"', '')} = {p2}"""
    
def php_is_object(p1):
    return f"isinstance({p1}, object)"
    
def php_in_array(p1, p2, p3=None): #@@
    return f"{p1} in {p2}"

def php_defined(p1):
    return f"""({p1} in  {{**globals(), **locals()}})"""

def php_is_null(p1):
    return f"({p1} is None)"
      
def php_is_array(p1):
    return f"isinstance({p1}, list)"

def php_explode(p1, p2, p3=None): #@@
    return f"{p2}.split({p1})"

def php_intval(p1, p2=10):
    return f"int({p1}, p2)"

def php_header(p1, p2=None, p3=None): #@@
    return f"print({p1})"
    
def php_is_string(p1):
    return f"isinstance({p1}, str)"

def php_abs(p1):
    return f"abs({p1})"

def php_error_reporting(*args):
    return ""

def array_merge(*args):
    if len(args) == 0:
        return args
        
    if isinstance(args[0], list):
        out = []
        for i in args:
            out.extend(i)
        return out
    else:
        out = {}
        for i in args:
            out.update(i)
        return out