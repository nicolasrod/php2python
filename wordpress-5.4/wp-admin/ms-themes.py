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
#// Multisite themes administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#//
php_include_file(__DIR__ + "/admin.php", once=True)
wp_redirect(network_admin_url("themes.php"))
php_exit(0)
