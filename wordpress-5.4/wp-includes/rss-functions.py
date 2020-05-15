#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import cgi
    import os
    import os.path
    import copy
    import sys
    from goto import with_goto
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// Deprecated. Use rss.php instead.
#// 
#// @package WordPress
#// @deprecated 2.1.0
#//
_deprecated_file(php_basename(__FILE__), "2.1.0", WPINC + "/rss.php")
php_include_file(ABSPATH + WPINC + "/rss.php", once=True)
