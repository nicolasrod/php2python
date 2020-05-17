#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// Multisite administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#//
php_include_file(__DIR__ + "/admin.php", once=True)
wp_redirect(network_admin_url())
php_exit(0)
