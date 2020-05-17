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
#// Error Protection API: WP_Paused_Extensions_Storage class
#// 
#// @package WordPress
#// @since 5.2.0
#// 
#// 
#// Core class used for storing paused extensions.
#// 
#// @since 5.2.0
#//
class WP_Paused_Extensions_Storage():
    #// 
    #// Type of extension. Used to key extension storage.
    #// 
    #// @since 5.2.0
    #// @var string
    #//
    type = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $extension_type Extension type. Either 'plugin' or 'theme'.
    #//
    def __init__(self, extension_type_=None):
        
        
        self.type = extension_type_
    # end def __init__
    #// 
    #// Records an extension error.
    #// 
    #// Only one error is stored per extension, with subsequent errors for the same extension overriding the
    #// previously stored error.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $extension Plugin or theme directory name.
    #// @param array  $error     {
    #// Error that was triggered.
    #// 
    #// @type string $type    The error type.
    #// @type string $file    The name of the file in which the error occurred.
    #// @type string $line    The line number in which the error occurred.
    #// @type string $message The error message.
    #// }
    #// @return bool True on success, false on failure.
    #//
    def set(self, extension_=None, error_=None):
        
        
        if (not self.is_api_loaded()):
            return False
        # end if
        option_name_ = self.get_option_name()
        if (not option_name_):
            return False
        # end if
        paused_extensions_ = get_option(option_name_, Array())
        #// Do not update if the error is already stored.
        if (php_isset(lambda : paused_extensions_[self.type][extension_])) and paused_extensions_[self.type][extension_] == error_:
            return True
        # end if
        paused_extensions_[self.type][extension_] = error_
        return update_option(option_name_, paused_extensions_)
    # end def set
    #// 
    #// Forgets a previously recorded extension error.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $extension Plugin or theme directory name.
    #// 
    #// @return bool True on success, false on failure.
    #//
    def delete(self, extension_=None):
        
        
        if (not self.is_api_loaded()):
            return False
        # end if
        option_name_ = self.get_option_name()
        if (not option_name_):
            return False
        # end if
        paused_extensions_ = get_option(option_name_, Array())
        #// Do not delete if no error is stored.
        if (not (php_isset(lambda : paused_extensions_[self.type][extension_]))):
            return True
        # end if
        paused_extensions_[self.type][extension_] = None
        if php_empty(lambda : paused_extensions_[self.type]):
            paused_extensions_[self.type] = None
        # end if
        #// Clean up the entire option if we're removing the only error.
        if (not paused_extensions_):
            return delete_option(option_name_)
        # end if
        return update_option(option_name_, paused_extensions_)
    # end def delete
    #// 
    #// Gets the error for an extension, if paused.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $extension Plugin or theme directory name.
    #// 
    #// @return array|null Error that is stored, or null if the extension is not paused.
    #//
    def get(self, extension_=None):
        
        
        if (not self.is_api_loaded()):
            return None
        # end if
        paused_extensions_ = self.get_all()
        if (not (php_isset(lambda : paused_extensions_[extension_]))):
            return None
        # end if
        return paused_extensions_[extension_]
    # end def get
    #// 
    #// Gets the paused extensions with their errors.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array Associative array of extension slugs to the error recorded.
    #//
    def get_all(self):
        
        
        if (not self.is_api_loaded()):
            return Array()
        # end if
        option_name_ = self.get_option_name()
        if (not option_name_):
            return Array()
        # end if
        paused_extensions_ = get_option(option_name_, Array())
        return paused_extensions_[self.type] if (php_isset(lambda : paused_extensions_[self.type])) else Array()
    # end def get_all
    #// 
    #// Remove all paused extensions.
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool
    #//
    def delete_all(self):
        
        
        if (not self.is_api_loaded()):
            return False
        # end if
        option_name_ = self.get_option_name()
        if (not option_name_):
            return False
        # end if
        paused_extensions_ = get_option(option_name_, Array())
        paused_extensions_[self.type] = None
        if (not paused_extensions_):
            return delete_option(option_name_)
        # end if
        return update_option(option_name_, paused_extensions_)
    # end def delete_all
    #// 
    #// Checks whether the underlying API to store paused extensions is loaded.
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool True if the API is loaded, false otherwise.
    #//
    def is_api_loaded(self):
        
        
        return php_function_exists("get_option")
    # end def is_api_loaded
    #// 
    #// Get the option name for storing paused extensions.
    #// 
    #// @since 5.2.0
    #// 
    #// @return string
    #//
    def get_option_name(self):
        
        
        if (not wp_recovery_mode().is_active()):
            return ""
        # end if
        session_id_ = wp_recovery_mode().get_session_id()
        if php_empty(lambda : session_id_):
            return ""
        # end if
        return str(session_id_) + str("_paused_extensions")
    # end def get_option_name
# end class WP_Paused_Extensions_Storage
