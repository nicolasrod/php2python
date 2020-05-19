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
#// Link Management Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_links")):
    wp_die(__("Sorry, you are not allowed to edit the links for this site."))
# end if
wp_list_table_ = _get_list_table("WP_Links_List_Table")
#// Handle bulk deletes.
doaction_ = wp_list_table_.current_action()
if doaction_ and (php_isset(lambda : PHP_REQUEST["linkcheck"])):
    check_admin_referer("bulk-bookmarks")
    redirect_to_ = admin_url("link-manager.php")
    bulklinks_ = PHP_REQUEST["linkcheck"]
    if "delete" == doaction_:
        for link_id_ in bulklinks_:
            link_id_ = php_int(link_id_)
            wp_delete_link(link_id_)
        # end for
        redirect_to_ = add_query_arg("deleted", php_count(bulklinks_), redirect_to_)
    else:
        screen_ = get_current_screen().id
        #// This action is documented in wp-admin/edit.php
        redirect_to_ = apply_filters(str("handle_bulk_actions-") + str(screen_), redirect_to_, doaction_, bulklinks_)
        pass
    # end if
    wp_redirect(redirect_to_)
    php_exit(0)
elif (not php_empty(lambda : PHP_REQUEST["_wp_http_referer"])):
    wp_redirect(remove_query_arg(Array("_wp_http_referer", "_wpnonce"), wp_unslash(PHP_SERVER["REQUEST_URI"])))
    php_exit(0)
# end if
wp_list_table_.prepare_items()
title_ = __("Links")
this_file_ = "link-manager.php"
parent_file_ = this_file_
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + php_sprintf(__("You can add links here to be displayed on your site, usually using <a href=\"%s\">Widgets</a>. By default, links to several sites in the WordPress community are included as examples."), "widgets.php") + "</p>" + "<p>" + __("Links may be separated into Link Categories; these are different than the categories used on your posts.") + "</p>" + "<p>" + __("You can customize the display of this screen using the Screen Options tab and/or the dropdown filters above the links table.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "deleting-links", "title": __("Deleting Links"), "content": "<p>" + __("If you delete a link, it will be removed permanently, as Links do not have a Trash function yet.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Links_Screen\">Documentation on Managing Links</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_list": __("Links list")}))
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
if (not current_user_can("manage_links")):
    wp_die(__("Sorry, you are not allowed to edit the links for this site."))
# end if
php_print("""
<div class=\"wrap nosubsub\">
<h1 class=\"wp-heading-inline\">
""")
php_print(esc_html(title_))
php_print("</h1>\n\n<a href=\"link-add.php\" class=\"page-title-action\">")
php_print(esc_html_x("Add New", "link"))
php_print("</a>\n\n")
if (php_isset(lambda : PHP_REQUEST["s"])) and php_strlen(PHP_REQUEST["s"]):
    #// translators: %s: Search query.
    php_printf("<span class=\"subtitle\">" + __("Search results for &#8220;%s&#8221;") + "</span>", esc_html(wp_unslash(PHP_REQUEST["s"])))
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
if (php_isset(lambda : PHP_REQUEST["deleted"])):
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    deleted_ = php_int(PHP_REQUEST["deleted"])
    #// translators: %s: Number of links.
    php_printf(_n("%s link deleted.", "%s links deleted.", deleted_), deleted_)
    php_print("</p></div>")
    PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("deleted"), PHP_SERVER["REQUEST_URI"])
# end if
php_print("""
<form id=\"posts-filter\" method=\"get\">
""")
wp_list_table_.search_box(__("Search Links"), "link")
php_print("\n")
wp_list_table_.display()
php_print("""
<div id=\"ajax-response\"></div>
</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
