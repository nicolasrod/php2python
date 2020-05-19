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
#// Multisite network settings administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
#// WordPress Translation Installation API
php_include_file(ABSPATH + "wp-admin/includes/translation-install.php", once=True)
if (not current_user_can("manage_network_options")):
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
title_ = __("Network Settings")
parent_file_ = "settings.php"
#// Handle network admin email change requests.
if (not php_empty(lambda : PHP_REQUEST["network_admin_hash"])):
    new_admin_details_ = get_site_option("network_admin_hash")
    redirect_ = "settings.php?updated=false"
    if php_is_array(new_admin_details_) and hash_equals(new_admin_details_["hash"], PHP_REQUEST["network_admin_hash"]) and (not php_empty(lambda : new_admin_details_["newemail"])):
        update_site_option("admin_email", new_admin_details_["newemail"])
        delete_site_option("network_admin_hash")
        delete_site_option("new_admin_email")
        redirect_ = "settings.php?updated=true"
    # end if
    wp_redirect(network_admin_url(redirect_))
    php_exit(0)
elif (not php_empty(lambda : PHP_REQUEST["dismiss"])) and "new_network_admin_email" == PHP_REQUEST["dismiss"]:
    check_admin_referer("dismiss_new_network_admin_email")
    delete_site_option("network_admin_hash")
    delete_site_option("new_admin_email")
    wp_redirect(network_admin_url("settings.php?updated=true"))
    php_exit(0)
# end if
add_action("admin_head", "network_settings_add_js")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen sets and changes options for the network as a whole. The first site is the main site in the network and network options are pulled from that original site&#8217;s options.") + "</p>" + "<p>" + __("Operational settings has fields for the network&#8217;s name and admin email.") + "</p>" + "<p>" + __("Registration settings can disable/enable public signups. If you let others sign up for a site, install spam plugins. Spaces, not commas, should separate names banned as sites for this network.") + "</p>" + "<p>" + __("New site settings are defaults applied when a new site is created in the network. These include welcome email for when a new site or user account is registered, and what&#8127;s put in the first post, page, comment, comment author, and comment URL.") + "</p>" + "<p>" + __("Upload settings control the size of the uploaded files and the amount of available upload space for each site. You can change the default value for specific sites when you edit a particular site. Allowed file types are also listed (space separated only).") + "</p>" + "<p>" + __("You can set the language, and the translation files will be automatically downloaded and installed (available if your filesystem is writable).") + "</p>" + "<p>" + __("Menu setting enables/disables the plugin menus from appearing for non super admins, so that only super admins, not site admins, have access to activate plugins.") + "</p>" + "<p>" + __("Super admins can no longer be added on the Options screen. You must now go to the list of existing users on Network Admin > Users and click on Username or the Edit action link below that name. This goes to an Edit User page where you can check a box to grant super admin privileges.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Network_Admin_Settings_Screen\">Documentation on Network Settings</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
if PHP_POST:
    #// This action is documented in wp-admin/network/edit.php
    do_action("wpmuadminedit")
    check_admin_referer("siteoptions")
    checked_options_ = Array({"menu_items": Array(), "registrationnotification": "no", "upload_space_check_disabled": 1, "add_new_users": 0})
    for option_name_,option_unchecked_value_ in checked_options_.items():
        if (not (php_isset(lambda : PHP_POST[option_name_]))):
            PHP_POST[option_name_] = option_unchecked_value_
        # end if
    # end for
    options_ = Array("registrationnotification", "registration", "add_new_users", "menu_items", "upload_space_check_disabled", "blog_upload_space", "upload_filetypes", "site_name", "first_post", "first_page", "first_comment", "first_comment_url", "first_comment_author", "welcome_email", "welcome_user_email", "fileupload_maxk", "global_terms_enabled", "illegal_names", "limited_email_domains", "banned_email_domains", "WPLANG", "new_admin_email", "first_comment_email")
    #// Handle translation installation.
    if (not php_empty(lambda : PHP_POST["WPLANG"])) and current_user_can("install_languages") and wp_can_install_language_pack():
        language_ = wp_download_language_pack(PHP_POST["WPLANG"])
        if language_:
            PHP_POST["WPLANG"] = language_
        # end if
    # end if
    for option_name_ in options_:
        if (not (php_isset(lambda : PHP_POST[option_name_]))):
            continue
        # end if
        value_ = wp_unslash(PHP_POST[option_name_])
        update_site_option(option_name_, value_)
    # end for
    #// 
    #// Fires after the network options are updated.
    #// 
    #// @since MU (3.0.0)
    #//
    do_action("update_wpmu_options")
    wp_redirect(add_query_arg("updated", "true", network_admin_url("settings.php")))
    php_exit(0)
# end if
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
if (php_isset(lambda : PHP_REQUEST["updated"])):
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    _e("Settings saved.")
    php_print("</p></div>\n ")
# end if
php_print("\n<div class=\"wrap\">\n <h1>")
php_print(esc_html(title_))
php_print("</h1>\n  <form method=\"post\" action=\"settings.php\" novalidate=\"novalidate\">\n      ")
wp_nonce_field("siteoptions")
php_print("     <h2>")
_e("Operational Settings")
php_print("""</h2>
<table class=\"form-table\" role=\"presentation\">
<tr>
<th scope=\"row\"><label for=\"site_name\">""")
_e("Network Title")
php_print("</label></th>\n              <td>\n                  <input name=\"site_name\" type=\"text\" id=\"site_name\" class=\"regular-text\" value=\"")
php_print(esc_attr(get_network().site_name))
php_print("""\" />
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"admin_email\">""")
_e("Network Admin Email")
php_print("</label></th>\n              <td>\n                  <input name=\"new_admin_email\" type=\"email\" id=\"admin_email\" aria-describedby=\"admin-email-desc\" class=\"regular-text\" value=\"")
php_print(esc_attr(get_site_option("admin_email")))
php_print("\" />\n                  <p class=\"description\" id=\"admin-email-desc\">\n                     ")
_e("This address is used for admin purposes. If you change this, we will send you an email at your new address to confirm it. <strong>The new address will not become active until confirmed.</strong>")
php_print("                 </p>\n                  ")
new_admin_email_ = get_site_option("new_admin_email")
if new_admin_email_ and get_site_option("admin_email") != new_admin_email_:
    php_print("                     <div class=\"updated inline\">\n                        <p>\n                       ")
    php_printf(__("There is a pending change of the network admin email to %s."), "<code>" + esc_html(new_admin_email_) + "</code>")
    php_printf(" <a href=\"%1$s\">%2$s</a>", esc_url(wp_nonce_url(network_admin_url("settings.php?dismiss=new_network_admin_email"), "dismiss_new_network_admin_email")), __("Cancel"))
    php_print("                     </p>\n                      </div>\n                    ")
# end if
php_print("""               </td>
</tr>
</table>
<h2>""")
_e("Registration Settings")
php_print("""</h2>
<table class=\"form-table\" role=\"presentation\">
<tr>
<th scope=\"row\">""")
_e("Allow new registrations")
php_print("</th>\n              ")
if (not get_site_option("registration")):
    update_site_option("registration", "none")
# end if
reg_ = get_site_option("registration")
php_print("             <td>\n                  <fieldset>\n                    <legend class=\"screen-reader-text\">")
_e("New registrations settings")
php_print("</legend>\n                  <label><input name=\"registration\" type=\"radio\" id=\"registration1\" value=\"none\"")
checked(reg_, "none")
php_print(" /> ")
_e("Registration is disabled")
php_print("</label><br />\n                 <label><input name=\"registration\" type=\"radio\" id=\"registration2\" value=\"user\"")
checked(reg_, "user")
php_print(" /> ")
_e("User accounts may be registered")
php_print("</label><br />\n                 <label><input name=\"registration\" type=\"radio\" id=\"registration3\" value=\"blog\"")
checked(reg_, "blog")
php_print(" /> ")
_e("Logged in users may register new sites")
php_print("</label><br />\n                 <label><input name=\"registration\" type=\"radio\" id=\"registration4\" value=\"all\"")
checked(reg_, "all")
php_print(" /> ")
_e("Both sites and user accounts can be registered")
php_print("</label>\n                   ")
if is_subdomain_install():
    php_print("<p class=\"description\">")
    php_printf(__("If registration is disabled, please set %1$s in %2$s to a URL you will redirect visitors to if they visit a non-existent site."), "<code>NOBLOGREDIRECT</code>", "<code>wp-config.php</code>")
    php_print("</p>")
# end if
php_print("""                   </fieldset>
</td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Registration notification")
php_print("</th>\n              ")
if (not get_site_option("registrationnotification")):
    update_site_option("registrationnotification", "yes")
# end if
php_print("             <td>\n                  <label><input name=\"registrationnotification\" type=\"checkbox\" id=\"registrationnotification\" value=\"yes\"")
checked(get_site_option("registrationnotification"), "yes")
php_print(" /> ")
_e("Send the network admin an email notification every time someone registers a site or user account")
php_print("""</label>
</td>
</tr>
<tr id=\"addnewusers\">
<th scope=\"row\">""")
_e("Add New Users")
php_print("</th>\n              <td>\n                  <label><input name=\"add_new_users\" type=\"checkbox\" id=\"add_new_users\" value=\"1\"")
checked(get_site_option("add_new_users"))
php_print(" /> ")
_e("Allow site administrators to add new users to their site via the \"Users &rarr; Add New\" page")
php_print("""</label>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"illegal_names\">""")
_e("Banned Names")
php_print("</label></th>\n              <td>\n                  <input name=\"illegal_names\" type=\"text\" id=\"illegal_names\" aria-describedby=\"illegal-names-desc\" class=\"large-text\" value=\"")
php_print(esc_attr(php_implode(" ", get_site_option("illegal_names"))))
php_print("\" size=\"45\" />\n                  <p class=\"description\" id=\"illegal-names-desc\">\n                       ")
_e("Users are not allowed to register these sites. Separate names by spaces.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"limited_email_domains\">""")
_e("Limited Email Registrations")
php_print("</label></th>\n              <td>\n                  ")
limited_email_domains_ = get_site_option("limited_email_domains")
limited_email_domains_ = php_str_replace(" ", "\n", limited_email_domains_)
php_print("                 <textarea name=\"limited_email_domains\" id=\"limited_email_domains\" aria-describedby=\"limited-email-domains-desc\" cols=\"45\" rows=\"5\">\n")
php_print(esc_textarea("" if "" == limited_email_domains_ else php_implode("\n", limited_email_domains_)))
php_print("</textarea>\n                    <p class=\"description\" id=\"limited-email-domains-desc\">\n                       ")
_e("If you want to limit site registrations to certain domains. One domain per line.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"banned_email_domains\">""")
_e("Banned Email Domains")
php_print("""</label></th>
<td>
<textarea name=\"banned_email_domains\" id=\"banned_email_domains\" aria-describedby=\"banned-email-domains-desc\" cols=\"45\" rows=\"5\">
""")
php_print(esc_textarea("" if get_site_option("banned_email_domains") == "" else php_implode("\n", get_site_option("banned_email_domains"))))
php_print("</textarea>\n                    <p class=\"description\" id=\"banned-email-domains-desc\">\n                        ")
_e("If you want to ban domains from site registrations. One domain per line.")
php_print("""                   </p>
</td>
</tr>
</table>
<h2>""")
_e("New Site Settings")
php_print("""</h2>
<table class=\"form-table\" role=\"presentation\">
<tr>
<th scope=\"row\"><label for=\"welcome_email\">""")
_e("Welcome Email")
php_print("""</label></th>
<td>
<textarea name=\"welcome_email\" id=\"welcome_email\" aria-describedby=\"welcome-email-desc\" rows=\"5\" cols=\"45\" class=\"large-text\">
""")
php_print(esc_textarea(get_site_option("welcome_email")))
php_print("</textarea>\n                    <p class=\"description\" id=\"welcome-email-desc\">\n                       ")
_e("The welcome email sent to new site owners.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"welcome_user_email\">""")
_e("Welcome User Email")
php_print("""</label></th>
<td>
<textarea name=\"welcome_user_email\" id=\"welcome_user_email\" aria-describedby=\"welcome-user-email-desc\" rows=\"5\" cols=\"45\" class=\"large-text\">
""")
php_print(esc_textarea(get_site_option("welcome_user_email")))
php_print("</textarea>\n                    <p class=\"description\" id=\"welcome-user-email-desc\">\n                      ")
_e("The welcome email sent to new users.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"first_post\">""")
_e("First Post")
php_print("""</label></th>
<td>
<textarea name=\"first_post\" id=\"first_post\" aria-describedby=\"first-post-desc\" rows=\"5\" cols=\"45\" class=\"large-text\">
""")
php_print(esc_textarea(get_site_option("first_post")))
php_print("</textarea>\n                    <p class=\"description\" id=\"first-post-desc\">\n                      ")
_e("The first post on a new site.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"first_page\">""")
_e("First Page")
php_print("""</label></th>
<td>
<textarea name=\"first_page\" id=\"first_page\" aria-describedby=\"first-page-desc\" rows=\"5\" cols=\"45\" class=\"large-text\">
""")
php_print(esc_textarea(get_site_option("first_page")))
php_print("</textarea>\n                    <p class=\"description\" id=\"first-page-desc\">\n                      ")
_e("The first page on a new site.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"first_comment\">""")
_e("First Comment")
php_print("""</label></th>
<td>
<textarea name=\"first_comment\" id=\"first_comment\" aria-describedby=\"first-comment-desc\" rows=\"5\" cols=\"45\" class=\"large-text\">
""")
php_print(esc_textarea(get_site_option("first_comment")))
php_print("</textarea>\n                    <p class=\"description\" id=\"first-comment-desc\">\n                       ")
_e("The first comment on a new site.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"first_comment_author\">""")
_e("First Comment Author")
php_print("</label></th>\n              <td>\n                  <input type=\"text\" size=\"40\" name=\"first_comment_author\" id=\"first_comment_author\" aria-describedby=\"first-comment-author-desc\" value=\"")
php_print(esc_attr(get_site_option("first_comment_author")))
php_print("\" />\n                  <p class=\"description\" id=\"first-comment-author-desc\">\n                        ")
_e("The author of the first comment on a new site.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"first_comment_email\">""")
_e("First Comment Email")
php_print("</label></th>\n              <td>\n                  <input type=\"text\" size=\"40\" name=\"first_comment_email\" id=\"first_comment_email\" aria-describedby=\"first-comment-email-desc\" value=\"")
php_print(esc_attr(get_site_option("first_comment_email")))
php_print("\" />\n                  <p class=\"description\" id=\"first-comment-email-desc\">\n                     ")
_e("The email address of the first comment author on a new site.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"first_comment_url\">""")
_e("First Comment URL")
php_print("</label></th>\n              <td>\n                  <input type=\"text\" size=\"40\" name=\"first_comment_url\" id=\"first_comment_url\" aria-describedby=\"first-comment-url-desc\" value=\"")
php_print(esc_attr(get_site_option("first_comment_url")))
php_print("\" />\n                  <p class=\"description\" id=\"first-comment-url-desc\">\n                       ")
_e("The URL for the first comment on a new site.")
php_print("""                   </p>
</td>
</tr>
</table>
<h2>""")
_e("Upload Settings")
php_print("""</h2>
<table class=\"form-table\" role=\"presentation\">
<tr>
<th scope=\"row\">""")
_e("Site upload space")
php_print("</th>\n              <td>\n                  <label><input type=\"checkbox\" id=\"upload_space_check_disabled\" name=\"upload_space_check_disabled\" value=\"0\"")
checked(php_bool(get_site_option("upload_space_check_disabled")), False)
php_print("/>\n                     ")
php_printf(__("Limit total size of files uploaded to %s MB"), "</label><label><input name=\"blog_upload_space\" type=\"number\" min=\"0\" style=\"width: 100px\" id=\"blog_upload_space\" aria-describedby=\"blog-upload-space-desc\" value=\"" + esc_attr(get_site_option("blog_upload_space", 100)) + "\" />")
php_print("                 </label><br />\n                    <p class=\"screen-reader-text\" id=\"blog-upload-space-desc\">\n                        ")
_e("Size in megabytes")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"upload_filetypes\">""")
_e("Upload file types")
php_print("</label></th>\n              <td>\n                  <input name=\"upload_filetypes\" type=\"text\" id=\"upload_filetypes\" aria-describedby=\"upload-filetypes-desc\" class=\"large-text\" value=\"")
php_print(esc_attr(get_site_option("upload_filetypes", "jpg jpeg png gif")))
php_print("\" size=\"45\" />\n                  <p class=\"description\" id=\"upload-filetypes-desc\">\n                        ")
_e("Allowed file types. Separate types by spaces.")
php_print("""                   </p>
</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"fileupload_maxk\">""")
_e("Max upload file size")
php_print("</label></th>\n              <td>\n                  ")
php_printf(__("%s KB"), "<input name=\"fileupload_maxk\" type=\"number\" min=\"0\" style=\"width: 100px\" id=\"fileupload_maxk\" aria-describedby=\"fileupload-maxk-desc\" value=\"" + esc_attr(get_site_option("fileupload_maxk", 300)) + "\" />")
php_print("                 <p class=\"screen-reader-text\" id=\"fileupload-maxk-desc\">\n                      ")
_e("Size in kilobytes")
php_print("""                   </p>
</td>
</tr>
</table>
""")
languages_ = get_available_languages()
translations_ = wp_get_available_translations()
if (not php_empty(lambda : languages_)) or (not php_empty(lambda : translations_)):
    php_print("         <h2>")
    _e("Language Settings")
    php_print("""</h2>
    <table class=\"form-table\" role=\"presentation\">
    <tr>
    <th><label for=\"WPLANG\">""")
    _e("Default Language")
    php_print("</label></th>\n                  <td>\n                      ")
    lang_ = get_site_option("WPLANG")
    if (not php_in_array(lang_, languages_)):
        lang_ = ""
    # end if
    wp_dropdown_languages(Array({"name": "WPLANG", "id": "WPLANG", "selected": lang_, "languages": languages_, "translations": translations_, "show_available_translations": current_user_can("install_languages") and wp_can_install_language_pack()}))
    php_print("""                   </td>
    </tr>
    </table>
    """)
# end if
php_print("\n       <h2>")
_e("Menu Settings")
php_print("""</h2>
<table id=\"menu\" class=\"form-table\">
<tr>
<th scope=\"row\">""")
_e("Enable administration menus")
php_print("</th>\n              <td>\n          ")
menu_perms_ = get_site_option("menu_items")
#// 
#// Filters available network-wide administration menu options.
#// 
#// Options returned to this filter are output as individual checkboxes that, when selected,
#// enable site administrator access to the specified administration menu in certain contexts.
#// 
#// Adding options for specific menus here hinges on the appropriate checks and capabilities
#// being in place in the site dashboard on the other side. For instance, when the single
#// default option, 'plugins' is enabled, site administrators are granted access to the Plugins
#// screen in their individual sites' dashboards.
#// 
#// @since MU (3.0.0)
#// 
#// @param string[] $admin_menus Associative array of the menu items available.
#//
menu_items_ = apply_filters("mu_menu_items", Array({"plugins": __("Plugins")}))
php_print("<fieldset><legend class=\"screen-reader-text\">" + __("Enable menus") + "</legend>")
for key_,val_ in menu_items_.items():
    php_print("<label><input type='checkbox' name='menu_items[" + key_ + "]' value='1'" + checked(menu_perms_[key_], "1", False) if (php_isset(lambda : menu_perms_[key_])) else "" + " /> " + esc_html(val_) + "</label><br/>")
# end for
php_print("</fieldset>")
php_print("""               </td>
</tr>
</table>
""")
#// 
#// Fires at the end of the Network Settings form, before the submit button.
#// 
#// @since MU (3.0.0)
#//
do_action("wpmu_options")
php_print("     ")
submit_button()
php_print("""   </form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
