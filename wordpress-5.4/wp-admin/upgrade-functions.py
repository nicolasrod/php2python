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
#// WordPress Upgrade Functions. Old file, must not be used. Include
#// wp-admin/includes/upgrade.php instead.
#// 
#// @deprecated 2.5.0
#// @package WordPress
#// @subpackage Administration
#//
_deprecated_file(php_basename(__FILE__), "2.5.0", "wp-admin/includes/upgrade.php")
php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
