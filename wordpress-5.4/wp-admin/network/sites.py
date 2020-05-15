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
#// Multisite sites administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_sites")):
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
wp_list_table = _get_list_table("WP_MS_Sites_List_Table")
pagenum = wp_list_table.get_pagenum()
title = __("Sites")
parent_file = "sites.php"
add_screen_option("per_page")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("Add New takes you to the Add New Site screen. You can search for a site by Name, ID number, or IP address. Screen Options allows you to choose how many sites to display on one page.") + "</p>" + "<p>" + __("This is the main table of all sites on this network. Switch between list and excerpt views by using the icons above the right side of the table.") + "</p>" + "<p>" + __("Hovering over each site reveals seven options (three for the primary site):") + "</p>" + "<ul><li>" + __("An Edit link to a separate Edit Site screen.") + "</li>" + "<li>" + __("Dashboard leads to the Dashboard for that site.") + "</li>" + "<li>" + __("Deactivate, Archive, and Spam which lead to confirmation screens. These actions can be reversed later.") + "</li>" + "<li>" + __("Delete which is a permanent action after the confirmation screens.") + "</li>" + "<li>" + __("Visit to go to the front-end site live.") + "</li></ul>" + "<p>" + __("The site ID is used internally, and is not shown on the front end of the site or to users/viewers.") + "</p>" + "<p>" + __("Clicking on bold headings can re-sort this table.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/network-admin-sites-screen/\">Documentation on Site Management</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/forum/multisite/\">Support Forums</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_pagination": __("Sites list navigation"), "heading_list": __("Sites list")}))
id = php_intval(PHP_REQUEST["id"]) if (php_isset(lambda : PHP_REQUEST["id"])) else 0
if (php_isset(lambda : PHP_REQUEST["action"])):
    #// This action is documented in wp-admin/network/edit.php
    do_action("wpmuadminedit")
    #// A list of valid actions and their associated messaging for confirmation output.
    manage_actions = Array({"activateblog": __("You are about to activate the site %s."), "deactivateblog": __("You are about to deactivate the site %s."), "unarchiveblog": __("You are about to unarchive the site %s."), "archiveblog": __("You are about to archive the site %s."), "unspamblog": __("You are about to unspam the site %s."), "spamblog": __("You are about to mark the site %s as spam."), "deleteblog": __("You are about to delete the site %s."), "unmatureblog": __("You are about to mark the site %s as mature."), "matureblog": __("You are about to mark the site %s as not mature.")})
    if "confirm" == PHP_REQUEST["action"]:
        #// The action2 parameter contains the action being taken on the site.
        site_action = PHP_REQUEST["action2"]
        if (not php_array_key_exists(site_action, manage_actions)):
            wp_die(__("The requested action is not valid."))
        # end if
        #// The mature/unmature UI exists only as external code. Check the "confirm" nonce for backward compatibility.
        if "matureblog" == site_action or "unmatureblog" == site_action:
            check_admin_referer("confirm")
        else:
            check_admin_referer(site_action + "_" + id)
        # end if
        if (not php_headers_sent()):
            nocache_headers()
            php_header("Content-Type: text/html; charset=utf-8")
        # end if
        if get_network().site_id == id:
            wp_die(__("Sorry, you are not allowed to change the current site."))
        # end if
        site_details = get_site(id)
        site_address = untrailingslashit(site_details.domain + site_details.path)
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        php_print("         <div class=\"wrap\">\n              <h1>")
        _e("Confirm your action")
        php_print("</h1>\n              <form action=\"sites.php?action=")
        php_print(esc_attr(site_action))
        php_print("\" method=\"post\">\n                    <input type=\"hidden\" name=\"action\" value=\"")
        php_print(esc_attr(site_action))
        php_print("\" />\n                  <input type=\"hidden\" name=\"id\" value=\"")
        php_print(esc_attr(id))
        php_print("\" />\n                  <input type=\"hidden\" name=\"_wp_http_referer\" value=\"")
        php_print(esc_attr(wp_get_referer()))
        php_print("\" />\n                  ")
        wp_nonce_field(site_action + "_" + id, "_wpnonce", False)
        php_print("                 <p>")
        php_print(php_sprintf(manage_actions[site_action], site_address))
        php_print("</p>\n                   ")
        submit_button(__("Confirm"), "primary")
        php_print("             </form>\n           </div>\n        ")
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
        php_exit(0)
    elif php_array_key_exists(PHP_REQUEST["action"], manage_actions):
        action = PHP_REQUEST["action"]
        check_admin_referer(action + "_" + id)
    elif "allblogs" == PHP_REQUEST["action"]:
        check_admin_referer("bulk-sites")
    # end if
    updated_action = ""
    for case in Switch(PHP_REQUEST["action"]):
        if case("deleteblog"):
            if (not current_user_can("delete_sites")):
                wp_die(__("Sorry, you are not allowed to access this page."), "", Array({"response": 403}))
            # end if
            updated_action = "not_deleted"
            if "0" != id and get_network().site_id != id and current_user_can("delete_site", id):
                wpmu_delete_blog(id, True)
                updated_action = "delete"
            # end if
            break
        # end if
        if case("delete_sites"):
            check_admin_referer("ms-delete-sites")
            for site_id in PHP_POST["site_ids"]:
                site_id = int(site_id)
                if get_network().site_id == site_id:
                    continue
                # end if
                if (not current_user_can("delete_site", site_id)):
                    site = get_site(site_id)
                    site_address = untrailingslashit(site.domain + site.path)
                    wp_die(php_sprintf(__("Sorry, you are not allowed to delete the site %s."), site_address), 403)
                # end if
                updated_action = "all_delete"
                wpmu_delete_blog(site_id, True)
            # end for
            break
        # end if
        if case("allblogs"):
            if (php_isset(lambda : PHP_POST["action"])) or (php_isset(lambda : PHP_POST["action2"])) and (php_isset(lambda : PHP_POST["allblogs"])):
                doaction = PHP_POST["action"] if -1 != PHP_POST["action"] else PHP_POST["action2"]
                for key,val in PHP_POST["allblogs"]:
                    if "0" != val and get_network().site_id != val:
                        for case in Switch(doaction):
                            if case("delete"):
                                php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
                                php_print("                             <div class=\"wrap\">\n                                  <h1>")
                                _e("Confirm your action")
                                php_print("""</h1>
                                <form action=\"sites.php?action=delete_sites\" method=\"post\">
                                <input type=\"hidden\" name=\"action\" value=\"delete_sites\" />
                                <input type=\"hidden\" name=\"_wp_http_referer\" value=\"""")
                                php_print(esc_attr(wp_get_referer()))
                                php_print("\" />\n                                      ")
                                wp_nonce_field("ms-delete-sites", "_wpnonce", False)
                                php_print("                                     <p>")
                                _e("You are about to delete the following sites:")
                                php_print("</p>\n                                       <ul class=\"ul-disc\">\n                                            ")
                                for site_id in PHP_POST["allblogs"]:
                                    site = get_site(site_id)
                                    site_address = untrailingslashit(site.domain + site.path)
                                    php_print("                                             <li>\n                                                  ")
                                    php_print(site_address)
                                    php_print("                                                 <input type=\"hidden\" name=\"site_ids[]\" value=\"")
                                    php_print(int(site_id))
                                    php_print("\" />\n                                              </li>\n                                         ")
                                # end for
                                php_print("                                     </ul>\n                                     ")
                                submit_button(__("Confirm"), "primary")
                                php_print("                                 </form>\n                               </div>\n                                ")
                                php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
                                php_exit(0)
                                break
                            # end if
                            if case("spam"):
                                pass
                            # end if
                            if case("notspam"):
                                updated_action = "all_spam" if "spam" == doaction else "all_notspam"
                                update_blog_status(val, "spam", "1" if "spam" == doaction else "0")
                                break
                            # end if
                        # end for
                    else:
                        wp_die(__("Sorry, you are not allowed to change the current site."))
                    # end if
                # end for
                if (not php_in_array(doaction, Array("delete", "spam", "notspam"), True)):
                    redirect_to = wp_get_referer()
                    blogs = PHP_POST["allblogs"]
                    #// This action is documented in wp-admin/network/site-themes.php
                    redirect_to = apply_filters("handle_network_bulk_actions-" + get_current_screen().id, redirect_to, doaction, blogs, id)
                    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
                    wp_safe_redirect(redirect_to)
                    php_exit(0)
                # end if
            else:
                #// Process query defined by WP_MS_Site_List_Table::extra_table_nav().
                location = remove_query_arg(Array("_wp_http_referer", "_wpnonce"), add_query_arg(PHP_POST, network_admin_url("sites.php")))
                wp_redirect(location)
                php_exit(0)
            # end if
            break
        # end if
        if case("archiveblog"):
            pass
        # end if
        if case("unarchiveblog"):
            update_blog_status(id, "archived", "1" if "archiveblog" == PHP_REQUEST["action"] else "0")
            break
        # end if
        if case("activateblog"):
            update_blog_status(id, "deleted", "0")
            #// 
            #// Fires after a network site is activated.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param string $id The ID of the activated site.
            #//
            do_action("activate_blog", id)
            break
        # end if
        if case("deactivateblog"):
            #// 
            #// Fires before a network site is deactivated.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param string $id The ID of the site being deactivated.
            #//
            do_action("deactivate_blog", id)
            update_blog_status(id, "deleted", "1")
            break
        # end if
        if case("unspamblog"):
            pass
        # end if
        if case("spamblog"):
            update_blog_status(id, "spam", "1" if "spamblog" == PHP_REQUEST["action"] else "0")
            break
        # end if
        if case("unmatureblog"):
            pass
        # end if
        if case("matureblog"):
            update_blog_status(id, "mature", "1" if "matureblog" == PHP_REQUEST["action"] else "0")
            break
        # end if
    # end for
    if php_empty(lambda : updated_action) and php_array_key_exists(PHP_REQUEST["action"], manage_actions):
        updated_action = PHP_REQUEST["action"]
    # end if
    if (not php_empty(lambda : updated_action)):
        wp_safe_redirect(add_query_arg(Array({"updated": updated_action}), wp_get_referer()))
        php_exit(0)
    # end if
# end if
msg = ""
if (php_isset(lambda : PHP_REQUEST["updated"])):
    action = PHP_REQUEST["updated"]
    for case in Switch(action):
        if case("all_notspam"):
            msg = __("Sites removed from spam.")
            break
        # end if
        if case("all_spam"):
            msg = __("Sites marked as spam.")
            break
        # end if
        if case("all_delete"):
            msg = __("Sites deleted.")
            break
        # end if
        if case("delete"):
            msg = __("Site deleted.")
            break
        # end if
        if case("not_deleted"):
            msg = __("Sorry, you are not allowed to delete that site.")
            break
        # end if
        if case("archiveblog"):
            msg = __("Site archived.")
            break
        # end if
        if case("unarchiveblog"):
            msg = __("Site unarchived.")
            break
        # end if
        if case("activateblog"):
            msg = __("Site activated.")
            break
        # end if
        if case("deactivateblog"):
            msg = __("Site deactivated.")
            break
        # end if
        if case("unspamblog"):
            msg = __("Site removed from spam.")
            break
        # end if
        if case("spamblog"):
            msg = __("Site marked as spam.")
            break
        # end if
        if case():
            #// 
            #// Filters a specific, non-default, site-updated message in the Network admin.
            #// 
            #// The dynamic portion of the hook name, `$action`, refers to the non-default
            #// site update action.
            #// 
            #// @since 3.1.0
            #// 
            #// @param string $msg The update message. Default 'Settings saved'.
            #//
            msg = apply_filters(str("network_sites_updated_message_") + str(action), __("Settings saved."))
            break
        # end if
    # end for
    if (not php_empty(lambda : msg)):
        msg = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg + "</p></div>"
    # end if
# end if
wp_list_table.prepare_items()
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1 class=\"wp-heading-inline\">")
_e("Sites")
php_print("</h1>\n\n")
if current_user_can("create_sites"):
    php_print(" <a href=\"")
    php_print(network_admin_url("site-new.php"))
    php_print("\" class=\"page-title-action\">")
    php_print(esc_html_x("Add New", "site"))
    php_print("</a>\n")
# end if
php_print("\n")
if (php_isset(lambda : PHP_REQUEST["s"])) and php_strlen(PHP_REQUEST["s"]):
    #// translators: %s: Search query.
    printf("<span class=\"subtitle\">" + __("Search results for &#8220;%s&#8221;") + "</span>", esc_html(s))
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
wp_list_table.views()
php_print("\n")
php_print(msg)
php_print("\n<form method=\"get\" id=\"ms-search\" class=\"wp-clearfix\">\n")
wp_list_table.search_box(__("Search Sites"), "site")
php_print("""<input type=\"hidden\" name=\"action\" value=\"blogs\" />
</form>
<form id=\"form-site-list\" action=\"sites.php?action=allblogs\" method=\"post\">
""")
wp_list_table.display()
php_print("</form>\n</div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
