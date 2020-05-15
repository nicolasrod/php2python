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
#// Manage link administration actions.
#// 
#// This page is accessed by the link management pages and handles the forms and
#// Ajax processes for link actions.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
wp_reset_vars(Array("action", "cat_id", "link_id"))
if (not current_user_can("manage_links")):
    wp_link_manager_disabled_message()
# end if
if (not php_empty(lambda : PHP_POST["deletebookmarks"])):
    action = "deletebookmarks"
# end if
if (not php_empty(lambda : PHP_POST["move"])):
    action = "move"
# end if
if (not php_empty(lambda : PHP_POST["linkcheck"])):
    linkcheck = PHP_POST["linkcheck"]
# end if
this_file = admin_url("link-manager.php")
for case in Switch(action):
    if case("deletebookmarks"):
        check_admin_referer("bulk-bookmarks")
        #// For each link id (in $linkcheck[]) change category to selected value.
        if php_count(linkcheck) == 0:
            wp_redirect(this_file)
            php_exit(0)
        # end if
        deleted = 0
        for link_id in linkcheck:
            link_id = int(link_id)
            if wp_delete_link(link_id):
                deleted += 1
            # end if
        # end for
        wp_redirect(str(this_file) + str("?deleted=") + str(deleted))
        php_exit(0)
    # end if
    if case("move"):
        check_admin_referer("bulk-bookmarks")
        #// For each link id (in $linkcheck[]) change category to selected value.
        if php_count(linkcheck) == 0:
            wp_redirect(this_file)
            php_exit(0)
        # end if
        all_links = join(",", linkcheck)
        #// 
        #// Should now have an array of links we can change:
        #// $q = $wpdb->query("update $wpdb->links SET link_category='$category' WHERE link_id IN ($all_links)");
        #//
        wp_redirect(this_file)
        php_exit(0)
    # end if
    if case("add"):
        check_admin_referer("add-bookmark")
        redir = wp_get_referer()
        if add_link():
            redir = add_query_arg("added", "true", redir)
        # end if
        wp_redirect(redir)
        php_exit(0)
    # end if
    if case("save"):
        link_id = int(PHP_POST["link_id"])
        check_admin_referer("update-bookmark_" + link_id)
        edit_link(link_id)
        wp_redirect(this_file)
        php_exit(0)
    # end if
    if case("delete"):
        link_id = int(PHP_REQUEST["link_id"])
        check_admin_referer("delete-bookmark_" + link_id)
        wp_delete_link(link_id)
        wp_redirect(this_file)
        php_exit(0)
    # end if
    if case("edit"):
        wp_enqueue_script("link")
        wp_enqueue_script("xfn")
        if wp_is_mobile():
            wp_enqueue_script("jquery-touch-punch")
        # end if
        parent_file = "link-manager.php"
        submenu_file = "link-manager.php"
        title = __("Edit Link")
        link_id = int(PHP_REQUEST["link_id"])
        link = get_link_to_edit(link_id)
        if (not link):
            wp_die(__("Link not found."))
        # end if
        php_include_file(ABSPATH + "wp-admin/edit-link-form.php", once=False)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
        break
    # end if
    if case():
        break
    # end if
# end for
