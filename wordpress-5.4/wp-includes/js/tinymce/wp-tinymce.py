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
#// Not used in core since 5.1.
#// This is a back-compat for plugins that may be using this method of loading directly.
#// 
#// 
#// Disable error reporting
#// 
#// Set this to error_reporting( -1 ) for debugging.
#//
php_error_reporting(0)
basepath = __DIR__
def get_file(path=None, *args_):
    
    if php_function_exists("realpath"):
        path = php_realpath(path)
    # end if
    if (not path) or (not php_no_error(lambda: php_is_file(path))):
        return False
    # end if
    return php_no_error(lambda: php_file_get_contents(path))
# end def get_file
expires_offset = 31536000
#// 1 year.
php_header("Content-Type: application/javascript; charset=UTF-8")
php_header("Vary: Accept-Encoding")
#// Handle proxies.
php_header("Expires: " + gmdate("D, d M Y H:i:s", time() + expires_offset) + " GMT")
php_header(str("Cache-Control: public, max-age=") + str(expires_offset))
file = get_file(basepath + "/wp-tinymce.js")
if (php_isset(lambda : PHP_REQUEST["c"])) and file:
    php_print(file)
else:
    #// Even further back compat.
    php_print(get_file(basepath + "/tinymce.min.js"))
    php_print(get_file(basepath + "/plugins/compat3x/plugin.min.js"))
# end if
php_exit(0)
