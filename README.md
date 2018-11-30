# php2python

Convert PHP code to Python/Flask (PoC)

```
$ find <project_folder> -iname "*.php" -exec ./php2python.sh '{}' \;
$ python3 create_webapp.py <project_folder> > <project_folder>/webapp.py
$ cd <project_folder>
$ python3 webapp.py
```
