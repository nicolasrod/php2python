# coding: utf8

import sys
import os
import os.path
from fnmatch import fnmatch

if len(sys.argv) < 2:
    print(f"[-] Usage: {sys.argv[0]} <folder>")
    sys.exit(1)

src_dir = sys.argv[1]

if not os.path.isdir(src_dir):
    print(f"[-] Error: {src_dir} is not a folder!")
    sys.exit(2)

WEBAPP = """
import io
import os
import sys
import os.path

from flask import Flask, request
from contextlib import redirect_stdout

app = Flask(__name__)
WEBROOT = os.getcwd()

def php_include_file(fname, redirect=False):
    if fname.startswith("/"):
        fname = "." + fname

    tmp = os.path.abspath(os.path.join(WEBROOT, fname))
    filename, ext = os.path.splitext(tmp)
    
    with open(f"{filename}.py") as src:
        code = src.read()
    
    if redirect:
        f = io.StringIO()
        with redirect_stdout(f):
            exec(code)
        return f.getvalue()
    
    exec(code) 

@app.errorhandler(404)
def page_not_found(e):
    return php_include_file(request.path, True)
"""

def print_route(fname):
    _, filename = os.path.split(fname)
    fn = fname.lower().replace("-", "_").replace("/", "_").replace(".", "").strip()
    print(f"""
@app.route("/{fname}")
def php_{fn}():
    return php_include_file("{fname}", True)""")

print(WEBAPP)
for root, _, files in os.walk(src_dir):
    for name in files:
        fname = os.path.join(root, name)
        if fnmatch(fname, "*.py"):
            print_route(fname)

print("app.run(debug=True)")