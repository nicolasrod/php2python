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
php_include_file(php_dirname(php_dirname(__FILE__)) + "/autoload.php", once=True)
if PHP_VERSION_ID < 50300:
    sys.exit(-1)
# end if
def _closure_bec7b677(class_ = None):
    
    if class_[0] == "\\":
        class_ = php_substr(class_, 1)
    # end if
    namespace = "ParagonIE\\Sodium"
    #// Does the class use the namespace prefix?
    len = php_strlen(namespace)
    if php_strncmp(namespace, class_, len) != 0:
        return False
    # end if
    #// Get the relative class name
    relative_class = php_substr(class_, len)
    #// Replace the namespace prefix with the base directory, replace namespace
    #// separators with directory separators in the relative class name, append
    #// with .php
    file = php_dirname(php_dirname(__FILE__)) + "/namespaced/" + php_str_replace("\\", "/", relative_class) + ".php"
    #// if the file exists, require it
    if php_file_exists(file):
        php_include_file(file, once=True)
        return True
    # end if
    return False
# end def _closure_bec7b677
#// 
#// This file is just for convenience, to allow developers to reduce verbosity when
#// they add this project to their libraries.
#// 
#// Replace this:
#// 
#// $x = ParagonIE_Sodium_Compat::crypto_aead_xchacha20poly1305_encrypt(...$args);
#// 
#// with this:
#// 
#// use ParagonIE\Sodium\Compat;
#// 
#// $x = Compat::crypto_aead_xchacha20poly1305_encrypt(...$args);
#//
php_spl_autoload_register((lambda *args, **kwargs: _closure_bec7b677(*args, **kwargs)))
