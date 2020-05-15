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
#// My Sites dashboard.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#//
php_include_file(__DIR__ + "/admin.php", once=True)
if (not is_multisite()):
    wp_die(__("Multisite support is not enabled."))
# end if
if (not current_user_can("read")):
    wp_die(__("Sorry, you are not allowed to access this page."))
# end if
action = PHP_POST["action"] if (php_isset(lambda : PHP_POST["action"])) else "splash"
blogs = get_blogs_of_user(current_user.ID)
updated = False
if "updateblogsettings" == action and (php_isset(lambda : PHP_POST["primary_blog"])):
    check_admin_referer("update-my-sites")
    blog = get_site(int(PHP_POST["primary_blog"]))
    if blog and (php_isset(lambda : blog.domain)):
        update_user_option(current_user.ID, "primary_blog", int(PHP_POST["primary_blog"]), True)
        updated = True
    else:
        wp_die(__("The primary site you chose does not exist."))
    # end if
# end if
title = __("My Sites")
parent_file = "index.php"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen shows an individual user all of their sites in this network, and also allows that user to set a primary site. They can use the links under each site to visit either the front end or the dashboard for that site.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Dashboard_My_Sites_Screen\">Documentation on My Sites</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
if updated:
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\"><p><strong>")
    _e("Settings saved.")
    php_print("</strong></p></div>\n")
# end if
php_print("""
<div class=\"wrap\">
<h1 class=\"wp-heading-inline\">
""")
php_print(esc_html(title))
php_print("</h1>\n\n")
if php_in_array(get_site_option("registration"), Array("all", "blog")):
    #// This filter is documented in wp-login.php
    sign_up_url = apply_filters("wp_signup_location", network_site_url("wp-signup.php"))
    printf(" <a href=\"%s\" class=\"page-title-action\">%s</a>", esc_url(sign_up_url), esc_html_x("Add New", "site"))
# end if
if php_empty(lambda : blogs):
    php_print("<p>")
    _e("You must be a member of at least one site to use this page.")
    php_print("</p>")
else:
    php_print("""
    <hr class=\"wp-header-end\">
    <form id=\"myblogs\" method=\"post\">
    """)
    choose_primary_blog()
    #// 
    #// Fires before the sites list on the My Sites screen.
    #// 
    #// @since 3.0.0
    #//
    do_action("myblogs_allblogs_options")
    php_print(" <br clear=\"all\" />\n  <ul class=\"my-sites striped\">\n   ")
    #// 
    #// Enable the Global Settings section on the My Sites screen.
    #// 
    #// By default, the Global Settings section is hidden. Passing a non-empty
    #// string to this filter will enable the section, and allow new settings
    #// to be added, either globally or for specific sites.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $settings_html The settings HTML markup. Default empty.
    #// @param string $context       Context of the setting (global or site-specific). Default 'global'.
    #//
    settings_html = apply_filters("myblogs_options", "", "global")
    if "" != settings_html:
        php_print("<h3>" + __("Global Settings") + "</h3>")
        php_print(settings_html)
    # end if
    reset(blogs)
    for user_blog in blogs:
        switch_to_blog(user_blog.userblog_id)
        php_print("<li>")
        php_print(str("<h3>") + str(user_blog.blogname) + str("</h3>"))
        actions = "<a href='" + esc_url(home_url()) + "'>" + __("Visit") + "</a>"
        if current_user_can("read"):
            actions += " | <a href='" + esc_url(admin_url()) + "'>" + __("Dashboard") + "</a>"
        # end if
        #// 
        #// Filters the row links displayed for each site on the My Sites screen.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param string $actions   The HTML site link markup.
        #// @param object $user_blog An object containing the site data.
        #//
        actions = apply_filters("myblogs_blog_actions", actions, user_blog)
        php_print("<p class='my-sites-actions'>" + actions + "</p>")
        #// This filter is documented in wp-admin/my-sites.php
        php_print(apply_filters("myblogs_options", "", user_blog))
        php_print("</li>")
        restore_current_blog()
    # end for
    php_print(" </ul>\n ")
    if php_count(blogs) > 1 or has_action("myblogs_allblogs_options") or has_filter("myblogs_options"):
        php_print("     <input type=\"hidden\" name=\"action\" value=\"updateblogsettings\" />\n        ")
        wp_nonce_field("update-my-sites")
        submit_button()
    # end if
    php_print(" </form>\n")
# end if
php_print(" </div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
