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
#// User Profile Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// This is a profile page.
#// 
#// @since 2.5.0
#// @var bool
#//
php_define("IS_PROFILE_PAGE", True)
#// Load User Editing Page
php_include_file(__DIR__ + "/user-edit.php", once=True)
