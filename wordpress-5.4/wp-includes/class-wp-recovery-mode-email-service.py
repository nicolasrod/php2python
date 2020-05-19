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
    #// 
    #// Service to generate recovery mode URLs.
    #// 
    #// @since 5.2.0
    #// @var WP_Recovery_Mode_Link_Service
    #//
    link_service = Array()
    #// 
    #// WP_Recovery_Mode_Email_Service constructor.
    #// 
    #// @since 5.2.0
    #// 
    #// @param WP_Recovery_Mode_Link_Service $link_service
    #//
    def __init__(self, link_service_=None):
        
        
        self.link_service = link_service_
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
    def maybe_send_recovery_mode_email(self, rate_limit_=None, error_=None, extension_=None):
        
        
        last_sent_ = get_option(self.RATE_LIMIT_OPTION)
        if (not last_sent_) or time() > last_sent_ + rate_limit_:
            if (not update_option(self.RATE_LIMIT_OPTION, time())):
                return php_new_class("WP_Error", lambda : WP_Error("storage_error", __("Could not update the email last sent time.")))
            # end if
            sent_ = self.send_recovery_mode_email(rate_limit_, error_, extension_)
            if sent_:
                return True
            # end if
            return php_new_class("WP_Error", lambda : WP_Error("email_failed", php_sprintf(__("The email could not be sent. Possible reason: your host may have disabled the %s function."), "mail()")))
        # end if
        err_message_ = php_sprintf(__("A recovery link was already sent %1$s ago. Please wait another %2$s before requesting a new email."), human_time_diff(last_sent_), human_time_diff(last_sent_ + rate_limit_))
        return php_new_class("WP_Error", lambda : WP_Error("email_sent_already", err_message_))
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
    def send_recovery_mode_email(self, rate_limit_=None, error_=None, extension_=None):
        
        
        url_ = self.link_service.generate_url()
        blogname_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        switched_locale_ = False
        #// The switch_to_locale() function is loaded before it can actually be used.
        if php_function_exists("switch_to_locale") and (php_isset(lambda : PHP_GLOBALS["wp_locale_switcher"])):
            switched_locale_ = switch_to_locale(get_locale())
        # end if
        if extension_:
            cause_ = self.get_cause(extension_)
            details_ = wp_strip_all_tags(wp_get_extension_error_description(error_))
            if details_:
                header_ = __("Error Details")
                details_ = "\n\n" + header_ + "\n" + php_str_pad("", php_strlen(header_), "=") + "\n" + details_
            # end if
        else:
            cause_ = ""
            details_ = ""
        # end if
        #// 
        #// Filters the support message sent with the the fatal error protection email.
        #// 
        #// @since 5.2.0
        #// 
        #// @param $message string The Message to include in the email.
        #//
        support_ = apply_filters("recovery_email_support_info", __("Please contact your host for assistance with investigating this issue further."))
        #// 
        #// Filters the debug information included in the fatal error protection email.
        #// 
        #// @since 5.3.0
        #// 
        #// @param $message array An associated array of debug information.
        #//
        debug_ = apply_filters("recovery_email_debug_info", self.get_debug(extension_))
        #// translators: Do not translate LINK, EXPIRES, CAUSE, DETAILS, SITEURL, PAGEURL, SUPPORT. DEBUG: those are placeholders.
        message_ = __("""Howdy!
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
        message_ = php_str_replace(Array("###LINK###", "###EXPIRES###", "###CAUSE###", "###DETAILS###", "###SITEURL###", "###PAGEURL###", "###SUPPORT###", "###DEBUG###"), Array(url_, human_time_diff(time() + rate_limit_), str("\n") + str(cause_) + str("\n") if cause_ else "\n", details_, home_url("/"), home_url(PHP_SERVER["REQUEST_URI"]), support_, php_implode("\r\n", debug_)), message_)
        email_ = Array({"to": self.get_recovery_mode_email_address(), "subject": __("[%s] Your Site is Experiencing a Technical Issue"), "message": message_, "headers": ""})
        #// 
        #// Filter the contents of the Recovery Mode email.
        #// 
        #// @since 5.2.0
        #// 
        #// @param array  $email Used to build wp_mail().
        #// @param string $url   URL to enter recovery mode.
        #//
        email_ = apply_filters("recovery_mode_email", email_, url_)
        sent_ = wp_mail(email_["to"], wp_specialchars_decode(php_sprintf(email_["subject"], blogname_)), email_["message"], email_["headers"])
        if switched_locale_:
            restore_previous_locale()
        # end if
        return sent_
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
    def get_cause(self, extension_=None):
        
        
        if "plugin" == extension_["type"]:
            plugin_ = self.get_plugin(extension_)
            if False == plugin_:
                name_ = extension_["slug"]
            else:
                name_ = plugin_["Name"]
            # end if
            #// translators: %s: Plugin name.
            cause_ = php_sprintf(__("In this case, WordPress caught an error with one of your plugins, %s."), name_)
        else:
            theme_ = wp_get_theme(extension_["slug"])
            name_ = theme_.display("Name") if theme_.exists() else extension_["slug"]
            #// translators: %s: Theme name.
            cause_ = php_sprintf(__("In this case, WordPress caught an error with your theme, %s."), name_)
        # end if
        return cause_
    # end def get_cause
    #// 
    #// Return the details for a single plugin based on the extension data from an error.
    #// 
    #// @since 5.3.0
    #// 
    #// @param array $extension The extension that caused the error.
    #// @return bool|array A plugin array {@see get_plugins()} or `false` if no plugin was found.
    #//
    def get_plugin(self, extension_=None):
        
        
        if (not php_function_exists("get_plugins")):
            php_include_file(ABSPATH + "wp-admin/includes/plugin.php", once=True)
        # end if
        plugins_ = get_plugins()
        #// Assume plugin main file name first since it is a common convention.
        if (php_isset(lambda : plugins_[str(extension_["slug"]) + str("/") + str(extension_["slug"]) + str(".php")])):
            return plugins_[str(extension_["slug"]) + str("/") + str(extension_["slug"]) + str(".php")]
        else:
            for file_,plugin_data_ in plugins_.items():
                if 0 == php_strpos(file_, str(extension_["slug"]) + str("/")) or file_ == extension_["slug"]:
                    return plugin_data_
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
    def get_debug(self, extension_=None):
        
        
        theme_ = wp_get_theme()
        wp_version_ = get_bloginfo("version")
        if extension_:
            plugin_ = self.get_plugin(extension_)
        else:
            plugin_ = None
        # end if
        debug_ = Array({"wp": php_sprintf(__("WordPress version %s"), wp_version_), "theme": php_sprintf(__("Current theme: %1$s (version %2$s)"), theme_.get("Name"), theme_.get("Version"))})
        if None != plugin_:
            debug_["plugin"] = php_sprintf(__("Current plugin: %1$s (version %2$s)"), plugin_["Name"], plugin_["Version"])
        # end if
        debug_["php"] = php_sprintf(__("PHP version %s"), PHP_VERSION)
        return debug_
    # end def get_debug
# end class WP_Recovery_Mode_Email_Service
