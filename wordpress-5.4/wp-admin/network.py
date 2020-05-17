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
#// Network installation administration panel.
#// 
#// A multi-step process allowing the user to enable a network of WordPress sites.
#// 
#// @since 3.0.0
#// 
#// @package WordPress
#// @subpackage Administration
#//
php_define("WP_INSTALLING_NETWORK", True)
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("setup_network")):
    wp_die(__("Sorry, you are not allowed to manage options for this site."))
# end if
if is_multisite():
    if (not is_network_admin()):
        wp_redirect(network_admin_url("setup.php"))
        php_exit(0)
    # end if
    if (not php_defined("MULTISITE")):
        wp_die(__("The Network creation panel is not for WordPress MU networks."))
    # end if
# end if
php_include_file(__DIR__ + "/includes/network.php", once=True)
#// We need to create references to ms global tables to enable Network.
for table_,prefixed_table_ in wpdb_.tables("ms_global"):
    wpdb_.table_ = prefixed_table_
# end for
if (not network_domain_check()) and (not php_defined("WP_ALLOW_MULTISITE")) or (not WP_ALLOW_MULTISITE):
    wp_die(printf(__("You must define the %1$s constant as true in your %2$s file to allow creation of a Network."), "<code>WP_ALLOW_MULTISITE</code>", "<code>wp-config.php</code>"))
# end if
if is_network_admin():
    title_ = __("Network Setup")
    parent_file_ = "settings.php"
else:
    title_ = __("Create a Network of WordPress Sites")
    parent_file_ = "tools.php"
# end if
network_help_ = "<p>" + __("This screen allows you to configure a network as having subdomains (<code>site1.example.com</code>) or subdirectories (<code>example.com/site1</code>). Subdomains require wildcard subdomains to be enabled in Apache and DNS records, if your host allows it.") + "</p>" + "<p>" + __("Choose subdomains or subdirectories; this can only be switched afterwards by reconfiguring your installation. Fill out the network details, and click Install. If this does not work, you may have to add a wildcard DNS record (for subdomains) or change to another setting in Permalinks (for subdirectories).") + "</p>" + "<p>" + __("The next screen for Network Setup will give you individually-generated lines of code to add to your wp-config.php and .htaccess files. Make sure the settings of your FTP client make files starting with a dot visible, so that you can find .htaccess; you may have to create this file if it really is not there. Make backup copies of those two files.") + "</p>" + "<p>" + __("Add the designated lines of code to wp-config.php (just before <code>/*...stop editing...*/</code>) and <code>.htaccess</code> (replacing the existing WordPress rules).") + "</p>" + "<p>" + __("Once you add this code and refresh your browser, multisite should be enabled. This screen, now in the Network Admin navigation menu, will keep an archive of the added code. You can toggle between Network Admin and Site Admin by clicking on the Network Admin or an individual site name under the My Sites dropdown in the Toolbar.") + "</p>" + "<p>" + __("The choice of subdirectory sites is disabled if this setup is more than a month old because of permalink problems with &#8220;/blog/&#8221; from the main site. This disabling will be addressed in a future version.") + "</p>" + "<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/create-a-network/\">Documentation on Creating a Network</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/tools-network-screen/\">Documentation on the Network Screen</a>") + "</p>"
get_current_screen().add_help_tab(Array({"id": "network", "title": __("Network"), "content": network_help_}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/create-a-network/\">Documentation on Creating a Network</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/tools-network-screen/\">Documentation on the Network Screen</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n<h1>")
php_print(esc_html(title_))
php_print("</h1>\n\n")
if PHP_POST:
    check_admin_referer("install-network-1")
    php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
    #// Create network tables.
    install_network()
    base_ = php_parse_url(trailingslashit(get_option("home")), PHP_URL_PATH)
    subdomain_install_ = (not php_empty(lambda : PHP_POST["subdomain_install"])) if allow_subdomain_install() else False
    if (not network_domain_check()):
        result_ = populate_network(1, get_clean_basedomain(), sanitize_email(PHP_POST["email"]), wp_unslash(PHP_POST["sitename"]), base_, subdomain_install_)
        if is_wp_error(result_):
            if 1 == php_count(result_.get_error_codes()) and "no_wildcard_dns" == result_.get_error_code():
                network_step2(result_)
            else:
                network_step1(result_)
            # end if
        else:
            network_step2()
        # end if
    else:
        network_step2()
    # end if
elif is_multisite() or network_domain_check():
    network_step2()
else:
    network_step1()
# end if
php_print("</div>\n\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
