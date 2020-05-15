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
#// Edit Term Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.5.0
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if php_empty(lambda : PHP_REQUEST["tag_ID"]):
    sendback = admin_url("edit-tags.php")
    if (not php_empty(lambda : taxnow)):
        sendback = add_query_arg(Array({"taxonomy": taxnow}), sendback)
    # end if
    if "post" != get_current_screen().post_type:
        sendback = add_query_arg("post_type", get_current_screen().post_type, sendback)
    # end if
    wp_redirect(esc_url_raw(sendback))
    php_exit(0)
# end if
tag_ID = absint(PHP_REQUEST["tag_ID"])
tag = get_term(tag_ID, taxnow, OBJECT, "edit")
if (not type(tag).__name__ == "WP_Term"):
    wp_die(__("You attempted to edit an item that doesn&#8217;t exist. Perhaps it was deleted?"))
# end if
tax = get_taxonomy(tag.taxonomy)
taxonomy = tax.name
title = tax.labels.edit_item
if (not php_in_array(taxonomy, get_taxonomies(Array({"show_ui": True})))) or (not current_user_can("edit_term", tag.term_id)):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to edit this item.") + "</p>", 403)
# end if
post_type = get_current_screen().post_type
#// Default to the first object_type associated with the taxonomy if no post type was passed.
if php_empty(lambda : post_type):
    post_type = reset(tax.object_type)
# end if
if "post" != post_type:
    parent_file = "upload.php" if "attachment" == post_type else str("edit.php?post_type=") + str(post_type)
    submenu_file = str("edit-tags.php?taxonomy=") + str(taxonomy) + str("&amp;post_type=") + str(post_type)
elif "link_category" == taxonomy:
    parent_file = "link-manager.php"
    submenu_file = "edit-tags.php?taxonomy=link_category"
else:
    parent_file = "edit.php"
    submenu_file = str("edit-tags.php?taxonomy=") + str(taxonomy)
# end if
get_current_screen().set_screen_reader_content(Array({"heading_pagination": tax.labels.items_list_navigation, "heading_list": tax.labels.items_list}))
wp_enqueue_script("admin-tags")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_include_file(ABSPATH + "wp-admin/edit-tag-form.php", once=False)
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
