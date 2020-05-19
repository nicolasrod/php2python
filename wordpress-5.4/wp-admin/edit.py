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
#// Edit Posts Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not typenow_):
    wp_die(__("Invalid post type."))
# end if
if (not php_in_array(typenow_, get_post_types(Array({"show_ui": True})))):
    wp_die(__("Sorry, you are not allowed to edit posts in this post type."))
# end if
if "attachment" == typenow_:
    if wp_redirect(admin_url("upload.php")):
        php_exit(0)
    # end if
# end if
#// 
#// @global string       $post_type
#// @global WP_Post_Type $post_type_object
#//
global post_type_
global post_type_object_
php_check_if_defined("post_type_","post_type_object_")
post_type_ = typenow_
post_type_object_ = get_post_type_object(post_type_)
if (not post_type_object_):
    wp_die(__("Invalid post type."))
# end if
if (not current_user_can(post_type_object_.cap.edit_posts)):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to edit posts in this post type.") + "</p>", 403)
# end if
wp_list_table_ = _get_list_table("WP_Posts_List_Table")
pagenum_ = wp_list_table_.get_pagenum()
#// Back-compat for viewing comments of an entry.
for _redirect_ in Array("p", "attachment_id", "page_id"):
    if (not php_empty(lambda : PHP_REQUEST[_redirect_])):
        wp_redirect(admin_url("edit-comments.php?p=" + absint(PHP_REQUEST[_redirect_])))
        php_exit(0)
    # end if
# end for
_redirect_ = None
if "post" != post_type_:
    parent_file_ = str("edit.php?post_type=") + str(post_type_)
    submenu_file_ = str("edit.php?post_type=") + str(post_type_)
    post_new_file_ = str("post-new.php?post_type=") + str(post_type_)
else:
    parent_file_ = "edit.php"
    submenu_file_ = "edit.php"
    post_new_file_ = "post-new.php"
# end if
doaction_ = wp_list_table_.current_action()
if doaction_:
    check_admin_referer("bulk-posts")
    sendback_ = remove_query_arg(Array("trashed", "untrashed", "deleted", "locked", "ids"), wp_get_referer())
    if (not sendback_):
        sendback_ = admin_url(parent_file_)
    # end if
    sendback_ = add_query_arg("paged", pagenum_, sendback_)
    if php_strpos(sendback_, "post.php") != False:
        sendback_ = admin_url(post_new_file_)
    # end if
    if "delete_all" == doaction_:
        #// Prepare for deletion of all posts with a specified post status (i.e. Empty Trash).
        post_status_ = php_preg_replace("/[^a-z0-9_-]+/i", "", PHP_REQUEST["post_status"])
        #// Validate the post status exists.
        if get_post_status_object(post_status_):
            post_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE post_type=%s AND post_status = %s"), post_type_, post_status_))
        # end if
        doaction_ = "delete"
    elif (php_isset(lambda : PHP_REQUEST["media"])):
        post_ids_ = PHP_REQUEST["media"]
    elif (php_isset(lambda : PHP_REQUEST["ids"])):
        post_ids_ = php_explode(",", PHP_REQUEST["ids"])
    elif (not php_empty(lambda : PHP_REQUEST["post"])):
        post_ids_ = php_array_map("intval", PHP_REQUEST["post"])
    # end if
    if (not (php_isset(lambda : post_ids_))):
        wp_redirect(sendback_)
        php_exit(0)
    # end if
    for case in Switch(doaction_):
        if case("trash"):
            trashed_ = 0
            locked_ = 0
            for post_id_ in post_ids_:
                if (not current_user_can("delete_post", post_id_)):
                    wp_die(__("Sorry, you are not allowed to move this item to the Trash."))
                # end if
                if wp_check_post_lock(post_id_):
                    locked_ += 1
                    continue
                # end if
                if (not wp_trash_post(post_id_)):
                    wp_die(__("Error in moving to Trash."))
                # end if
                trashed_ += 1
            # end for
            sendback_ = add_query_arg(Array({"trashed": trashed_, "ids": join(",", post_ids_), "locked": locked_}), sendback_)
            break
        # end if
        if case("untrash"):
            untrashed_ = 0
            for post_id_ in post_ids_:
                if (not current_user_can("delete_post", post_id_)):
                    wp_die(__("Sorry, you are not allowed to restore this item from the Trash."))
                # end if
                if (not wp_untrash_post(post_id_)):
                    wp_die(__("Error in restoring from Trash."))
                # end if
                untrashed_ += 1
            # end for
            sendback_ = add_query_arg("untrashed", untrashed_, sendback_)
            break
        # end if
        if case("delete"):
            deleted_ = 0
            for post_id_ in post_ids_:
                post_del_ = get_post(post_id_)
                if (not current_user_can("delete_post", post_id_)):
                    wp_die(__("Sorry, you are not allowed to delete this item."))
                # end if
                if "attachment" == post_del_.post_type:
                    if (not wp_delete_attachment(post_id_)):
                        wp_die(__("Error in deleting."))
                    # end if
                else:
                    if (not wp_delete_post(post_id_)):
                        wp_die(__("Error in deleting."))
                    # end if
                # end if
                deleted_ += 1
            # end for
            sendback_ = add_query_arg("deleted", deleted_, sendback_)
            break
        # end if
        if case("edit"):
            if (php_isset(lambda : PHP_REQUEST["bulk_edit"])):
                done_ = bulk_edit_posts(PHP_REQUEST)
                if php_is_array(done_):
                    done_["updated"] = php_count(done_["updated"])
                    done_["skipped"] = php_count(done_["skipped"])
                    done_["locked"] = php_count(done_["locked"])
                    sendback_ = add_query_arg(done_, sendback_)
                # end if
            # end if
            break
        # end if
        if case():
            screen_ = get_current_screen().id
            #// 
            #// Fires when a custom bulk action should be handled.
            #// 
            #// The redirect link should be modified with success or failure feedback
            #// from the action to be used to display feedback to the user.
            #// 
            #// The dynamic portion of the hook name, `$screen`, refers to the current screen ID.
            #// 
            #// @since 4.7.0
            #// 
            #// @param string $sendback The redirect URL.
            #// @param string $doaction The action being taken.
            #// @param array  $items    The items to take the action on. Accepts an array of IDs of posts,
            #// comments, terms, links, plugins, attachments, or users.
            #//
            sendback_ = apply_filters(str("handle_bulk_actions-") + str(screen_), sendback_, doaction_, post_ids_)
            break
        # end if
    # end for
    sendback_ = remove_query_arg(Array("action", "action2", "tags_input", "post_author", "comment_status", "ping_status", "_status", "post", "bulk_edit", "post_view"), sendback_)
    wp_redirect(sendback_)
    php_exit(0)
elif (not php_empty(lambda : PHP_REQUEST["_wp_http_referer"])):
    wp_redirect(remove_query_arg(Array("_wp_http_referer", "_wpnonce"), wp_unslash(PHP_SERVER["REQUEST_URI"])))
    php_exit(0)
# end if
wp_list_table_.prepare_items()
wp_enqueue_script("inline-edit-post")
wp_enqueue_script("heartbeat")
if "wp_block" == post_type_:
    wp_enqueue_script("wp-list-reusable-blocks")
    wp_enqueue_style("wp-list-reusable-blocks")
# end if
title_ = post_type_object_.labels.name
if "post" == post_type_:
    get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen provides access to all of your posts. You can customize the display of this screen to suit your workflow.") + "</p>"}))
    get_current_screen().add_help_tab(Array({"id": "screen-content", "title": __("Screen Content"), "content": "<p>" + __("You can customize the display of this screen&#8217;s contents in a number of ways:") + "</p>" + "<ul>" + "<li>" + __("You can hide/display columns based on your needs and decide how many posts to list per screen using the Screen Options tab.") + "</li>" + "<li>" + __("You can filter the list of posts by post status using the text links above the posts list to only show posts with that status. The default view is to show all posts.") + "</li>" + "<li>" + __("You can view posts in a simple title list or with an excerpt using the Screen Options tab.") + "</li>" + "<li>" + __("You can refine the list to show only posts in a specific category or from a specific month by using the dropdown menus above the posts list. Click the Filter button after making your selection. You also can refine the list by clicking on the post author, category or tag in the posts list.") + "</li>" + "</ul>"}))
    get_current_screen().add_help_tab(Array({"id": "action-links", "title": __("Available Actions"), "content": "<p>" + __("Hovering over a row in the posts list will display action links that allow you to manage your post. You can perform the following actions:") + "</p>" + "<ul>" + "<li>" + __("<strong>Edit</strong> takes you to the editing screen for that post. You can also reach that screen by clicking on the post title.") + "</li>" + "<li>" + __("<strong>Quick Edit</strong> provides inline access to the metadata of your post, allowing you to update post details without leaving this screen.") + "</li>" + "<li>" + __("<strong>Trash</strong> removes your post from this list and places it in the Trash, from which you can permanently delete it.") + "</li>" + "<li>" + __("<strong>Preview</strong> will show you what your draft post will look like if you publish it. View will take you to your live site to view the post. Which link is available depends on your post&#8217;s status.") + "</li>" + "</ul>"}))
    get_current_screen().add_help_tab(Array({"id": "bulk-actions", "title": __("Bulk Actions"), "content": "<p>" + __("You can also edit or move multiple posts to the Trash at once. Select the posts you want to act on using the checkboxes, then select the action you want to take from the Bulk Actions menu and click Apply.") + "</p>" + "<p>" + __("When using Bulk Edit, you can change the metadata (categories, author, etc.) for all selected posts at once. To remove a post from the grouping, just click the x next to its name in the Bulk Edit area that appears.") + "</p>"}))
    get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/posts-screen/\">Documentation on Managing Posts</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
elif "page" == post_type_:
    get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("Pages are similar to posts in that they have a title, body text, and associated metadata, but they are different in that they are not part of the chronological blog stream, kind of like permanent posts. Pages are not categorized or tagged, but can have a hierarchy. You can nest pages under other pages by making one the &#8220;Parent&#8221; of the other, creating a group of pages.") + "</p>"}))
    get_current_screen().add_help_tab(Array({"id": "managing-pages", "title": __("Managing Pages"), "content": "<p>" + __("Managing pages is very similar to managing posts, and the screens can be customized in the same way.") + "</p>" + "<p>" + __("You can also perform the same types of actions, including narrowing the list by using the filters, acting on a page using the action links that appear when you hover over a row, or using the Bulk Actions menu to edit the metadata for multiple pages at once.") + "</p>"}))
    get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/pages-screen/\">Documentation on Managing Pages</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
# end if
get_current_screen().set_screen_reader_content(Array({"heading_views": post_type_object_.labels.filter_items_list, "heading_pagination": post_type_object_.labels.items_list_navigation, "heading_list": post_type_object_.labels.items_list}))
add_screen_option("per_page", Array({"default": 20, "option": "edit_" + post_type_ + "_per_page"}))
bulk_counts_ = Array({"updated": absint(PHP_REQUEST["updated"]) if (php_isset(lambda : PHP_REQUEST["updated"])) else 0, "locked": absint(PHP_REQUEST["locked"]) if (php_isset(lambda : PHP_REQUEST["locked"])) else 0, "deleted": absint(PHP_REQUEST["deleted"]) if (php_isset(lambda : PHP_REQUEST["deleted"])) else 0, "trashed": absint(PHP_REQUEST["trashed"]) if (php_isset(lambda : PHP_REQUEST["trashed"])) else 0, "untrashed": absint(PHP_REQUEST["untrashed"]) if (php_isset(lambda : PHP_REQUEST["untrashed"])) else 0})
bulk_messages_ = Array()
bulk_messages_["post"] = Array({"updated": _n("%s post updated.", "%s posts updated.", bulk_counts_["updated"]), "locked": __("1 post not updated, somebody is editing it.") if 1 == bulk_counts_["locked"] else _n("%s post not updated, somebody is editing it.", "%s posts not updated, somebody is editing them.", bulk_counts_["locked"]), "deleted": _n("%s post permanently deleted.", "%s posts permanently deleted.", bulk_counts_["deleted"]), "trashed": _n("%s post moved to the Trash.", "%s posts moved to the Trash.", bulk_counts_["trashed"]), "untrashed": _n("%s post restored from the Trash.", "%s posts restored from the Trash.", bulk_counts_["untrashed"])})
bulk_messages_["page"] = Array({"updated": _n("%s page updated.", "%s pages updated.", bulk_counts_["updated"]), "locked": __("1 page not updated, somebody is editing it.") if 1 == bulk_counts_["locked"] else _n("%s page not updated, somebody is editing it.", "%s pages not updated, somebody is editing them.", bulk_counts_["locked"]), "deleted": _n("%s page permanently deleted.", "%s pages permanently deleted.", bulk_counts_["deleted"]), "trashed": _n("%s page moved to the Trash.", "%s pages moved to the Trash.", bulk_counts_["trashed"]), "untrashed": _n("%s page restored from the Trash.", "%s pages restored from the Trash.", bulk_counts_["untrashed"])})
bulk_messages_["wp_block"] = Array({"updated": _n("%s block updated.", "%s blocks updated.", bulk_counts_["updated"]), "locked": __("1 block not updated, somebody is editing it.") if 1 == bulk_counts_["locked"] else _n("%s block not updated, somebody is editing it.", "%s blocks not updated, somebody is editing them.", bulk_counts_["locked"]), "deleted": _n("%s block permanently deleted.", "%s blocks permanently deleted.", bulk_counts_["deleted"]), "trashed": _n("%s block moved to the Trash.", "%s blocks moved to the Trash.", bulk_counts_["trashed"]), "untrashed": _n("%s block restored from the Trash.", "%s blocks restored from the Trash.", bulk_counts_["untrashed"])})
#// 
#// Filters the bulk action updated messages.
#// 
#// By default, custom post types use the messages for the 'post' post type.
#// 
#// @since 3.7.0
#// 
#// @param array[] $bulk_messages Arrays of messages, each keyed by the corresponding post type. Messages are
#// keyed with 'updated', 'locked', 'deleted', 'trashed', and 'untrashed'.
#// @param int[]   $bulk_counts   Array of item counts for each message, used to build internationalized strings.
#//
bulk_messages_ = apply_filters("bulk_post_updated_messages", bulk_messages_, bulk_counts_)
bulk_counts_ = php_array_filter(bulk_counts_)
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n<h1 class=\"wp-heading-inline\">\n")
php_print(esc_html(post_type_object_.labels.name))
php_print("</h1>\n\n")
if current_user_can(post_type_object_.cap.create_posts):
    php_print(" <a href=\"" + esc_url(admin_url(post_new_file_)) + "\" class=\"page-title-action\">" + esc_html(post_type_object_.labels.add_new) + "</a>")
# end if
if (php_isset(lambda : PHP_REQUEST["s"])) and php_strlen(PHP_REQUEST["s"]):
    #// translators: %s: Search query.
    printf(" <span class=\"subtitle\">" + __("Search results for &#8220;%s&#8221;") + "</span>", get_search_query())
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
#// If we have a bulk message to issue:
messages_ = Array()
for message_,count_ in bulk_counts_.items():
    if (php_isset(lambda : bulk_messages_[post_type_][message_])):
        messages_[-1] = php_sprintf(bulk_messages_[post_type_][message_], number_format_i18n(count_))
    elif (php_isset(lambda : bulk_messages_["post"][message_])):
        messages_[-1] = php_sprintf(bulk_messages_["post"][message_], number_format_i18n(count_))
    # end if
    if "trashed" == message_ and (php_isset(lambda : PHP_REQUEST["ids"])):
        ids_ = php_preg_replace("/[^0-9,]/", "", PHP_REQUEST["ids"])
        messages_[-1] = "<a href=\"" + esc_url(wp_nonce_url(str("edit.php?post_type=") + str(post_type_) + str("&doaction=undo&action=untrash&ids=") + str(ids_), "bulk-posts")) + "\">" + __("Undo") + "</a>"
    # end if
# end for
if messages_:
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + join(" ", messages_) + "</p></div>")
# end if
messages_ = None
PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("locked", "skipped", "updated", "deleted", "trashed", "untrashed"), PHP_SERVER["REQUEST_URI"])
php_print("\n")
wp_list_table_.views()
php_print("""
<form id=\"posts-filter\" method=\"get\">
""")
wp_list_table_.search_box(post_type_object_.labels.search_items, "post")
php_print("\n<input type=\"hidden\" name=\"post_status\" class=\"post_status_page\" value=\"")
php_print(esc_attr(PHP_REQUEST["post_status"]) if (not php_empty(lambda : PHP_REQUEST["post_status"])) else "all")
php_print("\" />\n<input type=\"hidden\" name=\"post_type\" class=\"post_type_page\" value=\"")
php_print(post_type_)
php_print("\" />\n\n")
if (not php_empty(lambda : PHP_REQUEST["author"])):
    php_print("<input type=\"hidden\" name=\"author\" value=\"")
    php_print(esc_attr(PHP_REQUEST["author"]))
    php_print("\" />\n")
# end if
php_print("\n")
if (not php_empty(lambda : PHP_REQUEST["show_sticky"])):
    php_print("<input type=\"hidden\" name=\"show_sticky\" value=\"1\" />\n")
# end if
php_print("\n")
wp_list_table_.display()
php_print("""
</form>
""")
if wp_list_table_.has_items():
    wp_list_table_.inline_edit()
# end if
php_print("""
<div id=\"ajax-response\"></div>
<br class=\"clear\" />
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
