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
    #// 
    #// Holds the WP_Error object.
    #// 
    #// @since 4.6.0
    #// @var null|WP_Error
    #//
    errors = None
    #// 
    #// Constructor.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array $args Options for the upgrader, see WP_Upgrader_Skin::__construct().
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        super().__init__(args_)
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
        
        
        messages_ = Array()
        for error_code_ in self.errors.get_error_codes():
            error_data_ = self.errors.get_error_data(error_code_)
            if error_data_ and php_is_string(error_data_):
                messages_[-1] = self.errors.get_error_message(error_code_) + " " + esc_html(strip_tags(error_data_))
            else:
                messages_[-1] = self.errors.get_error_message(error_code_)
            # end if
        # end for
        return php_implode(", ", messages_)
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
    def error(self, errors_=None, *args_):
        
        
        if php_is_string(errors_):
            string_ = errors_
            if (not php_empty(lambda : self.upgrader.strings[string_])):
                string_ = self.upgrader.strings[string_]
            # end if
            if False != php_strpos(string_, "%"):
                if (not php_empty(lambda : args_)):
                    string_ = vsprintf(string_, args_)
                # end if
            # end if
            #// Count existing errors to generate a unique error code.
            errors_count_ = php_count(self.errors.get_error_codes())
            self.errors.add("unknown_upgrade_error_" + errors_count_ + 1, string_)
        elif is_wp_error(errors_):
            for error_code_ in errors_.get_error_codes():
                self.errors.add(error_code_, errors_.get_error_message(error_code_), errors_.get_error_data(error_code_))
            # end for
        # end if
        super().error(errors_, args_)
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
    def feedback(self, data_=None, *args_):
        
        
        if is_wp_error(data_):
            for error_code_ in data_.get_error_codes():
                self.errors.add(error_code_, data_.get_error_message(error_code_), data_.get_error_data(error_code_))
            # end for
        # end if
        super().feedback(data_, args_)
    # end def feedback
# end class WP_Ajax_Upgrader_Skin
