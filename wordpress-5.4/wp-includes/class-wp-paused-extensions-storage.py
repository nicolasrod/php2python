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
    type = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $extension_type Extension type. Either 'plugin' or 'theme'.
    #//
    def __init__(self, extension_type=None):
        
        self.type = extension_type
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
    def set(self, extension=None, error=None):
        
        if (not self.is_api_loaded()):
            return False
        # end if
        option_name = self.get_option_name()
        if (not option_name):
            return False
        # end if
        paused_extensions = get_option(option_name, Array())
        #// Do not update if the error is already stored.
        if (php_isset(lambda : paused_extensions[self.type][extension])) and paused_extensions[self.type][extension] == error:
            return True
        # end if
        paused_extensions[self.type][extension] = error
        return update_option(option_name, paused_extensions)
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
    def delete(self, extension=None):
        
        if (not self.is_api_loaded()):
            return False
        # end if
        option_name = self.get_option_name()
        if (not option_name):
            return False
        # end if
        paused_extensions = get_option(option_name, Array())
        #// Do not delete if no error is stored.
        if (not (php_isset(lambda : paused_extensions[self.type][extension]))):
            return True
        # end if
        paused_extensions[self.type][extension] = None
        if php_empty(lambda : paused_extensions[self.type]):
            paused_extensions[self.type] = None
        # end if
        #// Clean up the entire option if we're removing the only error.
        if (not paused_extensions):
            return delete_option(option_name)
        # end if
        return update_option(option_name, paused_extensions)
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
    def get(self, extension=None):
        
        if (not self.is_api_loaded()):
            return None
        # end if
        paused_extensions = self.get_all()
        if (not (php_isset(lambda : paused_extensions[extension]))):
            return None
        # end if
        return paused_extensions[extension]
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
        option_name = self.get_option_name()
        if (not option_name):
            return Array()
        # end if
        paused_extensions = get_option(option_name, Array())
        return paused_extensions[self.type] if (php_isset(lambda : paused_extensions[self.type])) else Array()
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
        option_name = self.get_option_name()
        if (not option_name):
            return False
        # end if
        paused_extensions = get_option(option_name, Array())
        paused_extensions[self.type] = None
        if (not paused_extensions):
            return delete_option(option_name)
        # end if
        return update_option(option_name, paused_extensions)
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
        session_id = wp_recovery_mode().get_session_id()
        if php_empty(lambda : session_id):
            return ""
        # end if
        return str(session_id) + str("_paused_extensions")
    # end def get_option_name
# end class WP_Paused_Extensions_Storage
