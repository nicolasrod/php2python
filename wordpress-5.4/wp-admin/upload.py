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
#// Media Library administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("upload_files")):
    wp_die(__("Sorry, you are not allowed to upload files."))
# end if
mode = get_user_option("media_library_mode", get_current_user_id()) if get_user_option("media_library_mode", get_current_user_id()) else "grid"
modes = Array("grid", "list")
if (php_isset(lambda : PHP_REQUEST["mode"])) and php_in_array(PHP_REQUEST["mode"], modes):
    mode = PHP_REQUEST["mode"]
    update_user_option(get_current_user_id(), "media_library_mode", mode)
# end if
if "grid" == mode:
    wp_enqueue_media()
    wp_enqueue_script("media-grid")
    wp_enqueue_script("media")
    remove_action("admin_head", "wp_admin_canonical_url")
    q = PHP_REQUEST
    q["s"] = None
    vars = wp_edit_attachments_query_vars(q)
    ignore = Array("mode", "post_type", "post_status", "posts_per_page")
    for key,value in vars:
        if (not value) or php_in_array(key, ignore):
            vars[key] = None
        # end if
    # end for
    wp_localize_script("media-grid", "_wpMediaGridSettings", Array({"adminUrl": php_parse_url(self_admin_url(), PHP_URL_PATH), "queryVars": vars}))
    get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("All the files you&#8217;ve uploaded are listed in the Media Library, with the most recent uploads listed first.") + "</p>" + "<p>" + __("You can view your media in a simple visual grid or a list with columns. Switch between these views using the icons to the left above the media.") + "</p>" + "<p>" + __("To delete media items, click the Bulk Select button at the top of the screen. Select any items you wish to delete, then click the Delete Selected button. Clicking the Cancel Selection button takes you back to viewing your media.") + "</p>"}))
    get_current_screen().add_help_tab(Array({"id": "attachment-details", "title": __("Attachment Details"), "content": "<p>" + __("Clicking an item will display an Attachment Details dialog, which allows you to preview media and make quick edits. Any changes you make to the attachment details will be automatically saved.") + "</p>" + "<p>" + __("Use the arrow buttons at the top of the dialog, or the left and right arrow keys on your keyboard, to navigate between media items quickly.") + "</p>" + "<p>" + __("You can also delete individual items and access the extended edit screen from the details dialog.") + "</p>"}))
    get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/media-library-screen/\">Documentation on Media Library</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
    title = __("Media Library")
    parent_file = "upload.php"
    php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
    php_print(" <div class=\"wrap\" id=\"wp-media-grid\" data-search=\"")
    _admin_search_query()
    php_print("\">\n        <h1 class=\"wp-heading-inline\">")
    php_print(esc_html(title))
    php_print("</h1>\n\n        ")
    if current_user_can("upload_files"):
        php_print("         <a href=\"")
        php_print(admin_url("media-new.php"))
        php_print("\" class=\"page-title-action aria-button-if-js\">")
        php_print(esc_html_x("Add New", "file"))
        php_print("</a>\n                               ")
    # end if
    php_print("""
    <hr class=\"wp-header-end\">
    <div class=\"error hide-if-js\">
    <p>
    """)
    printf(__("The grid view for the Media Library requires JavaScript. <a href=\"%s\">Switch to the list view</a>."), "upload.php?mode=list")
    php_print("""           </p>
    </div>
    </div>
    """)
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    php_exit(0)
# end if
wp_list_table = _get_list_table("WP_Media_List_Table")
pagenum = wp_list_table.get_pagenum()
#// Handle bulk actions.
doaction = wp_list_table.current_action()
if doaction:
    check_admin_referer("bulk-media")
    if "delete_all" == doaction:
        post_ids = wpdb.get_col(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_type='attachment' AND post_status = 'trash'"))
        doaction = "delete"
    elif (php_isset(lambda : PHP_REQUEST["media"])):
        post_ids = PHP_REQUEST["media"]
    elif (php_isset(lambda : PHP_REQUEST["ids"])):
        post_ids = php_explode(",", PHP_REQUEST["ids"])
    # end if
    location = "upload.php"
    referer = wp_get_referer()
    if referer:
        if False != php_strpos(referer, "upload.php"):
            location = remove_query_arg(Array("trashed", "untrashed", "deleted", "message", "ids", "posted"), referer)
        # end if
    # end if
    for case in Switch(doaction):
        if case("detach"):
            wp_media_attach_action(PHP_REQUEST["parent_post_id"], "detach")
            break
        # end if
        if case("attach"):
            wp_media_attach_action(PHP_REQUEST["found_post_id"])
            break
        # end if
        if case("trash"):
            if (not (php_isset(lambda : post_ids))):
                break
            # end if
            for post_id in post_ids:
                if (not current_user_can("delete_post", post_id)):
                    wp_die(__("Sorry, you are not allowed to move this item to the Trash."))
                # end if
                if (not wp_trash_post(post_id)):
                    wp_die(__("Error in moving to Trash."))
                # end if
            # end for
            location = add_query_arg(Array({"trashed": php_count(post_ids), "ids": join(",", post_ids)}), location)
            break
        # end if
        if case("untrash"):
            if (not (php_isset(lambda : post_ids))):
                break
            # end if
            for post_id in post_ids:
                if (not current_user_can("delete_post", post_id)):
                    wp_die(__("Sorry, you are not allowed to restore this item from the Trash."))
                # end if
                if (not wp_untrash_post(post_id)):
                    wp_die(__("Error in restoring from Trash."))
                # end if
            # end for
            location = add_query_arg("untrashed", php_count(post_ids), location)
            break
        # end if
        if case("delete"):
            if (not (php_isset(lambda : post_ids))):
                break
            # end if
            for post_id_del in post_ids:
                if (not current_user_can("delete_post", post_id_del)):
                    wp_die(__("Sorry, you are not allowed to delete this item."))
                # end if
                if (not wp_delete_attachment(post_id_del)):
                    wp_die(__("Error in deleting."))
                # end if
            # end for
            location = add_query_arg("deleted", php_count(post_ids), location)
            break
        # end if
        if case():
            screen = get_current_screen().id
            #// This action is documented in wp-admin/edit.php
            location = apply_filters(str("handle_bulk_actions-") + str(screen), location, doaction, post_ids)
        # end if
    # end for
    wp_redirect(location)
    php_exit(0)
elif (not php_empty(lambda : PHP_REQUEST["_wp_http_referer"])):
    wp_redirect(remove_query_arg(Array("_wp_http_referer", "_wpnonce"), wp_unslash(PHP_SERVER["REQUEST_URI"])))
    php_exit(0)
# end if
wp_list_table.prepare_items()
title = __("Media Library")
parent_file = "upload.php"
wp_enqueue_script("media")
add_screen_option("per_page")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("All the files you&#8217;ve uploaded are listed in the Media Library, with the most recent uploads listed first. You can use the Screen Options tab to customize the display of this screen.") + "</p>" + "<p>" + __("You can narrow the list by file type/status or by date using the dropdown menus above the media table.") + "</p>" + "<p>" + __("You can view your media in a simple visual grid or a list with columns. Switch between these views using the icons to the left above the media.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "actions-links", "title": __("Available Actions"), "content": "<p>" + __("Hovering over a row reveals action links: Edit, Delete Permanently, and View. Clicking Edit or on the media file&#8217;s name displays a simple screen to edit that individual file&#8217;s metadata. Clicking Delete Permanently will delete the file from the media library (as well as from any posts to which it is currently attached). View will take you to the display page for that file.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "attaching-files", "title": __("Attaching Files"), "content": "<p>" + __("If a media file has not been attached to any content, you will see that in the Uploaded To column, and can click on Attach to launch a small popup that will allow you to search for existing content and attach the file.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/media-library-screen/\">Documentation on Media Library</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter media items list"), "heading_pagination": __("Media items list navigation"), "heading_list": __("Media items list")}))
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1 class=\"wp-heading-inline\">")
php_print(esc_html(title))
php_print("</h1>\n\n")
if current_user_can("upload_files"):
    php_print(" <a href=\"")
    php_print(admin_url("media-new.php"))
    php_print("\" class=\"page-title-action\">")
    php_print(esc_html_x("Add New", "file"))
    php_print("</a>\n                       ")
# end if
if (php_isset(lambda : PHP_REQUEST["s"])) and php_strlen(PHP_REQUEST["s"]):
    #// translators: %s: Search query.
    printf("<span class=\"subtitle\">" + __("Search results for &#8220;%s&#8221;") + "</span>", get_search_query())
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
message = ""
if (not php_empty(lambda : PHP_REQUEST["posted"])):
    message = __("Media file updated.")
    PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("posted"), PHP_SERVER["REQUEST_URI"])
# end if
if (not php_empty(lambda : PHP_REQUEST["attached"])) and absint(PHP_REQUEST["attached"]):
    attached = absint(PHP_REQUEST["attached"])
    if 1 == attached:
        message = __("Media file attached.")
    else:
        #// translators: %s: Number of media files.
        message = _n("%s media file attached.", "%s media files attached.", attached)
    # end if
    message = php_sprintf(message, number_format_i18n(attached))
    PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("detach", "attached"), PHP_SERVER["REQUEST_URI"])
# end if
if (not php_empty(lambda : PHP_REQUEST["detach"])) and absint(PHP_REQUEST["detach"]):
    detached = absint(PHP_REQUEST["detach"])
    if 1 == detached:
        message = __("Media file detached.")
    else:
        #// translators: %s: Number of media files.
        message = _n("%s media file detached.", "%s media files detached.", detached)
    # end if
    message = php_sprintf(message, number_format_i18n(detached))
    PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("detach", "attached"), PHP_SERVER["REQUEST_URI"])
# end if
if (not php_empty(lambda : PHP_REQUEST["deleted"])) and absint(PHP_REQUEST["deleted"]):
    deleted = absint(PHP_REQUEST["deleted"])
    if 1 == deleted:
        message = __("Media file permanently deleted.")
    else:
        #// translators: %s: Number of media files.
        message = _n("%s media file permanently deleted.", "%s media files permanently deleted.", deleted)
    # end if
    message = php_sprintf(message, number_format_i18n(deleted))
    PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("deleted"), PHP_SERVER["REQUEST_URI"])
# end if
if (not php_empty(lambda : PHP_REQUEST["trashed"])) and absint(PHP_REQUEST["trashed"]):
    trashed = absint(PHP_REQUEST["trashed"])
    if 1 == trashed:
        message = __("Media file moved to the Trash.")
    else:
        #// translators: %s: Number of media files.
        message = _n("%s media file moved to the Trash.", "%s media files moved to the Trash.", trashed)
    # end if
    message = php_sprintf(message, number_format_i18n(trashed))
    message += " <a href=\"" + esc_url(wp_nonce_url("upload.php?doaction=undo&action=untrash&ids=" + PHP_REQUEST["ids"] if (php_isset(lambda : PHP_REQUEST["ids"])) else "", "bulk-media")) + "\">" + __("Undo") + "</a>"
    PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("trashed"), PHP_SERVER["REQUEST_URI"])
# end if
if (not php_empty(lambda : PHP_REQUEST["untrashed"])) and absint(PHP_REQUEST["untrashed"]):
    untrashed = absint(PHP_REQUEST["untrashed"])
    if 1 == untrashed:
        message = __("Media file restored from the Trash.")
    else:
        #// translators: %s: Number of media files.
        message = _n("%s media file restored from the Trash.", "%s media files restored from the Trash.", untrashed)
    # end if
    message = php_sprintf(message, number_format_i18n(untrashed))
    PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("untrashed"), PHP_SERVER["REQUEST_URI"])
# end if
messages[1] = __("Media file updated.")
messages[2] = __("Media file permanently deleted.")
messages[3] = __("Error saving media file.")
messages[4] = __("Media file moved to the Trash.") + " <a href=\"" + esc_url(wp_nonce_url("upload.php?doaction=undo&action=untrash&ids=" + PHP_REQUEST["ids"] if (php_isset(lambda : PHP_REQUEST["ids"])) else "", "bulk-media")) + "\">" + __("Undo") + "</a>"
messages[5] = __("Media file restored from the Trash.")
if (not php_empty(lambda : PHP_REQUEST["message"])) and (php_isset(lambda : messages[PHP_REQUEST["message"]])):
    message = messages[PHP_REQUEST["message"]]
    PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("message"), PHP_SERVER["REQUEST_URI"])
# end if
if (not php_empty(lambda : message)):
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    php_print(message)
    php_print("</p></div>\n")
# end if
php_print("""
<form id=\"posts-filter\" method=\"get\">
""")
wp_list_table.views()
php_print("\n")
wp_list_table.display()
php_print("\n<div id=\"ajax-response\"></div>\n")
find_posts_div()
php_print("""</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
