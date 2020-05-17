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
#// Options Management Administration Screen.
#// 
#// If accessed directly in a browser this page shows a list of all saved options
#// along with editable fields for their values. Serialized data is not supported
#// and there is no way to remove options via this page. It is not linked to from
#// anywhere else in the admin.
#// 
#// This file is also the target of the forms in core and custom options pages
#// that use the Settings API. In this case it saves the new option values
#// and returns the user to their page of origin.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
title_ = __("Settings")
this_file_ = "options.php"
parent_file_ = "options-general.php"
wp_reset_vars(Array("action", "option_page"))
capability_ = "manage_options"
#// This is for back compat and will eventually be removed.
if php_empty(lambda : option_page_):
    option_page_ = "options"
else:
    #// 
    #// Filters the capability required when using the Settings API.
    #// 
    #// By default, the options groups for all registered settings require the manage_options capability.
    #// This filter is required to change the capability required for a certain options page.
    #// 
    #// @since 3.2.0
    #// 
    #// @param string $capability The capability used for the page, which is manage_options by default.
    #//
    capability_ = apply_filters(str("option_page_capability_") + str(option_page_), capability_)
# end if
if (not current_user_can(capability_)):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to manage options for this site.") + "</p>", 403)
# end if
#// Handle admin email change requests.
if (not php_empty(lambda : PHP_REQUEST["adminhash"])):
    new_admin_details_ = get_option("adminhash")
    redirect_ = "options-general.php?updated=false"
    if php_is_array(new_admin_details_) and hash_equals(new_admin_details_["hash"], PHP_REQUEST["adminhash"]) and (not php_empty(lambda : new_admin_details_["newemail"])):
        update_option("admin_email", new_admin_details_["newemail"])
        delete_option("adminhash")
        delete_option("new_admin_email")
        redirect_ = "options-general.php?updated=true"
    # end if
    wp_redirect(admin_url(redirect_))
    php_exit(0)
elif (not php_empty(lambda : PHP_REQUEST["dismiss"])) and "new_admin_email" == PHP_REQUEST["dismiss"]:
    check_admin_referer("dismiss-" + get_current_blog_id() + "-new_admin_email")
    delete_option("adminhash")
    delete_option("new_admin_email")
    wp_redirect(admin_url("options-general.php?updated=true"))
    php_exit(0)
# end if
if is_multisite() and (not current_user_can("manage_network_options")) and "update" != action_:
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to delete these items.") + "</p>", 403)
# end if
whitelist_options_ = Array({"general": Array("blogname", "blogdescription", "gmt_offset", "date_format", "time_format", "start_of_week", "timezone_string", "WPLANG", "new_admin_email"), "discussion": Array("default_pingback_flag", "default_ping_status", "default_comment_status", "comments_notify", "moderation_notify", "comment_moderation", "require_name_email", "comment_whitelist", "comment_max_links", "moderation_keys", "blacklist_keys", "show_avatars", "avatar_rating", "avatar_default", "close_comments_for_old_posts", "close_comments_days_old", "thread_comments", "thread_comments_depth", "page_comments", "comments_per_page", "default_comments_page", "comment_order", "comment_registration", "show_comments_cookies_opt_in"), "media": Array("thumbnail_size_w", "thumbnail_size_h", "thumbnail_crop", "medium_size_w", "medium_size_h", "large_size_w", "large_size_h", "image_default_size", "image_default_align", "image_default_link_type"), "reading": Array("posts_per_page", "posts_per_rss", "rss_use_excerpt", "show_on_front", "page_on_front", "page_for_posts", "blog_public"), "writing": Array("default_category", "default_email_category", "default_link_category", "default_post_format")})
whitelist_options_["misc"] = Array()
whitelist_options_["options"] = Array()
whitelist_options_["privacy"] = Array()
mail_options_ = Array("mailserver_url", "mailserver_port", "mailserver_login", "mailserver_pass")
if (not php_in_array(get_option("blog_charset"), Array("utf8", "utf-8", "UTF8", "UTF-8"))):
    whitelist_options_["reading"][-1] = "blog_charset"
# end if
if get_site_option("initial_db_version") < 32453:
    whitelist_options_["writing"][-1] = "use_smilies"
    whitelist_options_["writing"][-1] = "use_balanceTags"
# end if
if (not is_multisite()):
    if (not php_defined("WP_SITEURL")):
        whitelist_options_["general"][-1] = "siteurl"
    # end if
    if (not php_defined("WP_HOME")):
        whitelist_options_["general"][-1] = "home"
    # end if
    whitelist_options_["general"][-1] = "users_can_register"
    whitelist_options_["general"][-1] = "default_role"
    whitelist_options_["writing"] = php_array_merge(whitelist_options_["writing"], mail_options_)
    whitelist_options_["writing"][-1] = "ping_sites"
    whitelist_options_["media"][-1] = "uploads_use_yearmonth_folders"
    #// If upload_url_path and upload_path are both default values, they're locked.
    if get_option("upload_url_path") or get_option("upload_path") != "wp-content/uploads" and get_option("upload_path"):
        whitelist_options_["media"][-1] = "upload_path"
        whitelist_options_["media"][-1] = "upload_url_path"
    # end if
else:
    #// 
    #// Filters whether the post-by-email functionality is enabled.
    #// 
    #// @since 3.0.0
    #// 
    #// @param bool $enabled Whether post-by-email configuration is enabled. Default true.
    #//
    if apply_filters("enable_post_by_email_configuration", True):
        whitelist_options_["writing"] = php_array_merge(whitelist_options_["writing"], mail_options_)
    # end if
# end if
#// 
#// Filters the options whitelist.
#// 
#// @since 2.7.0
#// 
#// @param array $whitelist_options The options whitelist.
#//
whitelist_options_ = apply_filters("whitelist_options", whitelist_options_)
if "update" == action_:
    #// We are saving settings sent from a settings page.
    if "options" == option_page_ and (not (php_isset(lambda : PHP_POST["option_page"]))):
        #// This is for back compat and will eventually be removed.
        unregistered_ = True
        check_admin_referer("update-options")
    else:
        unregistered_ = False
        check_admin_referer(option_page_ + "-options")
    # end if
    if (not (php_isset(lambda : whitelist_options_[option_page_]))):
        wp_die(php_sprintf(__("<strong>Error</strong>: Options page %s not found in the options whitelist."), "<code>" + esc_html(option_page_) + "</code>"))
    # end if
    if "options" == option_page_:
        if is_multisite() and (not current_user_can("manage_network_options")):
            wp_die(__("Sorry, you are not allowed to modify unregistered settings for this site."))
        # end if
        options_ = php_explode(",", wp_unslash(PHP_POST["page_options"]))
    else:
        options_ = whitelist_options_[option_page_]
    # end if
    if "general" == option_page_:
        #// Handle custom date/time formats.
        if (not php_empty(lambda : PHP_POST["date_format"])) and (php_isset(lambda : PHP_POST["date_format_custom"])) and "\\c\\u\\s\\t\\o\\m" == wp_unslash(PHP_POST["date_format"]):
            PHP_POST["date_format"] = PHP_POST["date_format_custom"]
        # end if
        if (not php_empty(lambda : PHP_POST["time_format"])) and (php_isset(lambda : PHP_POST["time_format_custom"])) and "\\c\\u\\s\\t\\o\\m" == wp_unslash(PHP_POST["time_format"]):
            PHP_POST["time_format"] = PHP_POST["time_format_custom"]
        # end if
        #// Map UTC+- timezones to gmt_offsets and set timezone_string to empty.
        if (not php_empty(lambda : PHP_POST["timezone_string"])) and php_preg_match("/^UTC[+-]/", PHP_POST["timezone_string"]):
            PHP_POST["gmt_offset"] = PHP_POST["timezone_string"]
            PHP_POST["gmt_offset"] = php_preg_replace("/UTC\\+?/", "", PHP_POST["gmt_offset"])
            PHP_POST["timezone_string"] = ""
        # end if
        #// Handle translation installation.
        if (not php_empty(lambda : PHP_POST["WPLANG"])) and current_user_can("install_languages"):
            php_include_file(ABSPATH + "wp-admin/includes/translation-install.php", once=True)
            if wp_can_install_language_pack():
                language_ = wp_download_language_pack(PHP_POST["WPLANG"])
                if language_:
                    PHP_POST["WPLANG"] = language_
                # end if
            # end if
        # end if
    # end if
    if options_:
        user_language_old_ = get_user_locale()
        for option_ in options_:
            if unregistered_:
                _deprecated_argument("options.php", "2.7.0", php_sprintf(__("The %s setting is unregistered. Unregistered settings are deprecated. See https://developer.wordpress.org/plugins/settings/settings-api/"), "<code>" + esc_html(option_) + "</code>"))
            # end if
            option_ = php_trim(option_)
            value_ = None
            if (php_isset(lambda : PHP_POST[option_])):
                value_ = PHP_POST[option_]
                if (not php_is_array(value_)):
                    value_ = php_trim(value_)
                # end if
                value_ = wp_unslash(value_)
            # end if
            update_option(option_, value_)
        # end for
        PHP_GLOBALS["locale"] = None
        user_language_new_ = get_user_locale()
        if user_language_old_ != user_language_new_:
            load_default_textdomain(user_language_new_)
        # end if
    # end if
    #// 
    #// Handle settings errors and return to options page.
    #// 
    #// If no settings errors were registered add a general 'updated' message.
    if (not php_count(get_settings_errors())):
        add_settings_error("general", "settings_updated", __("Settings saved."), "success")
    # end if
    set_transient("settings_errors", get_settings_errors(), 30)
    #// Redirect back to the settings page that was submitted.
    goback_ = add_query_arg("settings-updated", "true", wp_get_referer())
    wp_redirect(goback_)
    php_exit(0)
# end if
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n <h1>")
esc_html_e("All Settings")
php_print("""</h1>
<div class=\"notice notice-warning\">
<p><strong>""")
_e("WARNING!")
php_print("</strong> ")
_e("This page allows direct access to your site settings. You can break things here. Please be cautious!")
php_print("""</p>
</div>
<form name=\"form\" action=\"options.php\" method=\"post\" id=\"all-options\">
""")
wp_nonce_field("options-options")
php_print("""       <input type=\"hidden\" name=\"action\" value=\"update\" />
<input type=\"hidden\" name=\"option_page\" value=\"options\" />
<table class=\"form-table\" role=\"presentation\">
""")
options_ = wpdb_.get_results(str("SELECT * FROM ") + str(wpdb_.options) + str(" ORDER BY option_name"))
for option_ in options_:
    disabled_ = False
    if "" == option_.option_name:
        continue
    # end if
    if is_serialized(option_.option_value):
        if is_serialized_string(option_.option_value):
            #// This is a serialized string, so we should display it.
            value_ = maybe_unserialize(option_.option_value)
            options_to_update_[-1] = option_.option_name
            class_ = "all-options"
        else:
            value_ = "SERIALIZED DATA"
            disabled_ = True
            class_ = "all-options disabled"
        # end if
    else:
        value_ = option_.option_value
        options_to_update_[-1] = option_.option_name
        class_ = "all-options"
    # end if
    name_ = esc_attr(option_.option_name)
    php_print("<tr>\n   <th scope=\"row\"><label for=\"")
    php_print(name_)
    php_print("\">")
    php_print(esc_html(option_.option_name))
    php_print("</label></th>\n<td>\n    ")
    if php_strpos(value_, "\n") != False:
        php_print("     <textarea class=\"")
        php_print(class_)
        php_print("\" name=\"")
        php_print(name_)
        php_print("\" id=\"")
        php_print(name_)
        php_print("\" cols=\"30\" rows=\"5\">")
        php_print(esc_textarea(value_))
        php_print("</textarea>\n    ")
    else:
        php_print("     <input class=\"regular-text ")
        php_print(class_)
        php_print("\" type=\"text\" name=\"")
        php_print(name_)
        php_print("\" id=\"")
        php_print(name_)
        php_print("\" value=\"")
        php_print(esc_attr(value_))
        php_print("\"")
        disabled(disabled_, True)
        php_print(" />\n    ")
    # end if
    php_print("</td>\n</tr>\n")
# end for
php_print("</table>\n\n<input type=\"hidden\" name=\"page_options\" value=\"")
php_print(esc_attr(php_implode(",", options_to_update_)))
php_print("\" />\n\n")
submit_button(__("Save Changes"), "primary", "Update")
php_print("""
</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
