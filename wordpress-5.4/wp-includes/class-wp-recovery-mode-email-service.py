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
#// Error Protection API: WP_Recovery_Mode_Email_Link class
#// 
#// @package WordPress
#// @since 5.2.0
#// 
#// 
#// Core class used to send an email with a link to begin Recovery Mode.
#// 
#// @since 5.2.0
#//
class WP_Recovery_Mode_Email_Service():
    RATE_LIMIT_OPTION = "recovery_mode_email_last_sent"
    link_service = Array()
    #// 
    #// WP_Recovery_Mode_Email_Service constructor.
    #// 
    #// @since 5.2.0
    #// 
    #// @param WP_Recovery_Mode_Link_Service $link_service
    #//
    def __init__(self, link_service=None):
        
        self.link_service = link_service
    # end def __init__
    #// 
    #// Sends the recovery mode email if the rate limit has not been sent.
    #// 
    #// @since 5.2.0
    #// 
    #// @param int   $rate_limit Number of seconds before another email can be sent.
    #// @param array $error      Error details from {@see error_get_last()}
    #// @param array $extension  The extension that caused the error. {
    #// @type string $slug The extension slug. The plugin or theme's directory.
    #// @type string $type The extension type. Either 'plugin' or 'theme'.
    #// }
    #// @return true|WP_Error True if email sent, WP_Error otherwise.
    #//
    def maybe_send_recovery_mode_email(self, rate_limit=None, error=None, extension=None):
        
        last_sent = get_option(self.RATE_LIMIT_OPTION)
        if (not last_sent) or time() > last_sent + rate_limit:
            if (not update_option(self.RATE_LIMIT_OPTION, time())):
                return php_new_class("WP_Error", lambda : WP_Error("storage_error", __("Could not update the email last sent time.")))
            # end if
            sent = self.send_recovery_mode_email(rate_limit, error, extension)
            if sent:
                return True
            # end if
            return php_new_class("WP_Error", lambda : WP_Error("email_failed", php_sprintf(__("The email could not be sent. Possible reason: your host may have disabled the %s function."), "mail()")))
        # end if
        err_message = php_sprintf(__("A recovery link was already sent %1$s ago. Please wait another %2$s before requesting a new email."), human_time_diff(last_sent), human_time_diff(last_sent + rate_limit))
        return php_new_class("WP_Error", lambda : WP_Error("email_sent_already", err_message))
    # end def maybe_send_recovery_mode_email
    #// 
    #// Clears the rate limit, allowing a new recovery mode email to be sent immediately.
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool True on success, false on failure.
    #//
    def clear_rate_limit(self):
        
        return delete_option(self.RATE_LIMIT_OPTION)
    # end def clear_rate_limit
    #// 
    #// Sends the Recovery Mode email to the site admin email address.
    #// 
    #// @since 5.2.0
    #// 
    #// @param int   $rate_limit Number of seconds before another email can be sent.
    #// @param array $error      Error details from {@see error_get_last()}
    #// @param array $extension  Extension that caused the error.
    #// 
    #// @return bool Whether the email was sent successfully.
    #//
    def send_recovery_mode_email(self, rate_limit=None, error=None, extension=None):
        
        url = self.link_service.generate_url()
        blogname = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        switched_locale = False
        #// The switch_to_locale() function is loaded before it can actually be used.
        if php_function_exists("switch_to_locale") and (php_isset(lambda : PHP_GLOBALS["wp_locale_switcher"])):
            switched_locale = switch_to_locale(get_locale())
        # end if
        if extension:
            cause = self.get_cause(extension)
            details = wp_strip_all_tags(wp_get_extension_error_description(error))
            if details:
                header = __("Error Details")
                details = "\n\n" + header + "\n" + php_str_pad("", php_strlen(header), "=") + "\n" + details
            # end if
        else:
            cause = ""
            details = ""
        # end if
        #// 
        #// Filters the support message sent with the the fatal error protection email.
        #// 
        #// @since 5.2.0
        #// 
        #// @param $message string The Message to include in the email.
        #//
        support = apply_filters("recovery_email_support_info", __("Please contact your host for assistance with investigating this issue further."))
        #// 
        #// Filters the debug information included in the fatal error protection email.
        #// 
        #// @since 5.3.0
        #// 
        #// @param $message array An associated array of debug information.
        #//
        debug = apply_filters("recovery_email_debug_info", self.get_debug(extension))
        #// translators: Do not translate LINK, EXPIRES, CAUSE, DETAILS, SITEURL, PAGEURL, SUPPORT. DEBUG: those are placeholders.
        message = __("""Howdy!
        Since WordPress 5.2 there is a built-in feature that detects when a plugin or theme causes a fatal error on your site, and notifies you with this automated email.
        ###CAUSE###
        First, visit your website (###SITEURL###) and check for any visible issues. Next, visit the page where the error was caught (###PAGEURL###) and check for any visible issues.
        ###SUPPORT###
        If your site appears broken and you can't access your dashboard normally, WordPress now has a special \"recovery mode\". This lets you safely login to your dashboard and investigate further.
        ###LINK###
        To keep your site safe, this link will expire in ###EXPIRES###. Don't worry about that, though: a new link will be emailed to you if the error occurs again after it expires.
        When seeking help with this issue, you may be asked for some of the following information:
        ###DEBUG###
        ###DETAILS###""")
        message = php_str_replace(Array("###LINK###", "###EXPIRES###", "###CAUSE###", "###DETAILS###", "###SITEURL###", "###PAGEURL###", "###SUPPORT###", "###DEBUG###"), Array(url, human_time_diff(time() + rate_limit), str("\n") + str(cause) + str("\n") if cause else "\n", details, home_url("/"), home_url(PHP_SERVER["REQUEST_URI"]), support, php_implode("\r\n", debug)), message)
        email = Array({"to": self.get_recovery_mode_email_address(), "subject": __("[%s] Your Site is Experiencing a Technical Issue"), "message": message, "headers": ""})
        #// 
        #// Filter the contents of the Recovery Mode email.
        #// 
        #// @since 5.2.0
        #// 
        #// @param array  $email Used to build wp_mail().
        #// @param string $url   URL to enter recovery mode.
        #//
        email = apply_filters("recovery_mode_email", email, url)
        sent = wp_mail(email["to"], wp_specialchars_decode(php_sprintf(email["subject"], blogname)), email["message"], email["headers"])
        if switched_locale:
            restore_previous_locale()
        # end if
        return sent
    # end def send_recovery_mode_email
    #// 
    #// Gets the email address to send the recovery mode link to.
    #// 
    #// @since 5.2.0
    #// 
    #// @return string Email address to send recovery mode link to.
    #//
    def get_recovery_mode_email_address(self):
        
        if php_defined("RECOVERY_MODE_EMAIL") and is_email(RECOVERY_MODE_EMAIL):
            return RECOVERY_MODE_EMAIL
        # end if
        return get_option("admin_email")
    # end def get_recovery_mode_email_address
    #// 
    #// Gets the description indicating the possible cause for the error.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $extension The extension that caused the error.
    #// @return string Message about which extension caused the error.
    #//
    def get_cause(self, extension=None):
        
        if "plugin" == extension["type"]:
            plugin = self.get_plugin(extension)
            if False == plugin:
                name = extension["slug"]
            else:
                name = plugin["Name"]
            # end if
            #// translators: %s: Plugin name.
            cause = php_sprintf(__("In this case, WordPress caught an error with one of your plugins, %s."), name)
        else:
            theme = wp_get_theme(extension["slug"])
            name = theme.display("Name") if theme.exists() else extension["slug"]
            #// translators: %s: Theme name.
            cause = php_sprintf(__("In this case, WordPress caught an error with your theme, %s."), name)
        # end if
        return cause
    # end def get_cause
    #// 
    #// Return the details for a single plugin based on the extension data from an error.
    #// 
    #// @since 5.3.0
    #// 
    #// @param array $extension The extension that caused the error.
    #// @return bool|array A plugin array {@see get_plugins()} or `false` if no plugin was found.
    #//
    def get_plugin(self, extension=None):
        
        if (not php_function_exists("get_plugins")):
            php_include_file(ABSPATH + "wp-admin/includes/plugin.php", once=True)
        # end if
        plugins = get_plugins()
        #// Assume plugin main file name first since it is a common convention.
        if (php_isset(lambda : plugins[str(extension["slug"]) + str("/") + str(extension["slug"]) + str(".php")])):
            return plugins[str(extension["slug"]) + str("/") + str(extension["slug"]) + str(".php")]
        else:
            for file,plugin_data in plugins:
                if 0 == php_strpos(file, str(extension["slug"]) + str("/")) or file == extension["slug"]:
                    return plugin_data
                # end if
            # end for
        # end if
        return False
    # end def get_plugin
    #// 
    #// Return debug information in an easy to manipulate format.
    #// 
    #// @since 5.3.0
    #// 
    #// @param array $extension The extension that caused the error.
    #// @return array An associative array of debug information.
    #//
    def get_debug(self, extension=None):
        
        theme = wp_get_theme()
        wp_version = get_bloginfo("version")
        if extension:
            plugin = self.get_plugin(extension)
        else:
            plugin = None
        # end if
        debug = Array({"wp": php_sprintf(__("WordPress version %s"), wp_version), "theme": php_sprintf(__("Current theme: %1$s (version %2$s)"), theme.get("Name"), theme.get("Version"))})
        if None != plugin:
            debug["plugin"] = php_sprintf(__("Current plugin: %1$s (version %2$s)"), plugin["Name"], plugin["Version"])
        # end if
        debug["php"] = php_sprintf(__("PHP version %s"), PHP_VERSION)
        return debug
    # end def get_debug
# end class WP_Recovery_Mode_Email_Service
