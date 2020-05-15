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
#// Multisite administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
#// Load WordPress dashboard API
php_include_file(ABSPATH + "wp-admin/includes/dashboard.php", once=True)
if (not current_user_can("manage_network")):
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
title = __("Dashboard")
parent_file = "index.php"
overview = "<p>" + __("Welcome to your Network Admin. This area of the Administration Screens is used for managing all aspects of your Multisite Network.") + "</p>"
overview += "<p>" + __("From here you can:") + "</p>"
overview += "<ul><li>" + __("Add and manage sites or users") + "</li>"
overview += "<li>" + __("Install and activate themes or plugins") + "</li>"
overview += "<li>" + __("Update your network") + "</li>"
overview += "<li>" + __("Modify global network settings") + "</li></ul>"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": overview}))
quick_tasks = "<p>" + __("The Right Now widget on this screen provides current user and site counts on your network.") + "</p>"
quick_tasks += "<ul><li>" + __("To add a new user, <strong>click Create a New User</strong>.") + "</li>"
quick_tasks += "<li>" + __("To add a new site, <strong>click Create a New Site</strong>.") + "</li></ul>"
quick_tasks += "<p>" + __("To search for a user or site, use the search boxes.") + "</p>"
quick_tasks += "<ul><li>" + __("To search for a user, <strong>enter an email address or username</strong>. Use a wildcard to search for a partial username, such as user&#42;.") + "</li>"
quick_tasks += "<li>" + __("To search for a site, <strong>enter the path or domain</strong>.") + "</li></ul>"
get_current_screen().add_help_tab(Array({"id": "quick-tasks", "title": __("Quick Tasks"), "content": quick_tasks}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/network-admin/\">Documentation on the Network Admin</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/forum/multisite/\">Support Forums</a>") + "</p>")
wp_dashboard_setup()
wp_enqueue_script("dashboard")
wp_enqueue_script("plugin-install")
add_thickbox()
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1>")
php_print(esc_html(title))
php_print("""</h1>
<div id=\"dashboard-widgets-wrap\">
""")
wp_dashboard()
php_print("""
<div class=\"clear\"></div>
</div><!-- dashboard-widgets-wrap -->
</div><!-- wrap -->
""")
wp_print_community_events_templates()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
