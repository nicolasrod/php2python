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
#// Upgrader API: WP_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Generic Skin for the WordPress Upgrader classes. This skin is designed to be extended for specific purposes.
#// 
#// @since 2.8.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#//
class WP_Upgrader_Skin():
    upgrader = Array()
    done_header = False
    done_footer = False
    result = False
    options = Array()
    #// 
    #// @param array $args
    #//
    def __init__(self, args=Array()):
        
        defaults = Array({"url": "", "nonce": "", "title": "", "context": False})
        self.options = wp_parse_args(args, defaults)
    # end def __init__
    #// 
    #// @param WP_Upgrader $upgrader
    #//
    def set_upgrader(self, upgrader=None):
        
        if php_is_object(upgrader):
            self.upgrader = upgrader
        # end if
        self.add_strings()
    # end def set_upgrader
    #// 
    #//
    def add_strings(self):
        
        pass
    # end def add_strings
    #// 
    #// Sets the result of an upgrade.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string|bool|WP_Error $result The result of an upgrade.
    #//
    def set_result(self, result=None):
        
        self.result = result
    # end def set_result
    #// 
    #// Displays a form to the user to request for their FTP/SSH details in order
    #// to connect to the filesystem.
    #// 
    #// @since 2.8.0
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
    def request_filesystem_credentials(self, error=False, context="", allow_relaxed_file_ownership=False):
        
        url = self.options["url"]
        if (not context):
            context = self.options["context"]
        # end if
        if (not php_empty(lambda : self.options["nonce"])):
            url = wp_nonce_url(url, self.options["nonce"])
        # end if
        extra_fields = Array()
        return request_filesystem_credentials(url, "", error, context, extra_fields, allow_relaxed_file_ownership)
    # end def request_filesystem_credentials
    #// 
    #//
    def header(self):
        
        if self.done_header:
            return
        # end if
        self.done_header = True
        php_print("<div class=\"wrap\">")
        php_print("<h1>" + self.options["title"] + "</h1>")
    # end def header
    #// 
    #//
    def footer(self):
        
        if self.done_footer:
            return
        # end if
        self.done_footer = True
        php_print("</div>")
    # end def footer
    #// 
    #// @param string|WP_Error $errors
    #//
    def error(self, errors=None):
        
        if (not self.done_header):
            self.header()
        # end if
        if php_is_string(errors):
            self.feedback(errors)
        elif is_wp_error(errors) and errors.has_errors():
            for message in errors.get_error_messages():
                if errors.get_error_data() and php_is_string(errors.get_error_data()):
                    self.feedback(message + " " + esc_html(strip_tags(errors.get_error_data())))
                else:
                    self.feedback(message)
                # end if
            # end for
        # end if
    # end def error
    #// 
    #// @param string $string
    #// @param mixed  ...$args Optional text replacements.
    #//
    def feedback(self, string=None, *args):
        
        if (php_isset(lambda : self.upgrader.strings[string])):
            string = self.upgrader.strings[string]
        # end if
        if php_strpos(string, "%") != False:
            if args:
                args = php_array_map("strip_tags", args)
                args = php_array_map("esc_html", args)
                string = vsprintf(string, args)
            # end if
        # end if
        if php_empty(lambda : string):
            return
        # end if
        show_message(string)
    # end def feedback
    #// 
    #//
    def before(self):
        
        pass
    # end def before
    #// 
    #//
    def after(self):
        
        pass
    # end def after
    #// 
    #// Output JavaScript that calls function to decrement the update counts.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $type Type of update count to decrement. Likely values include 'plugin',
    #// 'theme', 'translation', etc.
    #//
    def decrement_update_count(self, type=None):
        
        if (not self.result) or is_wp_error(self.result) or "up_to_date" == self.result:
            return
        # end if
        if php_defined("IFRAME_REQUEST"):
            php_print("<script type=\"text/javascript\">\n                  if ( window.postMessage && JSON ) {\n                       window.parent.postMessage( JSON.stringify( { action: \"decrementUpdateCount\", upgradeType: \"" + type + "\" } ), window.location.protocol + \"//\" + window.location.hostname );\n                 }\n             </script>")
        else:
            php_print("""<script type=\"text/javascript\">
            (function( wp ) {
        if ( wp && wp.updates && wp.updates.decrementCount ) {
            wp.updates.decrementCount( \"""" + type + """\" );
            }
            })( window.wp );
            </script>""")
        # end if
    # end def decrement_update_count
    #// 
    #//
    def bulk_header(self):
        
        pass
    # end def bulk_header
    #// 
    #//
    def bulk_footer(self):
        
        pass
    # end def bulk_footer
# end class WP_Upgrader_Skin
