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
#// Upgrader API: Bulk_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Generic Bulk Upgrader Skin for WordPress Upgrades.
#// 
#// @since 3.0.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see WP_Upgrader_Skin
#//
class Bulk_Upgrader_Skin(WP_Upgrader_Skin):
    in_loop = False
    error = False
    #// 
    #// @param array $args
    #//
    def __init__(self, args=Array()):
        
        defaults = Array({"url": "", "nonce": ""})
        args = wp_parse_args(args, defaults)
        super().__init__(args)
    # end def __init__
    #// 
    #//
    def add_strings(self):
        
        self.upgrader.strings["skin_upgrade_start"] = __("The update process is starting. This process may take a while on some hosts, so please be patient.")
        #// translators: 1: Title of an update, 2: Error message.
        self.upgrader.strings["skin_update_failed_error"] = __("An error occurred while updating %1$s: %2$s")
        #// translators: %s: Title of an update.
        self.upgrader.strings["skin_update_failed"] = __("The update of %s failed.")
        #// translators: %s: Title of an update.
        self.upgrader.strings["skin_update_successful"] = __("%s updated successfully.")
        self.upgrader.strings["skin_upgrade_end"] = __("All updates have been completed.")
    # end def add_strings
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
        if self.in_loop:
            php_print(str(string) + str("<br />\n"))
        else:
            php_print(str("<p>") + str(string) + str("</p>\n"))
        # end if
    # end def feedback
    #// 
    #//
    def header(self):
        
        pass
    # end def header
    #// 
    #//
    def footer(self):
        
        pass
    # end def footer
    #// 
    #// @param string|WP_Error $error
    #//
    def error(self, error=None):
        
        if php_is_string(error) and (php_isset(lambda : self.upgrader.strings[error])):
            self.error = self.upgrader.strings[error]
        # end if
        if is_wp_error(error):
            messages = Array()
            for emessage in error.get_error_messages():
                if error.get_error_data() and php_is_string(error.get_error_data()):
                    messages[-1] = emessage + " " + esc_html(strip_tags(error.get_error_data()))
                else:
                    messages[-1] = emessage
                # end if
            # end for
            self.error = php_implode(", ", messages)
        # end if
        php_print("<script type=\"text/javascript\">jQuery('.waiting-" + esc_js(self.upgrader.update_current) + "').hide();</script>")
    # end def error
    #// 
    #//
    def bulk_header(self):
        
        self.feedback("skin_upgrade_start")
    # end def bulk_header
    #// 
    #//
    def bulk_footer(self):
        
        self.feedback("skin_upgrade_end")
    # end def bulk_footer
    #// 
    #// @param string $title
    #//
    def before(self, title=""):
        
        self.in_loop = True
        printf("<h2>" + self.upgrader.strings["skin_before_update_header"] + " <span class=\"spinner waiting-" + self.upgrader.update_current + "\"></span></h2>", title, self.upgrader.update_current, self.upgrader.update_count)
        php_print("<script type=\"text/javascript\">jQuery('.waiting-" + esc_js(self.upgrader.update_current) + "').css(\"display\", \"inline-block\");</script>")
        #// This progress messages div gets moved via JavaScript when clicking on "Show details.".
        php_print("<div class=\"update-messages hide-if-js\" id=\"progress-" + esc_attr(self.upgrader.update_current) + "\"><p>")
        self.flush_output()
    # end def before
    #// 
    #// @param string $title
    #//
    def after(self, title=""):
        
        php_print("</p></div>")
        if self.error or (not self.result):
            if self.error:
                php_print("<div class=\"error\"><p>" + php_sprintf(self.upgrader.strings["skin_update_failed_error"], title, "<strong>" + self.error + "</strong>") + "</p></div>")
            else:
                php_print("<div class=\"error\"><p>" + php_sprintf(self.upgrader.strings["skin_update_failed"], title) + "</p></div>")
            # end if
            php_print("<script type=\"text/javascript\">jQuery('#progress-" + esc_js(self.upgrader.update_current) + "').show();</script>")
        # end if
        if self.result and (not is_wp_error(self.result)):
            if (not self.error):
                php_print("<div class=\"updated js-update-details\" data-update-details=\"progress-" + esc_attr(self.upgrader.update_current) + "\">" + "<p>" + php_sprintf(self.upgrader.strings["skin_update_successful"], title) + " <button type=\"button\" class=\"hide-if-no-js button-link js-update-details-toggle\" aria-expanded=\"false\">" + __("Show details.") + "</button>" + "</p></div>")
            # end if
            php_print("<script type=\"text/javascript\">jQuery('.waiting-" + esc_js(self.upgrader.update_current) + "').hide();</script>")
        # end if
        self.reset()
        self.flush_output()
    # end def after
    #// 
    #//
    def reset(self):
        
        self.in_loop = False
        self.error = False
    # end def reset
    #// 
    #//
    def flush_output(self):
        
        wp_ob_end_flush_all()
        flush()
    # end def flush_output
# end class Bulk_Upgrader_Skin
