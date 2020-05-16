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
#// Upgrade WordPress Page.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// We are upgrading WordPress.
#// 
#// @since 1.5.1
#// @var bool
#//
php_define("WP_INSTALLING", True)
#// Load WordPress Bootstrap
php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=False)
nocache_headers()
php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
delete_site_transient("update_core")
if (php_isset(lambda : PHP_REQUEST["step"])):
    step = PHP_REQUEST["step"]
else:
    step = 0
# end if
#// Do it. No output.
if "upgrade_db" == step:
    wp_upgrade()
    php_print("0")
    php_exit()
# end if
#// 
#// @global string $wp_version             The WordPress version string.
#// @global string $required_php_version   The required PHP version string.
#// @global string $required_mysql_version The required MySQL version string.
#//
global wp_version,required_php_version,required_mysql_version
php_check_if_defined("wp_version","required_php_version","required_mysql_version")
step = php_int(step)
php_version = php_phpversion()
mysql_version = wpdb.db_version()
php_compat = php_version_compare(php_version, required_php_version, ">=")
if php_file_exists(WP_CONTENT_DIR + "/db.php") and php_empty(lambda : wpdb.is_mysql):
    mysql_compat = True
else:
    mysql_compat = php_version_compare(mysql_version, required_mysql_version, ">=")
# end if
php_header("Content-Type: " + get_option("html_type") + "; charset=" + get_option("blog_charset"))
php_print("<!DOCTYPE html>\n<html xmlns=\"http://www.w3.org/1999/xhtml\" ")
language_attributes()
php_print(""">
<head>
<meta name=\"viewport\" content=\"width=device-width\" />
<meta http-equiv=\"Content-Type\" content=\"""")
bloginfo("html_type")
php_print("; charset=")
php_print(get_option("blog_charset"))
php_print("\" />\n  <meta name=\"robots\" content=\"noindex,nofollow\" />\n <title>")
_e("WordPress &rsaquo; Update")
php_print("</title>\n   ")
wp_admin_css("install", True)
wp_admin_css("ie", True)
php_print("</head>\n<body class=\"wp-core-ui\">\n<p id=\"logo\"><a href=\"")
php_print(esc_url(__("https://wordpress.org/")))
php_print("\">")
_e("WordPress")
php_print("</a></p>\n\n")
if get_option("db_version") == wp_db_version or (not is_blog_installed()):
    php_print("\n<h1>")
    _e("No Update Required")
    php_print("</h1>\n<p>")
    _e("Your WordPress database is already up to date!")
    php_print("</p>\n<p class=\"step\"><a class=\"button button-large\" href=\"")
    php_print(get_option("home"))
    php_print("/\">")
    _e("Continue")
    php_print("</a></p>\n\n ")
elif (not php_compat) or (not mysql_compat):
    version_url = php_sprintf(esc_url(__("https://wordpress.org/support/wordpress-version/version-%s/")), sanitize_title(wp_version))
    #// translators: %s: URL to Update PHP page.
    php_update_message = "</p><p>" + php_sprintf(__("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
    annotation = wp_get_update_php_annotation()
    if annotation:
        php_update_message += "</p><p><em>" + annotation + "</em>"
    # end if
    if (not mysql_compat) and (not php_compat):
        message = php_sprintf(__("You cannot update because <a href=\"%1$s\">WordPress %2$s</a> requires PHP version %3$s or higher and MySQL version %4$s or higher. You are running PHP version %5$s and MySQL version %6$s."), version_url, wp_version, required_php_version, required_mysql_version, php_version, mysql_version) + php_update_message
    elif (not php_compat):
        message = php_sprintf(__("You cannot update because <a href=\"%1$s\">WordPress %2$s</a> requires PHP version %3$s or higher. You are running version %4$s."), version_url, wp_version, required_php_version, php_version) + php_update_message
    elif (not mysql_compat):
        message = php_sprintf(__("You cannot update because <a href=\"%1$s\">WordPress %2$s</a> requires MySQL version %3$s or higher. You are running version %4$s."), version_url, wp_version, required_mysql_version, mysql_version)
    # end if
    php_print("<p>" + message + "</p>")
    php_print(" ")
else:
    for case in Switch(step):
        if case(0):
            goback = wp_get_referer()
            if goback:
                goback = esc_url_raw(goback)
                goback = urlencode(goback)
            # end if
            php_print(" <h1>")
            _e("Database Update Required")
            php_print("</h1>\n<p>")
            _e("WordPress has been updated! Before we send you on your way, we have to update your database to the newest version.")
            php_print("</p>\n<p>")
            _e("The database update process may take a little while, so please be patient.")
            php_print("</p>\n<p class=\"step\"><a class=\"button button-large button-primary\" href=\"upgrade.php?step=1&amp;backto=")
            php_print(goback)
            php_print("\">")
            _e("Update WordPress Database")
            php_print("</a></p>\n           ")
            break
        # end if
        if case(1):
            wp_upgrade()
            backto = wp_unslash(urldecode(PHP_REQUEST["backto"])) if (not php_empty(lambda : PHP_REQUEST["backto"])) else __get_option("home") + "/"
            backto = esc_url(backto)
            backto = wp_validate_redirect(backto, __get_option("home") + "/")
            php_print(" <h1>")
            _e("Update Complete")
            php_print("</h1>\n  <p>")
            _e("Your WordPress database has been successfully updated!")
            php_print("</p>\n   <p class=\"step\"><a class=\"button button-large\" href=\"")
            php_print(backto)
            php_print("\">")
            _e("Continue")
            php_print("</a></p>\n           ")
            break
        # end if
    # end for
# end if
php_print("</body>\n</html>\n")
