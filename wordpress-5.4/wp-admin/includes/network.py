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
#// WordPress Network Administration API.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// Check for an existing network.
#// 
#// @since 3.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return string|false Base domain if network exists, otherwise false.
#//
def network_domain_check(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    sql = wpdb.prepare("SHOW TABLES LIKE %s", wpdb.esc_like(wpdb.site))
    if wpdb.get_var(sql):
        return wpdb.get_var(str("SELECT domain FROM ") + str(wpdb.site) + str(" ORDER BY id ASC LIMIT 1"))
    # end if
    return False
# end def network_domain_check
#// 
#// Allow subdomain installation
#// 
#// @since 3.0.0
#// @return bool Whether subdomain installation is allowed
#//
def allow_subdomain_install(*args_):
    
    domain = php_preg_replace("|https?://([^/]+)|", "$1", get_option("home"))
    if php_parse_url(get_option("home"), PHP_URL_PATH) or "localhost" == domain or php_preg_match("|^[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+$|", domain):
        return False
    # end if
    return True
# end def allow_subdomain_install
#// 
#// Allow subdirectory installation.
#// 
#// @since 3.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return bool Whether subdirectory installation is allowed
#//
def allow_subdirectory_install(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// 
    #// Filters whether to enable the subdirectory installation feature in Multisite.
    #// 
    #// @since 3.0.0
    #// 
    #// @param bool $allow Whether to enable the subdirectory installation feature in Multisite. Default is false.
    #//
    if apply_filters("allow_subdirectory_install", False):
        return True
    # end if
    if php_defined("ALLOW_SUBDIRECTORY_INSTALL") and ALLOW_SUBDIRECTORY_INSTALL:
        return True
    # end if
    post = wpdb.get_row(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_date < DATE_SUB(NOW(), INTERVAL 1 MONTH) AND post_status = 'publish'"))
    if php_empty(lambda : post):
        return True
    # end if
    return False
# end def allow_subdirectory_install
#// 
#// Get base domain of network.
#// 
#// @since 3.0.0
#// @return string Base domain.
#//
def get_clean_basedomain(*args_):
    
    existing_domain = network_domain_check()
    if existing_domain:
        return existing_domain
    # end if
    domain = php_preg_replace("|https?://|", "", get_option("siteurl"))
    slash = php_strpos(domain, "/")
    if slash:
        domain = php_substr(domain, 0, slash)
    # end if
    return domain
# end def get_clean_basedomain
#// 
#// Prints step 1 for Network installation process.
#// 
#// @todo Realistically, step 1 should be a welcome screen explaining what a Network is and such. Navigating to Tools > Network
#// should not be a sudden "Welcome to a new install process! Fill this out and click here." See also contextual help todo.
#// 
#// @since 3.0.0
#// 
#// @global bool $is_apache
#// 
#// @param WP_Error $errors
#//
def network_step1(errors=False, *args_):
    
    global is_apache
    php_check_if_defined("is_apache")
    if php_defined("DO_NOT_UPGRADE_GLOBAL_TABLES"):
        php_print("<div class=\"error\"><p><strong>" + __("Error:") + "</strong> " + php_sprintf(__("The constant %s cannot be defined when creating a network."), "<code>DO_NOT_UPGRADE_GLOBAL_TABLES</code>") + "</p></div>")
        php_print("</div>")
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
        php_exit(0)
    # end if
    active_plugins = get_option("active_plugins")
    if (not php_empty(lambda : active_plugins)):
        php_print("<div class=\"notice notice-warning\"><p><strong>" + __("Warning:") + "</strong> " + php_sprintf(__("Please <a href=\"%s\">deactivate your plugins</a> before enabling the Network feature."), admin_url("plugins.php?plugin_status=active")) + "</p></div>")
        php_print("<p>" + __("Once the network is created, you may reactivate your plugins.") + "</p>")
        php_print("</div>")
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
        php_exit(0)
    # end if
    hostname = get_clean_basedomain()
    has_ports = php_strstr(hostname, ":")
    if False != has_ports and (not php_in_array(has_ports, Array(":80", ":443"))):
        php_print("<div class=\"error\"><p><strong>" + __("Error:") + "</strong> " + __("You cannot install a network of sites with your server address.") + "</p></div>")
        php_print("<p>" + php_sprintf(__("You cannot use port numbers such as %s."), "<code>" + has_ports + "</code>") + "</p>")
        php_print("<a href=\"" + esc_url(admin_url()) + "\">" + __("Return to Dashboard") + "</a>")
        php_print("</div>")
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
        php_exit(0)
    # end if
    php_print("<form method=\"post\">")
    wp_nonce_field("install-network-1")
    error_codes = Array()
    if is_wp_error(errors):
        php_print("<div class=\"error\"><p><strong>" + __("Error: The network could not be created.") + "</strong></p>")
        for error in errors.get_error_messages():
            php_print(str("<p>") + str(error) + str("</p>"))
        # end for
        php_print("</div>")
        error_codes = errors.get_error_codes()
    # end if
    if (not php_empty(lambda : PHP_POST["sitename"])) and (not php_in_array("empty_sitename", error_codes)):
        site_name = PHP_POST["sitename"]
    else:
        #// translators: %s: Default network title.
        site_name = php_sprintf(__("%s Sites"), get_option("blogname"))
    # end if
    if (not php_empty(lambda : PHP_POST["email"])) and (not php_in_array("invalid_email", error_codes)):
        admin_email = PHP_POST["email"]
    else:
        admin_email = get_option("admin_email")
    # end if
    php_print(" <p>")
    _e("Welcome to the Network installation process!")
    php_print("</p>\n   <p>")
    _e("Fill in the information below and you&#8217;ll be on your way to creating a network of WordPress sites. We will create configuration files in the next step.")
    php_print("</p>\n   ")
    if (php_isset(lambda : PHP_POST["subdomain_install"])):
        subdomain_install = php_bool(PHP_POST["subdomain_install"])
    elif apache_mod_loaded("mod_rewrite"):
        #// Assume nothing.
        subdomain_install = True
    elif (not allow_subdirectory_install()):
        subdomain_install = True
    else:
        subdomain_install = False
        got_mod_rewrite = got_mod_rewrite()
        if got_mod_rewrite:
            #// Dangerous assumptions.
            php_print("<div class=\"updated inline\"><p><strong>" + __("Note:") + "</strong> ")
            printf(__("Please make sure the Apache %s module is installed as it will be used at the end of this installation."), "<code>mod_rewrite</code>")
            php_print("</p>")
        elif is_apache:
            php_print("<div class=\"error inline\"><p><strong>" + __("Warning:") + "</strong> ")
            printf(__("It looks like the Apache %s module is not installed."), "<code>mod_rewrite</code>")
            php_print("</p>")
        # end if
        if got_mod_rewrite or is_apache:
            #// Protect against mod_rewrite mimicry (but ! Apache).
            php_print("<p>")
            printf(__("If %1$s is disabled, ask your administrator to enable that module, or look at the <a href=\"%2$s\">Apache documentation</a> or <a href=\"%3$s\">elsewhere</a> for help setting it up."), "<code>mod_rewrite</code>", "https://httpd.apache.org/docs/mod/mod_rewrite.html", "https://www.google.com/search?q=apache+mod_rewrite")
            php_print("</p></div>")
        # end if
    # end if
    if allow_subdomain_install() and allow_subdirectory_install():
        php_print("     <h3>")
        esc_html_e("Addresses of Sites in your Network")
        php_print("</h3>\n      <p>")
        _e("Please choose whether you would like sites in your WordPress network to use sub-domains or sub-directories.")
        php_print("         <strong>")
        _e("You cannot change this later.")
        php_print("</strong></p>\n      <p>")
        _e("You will need a wildcard DNS record if you are going to use the virtual host (sub-domain) functionality.")
        php_print("</p>\n       ")
        pass
        php_print("     <table class=\"form-table\" role=\"presentation\">\n            <tr>\n              <th><label><input type=\"radio\" name=\"subdomain_install\" value=\"1\"")
        checked(subdomain_install)
        php_print(" /> ")
        _e("Sub-domains")
        php_print("</label></th>\n              <td>\n              ")
        printf(_x("like <code>site1.%1$s</code> and <code>site2.%1$s</code>", "subdomain examples"), hostname)
        php_print("""               </td>
        </tr>
        <tr>
        <th><label><input type=\"radio\" name=\"subdomain_install\" value=\"0\"""")
        checked((not subdomain_install))
        php_print(" /> ")
        _e("Sub-directories")
        php_print("</label></th>\n              <td>\n              ")
        printf(_x("like <code>%1$s/site1</code> and <code>%1$s/site2</code>", "subdirectory examples"), hostname)
        php_print("""               </td>
        </tr>
        </table>
        """)
    # end if
    if WP_CONTENT_DIR != ABSPATH + "wp-content" and allow_subdirectory_install() or (not allow_subdomain_install()):
        php_print("<div class=\"error inline\"><p><strong>" + __("Warning:") + "</strong> " + __("Subdirectory networks may not be fully compatible with custom wp-content directories.") + "</p></div>")
    # end if
    is_www = 0 == php_strpos(hostname, "www.")
    if is_www:
        php_print("     <h3>")
        esc_html_e("Server Address")
        php_print("</h3>\n      <p>\n       ")
        printf(__("We recommend you change your site domain to %1$s before enabling the network feature. It will still be possible to visit your site using the %3$s prefix with an address like %2$s but any links will not have the %3$s prefix."), "<code>" + php_substr(hostname, 4) + "</code>", "<code>" + hostname + "</code>", "<code>www</code>")
        php_print("""       </p>
        <table class=\"form-table\" role=\"presentation\">
        <tr>
        <th scope='row'>""")
        esc_html_e("Server Address")
        php_print("</th>\n          <td>\n              ")
        printf(__("The internet address of your network will be %s."), "<code>" + hostname + "</code>")
        php_print("""               </td>
        </tr>
        </table>
        """)
    # end if
    php_print("\n       <h3>")
    esc_html_e("Network Details")
    php_print("</h3>\n      <table class=\"form-table\" role=\"presentation\">\n        ")
    if "localhost" == hostname:
        php_print("         <tr>\n              <th scope=\"row\">")
        esc_html_e("Sub-directory Installation")
        php_print("</th>\n              <td>\n              ")
        printf(__("Because you are using %1$s, the sites in your WordPress network must use sub-directories. Consider using %2$s if you wish to use sub-domains."), "<code>localhost</code>", "<code>localhost.localdomain</code>")
        #// Uh oh:
        if (not allow_subdirectory_install()):
            php_print(" <strong>" + __("Warning:") + " " + __("The main site in a sub-directory installation will need to use a modified permalink structure, potentially breaking existing links.") + "</strong>")
        # end if
        php_print("             </td>\n         </tr>\n     ")
    elif (not allow_subdomain_install()):
        php_print("         <tr>\n              <th scope=\"row\">")
        esc_html_e("Sub-directory Installation")
        php_print("</th>\n              <td>\n              ")
        _e("Because your installation is in a directory, the sites in your WordPress network must use sub-directories.")
        #// Uh oh:
        if (not allow_subdirectory_install()):
            php_print(" <strong>" + __("Warning:") + " " + __("The main site in a sub-directory installation will need to use a modified permalink structure, potentially breaking existing links.") + "</strong>")
        # end if
        php_print("             </td>\n         </tr>\n     ")
    elif (not allow_subdirectory_install()):
        php_print("         <tr>\n              <th scope=\"row\">")
        esc_html_e("Sub-domain Installation")
        php_print("</th>\n              <td>\n              ")
        _e("Because your installation is not new, the sites in your WordPress network must use sub-domains.")
        php_print(" <strong>" + __("The main site in a sub-directory installation will need to use a modified permalink structure, potentially breaking existing links.") + "</strong>")
        php_print("             </td>\n         </tr>\n     ")
    # end if
    php_print("     ")
    if (not is_www):
        php_print("         <tr>\n              <th scope='row'>")
        esc_html_e("Server Address")
        php_print("</th>\n              <td>\n                  ")
        printf(__("The internet address of your network will be %s."), "<code>" + hostname + "</code>")
        php_print("             </td>\n         </tr>\n     ")
    # end if
    php_print("         <tr>\n              <th scope='row'><label for=\"sitename\">")
    esc_html_e("Network Title")
    php_print("</label></th>\n              <td>\n                  <input name='sitename' id='sitename' type='text' size='45' value='")
    php_print(esc_attr(site_name))
    php_print("' />\n                   <p class=\"description\">\n                     ")
    _e("What would you like to call your network?")
    php_print("""                   </p>
    </td>
    </tr>
    <tr>
    <th scope='row'><label for=\"email\">""")
    esc_html_e("Network Admin Email")
    php_print("</label></th>\n              <td>\n                  <input name='email' id='email' type='text' size='45' value='")
    php_print(esc_attr(admin_email))
    php_print("' />\n                   <p class=\"description\">\n                     ")
    _e("Your email address.")
    php_print("""                   </p>
    </td>
    </tr>
    </table>
    """)
    submit_button(__("Install"), "primary", "submit")
    php_print(" </form>\n   ")
# end def network_step1
#// 
#// Prints step 2 for Network installation process.
#// 
#// @since 3.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param WP_Error $errors
#//
def network_step2(errors=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    hostname = get_clean_basedomain()
    slashed_home = trailingslashit(get_option("home"))
    base = php_parse_url(slashed_home, PHP_URL_PATH)
    document_root_fix = php_str_replace("\\", "/", php_realpath(PHP_SERVER["DOCUMENT_ROOT"]))
    abspath_fix = php_str_replace("\\", "/", ABSPATH)
    home_path = document_root_fix + base if 0 == php_strpos(abspath_fix, document_root_fix) else get_home_path()
    wp_siteurl_subdir = php_preg_replace("#^" + preg_quote(home_path, "#") + "#", "", abspath_fix)
    rewrite_base = php_ltrim(trailingslashit(wp_siteurl_subdir), "/") if (not php_empty(lambda : wp_siteurl_subdir)) else ""
    location_of_wp_config = abspath_fix
    if (not php_file_exists(ABSPATH + "wp-config.php")) and php_file_exists(php_dirname(ABSPATH) + "/wp-config.php"):
        location_of_wp_config = php_dirname(abspath_fix)
    # end if
    location_of_wp_config = trailingslashit(location_of_wp_config)
    #// Wildcard DNS message.
    if is_wp_error(errors):
        php_print("<div class=\"error\">" + errors.get_error_message() + "</div>")
    # end if
    if PHP_POST:
        if allow_subdomain_install():
            subdomain_install = (not php_empty(lambda : PHP_POST["subdomain_install"])) if allow_subdirectory_install() else True
        else:
            subdomain_install = False
        # end if
    else:
        if is_multisite():
            subdomain_install = is_subdomain_install()
            php_print(" <p>")
            _e("The original configuration steps are shown here for reference.")
            php_print("</p>\n           ")
        else:
            subdomain_install = php_bool(wpdb.get_var(str("SELECT meta_value FROM ") + str(wpdb.sitemeta) + str(" WHERE site_id = 1 AND meta_key = 'subdomain_install'")))
            php_print(" <div class=\"error\"><p><strong>")
            _e("Warning:")
            php_print("</strong> ")
            _e("An existing WordPress network was detected.")
            php_print("</p></div>\n <p>")
            _e("Please complete the configuration steps. To create a new network, you will need to empty or remove the network database tables.")
            php_print("</p>\n           ")
        # end if
    # end if
    subdir_match = "" if subdomain_install else "([_0-9a-zA-Z-]+/)?"
    subdir_replacement_01 = "" if subdomain_install else "$1"
    subdir_replacement_12 = "$1" if subdomain_install else "$2"
    if PHP_POST or (not is_multisite()):
        php_print("     <h3>")
        esc_html_e("Enabling the Network")
        php_print("</h3>\n      <p>")
        _e("Complete the following steps to enable the features for creating a network of sites.")
        php_print("</p>\n       <div class=\"notice notice-warning inline\"><p>\n       ")
        if php_file_exists(home_path + ".htaccess"):
            php_print("<strong>" + __("Caution:") + "</strong> ")
            printf(__("We recommend you back up your existing %1$s and %2$s files."), "<code>wp-config.php</code>", "<code>.htaccess</code>")
        elif php_file_exists(home_path + "web.config"):
            php_print("<strong>" + __("Caution:") + "</strong> ")
            printf(__("We recommend you back up your existing %1$s and %2$s files."), "<code>wp-config.php</code>", "<code>web.config</code>")
        else:
            php_print("<strong>" + __("Caution:") + "</strong> ")
            printf(__("We recommend you back up your existing %s file."), "<code>wp-config.php</code>")
        # end if
        php_print("     </p></div>\n        ")
    # end if
    php_print(" <ol>\n      <li><p>\n       ")
    printf(__("Add the following to your %1$s file in %2$s <strong>above</strong> the line reading %3$s:"), "<code>wp-config.php</code>", "<code>" + location_of_wp_config + "</code>", "<code>/* " + __("That&#8217;s all, stop editing! Happy publishing.") + " */</code>")
    php_print("""       </p>
    <textarea class=\"code\" readonly=\"readonly\" cols=\"100\" rows=\"7\">
    define('MULTISITE', true);
    define('SUBDOMAIN_INSTALL', """)
    php_print("true" if subdomain_install else "false")
    php_print(");\ndefine('DOMAIN_CURRENT_SITE', '")
    php_print(hostname)
    php_print("');\ndefine('PATH_CURRENT_SITE', '")
    php_print(base)
    php_print("""');
    define('SITE_ID_CURRENT_SITE', 1);
    define('BLOG_ID_CURRENT_SITE', 1);
    </textarea>
    """)
    keys_salts = Array({"AUTH_KEY": "", "SECURE_AUTH_KEY": "", "LOGGED_IN_KEY": "", "NONCE_KEY": "", "AUTH_SALT": "", "SECURE_AUTH_SALT": "", "LOGGED_IN_SALT": "", "NONCE_SALT": ""})
    for c,v in keys_salts:
        if php_defined(c):
            keys_salts[c] = None
        # end if
    # end for
    if (not php_empty(lambda : keys_salts)):
        keys_salts_str = ""
        from_api = wp_remote_get("https://api.wordpress.org/secret-key/1.1/salt/")
        if is_wp_error(from_api):
            for c,v in keys_salts:
                keys_salts_str += str("\ndefine( '") + str(c) + str("', '") + wp_generate_password(64, True, True) + "' );"
            # end for
        else:
            from_api = php_explode("\n", wp_remote_retrieve_body(from_api))
            for c,v in keys_salts:
                keys_salts_str += str("\ndefine( '") + str(c) + str("', '") + php_substr(php_array_shift(from_api), 28, 64) + "' );"
            # end for
        # end if
        num_keys_salts = php_count(keys_salts)
        php_print("     <p>\n           ")
        if 1 == num_keys_salts:
            printf(__("This unique authentication key is also missing from your %s file."), "<code>wp-config.php</code>")
        else:
            printf(__("These unique authentication keys are also missing from your %s file."), "<code>wp-config.php</code>")
        # end if
        php_print("         ")
        _e("To make your installation more secure, you should also add:")
        php_print("     </p>\n      <textarea class=\"code\" readonly=\"readonly\" cols=\"100\" rows=\"")
        php_print(num_keys_salts)
        php_print("\">")
        php_print(esc_textarea(keys_salts_str))
        php_print("</textarea>\n            ")
    # end if
    php_print("     </li>\n ")
    if iis7_supports_permalinks():
        #// IIS doesn't support RewriteBase, all your RewriteBase are belong to us.
        iis_subdir_match = php_ltrim(base, "/") + subdir_match
        iis_rewrite_base = php_ltrim(base, "/") + rewrite_base
        iis_subdir_replacement = "" if subdomain_install else "{R:1}"
        web_config_file = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
        <configuration>
        <system.webServer>
        <rewrite>
        <rules>
        <rule name=\"WordPress Rule 1\" stopProcessing=\"true\">
        <match url=\"^index\\.php$\" ignoreCase=\"false\" />
        <action type=\"None\" />
        </rule>"""
        if is_multisite() and get_site_option("ms_files_rewriting"):
            web_config_file += "\n                <rule name=\"WordPress Rule for Files\" stopProcessing=\"true\">\n                    <match url=\"^" + iis_subdir_match + "files/(.+)\" ignoreCase=\"false\" />\n                    <action type=\"Rewrite\" url=\"" + iis_rewrite_base + WPINC + "/ms-files.php?file={R:1}\" appendQueryString=\"false\" />\n                </rule>"
        # end if
        web_config_file += "\n                <rule name=\"WordPress Rule 2\" stopProcessing=\"true\">\n                    <match url=\"^" + iis_subdir_match + "wp-admin$\" ignoreCase=\"false\" />\n                    <action type=\"Redirect\" url=\"" + iis_subdir_replacement + """wp-admin/\" redirectType=\"Permanent\" />
        </rule>
        <rule name=\"WordPress Rule 3\" stopProcessing=\"true\">
        <match url=\"^\" ignoreCase=\"false\" />
        <conditions logicalGrouping=\"MatchAny\">
        <add input=\"{REQUEST_FILENAME}\" matchType=\"IsFile\" ignoreCase=\"false\" />
        <add input=\"{REQUEST_FILENAME}\" matchType=\"IsDirectory\" ignoreCase=\"false\" />
        </conditions>
        <action type=\"None\" />
        </rule>
        <rule name=\"WordPress Rule 4\" stopProcessing=\"true\">
        <match url=\"^""" + iis_subdir_match + "(wp-(content|admin|includes).*)\" ignoreCase=\"false\" />\n                    <action type=\"Rewrite\" url=\"" + iis_rewrite_base + """{R:1}\" />
        </rule>
        <rule name=\"WordPress Rule 5\" stopProcessing=\"true\">
        <match url=\"^""" + iis_subdir_match + "([_0-9a-zA-Z-]+/)?(.*\\.php)$\" ignoreCase=\"false\" />\n                    <action type=\"Rewrite\" url=\"" + iis_rewrite_base + """{R:2}\" />
        </rule>
        <rule name=\"WordPress Rule 6\" stopProcessing=\"true\">
        <match url=\".\" ignoreCase=\"false\" />
        <action type=\"Rewrite\" url=\"index.php\" />
        </rule>
        </rules>
        </rewrite>
        </system.webServer>
        </configuration>
        """
        php_print("<li><p>")
        printf(__("Add the following to your %1$s file in %2$s, <strong>replacing</strong> other WordPress rules:"), "<code>web.config</code>", "<code>" + home_path + "</code>")
        php_print("</p>")
        if (not subdomain_install) and WP_CONTENT_DIR != ABSPATH + "wp-content":
            php_print("<p><strong>" + __("Warning:") + " " + __("Subdirectory networks may not be fully compatible with custom wp-content directories.") + "</strong></p>")
        # end if
        php_print("     <textarea class=\"code\" readonly=\"readonly\" cols=\"100\" rows=\"20\">")
        php_print(esc_textarea(web_config_file))
        php_print("""</textarea>
        </li>
        </ol>
        """)
    else:
        #// End iis7_supports_permalinks(). Construct an .htaccess file instead:
        ms_files_rewriting = ""
        if is_multisite() and get_site_option("ms_files_rewriting"):
            ms_files_rewriting = "\n# uploaded files\nRewriteRule ^"
            ms_files_rewriting += subdir_match + str("files/(.+) ") + str(rewrite_base) + WPINC + str("/ms-files.php?file=") + str(subdir_replacement_12) + str(" [L]") + "\n"
        # end if
        htaccess_file = str("RewriteEngine On\nRewriteBase ") + str(base) + str("\nRewriteRule ^index\\.php$ - [L]\n") + str(ms_files_rewriting) + str("\n# add a trailing slash to /wp-admin\nRewriteRule ^") + str(subdir_match) + str("wp-admin$ ") + str(subdir_replacement_01) + str("""wp-admin/ [R=301,L]\n\nRewriteCond %{REQUEST_FILENAME} -f [OR]\nRewriteCond %{REQUEST_FILENAME} -d\nRewriteRule ^ - [L]\nRewriteRule ^""") + str(subdir_match) + str("(wp-(content|admin|includes).*) ") + str(rewrite_base) + str(subdir_replacement_12) + str(" [L]\nRewriteRule ^") + str(subdir_match) + str("(.*\\.php)$ ") + str(rewrite_base) + str(subdir_replacement_12) + str(" [L]\nRewriteRule . index.php [L]\n")
        php_print("<li><p>")
        printf(__("Add the following to your %1$s file in %2$s, <strong>replacing</strong> other WordPress rules:"), "<code>.htaccess</code>", "<code>" + home_path + "</code>")
        php_print("</p>")
        if (not subdomain_install) and WP_CONTENT_DIR != ABSPATH + "wp-content":
            php_print("<p><strong>" + __("Warning:") + " " + __("Subdirectory networks may not be fully compatible with custom wp-content directories.") + "</strong></p>")
        # end if
        php_print("     <textarea class=\"code\" readonly=\"readonly\" cols=\"100\" rows=\"")
        php_print(php_substr_count(htaccess_file, "\n") + 1)
        php_print("\">")
        php_print(esc_textarea(htaccess_file))
        php_print("""</textarea>
        </li>
        </ol>
        """)
    # end if
    #// End IIS/Apache code branches.
    if (not is_multisite()):
        php_print("     <p>")
        _e("Once you complete these steps, your network is enabled and configured. You will have to log in again.")
        php_print(" <a href=\"")
        php_print(esc_url(wp_login_url()))
        php_print("\">")
        _e("Log In")
        php_print("</a></p>\n       ")
    # end if
# end def network_step2
