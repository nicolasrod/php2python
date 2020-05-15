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
#// Upgrader API: WP_Ajax_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Upgrader Skin for Ajax WordPress upgrades.
#// 
#// This skin is designed to be used for Ajax updates.
#// 
#// @since 4.6.0
#// 
#// @see Automatic_Upgrader_Skin
#//
class WP_Ajax_Upgrader_Skin(Automatic_Upgrader_Skin):
    errors = None
    #// 
    #// Constructor.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array $args Options for the upgrader, see WP_Upgrader_Skin::__construct().
    #//
    def __init__(self, args=Array()):
        
        super().__init__(args)
        self.errors = php_new_class("WP_Error", lambda : WP_Error())
    # end def __init__
    #// 
    #// Retrieves the list of errors.
    #// 
    #// @since 4.6.0
    #// 
    #// @return WP_Error Errors during an upgrade.
    #//
    def get_errors(self):
        
        return self.errors
    # end def get_errors
    #// 
    #// Retrieves a string for error messages.
    #// 
    #// @since 4.6.0
    #// 
    #// @return string Error messages during an upgrade.
    #//
    def get_error_messages(self):
        
        messages = Array()
        for error_code in self.errors.get_error_codes():
            error_data = self.errors.get_error_data(error_code)
            if error_data and php_is_string(error_data):
                messages[-1] = self.errors.get_error_message(error_code) + " " + esc_html(strip_tags(error_data))
            else:
                messages[-1] = self.errors.get_error_message(error_code)
            # end if
        # end for
        return php_implode(", ", messages)
    # end def get_error_messages
    #// 
    #// Stores a log entry for an error.
    #// 
    #// @since 4.6.0
    #// @since 5.3.0 Formalized the existing `...$args` parameter by adding it
    #// to the function signature.
    #// 
    #// @param string|WP_Error $errors  Errors.
    #// @param mixed           ...$args Optional text replacements.
    #//
    def error(self, errors=None, *args):
        
        if php_is_string(errors):
            string = errors
            if (not php_empty(lambda : self.upgrader.strings[string])):
                string = self.upgrader.strings[string]
            # end if
            if False != php_strpos(string, "%"):
                if (not php_empty(lambda : args)):
                    string = vsprintf(string, args)
                # end if
            # end if
            #// Count existing errors to generate a unique error code.
            errors_count = php_count(self.errors.get_error_codes())
            self.errors.add("unknown_upgrade_error_" + errors_count + 1, string)
        elif is_wp_error(errors):
            for error_code in errors.get_error_codes():
                self.errors.add(error_code, errors.get_error_message(error_code), errors.get_error_data(error_code))
            # end for
        # end if
        super().error(errors, args)
    # end def error
    #// 
    #// Stores a log entry.
    #// 
    #// @since 4.6.0
    #// @since 5.3.0 Formalized the existing `...$args` parameter by adding it
    #// to the function signature.
    #// 
    #// @param string|array|WP_Error $data    Log entry data.
    #// @param mixed                 ...$args Optional text replacements.
    #//
    def feedback(self, data=None, *args):
        
        if is_wp_error(data):
            for error_code in data.get_error_codes():
                self.errors.add(error_code, data.get_error_message(error_code), data.get_error_data(error_code))
            # end for
        # end if
        super().feedback(data, args)
    # end def feedback
# end class WP_Ajax_Upgrader_Skin
