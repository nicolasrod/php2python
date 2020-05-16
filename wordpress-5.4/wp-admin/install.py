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
#// WordPress Installer
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Sanity check.
if False:
    php_print("""<!DOCTYPE html>
    <html xmlns=\"http://www.w3.org/1999/xhtml\">
    <head>
    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
    <title>Error: PHP is not running</title>
    </head>
    <body class=\"wp-core-ui\">
    <p id=\"logo\"><a href=\"https://wordpress.org/\">WordPress</a></p>
    <h1>Error: PHP is not running</h1>
    <p>WordPress requires that your web server is running PHP. Your server does not have PHP installed, or PHP is turned off.</p>
    </body>
    </html>
    """)
# end if
#// 
#// We are installing WordPress.
#// 
#// @since 1.5.1
#// @var bool
#//
php_define("WP_INSTALLING", True)
#// Load WordPress Bootstrap
php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
#// Load WordPress Administration Upgrade API
php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
#// Load WordPress Translation Install API
php_include_file(ABSPATH + "wp-admin/includes/translation-install.php", once=True)
#// Load wpdb
php_include_file(ABSPATH + WPINC + "/wp-db.php", once=True)
nocache_headers()
step = php_int(PHP_REQUEST["step"]) if (php_isset(lambda : PHP_REQUEST["step"])) else 0
#// 
#// Display installation header.
#// 
#// @since 2.5.0
#// 
#// @param string $body_classes
#//
def display_header(body_classes="", *args_):
    
    php_header("Content-Type: text/html; charset=utf-8")
    if is_rtl():
        body_classes += "rtl"
    # end if
    if body_classes:
        body_classes = " " + body_classes
    # end if
    php_print("<!DOCTYPE html>\n<html xmlns=\"http://www.w3.org/1999/xhtml\" ")
    language_attributes()
    php_print(""">
    <head>
    <meta name=\"viewport\" content=\"width=device-width\" />
    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
    <meta name=\"robots\" content=\"noindex,nofollow\" />
    <title>""")
    _e("WordPress &rsaquo; Installation")
    php_print("</title>\n   ")
    wp_admin_css("install", True)
    php_print("</head>\n<body class=\"wp-core-ui")
    php_print(body_classes)
    php_print("\">\n<p id=\"logo\"><a href=\"")
    php_print(esc_url(__("https://wordpress.org/")))
    php_print("\">")
    _e("WordPress")
    php_print("</a></p>\n\n ")
# end def display_header
#// End display_header().
#// 
#// Display installer setup form.
#// 
#// @since 2.8.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string|null $error
#//
def display_setup_form(error=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    sql = wpdb.prepare("SHOW TABLES LIKE %s", wpdb.esc_like(wpdb.users))
    user_table = wpdb.get_var(sql) != None
    #// Ensure that sites appear in search engines by default.
    blog_public = 1
    if (php_isset(lambda : PHP_POST["weblog_title"])):
        blog_public = (php_isset(lambda : PHP_POST["blog_public"]))
    # end if
    weblog_title = php_trim(wp_unslash(PHP_POST["weblog_title"])) if (php_isset(lambda : PHP_POST["weblog_title"])) else ""
    user_name = php_trim(wp_unslash(PHP_POST["user_name"])) if (php_isset(lambda : PHP_POST["user_name"])) else ""
    admin_email = php_trim(wp_unslash(PHP_POST["admin_email"])) if (php_isset(lambda : PHP_POST["admin_email"])) else ""
    if (not is_null(error)):
        php_print("<h1>")
        _ex("Welcome", "Howdy")
        php_print("</h1>\n<p class=\"message\">")
        php_print(error)
        php_print("</p>\n")
    # end if
    php_print("""<form id=\"setup\" method=\"post\" action=\"install.php?step=2\" novalidate=\"novalidate\">
    <table class=\"form-table\" role=\"presentation\">
    <tr>
    <th scope=\"row\"><label for=\"weblog_title\">""")
    _e("Site Title")
    php_print("</label></th>\n          <td><input name=\"weblog_title\" type=\"text\" id=\"weblog_title\" size=\"25\" value=\"")
    php_print(esc_attr(weblog_title))
    php_print("""\" /></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"user_login\">""")
    _e("Username")
    php_print("</label></th>\n          <td>\n          ")
    if user_table:
        _e("User(s) already exists.")
        php_print("<input name=\"user_name\" type=\"hidden\" value=\"admin\" />")
    else:
        php_print("             <input name=\"user_name\" type=\"text\" id=\"user_login\" size=\"25\" value=\"")
        php_print(esc_attr(sanitize_user(user_name, True)))
        php_print("\" />\n              <p>")
        _e("Usernames can have only alphanumeric characters, spaces, underscores, hyphens, periods, and the @ symbol.")
        php_print("</p>\n               ")
    # end if
    php_print("         </td>\n     </tr>\n     ")
    if (not user_table):
        php_print("""       <tr class=\"form-field form-required user-pass1-wrap\">
        <th scope=\"row\">
        <label for=\"pass1\">
        """)
        _e("Password")
        php_print("""               </label>
        </th>
        <td>
        <div class=\"wp-pwd\">
        """)
        initial_password = stripslashes(PHP_POST["admin_password"]) if (php_isset(lambda : PHP_POST["admin_password"])) else wp_generate_password(18)
        php_print("                 <input type=\"password\" name=\"admin_password\" id=\"pass1\" class=\"regular-text\" autocomplete=\"off\" data-reveal=\"1\" data-pw=\"")
        php_print(esc_attr(initial_password))
        php_print("\" aria-describedby=\"pass-strength-result\" />\n                    <button type=\"button\" class=\"button wp-hide-pw hide-if-no-js\" data-start-masked=\"")
        php_print(php_int((php_isset(lambda : PHP_POST["admin_password"]))))
        php_print("\" data-toggle=\"0\" aria-label=\"")
        esc_attr_e("Hide password")
        php_print("\">\n                        <span class=\"dashicons dashicons-hidden\"></span>\n                        <span class=\"text\">")
        _e("Hide")
        php_print("""</span>
        </button>
        <div id=\"pass-strength-result\" aria-live=\"polite\"></div>
        </div>
        <p><span class=\"description important hide-if-no-js\">
        <strong>""")
        _e("Important:")
        php_print("</strong>\n              ")
        pass
        php_print("             ")
        _e("You will need this password to log&nbsp;in. Please store it in a secure location.")
        php_print("""</span></p>
        </td>
        </tr>
        <tr class=\"form-field form-required user-pass2-wrap hide-if-js\">
        <th scope=\"row\">
        <label for=\"pass2\">""")
        _e("Repeat Password")
        php_print("                 <span class=\"description\">")
        _e("(required)")
        php_print("""</span>
        </label>
        </th>
        <td>
        <input name=\"admin_password2\" type=\"password\" id=\"pass2\" autocomplete=\"off\" />
        </td>
        </tr>
        <tr class=\"pw-weak\">
        <th scope=\"row\">""")
        _e("Confirm Password")
        php_print("""</th>
        <td>
        <label>
        <input type=\"checkbox\" name=\"pw_weak\" class=\"pw-checkbox\" />
        """)
        _e("Confirm use of weak password")
        php_print("""               </label>
        </td>
        </tr>
        """)
    # end if
    php_print("     <tr>\n          <th scope=\"row\"><label for=\"admin_email\">")
    _e("Your Email")
    php_print("</label></th>\n          <td><input name=\"admin_email\" type=\"email\" id=\"admin_email\" size=\"25\" value=\"")
    php_print(esc_attr(admin_email))
    php_print("\" />\n          <p>")
    _e("Double-check your email address before continuing.")
    php_print("""</p></td>
    </tr>
    <tr>
    <th scope=\"row\">""")
    _e("Site Visibility") if has_action("blog_privacy_selector") else _e("Search Engine Visibility")
    php_print("""</th>
    <td>
    <fieldset>
    <legend class=\"screen-reader-text\"><span>""")
    _e("Site Visibility") if has_action("blog_privacy_selector") else _e("Search Engine Visibility")
    php_print(" </span></legend>\n                  ")
    if has_action("blog_privacy_selector"):
        php_print("                     <input id=\"blog-public\" type=\"radio\" name=\"blog_public\" value=\"1\" ")
        checked(1, blog_public)
        php_print(" />\n                        <label for=\"blog-public\">")
        _e("Allow search engines to index this site")
        php_print("</label><br/>\n                      <input id=\"blog-norobots\" type=\"radio\" name=\"blog_public\" value=\"0\" ")
        checked(0, blog_public)
        php_print(" />\n                        <label for=\"blog-norobots\">")
        _e("Discourage search engines from indexing this site")
        php_print("</label>\n                       <p class=\"description\">")
        _e("Note: Neither of these options blocks access to your site &mdash; it is up to search engines to honor your request.")
        php_print("</p>\n                       ")
        #// This action is documented in wp-admin/options-reading.php
        do_action("blog_privacy_selector")
    else:
        php_print("                     <label for=\"blog_public\"><input name=\"blog_public\" type=\"checkbox\" id=\"blog_public\" value=\"0\" ")
        checked(0, blog_public)
        php_print(" />\n                        ")
        _e("Discourage search engines from indexing this site")
        php_print("</label>\n                       <p class=\"description\">")
        _e("It is up to search engines to honor this request.")
        php_print("</p>\n                   ")
    # end if
    php_print("""               </fieldset>
    </td>
    </tr>
    </table>
    <p class=\"step\">""")
    submit_button(__("Install WordPress"), "large", "Submit", False, Array({"id": "submit"}))
    php_print("</p>\n   <input type=\"hidden\" name=\"language\" value=\"")
    php_print(esc_attr(PHP_REQUEST["language"]) if (php_isset(lambda : PHP_REQUEST["language"])) else "")
    php_print("\" />\n</form>\n ")
# end def display_setup_form
#// End display_setup_form().
#// Let's check to make sure WP isn't already installed.
if is_blog_installed():
    display_header()
    php_print("<h1>" + __("Already Installed") + "</h1>" + "<p>" + __("You appear to have already installed WordPress. To reinstall please clear your old database tables first.") + "</p>" + "<p class=\"step\"><a href=\"" + esc_url(wp_login_url()) + "\" class=\"button button-large\">" + __("Log In") + "</a></p>" + "</body></html>")
    php_exit()
# end if
#// 
#// @global string $wp_version             The WordPress version string.
#// @global string $required_php_version   The required PHP version string.
#// @global string $required_mysql_version The required MySQL version string.
#//
global wp_version,required_php_version,required_mysql_version
php_check_if_defined("wp_version","required_php_version","required_mysql_version")
php_version = php_phpversion()
mysql_version = wpdb.db_version()
php_compat = php_version_compare(php_version, required_php_version, ">=")
mysql_compat = php_version_compare(mysql_version, required_mysql_version, ">=") or php_file_exists(WP_CONTENT_DIR + "/db.php")
version_url = php_sprintf(esc_url(__("https://wordpress.org/support/wordpress-version/version-%s/")), sanitize_title(wp_version))
#// translators: %s: URL to Update PHP page.
php_update_message = "</p><p>" + php_sprintf(__("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
annotation = wp_get_update_php_annotation()
if annotation:
    php_update_message += "</p><p><em>" + annotation + "</em>"
# end if
if (not mysql_compat) and (not php_compat):
    #// translators: 1: URL to WordPress release notes, 2: WordPress version number, 3: Minimum required PHP version number, 4: Minimum required MySQL version number, 5: Current PHP version number, 6: Current MySQL version number.
    compat = php_sprintf(__("You cannot install because <a href=\"%1$s\">WordPress %2$s</a> requires PHP version %3$s or higher and MySQL version %4$s or higher. You are running PHP version %5$s and MySQL version %6$s."), version_url, wp_version, required_php_version, required_mysql_version, php_version, mysql_version) + php_update_message
elif (not php_compat):
    #// translators: 1: URL to WordPress release notes, 2: WordPress version number, 3: Minimum required PHP version number, 4: Current PHP version number.
    compat = php_sprintf(__("You cannot install because <a href=\"%1$s\">WordPress %2$s</a> requires PHP version %3$s or higher. You are running version %4$s."), version_url, wp_version, required_php_version, php_version) + php_update_message
elif (not mysql_compat):
    #// translators: 1: URL to WordPress release notes, 2: WordPress version number, 3: Minimum required MySQL version number, 4: Current MySQL version number.
    compat = php_sprintf(__("You cannot install because <a href=\"%1$s\">WordPress %2$s</a> requires MySQL version %3$s or higher. You are running version %4$s."), version_url, wp_version, required_mysql_version, mysql_version)
# end if
if (not mysql_compat) or (not php_compat):
    display_header()
    php_print("<h1>" + __("Requirements Not Met") + "</h1><p>" + compat + "</p></body></html>")
    php_exit()
# end if
if (not php_is_string(wpdb.base_prefix)) or "" == wpdb.base_prefix:
    display_header()
    php_print("<h1>" + __("Configuration Error") + "</h1>" + "<p>" + php_sprintf(__("Your %s file has an empty database table prefix, which is not supported."), "<code>wp-config.php</code>") + "</p></body></html>")
    php_exit()
# end if
#// Set error message if DO_NOT_UPGRADE_GLOBAL_TABLES isn't set as it will break install.
if php_defined("DO_NOT_UPGRADE_GLOBAL_TABLES"):
    display_header()
    php_print("<h1>" + __("Configuration Error") + "</h1>" + "<p>" + php_sprintf(__("The constant %s cannot be defined when installing WordPress."), "<code>DO_NOT_UPGRADE_GLOBAL_TABLES</code>") + "</p></body></html>")
    php_exit()
# end if
#// 
#// @global string    $wp_local_package Locale code of the package.
#// @global WP_Locale $wp_locale        WordPress date and time locale object.
#//
language = ""
if (not php_empty(lambda : PHP_REQUEST["language"])):
    language = php_preg_replace("/[^a-zA-Z0-9_]/", "", PHP_REQUEST["language"])
elif (php_isset(lambda : PHP_GLOBALS["wp_local_package"])):
    language = PHP_GLOBALS["wp_local_package"]
# end if
scripts_to_print = Array("jquery")
for case in Switch(step):
    if case(0):
        #// Step 0.
        if wp_can_install_language_pack() and php_empty(lambda : language):
            languages = wp_get_available_translations()
            if languages:
                scripts_to_print[-1] = "language-chooser"
                display_header("language-chooser")
                php_print("<form id=\"setup\" method=\"post\" action=\"?step=1\">")
                wp_install_language_form(languages)
                php_print("</form>")
                break
            # end if
        # end if
    # end if
    if case(1):
        #// Step 1, direct link or from language chooser.
        if (not php_empty(lambda : language)):
            loaded_language = wp_download_language_pack(language)
            if loaded_language:
                load_default_textdomain(loaded_language)
                PHP_GLOBALS["wp_locale"] = php_new_class("WP_Locale", lambda : WP_Locale())
            # end if
        # end if
        scripts_to_print[-1] = "user-profile"
        display_header()
        php_print("<h1>")
        _ex("Welcome", "Howdy")
        php_print("</h1>\n<p>")
        _e("Welcome to the famous five-minute WordPress installation process! Just fill in the information below and you&#8217;ll be on your way to using the most extendable and powerful personal publishing platform in the world.")
        php_print("</p>\n\n<h2>")
        _e("Information needed")
        php_print("</h2>\n<p>")
        _e("Please provide the following information. Don&#8217;t worry, you can always change these settings later.")
        php_print("</p>\n\n     ")
        display_setup_form()
        break
    # end if
    if case(2):
        if (not php_empty(lambda : language)) and load_default_textdomain(language):
            loaded_language = language
            PHP_GLOBALS["wp_locale"] = php_new_class("WP_Locale", lambda : WP_Locale())
        else:
            loaded_language = "en_US"
        # end if
        if (not php_empty(lambda : wpdb.error)):
            wp_die(wpdb.error.get_error_message())
        # end if
        scripts_to_print[-1] = "user-profile"
        display_header()
        #// Fill in the data we gathered.
        weblog_title = php_trim(wp_unslash(PHP_POST["weblog_title"])) if (php_isset(lambda : PHP_POST["weblog_title"])) else ""
        user_name = php_trim(wp_unslash(PHP_POST["user_name"])) if (php_isset(lambda : PHP_POST["user_name"])) else ""
        admin_password = wp_unslash(PHP_POST["admin_password"]) if (php_isset(lambda : PHP_POST["admin_password"])) else ""
        admin_password_check = wp_unslash(PHP_POST["admin_password2"]) if (php_isset(lambda : PHP_POST["admin_password2"])) else ""
        admin_email = php_trim(wp_unslash(PHP_POST["admin_email"])) if (php_isset(lambda : PHP_POST["admin_email"])) else ""
        public = php_int(PHP_POST["blog_public"]) if (php_isset(lambda : PHP_POST["blog_public"])) else 1
        #// Check email address.
        error = False
        if php_empty(lambda : user_name):
            #// TODO: Poka-yoke.
            display_setup_form(__("Please provide a valid username."))
            error = True
        elif sanitize_user(user_name, True) != user_name:
            display_setup_form(__("The username you provided has invalid characters."))
            error = True
        elif admin_password != admin_password_check:
            #// TODO: Poka-yoke.
            display_setup_form(__("Your passwords do not match. Please try again."))
            error = True
        elif php_empty(lambda : admin_email):
            #// TODO: Poka-yoke.
            display_setup_form(__("You must provide an email address."))
            error = True
        elif (not is_email(admin_email)):
            #// TODO: Poka-yoke.
            display_setup_form(__("Sorry, that isn&#8217;t a valid email address. Email addresses look like <code>username@example.com</code>."))
            error = True
        # end if
        if False == error:
            wpdb.show_errors()
            result = wp_install(weblog_title, user_name, admin_email, public, "", wp_slash(admin_password), loaded_language)
            php_print("\n<h1>")
            _e("Success!")
            php_print("</h1>\n\n<p>")
            _e("WordPress has been installed. Thank you, and enjoy!")
            php_print("""</p>
            <table class=\"form-table install-success\">
            <tr>
            <th>""")
            _e("Username")
            php_print("</th>\n      <td>")
            php_print(esc_html(sanitize_user(user_name, True)))
            php_print("""</td>
            </tr>
            <tr>
            <th>""")
            _e("Password")
            php_print("</th>\n      <td>\n          ")
            if (not php_empty(lambda : result["password"])) and php_empty(lambda : admin_password_check):
                php_print("         <code>")
                php_print(esc_html(result["password"]))
                php_print("</code><br />\n      ")
            # end if
            php_print("         <p>")
            php_print(result["password_message"])
            php_print("""</p>
            </td>
            </tr>
            </table>
            <p class=\"step\"><a href=\"""")
            php_print(esc_url(wp_login_url()))
            php_print("\" class=\"button button-large\">")
            _e("Log In")
            php_print("</a></p>\n\n         ")
        # end if
        break
    # end if
# end for
if (not wp_is_mobile()):
    php_print("<script type=\"text/javascript\">var t = document.getElementById('weblog_title'); if (t){ t.focus(); }</script>\n    ")
# end if
wp_print_scripts(scripts_to_print)
php_print("""<script type=\"text/javascript\">
jQuery( function( $ ) {
$( '.hide-if-no-js' ).removeClass( 'hide-if-no-js' );
} );
</script>
</body>
</html>
""")
