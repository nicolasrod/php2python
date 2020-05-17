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
#// Writing settings administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_options")):
    wp_die(__("Sorry, you are not allowed to manage options for this site."))
# end if
title_ = __("Writing Settings")
parent_file_ = "options-general.php"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("You can submit content in several different ways; this screen holds the settings for all of them. The top section controls the editor within the dashboard, while the rest control external publishing methods. For more information on any of these methods, use the documentation links.") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
#// This filter is documented in wp-admin/options.php
if apply_filters("enable_post_by_email_configuration", True):
    get_current_screen().add_help_tab(Array({"id": "options-postemail", "title": __("Post Via Email"), "content": "<p>" + __("Post via email settings allow you to send your WordPress installation an email with the content of your post. You must set up a secret email account with POP3 access to use this, and any mail received at this address will be posted, so it&#8217;s a good idea to keep this address very secret.") + "</p>"}))
# end if
#// This filter is documented in wp-admin/options-writing.php
if apply_filters("enable_update_services_configuration", True):
    get_current_screen().add_help_tab(Array({"id": "options-services", "title": __("Update Services"), "content": "<p>" + __("If desired, WordPress will automatically alert various services of your new posts.") + "</p>"}))
# end if
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/settings-writing-screen/\">Documentation on Writing Settings</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1>")
php_print(esc_html(title_))
php_print("""</h1>
<form method=\"post\" action=\"options.php\">
""")
settings_fields("writing")
php_print("\n<table class=\"form-table\" role=\"presentation\">\n")
if get_site_option("initial_db_version") < 32453:
    php_print("<tr>\n<th scope=\"row\">")
    _e("Formatting")
    php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
    _e("Formatting")
    php_print("</span></legend>\n<label for=\"use_smilies\">\n<input name=\"use_smilies\" type=\"checkbox\" id=\"use_smilies\" value=\"1\" ")
    checked("1", get_option("use_smilies"))
    php_print(" />\n    ")
    _e("Convert emoticons like <code>:-)</code> and <code>:-P</code> to graphics on display")
    php_print("</label><br />\n<label for=\"use_balanceTags\"><input name=\"use_balanceTags\" type=\"checkbox\" id=\"use_balanceTags\" value=\"1\" ")
    checked("1", get_option("use_balanceTags"))
    php_print(" /> ")
    _e("WordPress should correct invalidly nested XHTML automatically")
    php_print("""</label>
    </fieldset></td>
    </tr>
    """)
# end if
php_print("<tr>\n<th scope=\"row\"><label for=\"default_category\">")
_e("Default Post Category")
php_print("</label></th>\n<td>\n")
wp_dropdown_categories(Array({"hide_empty": 0, "name": "default_category", "orderby": "name", "selected": get_option("default_category"), "hierarchical": True}))
php_print("</td>\n</tr>\n")
post_formats_ = get_post_format_strings()
post_formats_["standard"] = None
php_print("<tr>\n<th scope=\"row\"><label for=\"default_post_format\">")
_e("Default Post Format")
php_print("""</label></th>
<td>
<select name=\"default_post_format\" id=\"default_post_format\">
<option value=\"0\">""")
php_print(get_post_format_string("standard"))
php_print("</option>\n")
for format_slug_,format_name_ in post_formats_:
    php_print("     <option")
    selected(get_option("default_post_format"), format_slug_)
    php_print(" value=\"")
    php_print(esc_attr(format_slug_))
    php_print("\">")
    php_print(esc_html(format_name_))
    php_print("</option>\n")
# end for
php_print("""   </select>
</td>
</tr>
""")
if get_option("link_manager_enabled"):
    php_print("<tr>\n<th scope=\"row\"><label for=\"default_link_category\">")
    _e("Default Link Category")
    php_print("</label></th>\n<td>\n    ")
    wp_dropdown_categories(Array({"hide_empty": 0, "name": "default_link_category", "orderby": "name", "selected": get_option("default_link_category"), "hierarchical": True, "taxonomy": "link_category"}))
    php_print("</td>\n</tr>\n")
# end if
php_print("\n")
do_settings_fields("writing", "default")
do_settings_fields("writing", "remote_publishing")
pass
php_print("</table>\n\n")
#// This filter is documented in wp-admin/options.php
if apply_filters("enable_post_by_email_configuration", True):
    php_print("<h2 class=\"title\">")
    _e("Post via email")
    php_print("</h2>\n<p>\n ")
    printf(__("To post to WordPress by email you must set up a secret email account with POP3 access. Any mail received at this address will be posted, so it&#8217;s a good idea to keep this address very secret. Here are three random strings you could use: %1$s, %2$s, %3$s."), php_sprintf("<kbd>%s</kbd>", wp_generate_password(8, False)), php_sprintf("<kbd>%s</kbd>", wp_generate_password(8, False)), php_sprintf("<kbd>%s</kbd>", wp_generate_password(8, False)))
    php_print("""</p>
    <table class=\"form-table\" role=\"presentation\">
    <tr>
    <th scope=\"row\"><label for=\"mailserver_url\">""")
    _e("Mail Server")
    php_print("</label></th>\n<td><input name=\"mailserver_url\" type=\"text\" id=\"mailserver_url\" value=\"")
    form_option("mailserver_url")
    php_print("\" class=\"regular-text code\" />\n<label for=\"mailserver_port\">")
    _e("Port")
    php_print("</label>\n<input name=\"mailserver_port\" type=\"text\" id=\"mailserver_port\" value=\"")
    form_option("mailserver_port")
    php_print("""\" class=\"small-text\" />
    </td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"mailserver_login\">""")
    _e("Login Name")
    php_print("</label></th>\n<td><input name=\"mailserver_login\" type=\"text\" id=\"mailserver_login\" value=\"")
    form_option("mailserver_login")
    php_print("""\" class=\"regular-text ltr\" /></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"mailserver_pass\">""")
    _e("Password")
    php_print("</label></th>\n<td>\n<input name=\"mailserver_pass\" type=\"text\" id=\"mailserver_pass\" value=\"")
    form_option("mailserver_pass")
    php_print("""\" class=\"regular-text ltr\" />
    </td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"default_email_category\">""")
    _e("Default Mail Category")
    php_print("</label></th>\n<td>\n    ")
    wp_dropdown_categories(Array({"hide_empty": 0, "name": "default_email_category", "orderby": "name", "selected": get_option("default_email_category"), "hierarchical": True}))
    php_print("</td>\n</tr>\n   ")
    do_settings_fields("writing", "post_via_email")
    php_print("</table>\n")
# end if
php_print("\n")
#// 
#// Filters whether to enable the Update Services section in the Writing settings screen.
#// 
#// @since 3.0.0
#// 
#// @param bool $enable Whether to enable the Update Services settings area. Default true.
#//
if apply_filters("enable_update_services_configuration", True):
    php_print("<h2 class=\"title\">")
    _e("Update Services")
    php_print("</h2>\n\n    ")
    if 1 == get_option("blog_public"):
        php_print("\n   <p><label for=\"ping_sites\">\n     ")
        printf(__("When you publish a new post, WordPress automatically notifies the following site update services. For more about this, see <a href=\"%s\">Update Services</a> on the Codex. Separate multiple service URLs with line breaks."), __("https://codex.wordpress.org/Update_Services"))
        php_print(" </label></p>\n\n    <textarea name=\"ping_sites\" id=\"ping_sites\" class=\"large-text code\" rows=\"3\">")
        php_print(esc_textarea(get_option("ping_sites")))
        php_print("</textarea>\n\n  ")
    else:
        php_print("\n   <p>\n       ")
        printf(__("WordPress is not notifying any <a href=\"%1$s\">Update Services</a> because of your site&#8217;s <a href=\"%2$s\">visibility settings</a>."), __("https://codex.wordpress.org/Update_Services"), "options-reading.php")
        php_print(" </p>\n\n    ")
    # end if
# end if
pass
php_print("\n")
do_settings_sections("writing")
php_print("\n")
submit_button()
php_print("""</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
