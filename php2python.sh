#!/bin/bash

set -ue

if [ ! -e "$1" ]
then
    echo "[-] Error: file $1 not found!"
    exit 1
fi

base=$(basename -- "$1")
dirname=$(dirname -- "$1")
fname="${dirname}/${base%.*}"
ast="${fname}.ast"
dst="${fname}.py"
echo "[*] Processing $1..."
php php2ast.php "$1" > "${ast}"
python3 ast2python.py "${ast}" > "${dst}"
rm "${ast}"