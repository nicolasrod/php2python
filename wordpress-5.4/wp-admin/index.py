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
#// Dashboard Administration Screen
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Load WordPress Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
#// Load WordPress dashboard API
php_include_file(ABSPATH + "wp-admin/includes/dashboard.php", once=True)
wp_dashboard_setup()
wp_enqueue_script("dashboard")
if current_user_can("install_plugins"):
    wp_enqueue_script("plugin-install")
    wp_enqueue_script("updates")
# end if
if current_user_can("upload_files"):
    wp_enqueue_script("media-upload")
# end if
add_thickbox()
if wp_is_mobile():
    wp_enqueue_script("jquery-touch-punch")
# end if
title = __("Dashboard")
parent_file = "index.php"
help = "<p>" + __("Welcome to your WordPress Dashboard! This is the screen you will see when you log in to your site, and gives you access to all the site management features of WordPress. You can get help for any screen by clicking the Help tab above the screen title.") + "</p>"
screen = get_current_screen()
screen.add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": help}))
#// Help tabs.
help = "<p>" + __("The left-hand navigation menu provides links to all of the WordPress administration screens, with submenu items displayed on hover. You can minimize this menu to a narrow icon strip by clicking on the Collapse Menu arrow at the bottom.") + "</p>"
help += "<p>" + __("Links in the Toolbar at the top of the screen connect your dashboard and the front end of your site, and provide access to your profile and helpful WordPress information.") + "</p>"
screen.add_help_tab(Array({"id": "help-navigation", "title": __("Navigation"), "content": help}))
help = "<p>" + __("You can use the following controls to arrange your Dashboard screen to suit your workflow. This is true on most other administration screens as well.") + "</p>"
help += "<p>" + __("<strong>Screen Options</strong> &mdash; Use the Screen Options tab to choose which Dashboard boxes to show.") + "</p>"
help += "<p>" + __("<strong>Drag and Drop</strong> &mdash; To rearrange the boxes, drag and drop by clicking on the title bar of the selected box and releasing when you see a gray dotted-line rectangle appear in the location you want to place the box.") + "</p>"
help += "<p>" + __("<strong>Box Controls</strong> &mdash; Click the title bar of the box to expand or collapse it. Some boxes added by plugins may have configurable content, and will show a &#8220;Configure&#8221; link in the title bar if you hover over it.") + "</p>"
screen.add_help_tab(Array({"id": "help-layout", "title": __("Layout"), "content": help}))
help = "<p>" + __("The boxes on your Dashboard screen are:") + "</p>"
if current_user_can("edit_posts"):
    help += "<p>" + __("<strong>At A Glance</strong> &mdash; Displays a summary of the content on your site and identifies which theme and version of WordPress you are using.") + "</p>"
# end if
help += "<p>" + __("<strong>Activity</strong> &mdash; Shows the upcoming scheduled posts, recently published posts, and the most recent comments on your posts and allows you to moderate them.") + "</p>"
if is_blog_admin() and current_user_can("edit_posts"):
    help += "<p>" + __("<strong>Quick Draft</strong> &mdash; Allows you to create a new post and save it as a draft. Also displays links to the 3 most recent draft posts you've started.") + "</p>"
# end if
help += "<p>" + php_sprintf(__("<strong>WordPress Events and News</strong> &mdash; Upcoming events near you as well as the latest news from the official WordPress project and the <a href=\"%s\">WordPress Planet</a>."), __("https://planet.wordpress.org/")) + "</p>"
if current_user_can("edit_theme_options"):
    help += "<p>" + __("<strong>Welcome</strong> &mdash; Shows links for some of the most common tasks when setting up a new site.") + "</p>"
# end if
screen.add_help_tab(Array({"id": "help-content", "title": __("Content"), "content": help}))
help = None
screen.set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/dashboard-screen/\">Documentation on Dashboard</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n <h1>")
php_print(esc_html(title))
php_print("</h1>\n\n")
if has_action("welcome_panel") and current_user_can("edit_theme_options"):
    classes = "welcome-panel"
    option = get_user_meta(get_current_user_id(), "show_welcome_panel", True)
    #// 0 = hide, 1 = toggled to show or single site creator, 2 = multisite site owner.
    hide = 0 == option or 2 == option and wp_get_current_user().user_email != get_option("admin_email")
    if hide:
        classes += " hidden"
    # end if
    php_print("\n   <div id=\"welcome-panel\" class=\"")
    php_print(esc_attr(classes))
    php_print("\">\n        ")
    wp_nonce_field("welcome-panel-nonce", "welcomepanelnonce", False)
    php_print("     <a class=\"welcome-panel-close\" href=\"")
    php_print(esc_url(admin_url("?welcome=0")))
    php_print("\" aria-label=\"")
    esc_attr_e("Dismiss the welcome panel")
    php_print("\">")
    _e("Dismiss")
    php_print("</a>\n       ")
    #// 
    #// Add content to the welcome panel on the admin dashboard.
    #// 
    #// To remove the default welcome panel, use remove_action():
    #// 
    #// remove_action( 'welcome_panel', 'wp_welcome_panel' );
    #// 
    #// @since 3.5.0
    #//
    do_action("welcome_panel")
    php_print(" </div>\n")
# end if
php_print("\n   <div id=\"dashboard-widgets-wrap\">\n   ")
wp_dashboard()
php_print("""   </div><!-- dashboard-widgets-wrap -->
</div><!-- wrap -->
""")
wp_print_community_events_templates()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
