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
#// Edit post administration panel.
#// 
#// Manage Post actions: post, edit, delete, etc.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
parent_file = "edit.php"
submenu_file = "edit.php"
wp_reset_vars(Array("action"))
if (php_isset(lambda : PHP_REQUEST["post"])) and (php_isset(lambda : PHP_POST["post_ID"])) and int(PHP_REQUEST["post"]) != int(PHP_POST["post_ID"]):
    wp_die(__("A post ID mismatch has been detected."), __("Sorry, you are not allowed to edit this item."), 400)
elif (php_isset(lambda : PHP_REQUEST["post"])):
    post_id = int(PHP_REQUEST["post"])
elif (php_isset(lambda : PHP_POST["post_ID"])):
    post_id = int(PHP_POST["post_ID"])
else:
    post_id = 0
# end if
post_ID = post_id
#// 
#// @global string  $post_type
#// @global object  $post_type_object
#// @global WP_Post $post             Global post object.
#//
global post_type,post_type_object,post
php_check_if_defined("post_type","post_type_object","post")
if post_id:
    post = get_post(post_id)
# end if
if post:
    post_type = post.post_type
    post_type_object = get_post_type_object(post_type)
# end if
if (php_isset(lambda : PHP_POST["post_type"])) and post and post_type != PHP_POST["post_type"]:
    wp_die(__("A post type mismatch has been detected."), __("Sorry, you are not allowed to edit this item."), 400)
# end if
if (php_isset(lambda : PHP_POST["deletepost"])):
    action = "delete"
elif (php_isset(lambda : PHP_POST["wp-preview"])) and "dopreview" == PHP_POST["wp-preview"]:
    action = "preview"
# end if
sendback = wp_get_referer()
if (not sendback) or False != php_strpos(sendback, "post.php") or False != php_strpos(sendback, "post-new.php"):
    if "attachment" == post_type:
        sendback = admin_url("upload.php")
    else:
        sendback = admin_url("edit.php")
        if (not php_empty(lambda : post_type)):
            sendback = add_query_arg("post_type", post_type, sendback)
        # end if
    # end if
else:
    sendback = remove_query_arg(Array("trashed", "untrashed", "deleted", "ids"), sendback)
# end if
for case in Switch(action):
    if case("post-quickdraft-save"):
        #// Check nonce and capabilities.
        nonce = PHP_REQUEST["_wpnonce"]
        error_msg = False
        #// For output of the Quick Draft dashboard widget.
        php_include_file(ABSPATH + "wp-admin/includes/dashboard.php", once=True)
        if (not wp_verify_nonce(nonce, "add-post")):
            error_msg = __("Unable to submit this form, please refresh and try again.")
        # end if
        if (not current_user_can(get_post_type_object("post").cap.create_posts)):
            php_exit(0)
        # end if
        if error_msg:
            php_set_include_retval(wp_dashboard_quick_press(error_msg))
            sys.exit(-1)
        # end if
        post = get_post(PHP_REQUEST["post_ID"])
        check_admin_referer("add-" + post.post_type)
        PHP_POST["comment_status"] = get_default_comment_status(post.post_type)
        PHP_POST["ping_status"] = get_default_comment_status(post.post_type, "pingback")
        #// Wrap Quick Draft content in the Paragraph block.
        if False == php_strpos(PHP_POST["content"], "<!-- wp:paragraph -->"):
            PHP_POST["content"] = php_sprintf("<!-- wp:paragraph -->%s<!-- /wp:paragraph -->", php_str_replace(Array("\r\n", "\r", "\n"), "<br />", PHP_POST["content"]))
        # end if
        edit_post()
        wp_dashboard_quick_press()
        php_exit(0)
    # end if
    if case("postajaxpost"):
        pass
    # end if
    if case("post"):
        check_admin_referer("add-" + post_type)
        post_id = edit_post() if "postajaxpost" == action else write_post()
        redirect_post(post_id)
        php_exit(0)
    # end if
    if case("edit"):
        editing = True
        if php_empty(lambda : post_id):
            wp_redirect(admin_url("post.php"))
            php_exit(0)
        # end if
        if (not post):
            wp_die(__("You attempted to edit an item that doesn&#8217;t exist. Perhaps it was deleted?"))
        # end if
        if (not post_type_object):
            wp_die(__("Invalid post type."))
        # end if
        if (not php_in_array(typenow, get_post_types(Array({"show_ui": True})))):
            wp_die(__("Sorry, you are not allowed to edit posts in this post type."))
        # end if
        if (not current_user_can("edit_post", post_id)):
            wp_die(__("Sorry, you are not allowed to edit this item."))
        # end if
        if "trash" == post.post_status:
            wp_die(__("You can&#8217;t edit this item because it is in the Trash. Please restore it and try again."))
        # end if
        if (not php_empty(lambda : PHP_REQUEST["get-post-lock"])):
            check_admin_referer("lock-post_" + post_id)
            wp_set_post_lock(post_id)
            wp_redirect(get_edit_post_link(post_id, "url"))
            php_exit(0)
        # end if
        post_type = post.post_type
        if "post" == post_type:
            parent_file = "edit.php"
            submenu_file = "edit.php"
            post_new_file = "post-new.php"
        elif "attachment" == post_type:
            parent_file = "upload.php"
            submenu_file = "upload.php"
            post_new_file = "media-new.php"
        else:
            if (php_isset(lambda : post_type_object)) and post_type_object.show_in_menu and True != post_type_object.show_in_menu:
                parent_file = post_type_object.show_in_menu
            else:
                parent_file = str("edit.php?post_type=") + str(post_type)
            # end if
            submenu_file = str("edit.php?post_type=") + str(post_type)
            post_new_file = str("post-new.php?post_type=") + str(post_type)
        # end if
        title = post_type_object.labels.edit_item
        #// 
        #// Allows replacement of the editor.
        #// 
        #// @since 4.9.0
        #// 
        #// @param bool    $replace Whether to replace the editor. Default false.
        #// @param WP_Post $post    Post object.
        #//
        if True == apply_filters("replace_editor", False, post):
            break
        # end if
        if use_block_editor_for_post(post):
            php_include_file(ABSPATH + "wp-admin/edit-form-blocks.php", once=False)
            break
        # end if
        if (not wp_check_post_lock(post.ID)):
            active_post_lock = wp_set_post_lock(post.ID)
            if "attachment" != post_type:
                wp_enqueue_script("autosave")
            # end if
        # end if
        post = get_post(post_id, OBJECT, "edit")
        if post_type_supports(post_type, "comments"):
            wp_enqueue_script("admin-comments")
            enqueue_comment_hotkeys_js()
        # end if
        php_include_file(ABSPATH + "wp-admin/edit-form-advanced.php", once=False)
        break
    # end if
    if case("editattachment"):
        check_admin_referer("update-post_" + post_id)
        PHP_POST["guid"] = None
        PHP_POST["post_type"] = "attachment"
        #// Update the thumbnail filename.
        newmeta = wp_get_attachment_metadata(post_id, True)
        newmeta["thumb"] = wp_basename(PHP_POST["thumb"])
        wp_update_attachment_metadata(post_id, newmeta)
    # end if
    if case("editpost"):
        check_admin_referer("update-post_" + post_id)
        post_id = edit_post()
        #// Session cookie flag that the post was saved.
        if (php_isset(lambda : PHP_COOKIE["wp-saving-post"])) and PHP_COOKIE["wp-saving-post"] == post_id + "-check":
            setcookie("wp-saving-post", post_id + "-saved", time() + DAY_IN_SECONDS, ADMIN_COOKIE_PATH, COOKIE_DOMAIN, is_ssl())
        # end if
        redirect_post(post_id)
        #// Send user on their way while we keep working.
        php_exit(0)
    # end if
    if case("trash"):
        check_admin_referer("trash-post_" + post_id)
        if (not post):
            wp_die(__("The item you are trying to move to the Trash no longer exists."))
        # end if
        if (not post_type_object):
            wp_die(__("Invalid post type."))
        # end if
        if (not current_user_can("delete_post", post_id)):
            wp_die(__("Sorry, you are not allowed to move this item to the Trash."))
        # end if
        user_id = wp_check_post_lock(post_id)
        if user_id:
            user = get_userdata(user_id)
            #// translators: %s: User's display name.
            wp_die(php_sprintf(__("You cannot move this item to the Trash. %s is currently editing."), user.display_name))
        # end if
        if (not wp_trash_post(post_id)):
            wp_die(__("Error in moving to Trash."))
        # end if
        wp_redirect(add_query_arg(Array({"trashed": 1, "ids": post_id}), sendback))
        php_exit(0)
    # end if
    if case("untrash"):
        check_admin_referer("untrash-post_" + post_id)
        if (not post):
            wp_die(__("The item you are trying to restore from the Trash no longer exists."))
        # end if
        if (not post_type_object):
            wp_die(__("Invalid post type."))
        # end if
        if (not current_user_can("delete_post", post_id)):
            wp_die(__("Sorry, you are not allowed to restore this item from the Trash."))
        # end if
        if (not wp_untrash_post(post_id)):
            wp_die(__("Error in restoring from Trash."))
        # end if
        wp_redirect(add_query_arg("untrashed", 1, sendback))
        php_exit(0)
    # end if
    if case("delete"):
        check_admin_referer("delete-post_" + post_id)
        if (not post):
            wp_die(__("This item has already been deleted."))
        # end if
        if (not post_type_object):
            wp_die(__("Invalid post type."))
        # end if
        if (not current_user_can("delete_post", post_id)):
            wp_die(__("Sorry, you are not allowed to delete this item."))
        # end if
        if "attachment" == post.post_type:
            force = (not MEDIA_TRASH)
            if (not wp_delete_attachment(post_id, force)):
                wp_die(__("Error in deleting."))
            # end if
        else:
            if (not wp_delete_post(post_id, True)):
                wp_die(__("Error in deleting."))
            # end if
        # end if
        wp_redirect(add_query_arg("deleted", 1, sendback))
        php_exit(0)
    # end if
    if case("preview"):
        check_admin_referer("update-post_" + post_id)
        url = post_preview()
        wp_redirect(url)
        php_exit(0)
    # end if
    if case("toggle-custom-fields"):
        check_admin_referer("toggle-custom-fields")
        current_user_id = get_current_user_id()
        if current_user_id:
            enable_custom_fields = bool(get_user_meta(current_user_id, "enable_custom_fields", True))
            update_user_meta(current_user_id, "enable_custom_fields", (not enable_custom_fields))
        # end if
        wp_safe_redirect(wp_get_referer())
        php_exit(0)
    # end if
    if case():
        #// 
        #// Fires for a given custom post action request.
        #// 
        #// The dynamic portion of the hook name, `$action`, refers to the custom post action.
        #// 
        #// @since 4.6.0
        #// 
        #// @param int $post_id Post ID sent with the request.
        #//
        do_action(str("post_action_") + str(action), post_id)
        wp_redirect(admin_url("edit.php"))
        php_exit(0)
    # end if
# end for
#// End switch.
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
