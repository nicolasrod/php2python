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
    #// 
    #// The handle name.
    #// 
    #// @since 2.6.0
    #// @var null
    #//
    handle = Array()
    #// 
    #// The handle source.
    #// 
    #// @since 2.6.0
    #// @var null
    #//
    src = Array()
    #// 
    #// An array of handle dependencies.
    #// 
    #// @since 2.6.0
    #// @var string[]
    #//
    deps = Array()
    #// 
    #// The handle version.
    #// 
    #// Used for cache-busting.
    #// 
    #// @since 2.6.0
    #// @var bool|string
    #//
    ver = False
    #// 
    #// Additional arguments for the handle.
    #// 
    #// @since 2.6.0
    #// @var null
    #//
    args = None
    #// Custom property, such as $in_footer or $media.
    #// 
    #// Extra data to supply to the handle.
    #// 
    #// @since 2.6.0
    #// @var array
    #//
    extra = Array()
    #// 
    #// Translation textdomain set for this dependency.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
    textdomain = Array()
    #// 
    #// Translation path set for this dependency.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
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
    def __init__(self, *args_):
        
        
        self.handle, self.src, self.deps, self.ver, self.args = args_
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
    def add_data(self, name_=None, data_=None):
        
        
        if (not php_is_scalar(name_)):
            return False
        # end if
        self.extra[name_] = data_
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
    def set_translations(self, domain_=None, path_=None):
        if path_ is None:
            path_ = None
        # end if
        
        if (not php_is_string(domain_)):
            return False
        # end if
        self.textdomain = domain_
        self.translations_path = path_
        return True
    # end def set_translations
# end class _WP_Dependency
