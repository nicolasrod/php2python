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
#// WordPress Administration Template Header
#// 
#// @package WordPress
#// @subpackage Administration
#//
php_header("Content-Type: " + get_option("html_type") + "; charset=" + get_option("blog_charset"))
if (not php_defined("WP_ADMIN")):
    php_include_file(__DIR__ + "/admin.php", once=True)
# end if
#// 
#// In case admin-header.php is included in a function.
#// 
#// @global string    $title
#// @global string    $hook_suffix
#// @global WP_Screen $current_screen     WordPress current screen object.
#// @global WP_Locale $wp_locale          WordPress date and time locale object.
#// @global string    $pagenow
#// @global string    $update_title
#// @global int       $total_update_count
#// @global string    $parent_file
#//
global title,hook_suffix,current_screen,wp_locale,pagenow,update_title,total_update_count,parent_file
php_check_if_defined("title","hook_suffix","current_screen","wp_locale","pagenow","update_title","total_update_count","parent_file")
#// Catch plugins that include admin-header.php before admin.php completes.
if php_empty(lambda : current_screen):
    set_current_screen()
# end if
get_admin_page_title()
title = esc_html(strip_tags(title))
if is_network_admin():
    #// translators: Network admin screen title. %s: Network title.
    admin_title = php_sprintf(__("Network Admin: %s"), esc_html(get_network().site_name))
elif is_user_admin():
    #// translators: User dashboard screen title. %s: Network title.
    admin_title = php_sprintf(__("User Dashboard: %s"), esc_html(get_network().site_name))
else:
    admin_title = get_bloginfo("name")
# end if
if admin_title == title:
    #// translators: Admin screen title. %s: Admin screen name.
    admin_title = php_sprintf(__("%s &#8212; WordPress"), title)
else:
    #// translators: Admin screen title. 1: Admin screen name, 2: Network or site name.
    admin_title = php_sprintf(__("%1$s &lsaquo; %2$s &#8212; WordPress"), title, admin_title)
# end if
if wp_is_recovery_mode():
    #// translators: %s: Admin screen title.
    admin_title = php_sprintf(__("Recovery Mode &#8212; %s"), admin_title)
# end if
#// 
#// Filters the title tag content for an admin page.
#// 
#// @since 3.1.0
#// 
#// @param string $admin_title The page title, with extra context added.
#// @param string $title       The original page title.
#//
admin_title = apply_filters("admin_title", admin_title, title)
wp_user_settings()
_wp_admin_html_begin()
php_print("<title>")
php_print(admin_title)
php_print("</title>\n")
wp_enqueue_style("colors")
wp_enqueue_style("ie")
wp_enqueue_script("utils")
wp_enqueue_script("svg-painter")
admin_body_class = php_preg_replace("/[^a-z0-9_-]+/i", "-", hook_suffix)
php_print("<script type=\"text/javascript\">\naddLoadEvent = function(func){if(typeof jQuery!=\"undefined\")jQuery(document).ready(func);else if(typeof wpOnload!='function'){wpOnload=func;}else{var oldonload=wpOnload;wpOnload=function(){oldonload();func();}}};\nvar ajaxurl = '")
php_print(admin_url("admin-ajax.php", "relative"))
php_print("',\n pagenow = '")
php_print(current_screen.id)
php_print("',\n typenow = '")
php_print(current_screen.post_type)
php_print("',\n adminpage = '")
php_print(admin_body_class)
php_print("',\n thousandsSeparator = '")
php_print(addslashes(wp_locale.number_format["thousands_sep"]))
php_print("',\n decimalPoint = '")
php_print(addslashes(wp_locale.number_format["decimal_point"]))
php_print("',\n isRtl = ")
php_print(int(is_rtl()))
php_print(""";
</script>
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">
""")
#// 
#// Enqueue scripts for all admin pages.
#// 
#// @since 2.8.0
#// 
#// @param string $hook_suffix The current admin page.
#//
do_action("admin_enqueue_scripts", hook_suffix)
#// 
#// Fires when styles are printed for a specific admin page based on $hook_suffix.
#// 
#// @since 2.6.0
#//
do_action(str("admin_print_styles-") + str(hook_suffix))
#// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
#// 
#// Fires when styles are printed for all admin pages.
#// 
#// @since 2.6.0
#//
do_action("admin_print_styles")
#// 
#// Fires when scripts are printed for a specific admin page based on $hook_suffix.
#// 
#// @since 2.1.0
#//
do_action(str("admin_print_scripts-") + str(hook_suffix))
#// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
#// 
#// Fires when scripts are printed for all admin pages.
#// 
#// @since 2.1.0
#//
do_action("admin_print_scripts")
#// 
#// Fires in head section for a specific admin page.
#// 
#// The dynamic portion of the hook, `$hook_suffix`, refers to the hook suffix
#// for the admin page.
#// 
#// @since 2.1.0
#//
do_action(str("admin_head-") + str(hook_suffix))
#// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
#// 
#// Fires in head section for all admin pages.
#// 
#// @since 2.1.0
#//
do_action("admin_head")
if get_user_setting("mfold") == "f":
    admin_body_class += " folded"
# end if
if (not get_user_setting("unfold")):
    admin_body_class += " auto-fold"
# end if
if is_admin_bar_showing():
    admin_body_class += " admin-bar"
# end if
if is_rtl():
    admin_body_class += " rtl"
# end if
if current_screen.post_type:
    admin_body_class += " post-type-" + current_screen.post_type
# end if
if current_screen.taxonomy:
    admin_body_class += " taxonomy-" + current_screen.taxonomy
# end if
admin_body_class += " branch-" + php_str_replace(Array(".", ","), "-", floatval(get_bloginfo("version")))
admin_body_class += " version-" + php_str_replace(".", "-", php_preg_replace("/^([.0-9]+).*/", "$1", get_bloginfo("version")))
admin_body_class += " admin-color-" + sanitize_html_class(get_user_option("admin_color"), "fresh")
admin_body_class += " locale-" + sanitize_html_class(php_strtolower(php_str_replace("_", "-", get_user_locale())))
if wp_is_mobile():
    admin_body_class += " mobile"
# end if
if is_multisite():
    admin_body_class += " multisite"
# end if
if is_network_admin():
    admin_body_class += " network-admin"
# end if
admin_body_class += " no-customize-support no-svg"
if current_screen.is_block_editor():
    #// Default to is-fullscreen-mode to avoid jumps in the UI.
    admin_body_class += " block-editor-page is-fullscreen-mode wp-embed-responsive"
    if current_theme_supports("editor-styles") and current_theme_supports("dark-editor-style"):
        admin_body_class += " is-dark-theme"
    # end if
# end if
php_print("</head>\n")
#// 
#// Filters the CSS classes for the body tag in the admin.
#// 
#// This filter differs from the {@see 'post_class'} and {@see 'body_class'} filters
#// in two important ways:
#// 
#// 1. `$classes` is a space-separated string of class names instead of an array.
#// 2. Not all core admin classes are filterable, notably: wp-admin, wp-core-ui,
#// and no-js cannot be removed.
#// 
#// @since 2.3.0
#// 
#// @param string $classes Space-separated list of CSS classes.
#//
admin_body_classes = apply_filters("admin_body_class", "")
admin_body_classes = php_ltrim(admin_body_classes + " " + admin_body_class)
php_print("<body class=\"wp-admin wp-core-ui no-js ")
php_print(admin_body_classes)
php_print("""\">
<script type=\"text/javascript\">
document.body.className = document.body.className.replace('no-js','js');
</script>
""")
#// Make sure the customize body classes are correct as early as possible.
if current_user_can("customize"):
    wp_customize_support_script()
# end if
php_print("\n<div id=\"wpwrap\">\n")
php_include_file(ABSPATH + "wp-admin/menu-header.php", once=False)
php_print("<div id=\"wpcontent\">\n\n")
#// 
#// Fires at the beginning of the content section in an admin page.
#// 
#// @since 3.0.0
#//
do_action("in_admin_header")
php_print("\n<div id=\"wpbody\" role=\"main\">\n")
blog_name = None
total_update_count = None
update_title = None
current_screen.set_parentage(parent_file)
php_print("\n<div id=\"wpbody-content\">\n")
current_screen.render_screen_meta()
if is_network_admin():
    #// 
    #// Prints network admin screen notices.
    #// 
    #// @since 3.1.0
    #//
    do_action("network_admin_notices")
elif is_user_admin():
    #// 
    #// Prints user admin screen notices.
    #// 
    #// @since 3.1.0
    #//
    do_action("user_admin_notices")
else:
    #// 
    #// Prints admin screen notices.
    #// 
    #// @since 3.1.0
    #//
    do_action("admin_notices")
# end if
#// 
#// Prints generic admin screen notices.
#// 
#// @since 3.1.0
#//
do_action("all_admin_notices")
if "options-general.php" == parent_file:
    php_include_file(ABSPATH + "wp-admin/options-head.php", once=False)
# end if
