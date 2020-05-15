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
#// Multisite upgrade administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
php_include_file(ABSPATH + WPINC + "/http.php", once=True)
title = __("Upgrade Network")
parent_file = "upgrade.php"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("Only use this screen once you have updated to a new version of WordPress through Updates/Available Updates (via the Network Administration navigation menu or the Toolbar). Clicking the Upgrade Network button will step through each site in the network, five at a time, and make sure any database updates are applied.") + "</p>" + "<p>" + __("If a version update to core has not happened, clicking this button won&#8217;t affect anything.") + "</p>" + "<p>" + __("If this process fails for any reason, users logging in to their sites will force the same update.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/network-admin-updates-screen/\">Documentation on Upgrade Network</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
if (not current_user_can("upgrade_network")):
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
php_print("<div class=\"wrap\">")
php_print("<h1>" + __("Upgrade Network") + "</h1>")
action = PHP_REQUEST["action"] if (php_isset(lambda : PHP_REQUEST["action"])) else "show"
for case in Switch(action):
    if case("upgrade"):
        n = php_intval(PHP_REQUEST["n"]) if (php_isset(lambda : PHP_REQUEST["n"])) else 0
        if n < 5:
            #// 
            #// @global int $wp_db_version WordPress database version.
            #//
            global wp_db_version
            php_check_if_defined("wp_db_version")
            update_site_option("wpmu_upgrade_site", wp_db_version)
        # end if
        site_ids = get_sites(Array({"spam": 0, "deleted": 0, "archived": 0, "network_id": get_current_network_id(), "number": 5, "offset": n, "fields": "ids", "order": "DESC", "orderby": "id", "update_site_meta_cache": False}))
        if php_empty(lambda : site_ids):
            php_print("<p>" + __("All done!") + "</p>")
            break
        # end if
        php_print("<ul>")
        for site_id in site_ids:
            switch_to_blog(site_id)
            siteurl = site_url()
            upgrade_url = admin_url("upgrade.php?step=upgrade_db")
            restore_current_blog()
            php_print(str("<li>") + str(siteurl) + str("</li>"))
            response = wp_remote_get(upgrade_url, Array({"timeout": 120, "httpversion": "1.1", "sslverify": False}))
            if is_wp_error(response):
                wp_die(php_sprintf(__("Warning! Problem updating %1$s. Your server may not be able to connect to sites running on it. Error message: %2$s"), siteurl, "<em>" + response.get_error_message() + "</em>"))
            # end if
            #// 
            #// Fires after the Multisite DB upgrade for each site is complete.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param array|WP_Error $response The upgrade response array or WP_Error on failure.
            #//
            do_action("after_mu_upgrade", response)
            #// 
            #// Fires after each site has been upgraded.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id The Site ID.
            #//
            do_action("wpmu_upgrade_site", site_id)
        # end for
        php_print("</ul>")
        php_print("<p>")
        _e("If your browser doesn&#8217;t start loading the next page automatically, click this link:")
        php_print(" <a class=\"button\" href=\"upgrade.php?action=upgrade&amp;n=")
        php_print(n + 5)
        php_print("\">")
        _e("Next Sites")
        php_print("""</a></p>
        <script type=\"text/javascript\">
        <!--
        function nextpage() {
        location.href = \"upgrade.php?action=upgrade&n=""")
        php_print(n + 5)
        php_print("""\";
        }
        setTimeout( \"nextpage()\", 250 );
        //-->
        </script>
        """)
        break
    # end if
    if case("show"):
        pass
    # end if
    if case():
        if get_site_option("wpmu_upgrade_site") != PHP_GLOBALS["wp_db_version"]:
            php_print("     <h2>")
            _e("Database Update Required")
            php_print("</h2>\n      <p>")
            _e("WordPress has been updated! Before we send you on your way, we need to individually upgrade the sites in your network.")
            php_print("</p>\n       ")
        # end if
        php_print("\n       <p>")
        _e("The database update process may take a little while, so please be patient.")
        php_print("</p>\n       <p><a class=\"button button-primary\" href=\"upgrade.php?action=upgrade\">")
        _e("Upgrade Network")
        php_print("</a></p>\n       ")
        #// 
        #// Fires before the footer on the network upgrade screen.
        #// 
        #// @since MU (3.0.0)
        #//
        do_action("wpmu_upgrade_page")
        break
    # end if
# end for
php_print("</div>\n\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
