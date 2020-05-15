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
#// WordPress Error API.
#// 
#// Contains the WP_Error class and the is_wp_error() function.
#// 
#// @package WordPress
#// 
#// 
#// WordPress Error class.
#// 
#// Container for checking for WordPress errors and error messages. Return
#// WP_Error and use is_wp_error() to check if this class is returned. Many
#// core WordPress functions pass this class in the event of an error and
#// if not handled properly will result in code errors.
#// 
#// @since 2.1.0
#//
class WP_Error():
    errors = Array()
    error_data = Array()
    #// 
    #// Initialize the error.
    #// 
    #// If `$code` is empty, the other parameters will be ignored.
    #// When `$code` is not empty, `$message` will be used even if
    #// it is empty. The `$data` parameter will be used only if it
    #// is not empty.
    #// 
    #// Though the class is constructed with a single error code and
    #// message, multiple codes can be added using the `add()` method.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string|int $code Error code
    #// @param string $message Error message
    #// @param mixed $data Optional. Error data.
    #//
    def __init__(self, code="", message="", data=""):
        
        if php_empty(lambda : code):
            return
        # end if
        self.errors[code][-1] = message
        if (not php_empty(lambda : data)):
            self.error_data[code] = data
        # end if
    # end def __init__
    #// 
    #// Retrieve all error codes.
    #// 
    #// @since 2.1.0
    #// 
    #// @return array List of error codes, if available.
    #//
    def get_error_codes(self):
        
        if (not self.has_errors()):
            return Array()
        # end if
        return php_array_keys(self.errors)
    # end def get_error_codes
    #// 
    #// Retrieve first error code available.
    #// 
    #// @since 2.1.0
    #// 
    #// @return string|int Empty string, if no error codes.
    #//
    def get_error_code(self):
        
        codes = self.get_error_codes()
        if php_empty(lambda : codes):
            return ""
        # end if
        return codes[0]
    # end def get_error_code
    #// 
    #// Retrieve all error messages or error messages matching code.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string|int $code Optional. Retrieve messages matching code, if exists.
    #// @return array Error strings on success, or empty array on failure (if using code parameter).
    #//
    def get_error_messages(self, code=""):
        
        #// Return all messages if no code specified.
        if php_empty(lambda : code):
            all_messages = Array()
            for code,messages in self.errors:
                all_messages = php_array_merge(all_messages, messages)
            # end for
            return all_messages
        # end if
        if (php_isset(lambda : self.errors[code])):
            return self.errors[code]
        else:
            return Array()
        # end if
    # end def get_error_messages
    #// 
    #// Get single error message.
    #// 
    #// This will get the first message available for the code. If no code is
    #// given then the first code available will be used.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string|int $code Optional. Error code to retrieve message.
    #// @return string
    #//
    def get_error_message(self, code=""):
        
        if php_empty(lambda : code):
            code = self.get_error_code()
        # end if
        messages = self.get_error_messages(code)
        if php_empty(lambda : messages):
            return ""
        # end if
        return messages[0]
    # end def get_error_message
    #// 
    #// Retrieve error data for error code.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string|int $code Optional. Error code.
    #// @return mixed Error data, if it exists.
    #//
    def get_error_data(self, code=""):
        
        if php_empty(lambda : code):
            code = self.get_error_code()
        # end if
        if (php_isset(lambda : self.error_data[code])):
            return self.error_data[code]
        # end if
    # end def get_error_data
    #// 
    #// Verify if the instance contains errors.
    #// 
    #// @since 5.1.0
    #// 
    #// @return bool
    #//
    def has_errors(self):
        
        if (not php_empty(lambda : self.errors)):
            return True
        # end if
        return False
    # end def has_errors
    #// 
    #// Add an error or append additional message to an existing error.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string|int $code Error code.
    #// @param string $message Error message.
    #// @param mixed $data Optional. Error data.
    #//
    def add(self, code=None, message=None, data=""):
        
        self.errors[code][-1] = message
        if (not php_empty(lambda : data)):
            self.error_data[code] = data
        # end if
    # end def add
    #// 
    #// Add data for error code.
    #// 
    #// The error code can only contain one error data.
    #// 
    #// @since 2.1.0
    #// 
    #// @param mixed $data Error data.
    #// @param string|int $code Error code.
    #//
    def add_data(self, data=None, code=""):
        
        if php_empty(lambda : code):
            code = self.get_error_code()
        # end if
        self.error_data[code] = data
    # end def add_data
    #// 
    #// Removes the specified error.
    #// 
    #// This function removes all error messages associated with the specified
    #// error code, along with any error data for that code.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string|int $code Error code.
    #//
    def remove(self, code=None):
        
        self.errors[code] = None
        self.error_data[code] = None
    # end def remove
# end class WP_Error
