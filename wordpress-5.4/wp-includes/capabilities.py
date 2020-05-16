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
#// Core User Role & Capabilities API
#// 
#// @package WordPress
#// @subpackage Users
#// 
#// 
#// Maps meta capabilities to primitive capabilities.
#// 
#// This function also accepts an ID of an object to map against if the capability is a meta capability. Meta
#// capabilities such as `edit_post` and `edit_user` are capabilities used by this function to map to primitive
#// capabilities that a user or role has, such as `edit_posts` and `edit_others_posts`.
#// 
#// Example usage:
#// 
#// map_meta_cap( 'edit_posts', $user->ID );
#// map_meta_cap( 'edit_post', $user->ID, $post->ID );
#// map_meta_cap( 'edit_post_meta', $user->ID, $post->ID, $meta_key );
#// 
#// This does not actually compare whether the user ID has the actual capability,
#// just what the capability or capabilities are. Meta capability list value can
#// be 'delete_user', 'edit_user', 'remove_user', 'promote_user', 'delete_post',
#// 'delete_page', 'edit_post', 'edit_page', 'read_post', or 'read_page'.
#// 
#// @since 2.0.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @global array $post_type_meta_caps Used to get post type meta capabilities.
#// 
#// @param string $cap     Capability name.
#// @param int    $user_id User ID.
#// @param mixed  ...$args Optional further parameters, typically starting with an object ID.
#// @return string[] Actual capabilities for meta capability.
#//
def map_meta_cap(cap=None, user_id=None, *args):
    
    caps = Array()
    for case in Switch(cap):
        if case("remove_user"):
            #// In multisite the user must be a super admin to remove themselves.
            if (php_isset(lambda : args[0])) and user_id == args[0] and (not is_super_admin(user_id)):
                caps[-1] = "do_not_allow"
            else:
                caps[-1] = "remove_users"
            # end if
            break
        # end if
        if case("promote_user"):
            pass
        # end if
        if case("add_users"):
            caps[-1] = "promote_users"
            break
        # end if
        if case("edit_user"):
            pass
        # end if
        if case("edit_users"):
            #// Allow user to edit themselves.
            if "edit_user" == cap and (php_isset(lambda : args[0])) and user_id == args[0]:
                break
            # end if
            #// In multisite the user must have manage_network_users caps. If editing a super admin, the user must be a super admin.
            if is_multisite() and (not is_super_admin(user_id)) and "edit_user" == cap and is_super_admin(args[0]) or (not user_can(user_id, "manage_network_users")):
                caps[-1] = "do_not_allow"
            else:
                caps[-1] = "edit_users"
                pass
            # end if
            break
        # end if
        if case("delete_post"):
            pass
        # end if
        if case("delete_page"):
            post = get_post(args[0])
            if (not post):
                caps[-1] = "do_not_allow"
                break
            # end if
            if "revision" == post.post_type:
                caps[-1] = "do_not_allow"
                break
            # end if
            if get_option("page_for_posts") == post.ID or get_option("page_on_front") == post.ID:
                caps[-1] = "manage_options"
                break
            # end if
            post_type = get_post_type_object(post.post_type)
            if (not post_type):
                #// translators: 1: Post type, 2: Capability name.
                _doing_it_wrong(__FUNCTION__, php_sprintf(__("The post type %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post of that type."), post.post_type, cap), "4.4.0")
                caps[-1] = "edit_others_posts"
                break
            # end if
            if (not post_type.map_meta_cap):
                caps[-1] = post_type.cap.cap
                #// Prior to 3.1 we would re-call map_meta_cap here.
                if "delete_post" == cap:
                    cap = post_type.cap.cap
                # end if
                break
            # end if
            #// If the post author is set and the user is the author...
            if post.post_author and user_id == post.post_author:
                #// If the post is published or scheduled...
                if php_in_array(post.post_status, Array("publish", "future"), True):
                    caps[-1] = post_type.cap.delete_published_posts
                elif "trash" == post.post_status:
                    status = get_post_meta(post.ID, "_wp_trash_meta_status", True)
                    if php_in_array(status, Array("publish", "future"), True):
                        caps[-1] = post_type.cap.delete_published_posts
                    else:
                        caps[-1] = post_type.cap.delete_posts
                    # end if
                else:
                    #// If the post is draft...
                    caps[-1] = post_type.cap.delete_posts
                # end if
            else:
                #// The user is trying to edit someone else's post.
                caps[-1] = post_type.cap.delete_others_posts
                #// The post is published or scheduled, extra cap required.
                if php_in_array(post.post_status, Array("publish", "future"), True):
                    caps[-1] = post_type.cap.delete_published_posts
                elif "private" == post.post_status:
                    caps[-1] = post_type.cap.delete_private_posts
                # end if
            # end if
            #// 
            #// Setting the privacy policy page requires `manage_privacy_options`,
            #// so deleting it should require that too.
            #//
            if php_int(get_option("wp_page_for_privacy_policy")) == post.ID:
                caps = php_array_merge(caps, map_meta_cap("manage_privacy_options", user_id))
            # end if
            break
        # end if
        if case("edit_post"):
            pass
        # end if
        if case("edit_page"):
            post = get_post(args[0])
            if (not post):
                caps[-1] = "do_not_allow"
                break
            # end if
            if "revision" == post.post_type:
                post = get_post(post.post_parent)
                if (not post):
                    caps[-1] = "do_not_allow"
                    break
                # end if
            # end if
            post_type = get_post_type_object(post.post_type)
            if (not post_type):
                #// translators: 1: Post type, 2: Capability name.
                _doing_it_wrong(__FUNCTION__, php_sprintf(__("The post type %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post of that type."), post.post_type, cap), "4.4.0")
                caps[-1] = "edit_others_posts"
                break
            # end if
            if (not post_type.map_meta_cap):
                caps[-1] = post_type.cap.cap
                #// Prior to 3.1 we would re-call map_meta_cap here.
                if "edit_post" == cap:
                    cap = post_type.cap.cap
                # end if
                break
            # end if
            #// If the post author is set and the user is the author...
            if post.post_author and user_id == post.post_author:
                #// If the post is published or scheduled...
                if php_in_array(post.post_status, Array("publish", "future"), True):
                    caps[-1] = post_type.cap.edit_published_posts
                elif "trash" == post.post_status:
                    status = get_post_meta(post.ID, "_wp_trash_meta_status", True)
                    if php_in_array(status, Array("publish", "future"), True):
                        caps[-1] = post_type.cap.edit_published_posts
                    else:
                        caps[-1] = post_type.cap.edit_posts
                    # end if
                else:
                    #// If the post is draft...
                    caps[-1] = post_type.cap.edit_posts
                # end if
            else:
                #// The user is trying to edit someone else's post.
                caps[-1] = post_type.cap.edit_others_posts
                #// The post is published or scheduled, extra cap required.
                if php_in_array(post.post_status, Array("publish", "future"), True):
                    caps[-1] = post_type.cap.edit_published_posts
                elif "private" == post.post_status:
                    caps[-1] = post_type.cap.edit_private_posts
                # end if
            # end if
            #// 
            #// Setting the privacy policy page requires `manage_privacy_options`,
            #// so editing it should require that too.
            #//
            if php_int(get_option("wp_page_for_privacy_policy")) == post.ID:
                caps = php_array_merge(caps, map_meta_cap("manage_privacy_options", user_id))
            # end if
            break
        # end if
        if case("read_post"):
            pass
        # end if
        if case("read_page"):
            post = get_post(args[0])
            if (not post):
                caps[-1] = "do_not_allow"
                break
            # end if
            if "revision" == post.post_type:
                post = get_post(post.post_parent)
                if (not post):
                    caps[-1] = "do_not_allow"
                    break
                # end if
            # end if
            post_type = get_post_type_object(post.post_type)
            if (not post_type):
                #// translators: 1: Post type, 2: Capability name.
                _doing_it_wrong(__FUNCTION__, php_sprintf(__("The post type %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post of that type."), post.post_type, cap), "4.4.0")
                caps[-1] = "edit_others_posts"
                break
            # end if
            if (not post_type.map_meta_cap):
                caps[-1] = post_type.cap.cap
                #// Prior to 3.1 we would re-call map_meta_cap here.
                if "read_post" == cap:
                    cap = post_type.cap.cap
                # end if
                break
            # end if
            status_obj = get_post_status_object(post.post_status)
            if (not status_obj):
                #// translators: 1: Post status, 2: Capability name.
                _doing_it_wrong(__FUNCTION__, php_sprintf(__("The post status %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post with that status."), post.post_status, cap), "5.4.0")
                caps[-1] = "edit_others_posts"
                break
            # end if
            if status_obj.public:
                caps[-1] = post_type.cap.read
                break
            # end if
            if post.post_author and user_id == post.post_author:
                caps[-1] = post_type.cap.read
            elif status_obj.private:
                caps[-1] = post_type.cap.read_private_posts
            else:
                caps = map_meta_cap("edit_post", user_id, post.ID)
            # end if
            break
        # end if
        if case("publish_post"):
            post = get_post(args[0])
            if (not post):
                caps[-1] = "do_not_allow"
                break
            # end if
            post_type = get_post_type_object(post.post_type)
            if (not post_type):
                #// translators: 1: Post type, 2: Capability name.
                _doing_it_wrong(__FUNCTION__, php_sprintf(__("The post type %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post of that type."), post.post_type, cap), "4.4.0")
                caps[-1] = "edit_others_posts"
                break
            # end if
            caps[-1] = post_type.cap.publish_posts
            break
        # end if
        if case("edit_post_meta"):
            pass
        # end if
        if case("delete_post_meta"):
            pass
        # end if
        if case("add_post_meta"):
            pass
        # end if
        if case("edit_comment_meta"):
            pass
        # end if
        if case("delete_comment_meta"):
            pass
        # end if
        if case("add_comment_meta"):
            pass
        # end if
        if case("edit_term_meta"):
            pass
        # end if
        if case("delete_term_meta"):
            pass
        # end if
        if case("add_term_meta"):
            pass
        # end if
        if case("edit_user_meta"):
            pass
        # end if
        if case("delete_user_meta"):
            pass
        # end if
        if case("add_user_meta"):
            _, object_type, _ = php_explode("_", cap)
            object_id = php_int(args[0])
            object_subtype = get_object_subtype(object_type, object_id)
            if php_empty(lambda : object_subtype):
                caps[-1] = "do_not_allow"
                break
            # end if
            caps = map_meta_cap(str("edit_") + str(object_type), user_id, object_id)
            meta_key = args[1] if (php_isset(lambda : args[1])) else False
            if meta_key:
                allowed = (not is_protected_meta(meta_key, object_type))
                if (not php_empty(lambda : object_subtype)) and has_filter(str("auth_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype)):
                    #// 
                    #// Filters whether the user is allowed to edit a specific meta key of a specific object type and subtype.
                    #// 
                    #// The dynamic portions of the hook name, `$object_type`, `$meta_key`,
                    #// and `$object_subtype`, refer to the metadata object type (comment, post, term or user),
                    #// the meta key value, and the object subtype respectively.
                    #// 
                    #// @since 4.9.8
                    #// 
                    #// @param bool     $allowed   Whether the user can add the object meta. Default false.
                    #// @param string   $meta_key  The meta key.
                    #// @param int      $object_id Object ID.
                    #// @param int      $user_id   User ID.
                    #// @param string   $cap       Capability name.
                    #// @param string[] $caps      Array of the user's capabilities.
                    #//
                    allowed = apply_filters(str("auth_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype), allowed, meta_key, object_id, user_id, cap, caps)
                else:
                    #// 
                    #// Filters whether the user is allowed to edit a specific meta key of a specific object type.
                    #// 
                    #// Return true to have the mapped meta caps from `edit_{$object_type}` apply.
                    #// 
                    #// The dynamic portion of the hook name, `$object_type` refers to the object type being filtered.
                    #// The dynamic portion of the hook name, `$meta_key`, refers to the meta key passed to map_meta_cap().
                    #// 
                    #// @since 3.3.0 As `auth_post_meta_{$meta_key}`.
                    #// @since 4.6.0
                    #// 
                    #// @param bool     $allowed   Whether the user can add the object meta. Default false.
                    #// @param string   $meta_key  The meta key.
                    #// @param int      $object_id Object ID.
                    #// @param int      $user_id   User ID.
                    #// @param string   $cap       Capability name.
                    #// @param string[] $caps      Array of the user's capabilities.
                    #//
                    allowed = apply_filters(str("auth_") + str(object_type) + str("_meta_") + str(meta_key), allowed, meta_key, object_id, user_id, cap, caps)
                # end if
                if (not php_empty(lambda : object_subtype)):
                    #// 
                    #// Filters whether the user is allowed to edit meta for specific object types/subtypes.
                    #// 
                    #// Return true to have the mapped meta caps from `edit_{$object_type}` apply.
                    #// 
                    #// The dynamic portion of the hook name, `$object_type` refers to the object type being filtered.
                    #// The dynamic portion of the hook name, `$object_subtype` refers to the object subtype being filtered.
                    #// The dynamic portion of the hook name, `$meta_key`, refers to the meta key passed to map_meta_cap().
                    #// 
                    #// @since 4.6.0 As `auth_post_{$post_type}_meta_{$meta_key}`.
                    #// @since 4.7.0 Renamed from `auth_post_{$post_type}_meta_{$meta_key}` to
                    #// `auth_{$object_type}_{$object_subtype}_meta_{$meta_key}`.
                    #// @deprecated 4.9.8 Use {@see 'auth_{$object_type}_meta_{$meta_key}_for_{$object_subtype}'} instead.
                    #// 
                    #// @param bool     $allowed   Whether the user can add the object meta. Default false.
                    #// @param string   $meta_key  The meta key.
                    #// @param int      $object_id Object ID.
                    #// @param int      $user_id   User ID.
                    #// @param string   $cap       Capability name.
                    #// @param string[] $caps      Array of the user's capabilities.
                    #//
                    allowed = apply_filters_deprecated(str("auth_") + str(object_type) + str("_") + str(object_subtype) + str("_meta_") + str(meta_key), Array(allowed, meta_key, object_id, user_id, cap, caps), "4.9.8", str("auth_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype))
                # end if
                if (not allowed):
                    caps[-1] = cap
                # end if
            # end if
            break
        # end if
        if case("edit_comment"):
            comment = get_comment(args[0])
            if (not comment):
                caps[-1] = "do_not_allow"
                break
            # end if
            post = get_post(comment.comment_post_ID)
            #// 
            #// If the post doesn't exist, we have an orphaned comment.
            #// Fall back to the edit_posts capability, instead.
            #//
            if post:
                caps = map_meta_cap("edit_post", user_id, post.ID)
            else:
                caps = map_meta_cap("edit_posts", user_id)
            # end if
            break
        # end if
        if case("unfiltered_upload"):
            if php_defined("ALLOW_UNFILTERED_UPLOADS") and ALLOW_UNFILTERED_UPLOADS and (not is_multisite()) or is_super_admin(user_id):
                caps[-1] = cap
            else:
                caps[-1] = "do_not_allow"
            # end if
            break
        # end if
        if case("edit_css"):
            pass
        # end if
        if case("unfiltered_html"):
            #// Disallow unfiltered_html for all users, even admins and super admins.
            if php_defined("DISALLOW_UNFILTERED_HTML") and DISALLOW_UNFILTERED_HTML:
                caps[-1] = "do_not_allow"
            elif is_multisite() and (not is_super_admin(user_id)):
                caps[-1] = "do_not_allow"
            else:
                caps[-1] = "unfiltered_html"
            # end if
            break
        # end if
        if case("edit_files"):
            pass
        # end if
        if case("edit_plugins"):
            pass
        # end if
        if case("edit_themes"):
            #// Disallow the file editors.
            if php_defined("DISALLOW_FILE_EDIT") and DISALLOW_FILE_EDIT:
                caps[-1] = "do_not_allow"
            elif (not wp_is_file_mod_allowed("capability_edit_themes")):
                caps[-1] = "do_not_allow"
            elif is_multisite() and (not is_super_admin(user_id)):
                caps[-1] = "do_not_allow"
            else:
                caps[-1] = cap
            # end if
            break
        # end if
        if case("update_plugins"):
            pass
        # end if
        if case("delete_plugins"):
            pass
        # end if
        if case("install_plugins"):
            pass
        # end if
        if case("upload_plugins"):
            pass
        # end if
        if case("update_themes"):
            pass
        # end if
        if case("delete_themes"):
            pass
        # end if
        if case("install_themes"):
            pass
        # end if
        if case("upload_themes"):
            pass
        # end if
        if case("update_core"):
            #// Disallow anything that creates, deletes, or updates core, plugin, or theme files.
            #// Files in uploads are excepted.
            if (not wp_is_file_mod_allowed("capability_update_core")):
                caps[-1] = "do_not_allow"
            elif is_multisite() and (not is_super_admin(user_id)):
                caps[-1] = "do_not_allow"
            elif "upload_themes" == cap:
                caps[-1] = "install_themes"
            elif "upload_plugins" == cap:
                caps[-1] = "install_plugins"
            else:
                caps[-1] = cap
            # end if
            break
        # end if
        if case("install_languages"):
            pass
        # end if
        if case("update_languages"):
            if (not wp_is_file_mod_allowed("can_install_language_pack")):
                caps[-1] = "do_not_allow"
            elif is_multisite() and (not is_super_admin(user_id)):
                caps[-1] = "do_not_allow"
            else:
                caps[-1] = "install_languages"
            # end if
            break
        # end if
        if case("activate_plugins"):
            pass
        # end if
        if case("deactivate_plugins"):
            pass
        # end if
        if case("activate_plugin"):
            pass
        # end if
        if case("deactivate_plugin"):
            caps[-1] = "activate_plugins"
            if is_multisite():
                #// update_, install_, and delete_ are handled above with is_super_admin().
                menu_perms = get_site_option("menu_items", Array())
                if php_empty(lambda : menu_perms["plugins"]):
                    caps[-1] = "manage_network_plugins"
                # end if
            # end if
            break
        # end if
        if case("resume_plugin"):
            caps[-1] = "resume_plugins"
            break
        # end if
        if case("resume_theme"):
            caps[-1] = "resume_themes"
            break
        # end if
        if case("delete_user"):
            pass
        # end if
        if case("delete_users"):
            #// If multisite only super admins can delete users.
            if is_multisite() and (not is_super_admin(user_id)):
                caps[-1] = "do_not_allow"
            else:
                caps[-1] = "delete_users"
                pass
            # end if
            break
        # end if
        if case("create_users"):
            if (not is_multisite()):
                caps[-1] = cap
            elif is_super_admin(user_id) or get_site_option("add_new_users"):
                caps[-1] = cap
            else:
                caps[-1] = "do_not_allow"
            # end if
            break
        # end if
        if case("manage_links"):
            if get_option("link_manager_enabled"):
                caps[-1] = cap
            else:
                caps[-1] = "do_not_allow"
            # end if
            break
        # end if
        if case("customize"):
            caps[-1] = "edit_theme_options"
            break
        # end if
        if case("delete_site"):
            if is_multisite():
                caps[-1] = "manage_options"
            else:
                caps[-1] = "do_not_allow"
            # end if
            break
        # end if
        if case("edit_term"):
            pass
        # end if
        if case("delete_term"):
            pass
        # end if
        if case("assign_term"):
            term_id = php_int(args[0])
            term = get_term(term_id)
            if (not term) or is_wp_error(term):
                caps[-1] = "do_not_allow"
                break
            # end if
            tax = get_taxonomy(term.taxonomy)
            if (not tax):
                caps[-1] = "do_not_allow"
                break
            # end if
            if "delete_term" == cap and get_option("default_" + term.taxonomy) == term.term_id:
                caps[-1] = "do_not_allow"
                break
            # end if
            taxo_cap = cap + "s"
            caps = map_meta_cap(tax.cap.taxo_cap, user_id, term_id)
            break
        # end if
        if case("manage_post_tags"):
            pass
        # end if
        if case("edit_categories"):
            pass
        # end if
        if case("edit_post_tags"):
            pass
        # end if
        if case("delete_categories"):
            pass
        # end if
        if case("delete_post_tags"):
            caps[-1] = "manage_categories"
            break
        # end if
        if case("assign_categories"):
            pass
        # end if
        if case("assign_post_tags"):
            caps[-1] = "edit_posts"
            break
        # end if
        if case("create_sites"):
            pass
        # end if
        if case("delete_sites"):
            pass
        # end if
        if case("manage_network"):
            pass
        # end if
        if case("manage_sites"):
            pass
        # end if
        if case("manage_network_users"):
            pass
        # end if
        if case("manage_network_plugins"):
            pass
        # end if
        if case("manage_network_themes"):
            pass
        # end if
        if case("manage_network_options"):
            pass
        # end if
        if case("upgrade_network"):
            caps[-1] = cap
            break
        # end if
        if case("setup_network"):
            if is_multisite():
                caps[-1] = "manage_network_options"
            else:
                caps[-1] = "manage_options"
            # end if
            break
        # end if
        if case("update_php"):
            if is_multisite() and (not is_super_admin(user_id)):
                caps[-1] = "do_not_allow"
            else:
                caps[-1] = "update_core"
            # end if
            break
        # end if
        if case("export_others_personal_data"):
            pass
        # end if
        if case("erase_others_personal_data"):
            pass
        # end if
        if case("manage_privacy_options"):
            caps[-1] = "manage_network" if is_multisite() else "manage_options"
            break
        # end if
        if case():
            #// Handle meta capabilities for custom post types.
            global post_type_meta_caps
            php_check_if_defined("post_type_meta_caps")
            if (php_isset(lambda : post_type_meta_caps[cap])):
                return map_meta_cap(post_type_meta_caps[cap], user_id, args)
            # end if
            #// Block capabilities map to their post equivalent.
            block_caps = Array("edit_blocks", "edit_others_blocks", "publish_blocks", "read_private_blocks", "delete_blocks", "delete_private_blocks", "delete_published_blocks", "delete_others_blocks", "edit_private_blocks", "edit_published_blocks")
            if php_in_array(cap, block_caps, True):
                cap = php_str_replace("_blocks", "_posts", cap)
            # end if
            #// If no meta caps match, return the original cap.
            caps[-1] = cap
        # end if
    # end for
    #// 
    #// Filters a user's capabilities depending on specific context and/or privilege.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string[] $caps    Array of the user's capabilities.
    #// @param string   $cap     Capability name.
    #// @param int      $user_id The user ID.
    #// @param array    $args    Adds the context to the cap. Typically the object ID.
    #//
    return apply_filters("map_meta_cap", caps, cap, user_id, args)
# end def map_meta_cap
#// 
#// Returns whether the current user has the specified capability.
#// 
#// This function also accepts an ID of an object to check against if the capability is a meta capability. Meta
#// capabilities such as `edit_post` and `edit_user` are capabilities used by the `map_meta_cap()` function to
#// map to primitive capabilities that a user or role has, such as `edit_posts` and `edit_others_posts`.
#// 
#// Example usage:
#// 
#// current_user_can( 'edit_posts' );
#// current_user_can( 'edit_post', $post->ID );
#// current_user_can( 'edit_post_meta', $post->ID, $meta_key );
#// 
#// While checking against particular roles in place of a capability is supported
#// in part, this practice is discouraged as it may produce unreliable results.
#// 
#// Note: Will always return true if the current user is a super admin, unless specifically denied.
#// 
#// @since 2.0.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @see WP_User::has_cap()
#// @see map_meta_cap()
#// 
#// @param string $capability Capability name.
#// @param mixed  ...$args    Optional further parameters, typically starting with an object ID.
#// @return bool Whether the current user has the given capability. If `$capability` is a meta cap and `$object_id` is
#// passed, whether the current user has the given meta capability for the given object.
#//
def current_user_can(capability=None, *args):
    
    current_user = wp_get_current_user()
    if php_empty(lambda : current_user):
        return False
    # end if
    return current_user.has_cap(capability, args)
# end def current_user_can
#// 
#// Returns whether the current user has the specified capability for a given site.
#// 
#// This function also accepts an ID of an object to check against if the capability is a meta capability. Meta
#// capabilities such as `edit_post` and `edit_user` are capabilities used by the `map_meta_cap()` function to
#// map to primitive capabilities that a user or role has, such as `edit_posts` and `edit_others_posts`.
#// 
#// Example usage:
#// 
#// current_user_can_for_blog( $blog_id, 'edit_posts' );
#// current_user_can_for_blog( $blog_id, 'edit_post', $post->ID );
#// current_user_can_for_blog( $blog_id, 'edit_post_meta', $post->ID, $meta_key );
#// 
#// @since 3.0.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @param int    $blog_id    Site ID.
#// @param string $capability Capability name.
#// @param mixed  ...$args    Optional further parameters, typically starting with an object ID.
#// @return bool Whether the user has the given capability.
#//
def current_user_can_for_blog(blog_id=None, capability=None, *args):
    
    switched = switch_to_blog(blog_id) if is_multisite() else False
    current_user = wp_get_current_user()
    if php_empty(lambda : current_user):
        if switched:
            restore_current_blog()
        # end if
        return False
    # end if
    can = current_user.has_cap(capability, args)
    if switched:
        restore_current_blog()
    # end if
    return can
# end def current_user_can_for_blog
#// 
#// Returns whether the author of the supplied post has the specified capability.
#// 
#// This function also accepts an ID of an object to check against if the capability is a meta capability. Meta
#// capabilities such as `edit_post` and `edit_user` are capabilities used by the `map_meta_cap()` function to
#// map to primitive capabilities that a user or role has, such as `edit_posts` and `edit_others_posts`.
#// 
#// Example usage:
#// 
#// author_can( $post, 'edit_posts' );
#// author_can( $post, 'edit_post', $post->ID );
#// author_can( $post, 'edit_post_meta', $post->ID, $meta_key );
#// 
#// @since 2.9.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @param int|WP_Post $post       Post ID or post object.
#// @param string      $capability Capability name.
#// @param mixed       ...$args    Optional further parameters, typically starting with an object ID.
#// @return bool Whether the post author has the given capability.
#//
def author_can(post=None, capability=None, *args):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    author = get_userdata(post.post_author)
    if (not author):
        return False
    # end if
    return author.has_cap(capability, args)
# end def author_can
#// 
#// Returns whether a particular user has the specified capability.
#// 
#// This function also accepts an ID of an object to check against if the capability is a meta capability. Meta
#// capabilities such as `edit_post` and `edit_user` are capabilities used by the `map_meta_cap()` function to
#// map to primitive capabilities that a user or role has, such as `edit_posts` and `edit_others_posts`.
#// 
#// Example usage:
#// 
#// user_can( $user->ID, 'edit_posts' );
#// user_can( $user->ID, 'edit_post', $post->ID );
#// user_can( $user->ID, 'edit_post_meta', $post->ID, $meta_key );
#// 
#// @since 3.1.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @param int|WP_User $user       User ID or object.
#// @param string      $capability Capability name.
#// @param mixed       ...$args    Optional further parameters, typically starting with an object ID.
#// @return bool Whether the user has the given capability.
#//
def user_can(user=None, capability=None, *args):
    
    if (not php_is_object(user)):
        user = get_userdata(user)
    # end if
    if (not user) or (not user.exists()):
        return False
    # end if
    return user.has_cap(capability, args)
# end def user_can
#// 
#// Retrieves the global WP_Roles instance and instantiates it if necessary.
#// 
#// @since 4.3.0
#// 
#// @global WP_Roles $wp_roles WordPress role management object.
#// 
#// @return WP_Roles WP_Roles global instance if not already instantiated.
#//
def wp_roles(*args_):
    
    global wp_roles
    php_check_if_defined("wp_roles")
    if (not (php_isset(lambda : wp_roles))):
        wp_roles = php_new_class("WP_Roles", lambda : WP_Roles())
    # end if
    return wp_roles
# end def wp_roles
#// 
#// Retrieve role object.
#// 
#// @since 2.0.0
#// 
#// @param string $role Role name.
#// @return WP_Role|null WP_Role object if found, null if the role does not exist.
#//
def get_role(role=None, *args_):
    
    return wp_roles().get_role(role)
# end def get_role
#// 
#// Add role, if it does not exist.
#// 
#// @since 2.0.0
#// 
#// @param string $role         Role name.
#// @param string $display_name Display name for role.
#// @param bool[] $capabilities List of capabilities keyed by the capability name,
#// e.g. array( 'edit_posts' => true, 'delete_posts' => false ).
#// @return WP_Role|null WP_Role object if role is added, null if already exists.
#//
def add_role(role=None, display_name=None, capabilities=Array(), *args_):
    
    if php_empty(lambda : role):
        return
    # end if
    return wp_roles().add_role(role, display_name, capabilities)
# end def add_role
#// 
#// Remove role, if it exists.
#// 
#// @since 2.0.0
#// 
#// @param string $role Role name.
#//
def remove_role(role=None, *args_):
    
    wp_roles().remove_role(role)
# end def remove_role
#// 
#// Retrieve a list of super admins.
#// 
#// @since 3.0.0
#// 
#// @global array $super_admins
#// 
#// @return string[] List of super admin logins.
#//
def get_super_admins(*args_):
    
    global super_admins
    php_check_if_defined("super_admins")
    if (php_isset(lambda : super_admins)):
        return super_admins
    else:
        return get_site_option("site_admins", Array("admin"))
    # end if
# end def get_super_admins
#// 
#// Determine if user is a site admin.
#// 
#// @since 3.0.0
#// 
#// @param int $user_id (Optional) The ID of a user. Defaults to the current user.
#// @return bool True if the user is a site admin.
#//
def is_super_admin(user_id=False, *args_):
    
    if (not user_id) or get_current_user_id() == user_id:
        user = wp_get_current_user()
    else:
        user = get_userdata(user_id)
    # end if
    if (not user) or (not user.exists()):
        return False
    # end if
    if is_multisite():
        super_admins = get_super_admins()
        if php_is_array(super_admins) and php_in_array(user.user_login, super_admins):
            return True
        # end if
    else:
        if user.has_cap("delete_users"):
            return True
        # end if
    # end if
    return False
# end def is_super_admin
#// 
#// Grants Super Admin privileges.
#// 
#// @since 3.0.0
#// 
#// @global array $super_admins
#// 
#// @param int $user_id ID of the user to be granted Super Admin privileges.
#// @return bool True on success, false on failure. This can fail when the user is
#// already a super admin or when the `$super_admins` global is defined.
#//
def grant_super_admin(user_id=None, *args_):
    
    #// If global super_admins override is defined, there is nothing to do here.
    if (php_isset(lambda : PHP_GLOBALS["super_admins"])) or (not is_multisite()):
        return False
    # end if
    #// 
    #// Fires before the user is granted Super Admin privileges.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int $user_id ID of the user that is about to be granted Super Admin privileges.
    #//
    do_action("grant_super_admin", user_id)
    #// Directly fetch site_admins instead of using get_super_admins().
    super_admins = get_site_option("site_admins", Array("admin"))
    user = get_userdata(user_id)
    if user and (not php_in_array(user.user_login, super_admins)):
        super_admins[-1] = user.user_login
        update_site_option("site_admins", super_admins)
        #// 
        #// Fires after the user is granted Super Admin privileges.
        #// 
        #// @since 3.0.0
        #// 
        #// @param int $user_id ID of the user that was granted Super Admin privileges.
        #//
        do_action("granted_super_admin", user_id)
        return True
    # end if
    return False
# end def grant_super_admin
#// 
#// Revokes Super Admin privileges.
#// 
#// @since 3.0.0
#// 
#// @global array $super_admins
#// 
#// @param int $user_id ID of the user Super Admin privileges to be revoked from.
#// @return bool True on success, false on failure. This can fail when the user's email
#// is the network admin email or when the `$super_admins` global is defined.
#//
def revoke_super_admin(user_id=None, *args_):
    
    #// If global super_admins override is defined, there is nothing to do here.
    if (php_isset(lambda : PHP_GLOBALS["super_admins"])) or (not is_multisite()):
        return False
    # end if
    #// 
    #// Fires before the user's Super Admin privileges are revoked.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int $user_id ID of the user Super Admin privileges are being revoked from.
    #//
    do_action("revoke_super_admin", user_id)
    #// Directly fetch site_admins instead of using get_super_admins().
    super_admins = get_site_option("site_admins", Array("admin"))
    user = get_userdata(user_id)
    if user and 0 != strcasecmp(user.user_email, get_site_option("admin_email")):
        key = php_array_search(user.user_login, super_admins)
        if False != key:
            super_admins[key] = None
            update_site_option("site_admins", super_admins)
            #// 
            #// Fires after the user's Super Admin privileges are revoked.
            #// 
            #// @since 3.0.0
            #// 
            #// @param int $user_id ID of the user Super Admin privileges were revoked from.
            #//
            do_action("revoked_super_admin", user_id)
            return True
        # end if
    # end if
    return False
# end def revoke_super_admin
#// 
#// Filters the user capabilities to grant the 'install_languages' capability as necessary.
#// 
#// A user must have at least one out of the 'update_core', 'install_plugins', and
#// 'install_themes' capabilities to qualify for 'install_languages'.
#// 
#// @since 4.9.0
#// 
#// @param bool[] $allcaps An array of all the user's capabilities.
#// @return bool[] Filtered array of the user's capabilities.
#//
def wp_maybe_grant_install_languages_cap(allcaps=None, *args_):
    
    if (not php_empty(lambda : allcaps["update_core"])) or (not php_empty(lambda : allcaps["install_plugins"])) or (not php_empty(lambda : allcaps["install_themes"])):
        allcaps["install_languages"] = True
    # end if
    return allcaps
# end def wp_maybe_grant_install_languages_cap
#// 
#// Filters the user capabilities to grant the 'resume_plugins' and 'resume_themes' capabilities as necessary.
#// 
#// @since 5.2.0
#// 
#// @param bool[] $allcaps An array of all the user's capabilities.
#// @return bool[] Filtered array of the user's capabilities.
#//
def wp_maybe_grant_resume_extensions_caps(allcaps=None, *args_):
    
    #// Even in a multisite, regular administrators should be able to resume plugins.
    if (not php_empty(lambda : allcaps["activate_plugins"])):
        allcaps["resume_plugins"] = True
    # end if
    #// Even in a multisite, regular administrators should be able to resume themes.
    if (not php_empty(lambda : allcaps["switch_themes"])):
        allcaps["resume_themes"] = True
    # end if
    return allcaps
# end def wp_maybe_grant_resume_extensions_caps
#// 
#// Filters the user capabilities to grant the 'view_site_health_checks' capabilities as necessary.
#// 
#// @since 5.2.2
#// 
#// @param bool[]   $allcaps An array of all the user's capabilities.
#// @param string[] $caps    Required primitive capabilities for the requested capability.
#// @param array    $args {
#// Arguments that accompany the requested capability check.
#// 
#// @type string    $0 Requested capability.
#// @type int       $1 Concerned user ID.
#// @type mixed  ...$2 Optional second and further parameters, typically object ID.
#// }
#// @param WP_User  $user    The user object.
#// @return bool[] Filtered array of the user's capabilities.
#//
def wp_maybe_grant_site_health_caps(allcaps=None, caps=None, args=None, user=None, *args_):
    
    if (not php_empty(lambda : allcaps["install_plugins"])) and (not is_multisite()) or is_super_admin(user.ID):
        allcaps["view_site_health_checks"] = True
    # end if
    return allcaps
# end def wp_maybe_grant_site_health_caps
sys.exit(-1)
#// Dummy gettext calls to get strings in the catalog.
#// translators: User role for administrators.
_x("Administrator", "User role")
#// translators: User role for editors.
_x("Editor", "User role")
#// translators: User role for authors.
_x("Author", "User role")
#// translators: User role for contributors.
_x("Contributor", "User role")
#// translators: User role for subscribers.
_x("Subscriber", "User role")
