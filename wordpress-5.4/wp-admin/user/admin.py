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
#// WordPress User Administration Bootstrap
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#//
php_define("WP_USER_ADMIN", True)
php_include_file(php_dirname(__DIR__) + "/admin.php", once=True)
if (not is_multisite()):
    wp_redirect(admin_url())
    php_exit(0)
# end if
redirect_user_admin_request = 0 != strcasecmp(current_blog.domain, current_site.domain) or 0 != strcasecmp(current_blog.path, current_site.path)
#// 
#// Filters whether to redirect the request to the User Admin in Multisite.
#// 
#// @since 3.2.0
#// 
#// @param bool $redirect_user_admin_request Whether the request should be redirected.
#//
redirect_user_admin_request = apply_filters("redirect_user_admin_request", redirect_user_admin_request)
if redirect_user_admin_request:
    wp_redirect(user_admin_url())
    php_exit(0)
# end if
redirect_user_admin_request = None
