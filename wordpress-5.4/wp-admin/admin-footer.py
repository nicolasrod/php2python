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
#// WordPress Administration Template Footer
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Don't load directly.
if (not php_defined("ABSPATH")):
    php_print("-1")
    php_exit()
# end if
#// 
#// @global string $hook_suffix
#//
global hook_suffix_
php_check_if_defined("hook_suffix_")
php_print("""
<div class=\"clear\"></div></div><!-- wpbody-content -->
<div class=\"clear\"></div></div><!-- wpbody -->
<div class=\"clear\"></div></div><!-- wpcontent -->
<div id=\"wpfooter\" role=\"contentinfo\">
""")
#// 
#// Fires after the opening tag for the admin footer.
#// 
#// @since 2.5.0
#//
do_action("in_admin_footer")
php_print(" <p id=\"footer-left\" class=\"alignleft\">\n        ")
text_ = php_sprintf(__("Thank you for creating with <a href=\"%s\">WordPress</a>."), __("https://wordpress.org/"))
#// 
#// Filters the "Thank you" text displayed in the admin footer.
#// 
#// @since 2.8.0
#// 
#// @param string $text The content that will be printed.
#//
php_print(apply_filters("admin_footer_text", "<span id=\"footer-thankyou\">" + text_ + "</span>"))
php_print(" </p>\n  <p id=\"footer-upgrade\" class=\"alignright\">\n        ")
#// 
#// Filters the version/update text displayed in the admin footer.
#// 
#// WordPress prints the current version and update information,
#// using core_update_footer() at priority 10.
#// 
#// @since 2.3.0
#// 
#// @see core_update_footer()
#// 
#// @param string $content The content that will be printed.
#//
php_print(apply_filters("update_footer", ""))
php_print("""   </p>
<div class=\"clear\"></div>
</div>
""")
#// 
#// Prints scripts or data before the default footer scripts.
#// 
#// @since 1.2.0
#// 
#// @param string $data The data to print.
#//
do_action("admin_footer", "")
#// 
#// Prints scripts and data queued for the footer.
#// 
#// The dynamic portion of the hook name, `$hook_suffix`,
#// refers to the global hook suffix of the current page.
#// 
#// @since 4.6.0
#//
do_action(str("admin_print_footer_scripts-") + str(hook_suffix_))
#// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
#// 
#// Prints any scripts and data queued for the footer.
#// 
#// @since 2.8.0
#//
do_action("admin_print_footer_scripts")
#// 
#// Prints scripts or data after the default footer scripts.
#// 
#// The dynamic portion of the hook name, `$hook_suffix`,
#// refers to the global hook suffix of the current page.
#// 
#// @since 2.8.0
#//
do_action(str("admin_footer-") + str(hook_suffix_))
#// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
#// get_site_option() won't exist when auto upgrading from <= 2.7.
if php_function_exists("get_site_option"):
    if False == get_site_option("can_compress_scripts"):
        compression_test()
    # end if
# end if
php_print("""
<div class=\"clear\"></div></div><!-- wpwrap -->
<script type=\"text/javascript\">if(typeof wpOnload=='function')wpOnload();</script>
</body>
</html>
""")
