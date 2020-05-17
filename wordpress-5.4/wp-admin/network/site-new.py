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
#// Add Site Administration Screen
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.1.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
#// WordPress Translation Installation API
php_include_file(ABSPATH + "wp-admin/includes/translation-install.php", once=True)
if (not current_user_can("create_sites")):
    wp_die(__("Sorry, you are not allowed to add sites to this network."))
# end if
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen is for Super Admins to add new sites to the network. This is not affected by the registration settings.") + "</p>" + "<p>" + __("If the admin email for the new site does not exist in the database, a new user will also be created.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/network-admin-sites-screen/\">Documentation on Site Management</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/forum/multisite/\">Support Forums</a>") + "</p>")
if (php_isset(lambda : PHP_REQUEST["action"])) and "add-site" == PHP_REQUEST["action"]:
    check_admin_referer("add-blog", "_wpnonce_add-blog")
    if (not php_is_array(PHP_POST["blog"])):
        wp_die(__("Can&#8217;t create an empty site."))
    # end if
    blog_ = PHP_POST["blog"]
    domain_ = ""
    blog_["domain"] = php_trim(blog_["domain"])
    if php_preg_match("|^([a-zA-Z0-9-])+$|", blog_["domain"]):
        domain_ = php_strtolower(blog_["domain"])
    # end if
    #// If not a subdomain installation, make sure the domain isn't a reserved word.
    if (not is_subdomain_install()):
        subdirectory_reserved_names_ = get_subdirectory_reserved_names()
        if php_in_array(domain_, subdirectory_reserved_names_):
            wp_die(php_sprintf(__("The following words are reserved for use by WordPress functions and cannot be used as blog names: %s"), "<code>" + php_implode("</code>, <code>", subdirectory_reserved_names_) + "</code>"))
        # end if
    # end if
    title_ = blog_["title"]
    meta_ = Array({"public": 1})
    #// Handle translation installation for the new site.
    if (php_isset(lambda : PHP_POST["WPLANG"])):
        if "" == PHP_POST["WPLANG"]:
            meta_["WPLANG"] = ""
            pass
        elif php_in_array(PHP_POST["WPLANG"], get_available_languages()):
            meta_["WPLANG"] = PHP_POST["WPLANG"]
        elif current_user_can("install_languages") and wp_can_install_language_pack():
            language_ = wp_download_language_pack(wp_unslash(PHP_POST["WPLANG"]))
            if language_:
                meta_["WPLANG"] = language_
            # end if
        # end if
    # end if
    if php_empty(lambda : domain_):
        wp_die(__("Missing or invalid site address."))
    # end if
    if (php_isset(lambda : blog_["email"])) and "" == php_trim(blog_["email"]):
        wp_die(__("Missing email address."))
    # end if
    email_ = sanitize_email(blog_["email"])
    if (not is_email(email_)):
        wp_die(__("Invalid email address."))
    # end if
    if is_subdomain_install():
        newdomain_ = domain_ + "." + php_preg_replace("|^www\\.|", "", get_network().domain)
        path_ = get_network().path
    else:
        newdomain_ = get_network().domain
        path_ = get_network().path + domain_ + "/"
    # end if
    password_ = "N/A"
    user_id_ = email_exists(email_)
    if (not user_id_):
        #// Create a new user with a random password.
        #// 
        #// Fires immediately before a new user is created via the network site-new.php page.
        #// 
        #// @since 4.5.0
        #// 
        #// @param string $email Email of the non-existent user.
        #//
        do_action("pre_network_site_new_created_user", email_)
        user_id_ = username_exists(domain_)
        if user_id_:
            wp_die(__("The domain or path entered conflicts with an existing username."))
        # end if
        password_ = wp_generate_password(12, False)
        user_id_ = wpmu_create_user(domain_, password_, email_)
        if False == user_id_:
            wp_die(__("There was an error creating the user."))
        # end if
        #// 
        #// Fires after a new user has been created via the network site-new.php page.
        #// 
        #// @since 4.4.0
        #// 
        #// @param int $user_id ID of the newly created user.
        #//
        do_action("network_site_new_created_user", user_id_)
    # end if
    wpdb_.hide_errors()
    id_ = wpmu_create_blog(newdomain_, path_, title_, user_id_, meta_, get_current_network_id())
    wpdb_.show_errors()
    if (not is_wp_error(id_)):
        if (not is_super_admin(user_id_)) and (not get_user_option("primary_blog", user_id_)):
            update_user_option(user_id_, "primary_blog", id_, True)
        # end if
        wp_mail(get_site_option("admin_email"), php_sprintf(__("[%s] New Site Created"), get_network().site_name), php_sprintf(__("""New site created by %1$s
        Address: %2$s
        Name: %3$s"""), current_user_.user_login, get_site_url(id_), wp_unslash(title_)), php_sprintf("From: \"%1$s\" <%2$s>", _x("Site Admin", "email \"From\" field"), get_site_option("admin_email")))
        wpmu_welcome_notification(id_, user_id_, password_, title_, Array({"public": 1}))
        wp_redirect(add_query_arg(Array({"update": "added", "id": id_}), "site-new.php"))
        php_exit(0)
    else:
        wp_die(id_.get_error_message())
    # end if
# end if
if (php_isset(lambda : PHP_REQUEST["update"])):
    messages_ = Array()
    if "added" == PHP_REQUEST["update"]:
        messages_[-1] = php_sprintf(__("Site added. <a href=\"%1$s\">Visit Dashboard</a> or <a href=\"%2$s\">Edit Site</a>"), esc_url(get_admin_url(absint(PHP_REQUEST["id"]))), network_admin_url("site-info.php?id=" + absint(PHP_REQUEST["id"])))
    # end if
# end if
title_ = __("Add New Site")
parent_file_ = "sites.php"
wp_enqueue_script("user-suggest")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1 id=\"add-new-site\">")
_e("Add New Site")
php_print("</h1>\n")
if (not php_empty(lambda : messages_)):
    for msg_ in messages_:
        php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg_ + "</p></div>")
    # end for
# end if
php_print("<p>\n")
printf(__("Required fields are marked %s"), "<span class=\"required\">*</span>")
php_print("</p>\n<form method=\"post\" action=\"")
php_print(network_admin_url("site-new.php?action=add-site"))
php_print("\" novalidate=\"novalidate\">\n")
wp_nonce_field("add-blog", "_wpnonce_add-blog")
php_print(" <table class=\"form-table\" role=\"presentation\">\n        <tr class=\"form-field form-required\">\n           <th scope=\"row\"><label for=\"site-address\">")
_e("Site Address (URL)")
php_print(" <span class=\"required\">*</span></label></th>\n            <td>\n          ")
if is_subdomain_install():
    php_print("             <input name=\"blog[domain]\" type=\"text\" class=\"regular-text\" id=\"site-address\" aria-describedby=\"site-address-desc\" autocapitalize=\"none\" autocorrect=\"off\" required /><span class=\"no-break\">.")
    php_print(php_preg_replace("|^www\\.|", "", get_network().domain))
    php_print("</span>\n                ")
else:
    php_print(get_network().domain + get_network().path)
    php_print("             <input name=\"blog[domain]\" type=\"text\" class=\"regular-text\" id=\"site-address\" aria-describedby=\"site-address-desc\" autocapitalize=\"none\" autocorrect=\"off\" required />\n              ")
# end if
php_print("<p class=\"description\" id=\"site-address-desc\">" + __("Only lowercase letters (a-z), numbers, and hyphens are allowed.") + "</p>")
php_print("""           </td>
</tr>
<tr class=\"form-field form-required\">
<th scope=\"row\"><label for=\"site-title\">""")
_e("Site Title")
php_print(""" <span class=\"required\">*</span></label></th>
<td><input name=\"blog[title]\" type=\"text\" class=\"regular-text\" id=\"site-title\" required /></td>
</tr>
""")
languages_ = get_available_languages()
translations_ = wp_get_available_translations()
if (not php_empty(lambda : languages_)) or (not php_empty(lambda : translations_)):
    php_print("         <tr class=\"form-field form-required\">\n               <th scope=\"row\"><label for=\"site-language\">")
    _e("Site Language")
    php_print("</label></th>\n              <td>\n                  ")
    #// Network default.
    lang_ = get_site_option("WPLANG")
    #// Use English if the default isn't available.
    if (not php_in_array(lang_, languages_)):
        lang_ = ""
    # end if
    wp_dropdown_languages(Array({"name": "WPLANG", "id": "site-language", "selected": lang_, "languages": languages_, "translations": translations_, "show_available_translations": current_user_can("install_languages") and wp_can_install_language_pack()}))
    php_print("             </td>\n         </tr>\n     ")
# end if
pass
php_print("     <tr class=\"form-field form-required\">\n           <th scope=\"row\"><label for=\"admin-email\">")
_e("Admin Email")
php_print(""" <span class=\"required\">*</span></label></th>
<td><input name=\"blog[email]\" type=\"email\" class=\"regular-text wp-suggest-user\" id=\"admin-email\" data-autocomplete-type=\"search\" data-autocomplete-field=\"user_email\" aria-describedby=\"site-admin-email\" required /></td>
</tr>
<tr class=\"form-field\">
<td colspan=\"2\" class=\"td-full\"><p id=\"site-admin-email\">""")
_e("A new user will be created if the above email address is not in the database.")
php_print("<br />")
_e("The username and a link to set the password will be mailed to this email address.")
php_print("""</p></td>
</tr>
</table>
""")
#// 
#// Fires at the end of the new site form in network admin.
#// 
#// @since 4.5.0
#//
do_action("network_site_new_form")
submit_button(__("Add Site"), "primary", "add-site")
php_print(" </form>\n</div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
