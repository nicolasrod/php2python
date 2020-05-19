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
#// Retrieves and creates the wp-config.php file.
#// 
#// The permissions for the base directory must allow for writing files in order
#// for the wp-config.php to be created using this page.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// We are installing.
#//
php_define("WP_INSTALLING", True)
#// 
#// We are blissfully unaware of anything.
#//
php_define("WP_SETUP_CONFIG", True)
#// 
#// Disable error reporting
#// 
#// Set this to error_reporting( -1 ) for debugging
#//
php_error_reporting(0)
if (not php_defined("ABSPATH")):
    php_define("ABSPATH", php_dirname(__DIR__) + "/")
# end if
php_include_file(ABSPATH + "wp-settings.php", once=False)
#// Load WordPress Administration Upgrade API
php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
#// Load WordPress Translation Installation API
php_include_file(ABSPATH + "wp-admin/includes/translation-install.php", once=True)
nocache_headers()
#// Support wp-config-sample.php one level up, for the develop repo.
if php_file_exists(ABSPATH + "wp-config-sample.php"):
    config_file_ = file(ABSPATH + "wp-config-sample.php")
elif php_file_exists(php_dirname(ABSPATH) + "/wp-config-sample.php"):
    config_file_ = file(php_dirname(ABSPATH) + "/wp-config-sample.php")
else:
    wp_die(php_sprintf(__("Sorry, I need a %s file to work from. Please re-upload this file to your WordPress installation."), "<code>wp-config-sample.php</code>"))
# end if
#// Check if wp-config.php has been created.
if php_file_exists(ABSPATH + "wp-config.php"):
    wp_die("<p>" + php_sprintf(__("The file %1$s already exists. If you need to reset any of the configuration items in this file, please delete it first. You may try <a href=\"%2$s\">installing now</a>."), "<code>wp-config.php</code>", "install.php") + "</p>")
# end if
#// Check if wp-config.php exists above the root directory but is not part of another installation.
if php_no_error(lambda: php_file_exists(ABSPATH + "../wp-config.php")) and (not php_no_error(lambda: php_file_exists(ABSPATH + "../wp-settings.php"))):
    wp_die("<p>" + php_sprintf(__("The file %1$s already exists one level above your WordPress installation. If you need to reset any of the configuration items in this file, please delete it first. You may try <a href=\"%2$s\">installing now</a>."), "<code>wp-config.php</code>", "install.php") + "</p>")
# end if
step_ = php_int(PHP_REQUEST["step"]) if (php_isset(lambda : PHP_REQUEST["step"])) else -1
#// 
#// Display setup wp-config.php file header.
#// 
#// @ignore
#// @since 2.3.0
#// 
#// @global string    $wp_local_package Locale code of the package.
#// @global WP_Locale $wp_locale        WordPress date and time locale object.
#// 
#// @param string|array $body_classes
#//
def setup_config_display_header(body_classes_=None, *_args_):
    if body_classes_ is None:
        body_classes_ = Array()
    # end if
    
    body_classes_ = body_classes_
    body_classes_[-1] = "wp-core-ui"
    dir_attr_ = ""
    if is_rtl():
        body_classes_[-1] = "rtl"
        dir_attr_ = " dir=\"rtl\""
    # end if
    php_header("Content-Type: text/html; charset=utf-8")
    php_print("<!DOCTYPE html>\n<html xmlns=\"http://www.w3.org/1999/xhtml\"")
    php_print(dir_attr_)
    php_print(""">
    <head>
    <meta name=\"viewport\" content=\"width=device-width\" />
    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
    <meta name=\"robots\" content=\"noindex,nofollow\" />
    <title>""")
    _e("WordPress &rsaquo; Setup Configuration File")
    php_print("</title>\n   ")
    wp_admin_css("install", True)
    php_print("</head>\n<body class=\"")
    php_print(php_implode(" ", body_classes_))
    php_print("\">\n<p id=\"logo\"><a href=\"")
    php_print(esc_url(__("https://wordpress.org/")))
    php_print("\">")
    _e("WordPress")
    php_print("</a></p>\n   ")
# end def setup_config_display_header
#// End function setup_config_display_header();
language_ = ""
if (not php_empty(lambda : PHP_REQUEST["language"])):
    language_ = php_preg_replace("/[^a-zA-Z0-9_]/", "", PHP_REQUEST["language"])
elif (php_isset(lambda : PHP_GLOBALS["wp_local_package"])):
    language_ = PHP_GLOBALS["wp_local_package"]
# end if
for case in Switch(step_):
    if case(-1):
        if wp_can_install_language_pack() and php_empty(lambda : language_):
            languages_ = wp_get_available_translations()
            if languages_:
                setup_config_display_header("language-chooser")
                php_print("<h1 class=\"screen-reader-text\">Select a default language</h1>")
                php_print("<form id=\"setup\" method=\"post\" action=\"?step=0\">")
                wp_install_language_form(languages_)
                php_print("</form>")
                break
            # end if
        # end if
    # end if
    if case(0):
        if (not php_empty(lambda : language_)):
            loaded_language_ = wp_download_language_pack(language_)
            if loaded_language_:
                load_default_textdomain(loaded_language_)
                PHP_GLOBALS["wp_locale"] = php_new_class("WP_Locale", lambda : WP_Locale())
            # end if
        # end if
        setup_config_display_header()
        step_1_ = "setup-config.php?step=1"
        if (php_isset(lambda : PHP_REQUEST["noapi"])):
            step_1_ += "&amp;noapi"
        # end if
        if (not php_empty(lambda : loaded_language_)):
            step_1_ += "&amp;language=" + loaded_language_
        # end if
        php_print("<h1 class=\"screen-reader-text\">")
        _e("Before getting started")
        php_print("</h1>\n<p>")
        _e("Welcome to WordPress. Before getting started, we need some information on the database. You will need to know the following items before proceeding.")
        php_print("</p>\n<ol>\n <li>")
        _e("Database name")
        php_print("</li>\n  <li>")
        _e("Database username")
        php_print("</li>\n  <li>")
        _e("Database password")
        php_print("</li>\n  <li>")
        _e("Database host")
        php_print("</li>\n  <li>")
        _e("Table prefix (if you want to run more than one WordPress in a single database)")
        php_print("""</li>
        </ol>
        <p>
        """)
        php_printf(__("We&#8217;re going to use this information to create a %s file."), "<code>wp-config.php</code>")
        php_print(" <strong>\n      ")
        php_printf(__("If for any reason this automatic file creation doesn&#8217;t work, don&#8217;t worry. All this does is fill in the database information to a configuration file. You may also simply open %1$s in a text editor, fill in your information, and save it as %2$s."), "<code>wp-config-sample.php</code>", "<code>wp-config.php</code>")
        php_print(" </strong>\n     ")
        php_printf(__("Need more help? <a href=\"%s\">We got it</a>."), __("https://wordpress.org/support/article/editing-wp-config-php/"))
        php_print("</p>\n<p>")
        _e("In all likelihood, these items were supplied to you by your Web Host. If you don&#8217;t have this information, then you will need to contact them before you can continue. If you&#8217;re all ready&hellip;")
        php_print("</p>\n\n<p class=\"step\"><a href=\"")
        php_print(step_1_)
        php_print("\" class=\"button button-large\">")
        _e("Let&#8217;s go!")
        php_print("</a></p>\n       ")
        break
    # end if
    if case(1):
        load_default_textdomain(language_)
        PHP_GLOBALS["wp_locale"] = php_new_class("WP_Locale", lambda : WP_Locale())
        setup_config_display_header()
        autofocus_ = "" if wp_is_mobile() else " autofocus"
        php_print("<h1 class=\"screen-reader-text\">")
        _e("Set up your database connection")
        php_print("</h1>\n<form method=\"post\" action=\"setup-config.php?step=2\">\n   <p>")
        _e("Below you should enter your database connection details. If you&#8217;re not sure about these, contact your host.")
        php_print("""</p>
        <table class=\"form-table\" role=\"presentation\">
        <tr>
        <th scope=\"row\"><label for=\"dbname\">""")
        _e("Database Name")
        php_print("</label></th>\n          <td><input name=\"dbname\" id=\"dbname\" type=\"text\" aria-describedby=\"dbname-desc\" size=\"25\" value=\"wordpress\"")
        php_print(autofocus_)
        php_print("/></td>\n            <td id=\"dbname-desc\">")
        _e("The name of the database you want to use with WordPress.")
        php_print("""</td>
        </tr>
        <tr>
        <th scope=\"row\"><label for=\"uname\">""")
        _e("Username")
        php_print("</label></th>\n          <td><input name=\"uname\" id=\"uname\" type=\"text\" aria-describedby=\"uname-desc\" size=\"25\" value=\"")
        php_print(php_htmlspecialchars(_x("username", "example username"), ENT_QUOTES))
        php_print("\" /></td>\n         <td id=\"uname-desc\">")
        _e("Your database username.")
        php_print("""</td>
        </tr>
        <tr>
        <th scope=\"row\"><label for=\"pwd\">""")
        _e("Password")
        php_print("</label></th>\n          <td><input name=\"pwd\" id=\"pwd\" type=\"text\" aria-describedby=\"pwd-desc\" size=\"25\" value=\"")
        php_print(php_htmlspecialchars(_x("password", "example password"), ENT_QUOTES))
        php_print("\" autocomplete=\"off\" /></td>\n            <td id=\"pwd-desc\">")
        _e("Your database password.")
        php_print("""</td>
        </tr>
        <tr>
        <th scope=\"row\"><label for=\"dbhost\">""")
        _e("Database Host")
        php_print("""</label></th>
        <td><input name=\"dbhost\" id=\"dbhost\" type=\"text\" aria-describedby=\"dbhost-desc\" size=\"25\" value=\"localhost\" /></td>
        <td id=\"dbhost-desc\">
        """)
        #// translators: %s: localhost
        php_printf(__("You should be able to get this info from your web host, if %s doesn&#8217;t work."), "<code>localhost</code>")
        php_print("""           </td>
        </tr>
        <tr>
        <th scope=\"row\"><label for=\"prefix\">""")
        _e("Table Prefix")
        php_print("</label></th>\n          <td><input name=\"prefix\" id=\"prefix\" type=\"text\" aria-describedby=\"prefix-desc\" value=\"wp_\" size=\"25\" /></td>\n         <td id=\"prefix-desc\">")
        _e("If you want to run multiple WordPress installations in a single database, change this.")
        php_print("""</td>
        </tr>
        </table>
        """)
        if (php_isset(lambda : PHP_REQUEST["noapi"])):
            php_print("<input name=\"noapi\" type=\"hidden\" value=\"1\" />")
        # end if
        php_print(" <input type=\"hidden\" name=\"language\" value=\"")
        php_print(esc_attr(language_))
        php_print("\" />\n  <p class=\"step\"><input name=\"submit\" type=\"submit\" value=\"")
        php_print(php_htmlspecialchars(__("Submit"), ENT_QUOTES))
        php_print("\" class=\"button button-large\" /></p>\n</form>\n       ")
        break
    # end if
    if case(2):
        load_default_textdomain(language_)
        PHP_GLOBALS["wp_locale"] = php_new_class("WP_Locale", lambda : WP_Locale())
        dbname_ = php_trim(wp_unslash(PHP_POST["dbname"]))
        uname_ = php_trim(wp_unslash(PHP_POST["uname"]))
        pwd_ = php_trim(wp_unslash(PHP_POST["pwd"]))
        dbhost_ = php_trim(wp_unslash(PHP_POST["dbhost"]))
        prefix_ = php_trim(wp_unslash(PHP_POST["prefix"]))
        step_1_ = "setup-config.php?step=1"
        install_ = "install.php"
        if (php_isset(lambda : PHP_REQUEST["noapi"])):
            step_1_ += "&amp;noapi"
        # end if
        if (not php_empty(lambda : language_)):
            step_1_ += "&amp;language=" + language_
            install_ += "?language=" + language_
        else:
            install_ += "?language=en_US"
        # end if
        tryagain_link_ = "</p><p class=\"step\"><a href=\"" + step_1_ + "\" onclick=\"javascript:history.go(-1);return false;\" class=\"button button-large\">" + __("Try Again") + "</a>"
        if php_empty(lambda : prefix_):
            wp_die(__("<strong>Error</strong>: \"Table Prefix\" must not be empty.") + tryagain_link_)
        # end if
        #// Validate $prefix: it can only contain letters, numbers and underscores.
        if php_preg_match("|[^a-z0-9_]|i", prefix_):
            wp_die(__("<strong>Error</strong>: \"Table Prefix\" can only contain numbers, letters, and underscores.") + tryagain_link_)
        # end if
        #// Test the DB connection.
        #// #@+
        #// 
        #// @ignore
        #//
        php_define("DB_NAME", dbname_)
        php_define("DB_USER", uname_)
        php_define("DB_PASSWORD", pwd_)
        php_define("DB_HOST", dbhost_)
        wpdb_ = None
        require_wp_db()
        #// 
        #// The wpdb constructor bails when WP_SETUP_CONFIG is set, so we must
        #// fire this manually. We'll fail here if the values are no good.
        #//
        wpdb_.db_connect()
        if (not php_empty(lambda : wpdb_.error)):
            wp_die(wpdb_.error.get_error_message() + tryagain_link_)
        # end if
        errors_ = wpdb_.hide_errors()
        wpdb_.query(str("SELECT ") + str(prefix_))
        wpdb_.show_errors(errors_)
        if (not wpdb_.last_error):
            #// MySQL was able to parse the prefix as a value, which we don't want. Bail.
            wp_die(__("<strong>Error</strong>: \"Table Prefix\" is invalid."))
        # end if
        #// Generate keys and salts using secure CSPRNG; fallback to API if enabled; further fallback to original wp_generate_password().
        try: 
            chars_ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_ []{}<>~`+=,.;:/?|"
            max_ = php_strlen(chars_) - 1
            i_ = 0
            while i_ < 8:
                
                key_ = ""
                j_ = 0
                while j_ < 64:
                    
                    key_ += php_substr(chars_, php_random_int(0, max_), 1)
                    j_ += 1
                # end while
                secret_keys_[-1] = key_
                i_ += 1
            # end while
        except Exception as ex_:
            no_api_ = (php_isset(lambda : PHP_POST["noapi"]))
            if (not no_api_):
                secret_keys_ = wp_remote_get("https://api.wordpress.org/secret-key/1.1/salt/")
            # end if
            if no_api_ or is_wp_error(secret_keys_):
                secret_keys_ = Array()
                i_ = 0
                while i_ < 8:
                    
                    secret_keys_[-1] = wp_generate_password(64, True, True)
                    i_ += 1
                # end while
            else:
                secret_keys_ = php_explode("\n", wp_remote_retrieve_body(secret_keys_))
                for k_,v_ in secret_keys_.items():
                    secret_keys_[k_] = php_substr(v_, 28, 64)
                # end for
            # end if
        # end try
        key_ = 0
        for line_num_,line_ in config_file_.items():
            if "$table_prefix =" == php_substr(line_, 0, 15):
                config_file_[line_num_] = "$table_prefix = '" + addcslashes(prefix_, "\\'") + "';\r\n"
                continue
            # end if
            if (not php_preg_match("/^define\\(\\s*'([A-Z_]+)',([ ]+)/", line_, match_)):
                continue
            # end if
            constant_ = match_[1]
            padding_ = match_[2]
            for case in Switch(constant_):
                if case("DB_NAME"):
                    pass
                # end if
                if case("DB_USER"):
                    pass
                # end if
                if case("DB_PASSWORD"):
                    pass
                # end if
                if case("DB_HOST"):
                    config_file_[line_num_] = "define( '" + constant_ + "'," + padding_ + "'" + addcslashes(constant(constant_), "\\'") + "' );\r\n"
                    break
                # end if
                if case("DB_CHARSET"):
                    if "utf8mb4" == wpdb_.charset or (not wpdb_.charset) and wpdb_.has_cap("utf8mb4"):
                        config_file_[line_num_] = "define( '" + constant_ + "'," + padding_ + "'utf8mb4' );\r\n"
                    # end if
                    break
                # end if
                if case("AUTH_KEY"):
                    pass
                # end if
                if case("SECURE_AUTH_KEY"):
                    pass
                # end if
                if case("LOGGED_IN_KEY"):
                    pass
                # end if
                if case("NONCE_KEY"):
                    pass
                # end if
                if case("AUTH_SALT"):
                    pass
                # end if
                if case("SECURE_AUTH_SALT"):
                    pass
                # end if
                if case("LOGGED_IN_SALT"):
                    pass
                # end if
                if case("NONCE_SALT"):
                    config_file_[line_num_] = "define( '" + constant_ + "'," + padding_ + "'" + secret_keys_[key_] + "' );\r\n"
                    key_ += 1
                    break
                # end if
            # end for
        # end for
        line_ = None
        if (not php_is_writable(ABSPATH)):
            setup_config_display_header()
            php_print(" <p>\n           ")
            #// translators: %s: wp-config.php
            php_printf(__("Unable to write to %s file."), "<code>wp-config.php</code>")
            php_print("</p>\n<p>\n          ")
            #// translators: %s: wp-config.php
            php_printf(__("You can create the %s file manually and paste the following text into it."), "<code>wp-config.php</code>")
            config_text_ = ""
            for line_ in config_file_:
                config_text_ += htmlentities(line_, ENT_COMPAT, "UTF-8")
            # end for
            php_print("</p>\n<textarea id=\"wp-config\" cols=\"98\" rows=\"15\" class=\"code\" readonly=\"readonly\">")
            php_print(config_text_)
            php_print("</textarea>\n<p>")
            _e("After you&#8217;ve done that, click &#8220;Run the installation&#8221;.")
            php_print("</p>\n<p class=\"step\"><a href=\"")
            php_print(install_)
            php_print("\" class=\"button button-large\">")
            _e("Run the installation")
            php_print("""</a></p>
            <script>
            (function(){
        if ( ! /iPad|iPod|iPhone/.test( navigator.userAgent ) ) {
            var el = document.getElementById('wp-config');
            el.focus();
            el.select();
            }
            })();
            </script>
            """)
        else:
            #// 
            #// If this file doesn't exist, then we are using the wp-config-sample.php
            #// file one level up, which is for the develop repo.
            #//
            if php_file_exists(ABSPATH + "wp-config-sample.php"):
                path_to_wp_config_ = ABSPATH + "wp-config.php"
            else:
                path_to_wp_config_ = php_dirname(ABSPATH) + "/wp-config.php"
            # end if
            handle_ = fopen(path_to_wp_config_, "w")
            for line_ in config_file_:
                fwrite(handle_, line_)
            # end for
            php_fclose(handle_)
            chmod(path_to_wp_config_, 438)
            setup_config_display_header()
            php_print("<h1 class=\"screen-reader-text\">")
            _e("Successful database connection")
            php_print("</h1>\n<p>")
            _e("All right, sparky! You&#8217;ve made it through this part of the installation. WordPress can now communicate with your database. If you are ready, time now to&hellip;")
            php_print("</p>\n\n<p class=\"step\"><a href=\"")
            php_print(install_)
            php_print("\" class=\"button button-large\">")
            _e("Run the installation")
            php_print("</a></p>\n       ")
        # end if
        break
    # end if
# end for
wp_print_scripts("language-chooser")
php_print("</body>\n</html>\n")
