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
#// Class for generating SQL clauses that filter a primary query according to date.
#// 
#// This file is deprecated, use 'wp-includes/class-wp-date-query.php' instead.
#// 
#// @deprecated 5.3.0
#// @package WordPress
#//
_deprecated_file(php_basename(__FILE__), "5.3.0", "wp-includes/class-wp-date-query.php")
#// WP_Date_Query class
php_include_file(ABSPATH + "wp-includes/class-wp-date-query.php", once=True)
