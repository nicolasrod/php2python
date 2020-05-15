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
#// Dependencies API: _WP_Dependency class
#// 
#// @since 4.7.0
#// 
#// @package WordPress
#// @subpackage Dependencies
#// 
#// 
#// Class _WP_Dependency
#// 
#// Helper class to register a handle and associated data.
#// 
#// @access private
#// @since 2.6.0
#//
class _WP_Dependency():
    handle = Array()
    src = Array()
    deps = Array()
    ver = False
    args = None
    extra = Array()
    textdomain = Array()
    translations_path = Array()
    #// 
    #// Setup dependencies.
    #// 
    #// @since 2.6.0
    #// @since 5.3.0 Formalized the existing `...$args` parameter by adding it
    #// to the function signature.
    #// 
    #// @param ...$args Dependency information.
    #//
    def __init__(self, *args):
        
        self.handle, self.src, self.deps, self.ver, self.args = args
        if (not php_is_array(self.deps)):
            self.deps = Array()
        # end if
    # end def __init__
    #// 
    #// Add handle data.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $name The data key to add.
    #// @param mixed  $data The data value to add.
    #// @return bool False if not scalar, true otherwise.
    #//
    def add_data(self, name=None, data=None):
        
        if (not is_scalar(name)):
            return False
        # end if
        self.extra[name] = data
        return True
    # end def add_data
    #// 
    #// Sets the translation domain for this dependency.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $domain The translation textdomain.
    #// @param string $path   Optional. The full file path to the directory containing translation files.
    #// @return bool False if $domain is not a string, true otherwise.
    #//
    def set_translations(self, domain=None, path=None):
        
        if (not php_is_string(domain)):
            return False
        # end if
        self.textdomain = domain
        self.translations_path = path
        return True
    # end def set_translations
# end class _WP_Dependency
