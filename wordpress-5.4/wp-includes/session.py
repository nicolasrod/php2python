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
#// Session API
#// 
#// @since 4.0.0
#// @deprecated 4.7.0
#//
_deprecated_file(php_basename(__FILE__), "4.7.0")
php_include_file(ABSPATH + WPINC + "/class-wp-session-tokens.php", once=True)
php_include_file(ABSPATH + WPINC + "/class-wp-user-meta-session-tokens.php", once=True)
