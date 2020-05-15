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
#// Polyfill for SPL autoload feature. This file is separate to prevent compiler notices
#// on the deprecated __autoload() function.
#// 
#// See https://core.trac.wordpress.org/ticket/41134
#// 
#// @deprecated 5.3.0 No longer needed as the minimum PHP requirement has moved beyond PHP 5.3.
#// 
#// @package PHP
#// @access private
#//
_deprecated_file(php_basename(__FILE__), "5.3.0", None, "SPL can no longer be disabled as of PHP 5.3.")
