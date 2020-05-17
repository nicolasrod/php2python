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
#// Edit post administration panel.
#// 
#// Manage Post actions: post, edit, delete, etc.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
parent_file_ = "edit.php"
submenu_file_ = "edit.php"
wp_reset_vars(Array("action"))
if (php_isset(lambda : PHP_REQUEST["post"])) and (php_isset(lambda : PHP_POST["post_ID"])) and php_int(PHP_REQUEST["post"]) != php_int(PHP_POST["post_ID"]):
    wp_die(__("A post ID mismatch has been detected."), __("Sorry, you are not allowed to edit this item."), 400)
elif (php_isset(lambda : PHP_REQUEST["post"])):
    post_id_ = php_int(PHP_REQUEST["post"])
elif (php_isset(lambda : PHP_POST["post_ID"])):
    post_id_ = php_int(PHP_POST["post_ID"])
else:
    post_id_ = 0
# end if
post_ID_ = post_id_
#// 
#// @global string  $post_type
#// @global object  $post_type_object
#// @global WP_Post $post             Global post object.
#//
global post_type_
global post_type_object_
global post_
php_check_if_defined("post_type_","post_type_object_","post_")
if post_id_:
    post_ = get_post(post_id_)
# end if
if post_:
    post_type_ = post_.post_type
    post_type_object_ = get_post_type_object(post_type_)
# end if
if (php_isset(lambda : PHP_POST["post_type"])) and post_ and post_type_ != PHP_POST["post_type"]:
    wp_die(__("A post type mismatch has been detected."), __("Sorry, you are not allowed to edit this item."), 400)
# end if
if (php_isset(lambda : PHP_POST["deletepost"])):
    action_ = "delete"
elif (php_isset(lambda : PHP_POST["wp-preview"])) and "dopreview" == PHP_POST["wp-preview"]:
    action_ = "preview"
# end if
sendback_ = wp_get_referer()
if (not sendback_) or False != php_strpos(sendback_, "post.php") or False != php_strpos(sendback_, "post-new.php"):
    if "attachment" == post_type_:
        sendback_ = admin_url("upload.php")
    else:
        sendback_ = admin_url("edit.php")
        if (not php_empty(lambda : post_type_)):
            sendback_ = add_query_arg("post_type", post_type_, sendback_)
        # end if
    # end if
else:
    sendback_ = remove_query_arg(Array("trashed", "untrashed", "deleted", "ids"), sendback_)
# end if
for case in Switch(action_):
    if case("post-quickdraft-save"):
        #// Check nonce and capabilities.
        nonce_ = PHP_REQUEST["_wpnonce"]
        error_msg_ = False
        #// For output of the Quick Draft dashboard widget.
        php_include_file(ABSPATH + "wp-admin/includes/dashboard.php", once=True)
        if (not wp_verify_nonce(nonce_, "add-post")):
            error_msg_ = __("Unable to submit this form, please refresh and try again.")
        # end if
        if (not current_user_can(get_post_type_object("post").cap.create_posts)):
            php_exit(0)
        # end if
        if error_msg_:
            php_set_include_retval(wp_dashboard_quick_press(error_msg_))
            sys.exit(-1)
        # end if
        post_ = get_post(PHP_REQUEST["post_ID"])
        check_admin_referer("add-" + post_.post_type)
        PHP_POST["comment_status"] = get_default_comment_status(post_.post_type)
        PHP_POST["ping_status"] = get_default_comment_status(post_.post_type, "pingback")
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
        check_admin_referer("add-" + post_type_)
        post_id_ = edit_post() if "postajaxpost" == action_ else write_post()
        redirect_post(post_id_)
        php_exit(0)
    # end if
    if case("edit"):
        editing_ = True
        if php_empty(lambda : post_id_):
            wp_redirect(admin_url("post.php"))
            php_exit(0)
        # end if
        if (not post_):
            wp_die(__("You attempted to edit an item that doesn&#8217;t exist. Perhaps it was deleted?"))
        # end if
        if (not post_type_object_):
            wp_die(__("Invalid post type."))
        # end if
        if (not php_in_array(typenow_, get_post_types(Array({"show_ui": True})))):
            wp_die(__("Sorry, you are not allowed to edit posts in this post type."))
        # end if
        if (not current_user_can("edit_post", post_id_)):
            wp_die(__("Sorry, you are not allowed to edit this item."))
        # end if
        if "trash" == post_.post_status:
            wp_die(__("You can&#8217;t edit this item because it is in the Trash. Please restore it and try again."))
        # end if
        if (not php_empty(lambda : PHP_REQUEST["get-post-lock"])):
            check_admin_referer("lock-post_" + post_id_)
            wp_set_post_lock(post_id_)
            wp_redirect(get_edit_post_link(post_id_, "url"))
            php_exit(0)
        # end if
        post_type_ = post_.post_type
        if "post" == post_type_:
            parent_file_ = "edit.php"
            submenu_file_ = "edit.php"
            post_new_file_ = "post-new.php"
        elif "attachment" == post_type_:
            parent_file_ = "upload.php"
            submenu_file_ = "upload.php"
            post_new_file_ = "media-new.php"
        else:
            if (php_isset(lambda : post_type_object_)) and post_type_object_.show_in_menu and True != post_type_object_.show_in_menu:
                parent_file_ = post_type_object_.show_in_menu
            else:
                parent_file_ = str("edit.php?post_type=") + str(post_type_)
            # end if
            submenu_file_ = str("edit.php?post_type=") + str(post_type_)
            post_new_file_ = str("post-new.php?post_type=") + str(post_type_)
        # end if
        title_ = post_type_object_.labels.edit_item
        #// 
        #// Allows replacement of the editor.
        #// 
        #// @since 4.9.0
        #// 
        #// @param bool    $replace Whether to replace the editor. Default false.
        #// @param WP_Post $post    Post object.
        #//
        if True == apply_filters("replace_editor", False, post_):
            break
        # end if
        if use_block_editor_for_post(post_):
            php_include_file(ABSPATH + "wp-admin/edit-form-blocks.php", once=False)
            break
        # end if
        if (not wp_check_post_lock(post_.ID)):
            active_post_lock_ = wp_set_post_lock(post_.ID)
            if "attachment" != post_type_:
                wp_enqueue_script("autosave")
            # end if
        # end if
        post_ = get_post(post_id_, OBJECT, "edit")
        if post_type_supports(post_type_, "comments"):
            wp_enqueue_script("admin-comments")
            enqueue_comment_hotkeys_js()
        # end if
        php_include_file(ABSPATH + "wp-admin/edit-form-advanced.php", once=False)
        break
    # end if
    if case("editattachment"):
        check_admin_referer("update-post_" + post_id_)
        PHP_POST["guid"] = None
        PHP_POST["post_type"] = "attachment"
        #// Update the thumbnail filename.
        newmeta_ = wp_get_attachment_metadata(post_id_, True)
        newmeta_["thumb"] = wp_basename(PHP_POST["thumb"])
        wp_update_attachment_metadata(post_id_, newmeta_)
    # end if
    if case("editpost"):
        check_admin_referer("update-post_" + post_id_)
        post_id_ = edit_post()
        #// Session cookie flag that the post was saved.
        if (php_isset(lambda : PHP_COOKIE["wp-saving-post"])) and PHP_COOKIE["wp-saving-post"] == post_id_ + "-check":
            setcookie("wp-saving-post", post_id_ + "-saved", time() + DAY_IN_SECONDS, ADMIN_COOKIE_PATH, COOKIE_DOMAIN, is_ssl())
        # end if
        redirect_post(post_id_)
        #// Send user on their way while we keep working.
        php_exit(0)
    # end if
    if case("trash"):
        check_admin_referer("trash-post_" + post_id_)
        if (not post_):
            wp_die(__("The item you are trying to move to the Trash no longer exists."))
        # end if
        if (not post_type_object_):
            wp_die(__("Invalid post type."))
        # end if
        if (not current_user_can("delete_post", post_id_)):
            wp_die(__("Sorry, you are not allowed to move this item to the Trash."))
        # end if
        user_id_ = wp_check_post_lock(post_id_)
        if user_id_:
            user_ = get_userdata(user_id_)
            #// translators: %s: User's display name.
            wp_die(php_sprintf(__("You cannot move this item to the Trash. %s is currently editing."), user_.display_name))
        # end if
        if (not wp_trash_post(post_id_)):
            wp_die(__("Error in moving to Trash."))
        # end if
        wp_redirect(add_query_arg(Array({"trashed": 1, "ids": post_id_}), sendback_))
        php_exit(0)
    # end if
    if case("untrash"):
        check_admin_referer("untrash-post_" + post_id_)
        if (not post_):
            wp_die(__("The item you are trying to restore from the Trash no longer exists."))
        # end if
        if (not post_type_object_):
            wp_die(__("Invalid post type."))
        # end if
        if (not current_user_can("delete_post", post_id_)):
            wp_die(__("Sorry, you are not allowed to restore this item from the Trash."))
        # end if
        if (not wp_untrash_post(post_id_)):
            wp_die(__("Error in restoring from Trash."))
        # end if
        wp_redirect(add_query_arg("untrashed", 1, sendback_))
        php_exit(0)
    # end if
    if case("delete"):
        check_admin_referer("delete-post_" + post_id_)
        if (not post_):
            wp_die(__("This item has already been deleted."))
        # end if
        if (not post_type_object_):
            wp_die(__("Invalid post type."))
        # end if
        if (not current_user_can("delete_post", post_id_)):
            wp_die(__("Sorry, you are not allowed to delete this item."))
        # end if
        if "attachment" == post_.post_type:
            force_ = (not MEDIA_TRASH)
            if (not wp_delete_attachment(post_id_, force_)):
                wp_die(__("Error in deleting."))
            # end if
        else:
            if (not wp_delete_post(post_id_, True)):
                wp_die(__("Error in deleting."))
            # end if
        # end if
        wp_redirect(add_query_arg("deleted", 1, sendback_))
        php_exit(0)
    # end if
    if case("preview"):
        check_admin_referer("update-post_" + post_id_)
        url_ = post_preview()
        wp_redirect(url_)
        php_exit(0)
    # end if
    if case("toggle-custom-fields"):
        check_admin_referer("toggle-custom-fields")
        current_user_id_ = get_current_user_id()
        if current_user_id_:
            enable_custom_fields_ = php_bool(get_user_meta(current_user_id_, "enable_custom_fields", True))
            update_user_meta(current_user_id_, "enable_custom_fields", (not enable_custom_fields_))
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
        do_action(str("post_action_") + str(action_), post_id_)
        wp_redirect(admin_url("edit.php"))
        php_exit(0)
    # end if
# end for
#// End switch.
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
