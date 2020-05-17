#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if (not php_is_callable("sodiumCompatAutoloader")):
    #// 
    #// Sodium_Compat autoloader.
    #// 
    #// @param string $class Class name to be autoloaded.
    #// 
    #// @return bool         Stop autoloading?
    #//
    def sodiumCompatAutoloader(class_=None, *_args_):
        
        
        namespace_ = "ParagonIE_Sodium_"
        #// Does the class use the namespace prefix?
        len_ = php_strlen(namespace_)
        if php_strncmp(namespace_, class_, len_) != 0:
            #// no, move to the next registered autoloader
            return False
        # end if
        #// Get the relative class name
        relative_class_ = php_substr(class_, len_)
        #// Replace the namespace prefix with the base directory, replace namespace
        #// separators with directory separators in the relative class name, append
        #// with .php
        file_ = php_dirname(__FILE__) + "/src/" + php_str_replace("_", "/", relative_class_) + ".php"
        #// if the file exists, require it
        if php_file_exists(file_):
            php_include_file(file_, once=True)
            return True
        # end if
        return False
    # end def sodiumCompatAutoloader
    #// Now that we have an autoloader, let's register it!
    php_spl_autoload_register("sodiumCompatAutoloader")
# end if
php_include_file(php_dirname(__FILE__) + "/src/SodiumException.php", once=True)
if PHP_VERSION_ID >= 50300:
    #// Namespaces didn't exist before 5.3.0, so don't even try to use this
    #// unless PHP >= 5.3.0
    php_include_file(php_dirname(__FILE__) + "/lib/namespaced.php", once=True)
    php_include_file(php_dirname(__FILE__) + "/lib/sodium_compat.php", once=True)
else:
    php_include_file(php_dirname(__FILE__) + "/src/PHP52/SplFixedArray.php", once=True)
# end if
if PHP_VERSION_ID < 70200 or (not php_extension_loaded("sodium")):
    if PHP_VERSION_ID >= 50300 and (not php_defined("SODIUM_CRYPTO_SCALARMULT_BYTES")):
        php_include_file(php_dirname(__FILE__) + "/lib/php72compat_const.php", once=True)
    # end if
    if PHP_VERSION_ID >= 70000:
        assert(php_class_exists("ParagonIE_Sodium_Compat"), "Possible filesystem/autoloader bug?")
    else:
        assert(php_class_exists("ParagonIE_Sodium_Compat"))
    # end if
    php_include_file(php_dirname(__FILE__) + "/lib/php72compat.php", once=True)
# end if
