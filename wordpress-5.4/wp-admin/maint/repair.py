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
#// Database Repair and Optimization Script.
#// 
#// @package WordPress
#// @subpackage Database
#//
php_define("WP_REPAIRING", True)
php_include_file(php_dirname(php_dirname(__DIR__)) + "/wp-load.php", once=True)
php_header("Content-Type: text/html; charset=utf-8")
php_print("<!DOCTYPE html>\n<html xmlns=\"http://www.w3.org/1999/xhtml\" ")
language_attributes()
php_print(""">
<head>
<meta name=\"viewport\" content=\"width=device-width\" />
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
<meta name=\"robots\" content=\"noindex,nofollow\" />
<title>""")
_e("WordPress &rsaquo; Database Repair")
php_print("</title>\n   ")
wp_admin_css("install", True)
php_print("</head>\n<body class=\"wp-core-ui\">\n<p id=\"logo\"><a href=\"")
php_print(esc_url(__("https://wordpress.org/")))
php_print("\">")
_e("WordPress")
php_print("</a></p>\n\n")
if (not php_defined("WP_ALLOW_REPAIR")) or (not WP_ALLOW_REPAIR):
    php_print("<h1 class=\"screen-reader-text\">" + __("Allow automatic database repair") + "</h1>")
    php_print("<p>")
    printf(__("To allow use of this page to automatically repair database problems, please add the following line to your %s file. Once this line is added to your config, reload this page."), "<code>wp-config.php</code>")
    php_print("</p><p><code>define('WP_ALLOW_REPAIR', true);</code></p>")
    default_key = "put your unique phrase here"
    missing_key = False
    duplicated_keys = Array()
    for key in Array("AUTH_KEY", "SECURE_AUTH_KEY", "LOGGED_IN_KEY", "NONCE_KEY", "AUTH_SALT", "SECURE_AUTH_SALT", "LOGGED_IN_SALT", "NONCE_SALT"):
        if php_defined(key):
            #// Check for unique values of each key.
            duplicated_keys[constant(key)] = (php_isset(lambda : duplicated_keys[constant(key)]))
        else:
            #// If a constant is not defined, it's missing.
            missing_key = True
        # end if
    # end for
    #// If at least one key uses the default value, consider it duplicated.
    if (php_isset(lambda : duplicated_keys[default_key])):
        duplicated_keys[default_key] = True
    # end if
    #// Weed out all unique, non-default values.
    duplicated_keys = php_array_filter(duplicated_keys)
    if duplicated_keys or missing_key:
        php_print("<h2 class=\"screen-reader-text\">" + __("Check secret keys") + "</h2>")
        #// translators: 1: wp-config.php, 2: Secret key service URL.
        php_print("<p>" + php_sprintf(__("While you are editing your %1$s file, take a moment to make sure you have all 8 keys and that they are unique. You can generate these using the <a href=\"%2$s\">WordPress.org secret key service</a>."), "<code>wp-config.php</code>", "https://api.wordpress.org/secret-key/1.1/salt/") + "</p>")
    # end if
elif (php_isset(lambda : PHP_REQUEST["repair"])):
    php_print("<h1 class=\"screen-reader-text\">" + __("Database repair results") + "</h1>")
    optimize = 2 == PHP_REQUEST["repair"]
    okay = True
    problems = Array()
    tables = wpdb.tables()
    #// Sitecategories may not exist if global terms are disabled.
    query = wpdb.prepare("SHOW TABLES LIKE %s", wpdb.esc_like(wpdb.sitecategories))
    if is_multisite() and (not wpdb.get_var(query)):
        tables["sitecategories"] = None
    # end if
    #// 
    #// Filters additional database tables to repair.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string[] $tables Array of prefixed table names to be repaired.
    #//
    tables = php_array_merge(tables, apply_filters("tables_to_repair", Array()))
    #// Loop over the tables, checking and repairing as needed.
    for table in tables:
        check = wpdb.get_row(str("CHECK TABLE ") + str(table))
        php_print("<p>")
        if "OK" == check.Msg_text:
            #// translators: %s: Table name.
            printf(__("The %s table is okay."), str("<code>") + str(table) + str("</code>"))
        else:
            #// translators: 1: Table name, 2: Error message.
            printf(__("The %1$s table is not okay. It is reporting the following error: %2$s. WordPress will attempt to repair this table&hellip;"), str("<code>") + str(table) + str("</code>"), str("<code>") + str(check.Msg_text) + str("</code>"))
            repair = wpdb.get_row(str("REPAIR TABLE ") + str(table))
            php_print("<br />&nbsp;&nbsp;&nbsp;&nbsp;")
            if "OK" == check.Msg_text:
                #// translators: %s: Table name.
                printf(__("Successfully repaired the %s table."), str("<code>") + str(table) + str("</code>"))
            else:
                #// translators: 1: Table name, 2: Error message.
                php_print(php_sprintf(__("Failed to repair the %1$s table. Error: %2$s"), str("<code>") + str(table) + str("</code>"), str("<code>") + str(check.Msg_text) + str("</code>")) + "<br />")
                problems[table] = check.Msg_text
                okay = False
            # end if
        # end if
        if okay and optimize:
            check = wpdb.get_row(str("ANALYZE TABLE ") + str(table))
            php_print("<br />&nbsp;&nbsp;&nbsp;&nbsp;")
            if "Table is already up to date" == check.Msg_text:
                #// translators: %s: Table name.
                printf(__("The %s table is already optimized."), str("<code>") + str(table) + str("</code>"))
            else:
                check = wpdb.get_row(str("OPTIMIZE TABLE ") + str(table))
                php_print("<br />&nbsp;&nbsp;&nbsp;&nbsp;")
                if "OK" == check.Msg_text or "Table is already up to date" == check.Msg_text:
                    #// translators: %s: Table name.
                    printf(__("Successfully optimized the %s table."), str("<code>") + str(table) + str("</code>"))
                else:
                    #// translators: 1: Table name. 2: Error message.
                    printf(__("Failed to optimize the %1$s table. Error: %2$s"), str("<code>") + str(table) + str("</code>"), str("<code>") + str(check.Msg_text) + str("</code>"))
                # end if
            # end if
        # end if
        php_print("</p>")
    # end for
    if problems:
        printf("<p>" + __("Some database problems could not be repaired. Please copy-and-paste the following list of errors to the <a href=\"%s\">WordPress support forums</a> to get additional assistance.") + "</p>", __("https://wordpress.org/support/forum/how-to-and-troubleshooting"))
        problem_output = ""
        for table,problem in problems:
            problem_output += str(table) + str(": ") + str(problem) + str("\n")
        # end for
        php_print("<p><textarea name=\"errors\" id=\"errors\" rows=\"20\" cols=\"60\">" + esc_textarea(problem_output) + "</textarea></p>")
    else:
        php_print("<p>" + __("Repairs complete. Please remove the following line from wp-config.php to prevent this page from being used by unauthorized users.") + "</p><p><code>define('WP_ALLOW_REPAIR', true);</code></p>")
    # end if
else:
    php_print("<h1 class=\"screen-reader-text\">" + __("WordPress database repair") + "</h1>")
    if (php_isset(lambda : PHP_REQUEST["referrer"])) and "is_blog_installed" == PHP_REQUEST["referrer"]:
        php_print("<p>" + __("One or more database tables are unavailable. To allow WordPress to attempt to repair these tables, press the &#8220;Repair Database&#8221; button. Repairing can take a while, so please be patient.") + "</p>")
    else:
        php_print("<p>" + __("WordPress can automatically look for some common database problems and repair them. Repairing can take a while, so please be patient.") + "</p>")
    # end if
    php_print(" <p class=\"step\"><a class=\"button button-large\" href=\"repair.php?repair=1\">")
    _e("Repair Database")
    php_print("</a></p>\n   <p>")
    _e("WordPress can also attempt to optimize the database. This improves performance in some situations. Repairing and optimizing the database can take a long time and the database will be locked while optimizing.")
    php_print("</p>\n   <p class=\"step\"><a class=\"button button-large\" href=\"repair.php?repair=2\">")
    _e("Repair and Optimize Database")
    php_print("</a></p>\n   ")
# end if
php_print("</body>\n</html>\n")
