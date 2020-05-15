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
#// Comment Moderation Administration Screen.
#// 
#// Redirects to edit-comments.php?comment_status=moderated.
#// 
#// @package WordPress
#// @subpackage Administration
#//
php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
wp_redirect(admin_url("edit-comments.php?comment_status=moderated"))
php_exit(0)
