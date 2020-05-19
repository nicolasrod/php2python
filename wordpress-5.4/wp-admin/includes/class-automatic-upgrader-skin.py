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
#// Upgrader API: Automatic_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Upgrader Skin for Automatic WordPress Upgrades
#// 
#// This skin is designed to be used when no output is intended, all output
#// is captured and stored for the caller to process and log/email/discard.
#// 
#// @since 3.7.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see Bulk_Upgrader_Skin
#//
class Automatic_Upgrader_Skin(WP_Upgrader_Skin):
    messages = Array()
    #// 
    #// Determines whether the upgrader needs FTP/SSH details in order to connect
    #// to the filesystem.
    #// 
    #// @since 3.7.0
    #// @since 4.6.0 The `$context` parameter default changed from `false` to an empty string.
    #// 
    #// @see request_filesystem_credentials()
    #// 
    #// @param bool|WP_Error $error                        Optional. Whether the current request has failed to connect,
    #// or an error object. Default false.
    #// @param string        $context                      Optional. Full path to the directory that is tested
    #// for being writable. Default empty.
    #// @param bool          $allow_relaxed_file_ownership Optional. Whether to allow Group/World writable. Default false.
    #// @return bool True on success, false on failure.
    #//
    def request_filesystem_credentials(self, error_=None, context_="", allow_relaxed_file_ownership_=None):
        if error_ is None:
            error_ = False
        # end if
        if allow_relaxed_file_ownership_ is None:
            allow_relaxed_file_ownership_ = False
        # end if
        
        if context_:
            self.options["context"] = context_
        # end if
        #// 
        #// TODO: Fix up request_filesystem_credentials(), or split it, to allow us to request a no-output version.
        #// This will output a credentials form in event of failure. We don't want that, so just hide with a buffer.
        #//
        ob_start()
        result_ = super().request_filesystem_credentials(error_, context_, allow_relaxed_file_ownership_)
        ob_end_clean()
        return result_
    # end def request_filesystem_credentials
    #// 
    #// @return array
    #//
    def get_upgrade_messages(self):
        
        
        return self.messages
    # end def get_upgrade_messages
    #// 
    #// @param string|array|WP_Error $data
    #// @param mixed                 ...$args Optional text replacements.
    #//
    def feedback(self, data_=None, *args_):
        
        
        if is_wp_error(data_):
            string_ = data_.get_error_message()
        elif php_is_array(data_):
            return
        else:
            string_ = data_
        # end if
        if (not php_empty(lambda : self.upgrader.strings[string_])):
            string_ = self.upgrader.strings[string_]
        # end if
        if php_strpos(string_, "%") != False:
            if (not php_empty(lambda : args_)):
                string_ = php_vsprintf(string_, args_)
            # end if
        # end if
        string_ = php_trim(string_)
        #// Only allow basic HTML in the messages, as it'll be used in emails/logs rather than direct browser output.
        string_ = wp_kses(string_, Array({"a": Array({"href": True})}, {"br": True, "em": True, "strong": True}))
        if php_empty(lambda : string_):
            return
        # end if
        self.messages[-1] = string_
    # end def feedback
    #// 
    #//
    def header(self):
        
        
        ob_start()
    # end def header
    #// 
    #//
    def footer(self):
        
        
        output_ = ob_get_clean()
        if (not php_empty(lambda : output_)):
            self.feedback(output_)
        # end if
    # end def footer
# end class Automatic_Upgrader_Skin
