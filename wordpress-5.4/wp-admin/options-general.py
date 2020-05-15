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
#// General settings administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
#// WordPress Translation Installation API
php_include_file(ABSPATH + "wp-admin/includes/translation-install.php", once=True)
if (not current_user_can("manage_options")):
    wp_die(__("Sorry, you are not allowed to manage options for this site."))
# end if
title = __("General Settings")
parent_file = "options-general.php"
#// translators: Date and time format for exact current time, mainly about timezones, see https://www.php.net/date
timezone_format = _x("Y-m-d H:i:s", "timezone date format")
add_action("admin_head", "options_general_add_js")
options_help = "<p>" + __("The fields on this screen determine some of the basics of your site setup.") + "</p>" + "<p>" + __("Most themes display the site title at the top of every page, in the title bar of the browser, and as the identifying name for syndicated feeds. The tagline is also displayed by many themes.") + "</p>"
if (not is_multisite()):
    options_help += "<p>" + __("The WordPress URL and the Site URL can be the same (example.com) or different; for example, having the WordPress core files (example.com/wordpress) in a subdirectory instead of the root directory.") + "</p>" + "<p>" + __("If you want site visitors to be able to register themselves, as opposed to by the site administrator, check the membership box. A default user role can be set for all new users, whether self-registered or registered by the site admin.") + "</p>"
# end if
options_help += "<p>" + __("You can set the language, and the translation files will be automatically downloaded and installed (available if your filesystem is writable).") + "</p>" + "<p>" + __("UTC means Coordinated Universal Time.") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": options_help}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/settings-general-screen/\">Documentation on General Settings</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1>")
php_print(esc_html(title))
php_print("""</h1>
<form method=\"post\" action=\"options.php\" novalidate=\"novalidate\">
""")
settings_fields("general")
php_print("""
<table class=\"form-table\" role=\"presentation\">
<tr>
<th scope=\"row\"><label for=\"blogname\">""")
_e("Site Title")
php_print("</label></th>\n<td><input name=\"blogname\" type=\"text\" id=\"blogname\" value=\"")
form_option("blogname")
php_print("""\" class=\"regular-text\" /></td>
</tr>
<tr>
<th scope=\"row\"><label for=\"blogdescription\">""")
_e("Tagline")
php_print("</label></th>\n<td><input name=\"blogdescription\" type=\"text\" id=\"blogdescription\" aria-describedby=\"tagline-description\" value=\"")
form_option("blogdescription")
php_print("\" class=\"regular-text\" />\n<p class=\"description\" id=\"tagline-description\">")
_e("In a few words, explain what this site is about.")
php_print("""</p></td>
</tr>
""")
if (not is_multisite()):
    wp_site_url_class = ""
    wp_home_class = ""
    if php_defined("WP_SITEURL"):
        wp_site_url_class = " disabled"
    # end if
    if php_defined("WP_HOME"):
        wp_home_class = " disabled"
    # end if
    php_print("\n<tr>\n<th scope=\"row\"><label for=\"siteurl\">")
    _e("WordPress Address (URL)")
    php_print("</label></th>\n<td><input name=\"siteurl\" type=\"url\" id=\"siteurl\" value=\"")
    form_option("siteurl")
    php_print("\"")
    disabled(php_defined("WP_SITEURL"))
    php_print(" class=\"regular-text code")
    php_print(wp_site_url_class)
    php_print("""\" /></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"home\">""")
    _e("Site Address (URL)")
    php_print("</label></th>\n<td><input name=\"home\" type=\"url\" id=\"home\" aria-describedby=\"home-description\" value=\"")
    form_option("home")
    php_print("\"")
    disabled(php_defined("WP_HOME"))
    php_print(" class=\"regular-text code")
    php_print(wp_home_class)
    php_print("\" />\n  ")
    if (not php_defined("WP_HOME")):
        php_print("<p class=\"description\" id=\"home-description\">\n      ")
        printf(__("Enter the address here if you <a href=\"%s\">want your site home page to be different from your WordPress installation directory</a>."), __("https://wordpress.org/support/article/giving-wordpress-its-own-directory/"))
        php_print("</p>\n")
    # end if
    php_print("""</td>
    </tr>
    """)
# end if
php_print("\n<tr>\n<th scope=\"row\"><label for=\"new_admin_email\">")
_e("Administration Email Address")
php_print("</label></th>\n<td><input name=\"new_admin_email\" type=\"email\" id=\"new_admin_email\" aria-describedby=\"new-admin-email-description\" value=\"")
form_option("admin_email")
php_print("\" class=\"regular-text ltr\" />\n<p class=\"description\" id=\"new-admin-email-description\">")
_e("This address is used for admin purposes. If you change this, we will send you an email at your new address to confirm it. <strong>The new address will not become active until confirmed.</strong>")
php_print("</p>\n")
new_admin_email = get_option("new_admin_email")
if new_admin_email and get_option("admin_email") != new_admin_email:
    php_print(" <div class=\"updated inline\">\n    <p>\n   ")
    printf(__("There is a pending change of the admin email to %s."), "<code>" + esc_html(new_admin_email) + "</code>")
    printf(" <a href=\"%1$s\">%2$s</a>", esc_url(wp_nonce_url(admin_url("options.php?dismiss=new_admin_email"), "dismiss-" + get_current_blog_id() + "-new_admin_email")), __("Cancel"))
    php_print(" </p>\n  </div>\n")
# end if
php_print("""</td>
</tr>
""")
if (not is_multisite()):
    php_print("\n<tr>\n<th scope=\"row\">")
    _e("Membership")
    php_print("</th>\n<td> <fieldset><legend class=\"screen-reader-text\"><span>")
    _e("Membership")
    php_print("</span></legend><label for=\"users_can_register\">\n<input name=\"users_can_register\" type=\"checkbox\" id=\"users_can_register\" value=\"1\" ")
    checked("1", get_option("users_can_register"))
    php_print(" />\n    ")
    _e("Anyone can register")
    php_print("""</label>
    </fieldset></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"default_role\">""")
    _e("New User Default Role")
    php_print("</label></th>\n<td>\n<select name=\"default_role\" id=\"default_role\">")
    wp_dropdown_roles(get_option("default_role"))
    php_print("""</select>
    </td>
    </tr>
    """)
# end if
languages = get_available_languages()
translations = wp_get_available_translations()
if (not is_multisite()) and php_defined("WPLANG") and "" != WPLANG and "en_US" != WPLANG and (not php_in_array(WPLANG, languages)):
    languages[-1] = WPLANG
# end if
if (not php_empty(lambda : languages)) or (not php_empty(lambda : translations)):
    php_print(" <tr>\n      <th scope=\"row\"><label for=\"WPLANG\">")
    _e("Site Language")
    php_print("<span class=\"dashicons dashicons-translation\" aria-hidden=\"true\"></span></label></th>\n      <td>\n          ")
    locale = get_locale()
    if (not php_in_array(locale, languages)):
        locale = ""
    # end if
    wp_dropdown_languages(Array({"name": "WPLANG", "id": "WPLANG", "selected": locale, "languages": languages, "translations": translations, "show_available_translations": current_user_can("install_languages") and wp_can_install_language_pack()}))
    #// Add note about deprecated WPLANG constant.
    if php_defined("WPLANG") and "" != WPLANG and WPLANG != locale:
        _deprecated_argument("define()", "4.0.0", php_sprintf(__("The %1$s constant in your %2$s file is no longer needed."), "WPLANG", "wp-config.php"))
    # end if
    php_print("     </td>\n </tr>\n ")
# end if
php_print("<tr>\n")
current_offset = get_option("gmt_offset")
tzstring = get_option("timezone_string")
check_zone_info = True
#// Remove old Etc mappings. Fallback to gmt_offset.
if False != php_strpos(tzstring, "Etc/GMT"):
    tzstring = ""
# end if
if php_empty(lambda : tzstring):
    #// Create a UTC+- zone if no timezone string exists.
    check_zone_info = False
    if 0 == current_offset:
        tzstring = "UTC+0"
    elif current_offset < 0:
        tzstring = "UTC" + current_offset
    else:
        tzstring = "UTC+" + current_offset
    # end if
# end if
php_print("<th scope=\"row\"><label for=\"timezone_string\">")
_e("Timezone")
php_print("""</label></th>
<td>
<select id=\"timezone_string\" name=\"timezone_string\" aria-describedby=\"timezone-description\">
""")
php_print(wp_timezone_choice(tzstring, get_user_locale()))
php_print("""</select>
<p class=\"description\" id=\"timezone-description\">
""")
printf(__("Choose either a city in the same timezone as you or a %s (Coordinated Universal Time) time offset."), "<abbr>UTC</abbr>")
php_print("""</p>
<p class=\"timezone-info\">
<span id=\"utc-time\">
""")
printf(__("Universal time is %s."), "<code>" + date_i18n(timezone_format, False, True) + "</code>")
php_print(" </span>\n")
if get_option("timezone_string") or (not php_empty(lambda : current_offset)):
    php_print(" <span id=\"local-time\">\n  ")
    printf(__("Local time is %s."), "<code>" + date_i18n(timezone_format) + "</code>")
    php_print(" </span>\n")
# end if
php_print("</p>\n\n")
if check_zone_info and tzstring:
    php_print("<p class=\"timezone-info\">\n<span>\n    ")
    now = php_new_class("DateTime", lambda : DateTime("now", php_new_class("DateTimeZone", lambda : DateTimeZone(tzstring))))
    dst = bool(now.format("I"))
    if dst:
        _e("This timezone is currently in daylight saving time.")
    else:
        _e("This timezone is currently in standard time.")
    # end if
    php_print(" <br />\n    ")
    if php_in_array(tzstring, timezone_identifiers_list()):
        transitions = timezone_transitions_get(timezone_open(tzstring), time())
        #// 0 index is the state at current time, 1 index is the next transition, if any.
        if (not php_empty(lambda : transitions[1])):
            php_print(" ")
            message = __("Daylight saving time begins on: %s.") if transitions[1]["isdst"] else __("Standard time begins on: %s.")
            printf(message, "<code>" + wp_date(__("F j, Y") + " " + __("g:i a"), transitions[1]["ts"]) + "</code>")
        else:
            _e("This timezone does not observe daylight saving time.")
        # end if
    # end if
    php_print(" </span>\n</p>\n")
# end if
php_print("""</td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Date Format")
php_print("</th>\n<td>\n    <fieldset><legend class=\"screen-reader-text\"><span>")
_e("Date Format")
php_print("</span></legend>\n")
#// 
#// Filters the default date formats.
#// 
#// @since 2.7.0
#// @since 4.0.0 Added ISO date standard YYYY-MM-DD format.
#// 
#// @param string[] $default_date_formats Array of default date formats.
#//
date_formats = array_unique(apply_filters("date_formats", Array(__("F j, Y"), "Y-m-d", "m/d/Y", "d/m/Y")))
custom = True
for format in date_formats:
    php_print(" <label><input type='radio' name='date_format' value='" + esc_attr(format) + "'")
    if get_option("date_format") == format:
        #// checked() uses "==" rather than "===".
        php_print(" checked='checked'")
        custom = False
    # end if
    php_print(" /> <span class=\"date-time-text format-i18n\">" + date_i18n(format) + "</span><code>" + esc_html(format) + "</code></label><br />\n")
# end for
php_print("<label><input type=\"radio\" name=\"date_format\" id=\"date_format_custom_radio\" value=\"\\c\\u\\s\\t\\o\\m\"")
checked(custom)
php_print("/> <span class=\"date-time-text date-time-custom-text\">" + __("Custom:") + "<span class=\"screen-reader-text\"> " + __("enter a custom date format in the following field") + "</span></span></label>" + "<label for=\"date_format_custom\" class=\"screen-reader-text\">" + __("Custom date format:") + "</label>" + "<input type=\"text\" name=\"date_format_custom\" id=\"date_format_custom\" value=\"" + esc_attr(get_option("date_format")) + "\" class=\"small-text\" />" + "<br />" + "<p><strong>" + __("Preview:") + "</strong> <span class=\"example\">" + date_i18n(get_option("date_format")) + "</span>" + "<span class='spinner'></span>\n" + "</p>")
php_print("""   </fieldset>
</td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Time Format")
php_print("</th>\n<td>\n    <fieldset><legend class=\"screen-reader-text\"><span>")
_e("Time Format")
php_print("</span></legend>\n")
#// 
#// Filters the default time formats.
#// 
#// @since 2.7.0
#// 
#// @param string[] $default_time_formats Array of default time formats.
#//
time_formats = array_unique(apply_filters("time_formats", Array(__("g:i a"), "g:i A", "H:i")))
custom = True
for format in time_formats:
    php_print(" <label><input type='radio' name='time_format' value='" + esc_attr(format) + "'")
    if get_option("time_format") == format:
        #// checked() uses "==" rather than "===".
        php_print(" checked='checked'")
        custom = False
    # end if
    php_print(" /> <span class=\"date-time-text format-i18n\">" + date_i18n(format) + "</span><code>" + esc_html(format) + "</code></label><br />\n")
# end for
php_print("<label><input type=\"radio\" name=\"time_format\" id=\"time_format_custom_radio\" value=\"\\c\\u\\s\\t\\o\\m\"")
checked(custom)
php_print("/> <span class=\"date-time-text date-time-custom-text\">" + __("Custom:") + "<span class=\"screen-reader-text\"> " + __("enter a custom time format in the following field") + "</span></span></label>" + "<label for=\"time_format_custom\" class=\"screen-reader-text\">" + __("Custom time format:") + "</label>" + "<input type=\"text\" name=\"time_format_custom\" id=\"time_format_custom\" value=\"" + esc_attr(get_option("time_format")) + "\" class=\"small-text\" />" + "<br />" + "<p><strong>" + __("Preview:") + "</strong> <span class=\"example\">" + date_i18n(get_option("time_format")) + "</span>" + "<span class='spinner'></span>\n" + "</p>")
php_print(" <p class='date-time-doc'>" + __("<a href=\"https://wordpress.org/support/article/formatting-date-and-time/\">Documentation on date and time formatting</a>.") + "</p>\n")
php_print("""   </fieldset>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"start_of_week\">""")
_e("Week Starts On")
php_print("</label></th>\n<td><select name=\"start_of_week\" id=\"start_of_week\">\n")
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#//
global wp_locale
php_check_if_defined("wp_locale")
day_index = 0
while day_index <= 6:
    
    selected = "selected=\"selected\"" if get_option("start_of_week") == day_index else ""
    php_print("\n   <option value='" + esc_attr(day_index) + str("' ") + str(selected) + str(">") + wp_locale.get_weekday(day_index) + "</option>")
    day_index += 1
# end while
php_print("</select></td>\n</tr>\n")
do_settings_fields("general", "default")
php_print("</table>\n\n")
do_settings_sections("general")
php_print("\n")
submit_button()
php_print("""</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
