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
#// Front to the WordPress application. This file doesn't do anything, but loads
#// wp-blog-header.php which does and tells WordPress to load the theme.
#// 
#// @package WordPress
#// 
#// 
#// Tells WordPress to load the WordPress theme and output it.
#// 
#// @var bool
#//
php_define("WP_USE_THEMES", True)
#// Loads the WordPress Environment and Template
php_include_file(__DIR__ + "/wp-blog-header.php", once=False)
