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
#// Loads the WordPress environment and template.
#// 
#// @package WordPress
#//
if (not (php_isset(lambda : wp_did_header))):
    wp_did_header = True
    #// Load the WordPress library.
    php_include_file(__DIR__ + "/wp-load.php", once=True)
    #// Set up the WordPress query.
    wp()
    #// Load the theme template.
    php_include_file(ABSPATH + WPINC + "/template-loader.php", once=True)
# end if
