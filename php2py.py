# coding: utf8

import os
import os.path
import sys
import argparse
import ast2py
import resource
import multiprocessing as mp
import time
import json

from subprocess import check_output

def convert(fname, fname_ast, fname_py, args):
    if not args.quiet:
        print(f"[+] Converting {fname}...")

    ast = check_output(["php", "php2ast.php", fname], encoding='UTF-8')

    with open(fname_ast, "w") as f:
        data = json.loads(ast)
        json.dump(data, f, indent=2)

    pycode = ast2py.parse_ast(fname_ast)

    with open(fname_py, "w") as f:
        f.write(pycode)

    if not args.keep_ast:
        os.remove(fname_ast) 

def main():
    parser = argparse.ArgumentParser(description='Convert PHP files to Python')
    parser.add_argument('folder', type=str)
    parser.add_argument('--keep-ast', action='store_true')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print(f"[-] Error readin file {args.folder}!")
        sys.exit(1)

    resource.setrlimit(resource.RLIMIT_NOFILE, (8000, 8000))

    procs = []
    for root, dirs, files in os.walk(args.folder):
        for fname in files:
            fname = fname.strip()
            
            if not fname.lower().endswith(".php"):
                continue
            
            fullname = os.path.join(root, fname)
            basename, _ = os.path.splitext(fullname)
            fname_ast = f"{basename}.ast"
            fname_py = f"{basename}.py"

            if args.resume and os.path.exists(fname_py):
                continue

            proc = mp.Process(target=convert, args=(fullname, fname_ast, fname_py, args))
            procs.append(proc)
            proc.start()
            
            if len(procs) == 10:
                for proc in procs:
                    proc.join()
                procs = []
        time.sleep(0.05)
        
    if not args.quiet:
        print("[*] Done!")

if __name__ == "__main__":
    main()
