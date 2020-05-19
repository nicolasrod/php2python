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
def map_meta_cap(cap_=None, user_id_=None, *args_):
    
    
    caps_ = Array()
    for case in Switch(cap_):
        if case("remove_user"):
            #// In multisite the user must be a super admin to remove themselves.
            if (php_isset(lambda : args_[0])) and user_id_ == args_[0] and (not is_super_admin(user_id_)):
                caps_[-1] = "do_not_allow"
            else:
                caps_[-1] = "remove_users"
            # end if
            break
        # end if
        if case("promote_user"):
            pass
        # end if
        if case("add_users"):
            caps_[-1] = "promote_users"
            break
        # end if
        if case("edit_user"):
            pass
        # end if
        if case("edit_users"):
            #// Allow user to edit themselves.
            if "edit_user" == cap_ and (php_isset(lambda : args_[0])) and user_id_ == args_[0]:
                break
            # end if
            #// In multisite the user must have manage_network_users caps. If editing a super admin, the user must be a super admin.
            if is_multisite() and (not is_super_admin(user_id_)) and "edit_user" == cap_ and is_super_admin(args_[0]) or (not user_can(user_id_, "manage_network_users")):
                caps_[-1] = "do_not_allow"
            else:
                caps_[-1] = "edit_users"
                pass
            # end if
            break
        # end if
        if case("delete_post"):
            pass
        # end if
        if case("delete_page"):
            post_ = get_post(args_[0])
            if (not post_):
                caps_[-1] = "do_not_allow"
                break
            # end if
            if "revision" == post_.post_type:
                caps_[-1] = "do_not_allow"
                break
            # end if
            if get_option("page_for_posts") == post_.ID or get_option("page_on_front") == post_.ID:
                caps_[-1] = "manage_options"
                break
            # end if
            post_type_ = get_post_type_object(post_.post_type)
            if (not post_type_):
                #// translators: 1: Post type, 2: Capability name.
                _doing_it_wrong(inspect.currentframe().f_code.co_name, php_sprintf(__("The post type %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post of that type."), post_.post_type, cap_), "4.4.0")
                caps_[-1] = "edit_others_posts"
                break
            # end if
            if (not post_type_.map_meta_cap):
                caps_[-1] = post_type_.cap.cap_
                #// Prior to 3.1 we would re-call map_meta_cap here.
                if "delete_post" == cap_:
                    cap_ = post_type_.cap.cap_
                # end if
                break
            # end if
            #// If the post author is set and the user is the author...
            if post_.post_author and user_id_ == post_.post_author:
                #// If the post is published or scheduled...
                if php_in_array(post_.post_status, Array("publish", "future"), True):
                    caps_[-1] = post_type_.cap.delete_published_posts
                elif "trash" == post_.post_status:
                    status_ = get_post_meta(post_.ID, "_wp_trash_meta_status", True)
                    if php_in_array(status_, Array("publish", "future"), True):
                        caps_[-1] = post_type_.cap.delete_published_posts
                    else:
                        caps_[-1] = post_type_.cap.delete_posts
                    # end if
                else:
                    #// If the post is draft...
                    caps_[-1] = post_type_.cap.delete_posts
                # end if
            else:
                #// The user is trying to edit someone else's post.
                caps_[-1] = post_type_.cap.delete_others_posts
                #// The post is published or scheduled, extra cap required.
                if php_in_array(post_.post_status, Array("publish", "future"), True):
                    caps_[-1] = post_type_.cap.delete_published_posts
                elif "private" == post_.post_status:
                    caps_[-1] = post_type_.cap.delete_private_posts
                # end if
            # end if
            #// 
            #// Setting the privacy policy page requires `manage_privacy_options`,
            #// so deleting it should require that too.
            #//
            if php_int(get_option("wp_page_for_privacy_policy")) == post_.ID:
                caps_ = php_array_merge(caps_, map_meta_cap("manage_privacy_options", user_id_))
            # end if
            break
        # end if
        if case("edit_post"):
            pass
        # end if
        if case("edit_page"):
            post_ = get_post(args_[0])
            if (not post_):
                caps_[-1] = "do_not_allow"
                break
            # end if
            if "revision" == post_.post_type:
                post_ = get_post(post_.post_parent)
                if (not post_):
                    caps_[-1] = "do_not_allow"
                    break
                # end if
            # end if
            post_type_ = get_post_type_object(post_.post_type)
            if (not post_type_):
                #// translators: 1: Post type, 2: Capability name.
                _doing_it_wrong(inspect.currentframe().f_code.co_name, php_sprintf(__("The post type %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post of that type."), post_.post_type, cap_), "4.4.0")
                caps_[-1] = "edit_others_posts"
                break
            # end if
            if (not post_type_.map_meta_cap):
                caps_[-1] = post_type_.cap.cap_
                #// Prior to 3.1 we would re-call map_meta_cap here.
                if "edit_post" == cap_:
                    cap_ = post_type_.cap.cap_
                # end if
                break
            # end if
            #// If the post author is set and the user is the author...
            if post_.post_author and user_id_ == post_.post_author:
                #// If the post is published or scheduled...
                if php_in_array(post_.post_status, Array("publish", "future"), True):
                    caps_[-1] = post_type_.cap.edit_published_posts
                elif "trash" == post_.post_status:
                    status_ = get_post_meta(post_.ID, "_wp_trash_meta_status", True)
                    if php_in_array(status_, Array("publish", "future"), True):
                        caps_[-1] = post_type_.cap.edit_published_posts
                    else:
                        caps_[-1] = post_type_.cap.edit_posts
                    # end if
                else:
                    #// If the post is draft...
                    caps_[-1] = post_type_.cap.edit_posts
                # end if
            else:
                #// The user is trying to edit someone else's post.
                caps_[-1] = post_type_.cap.edit_others_posts
                #// The post is published or scheduled, extra cap required.
                if php_in_array(post_.post_status, Array("publish", "future"), True):
                    caps_[-1] = post_type_.cap.edit_published_posts
                elif "private" == post_.post_status:
                    caps_[-1] = post_type_.cap.edit_private_posts
                # end if
            # end if
            #// 
            #// Setting the privacy policy page requires `manage_privacy_options`,
            #// so editing it should require that too.
            #//
            if php_int(get_option("wp_page_for_privacy_policy")) == post_.ID:
                caps_ = php_array_merge(caps_, map_meta_cap("manage_privacy_options", user_id_))
            # end if
            break
        # end if
        if case("read_post"):
            pass
        # end if
        if case("read_page"):
            post_ = get_post(args_[0])
            if (not post_):
                caps_[-1] = "do_not_allow"
                break
            # end if
            if "revision" == post_.post_type:
                post_ = get_post(post_.post_parent)
                if (not post_):
                    caps_[-1] = "do_not_allow"
                    break
                # end if
            # end if
            post_type_ = get_post_type_object(post_.post_type)
            if (not post_type_):
                #// translators: 1: Post type, 2: Capability name.
                _doing_it_wrong(inspect.currentframe().f_code.co_name, php_sprintf(__("The post type %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post of that type."), post_.post_type, cap_), "4.4.0")
                caps_[-1] = "edit_others_posts"
                break
            # end if
            if (not post_type_.map_meta_cap):
                caps_[-1] = post_type_.cap.cap_
                #// Prior to 3.1 we would re-call map_meta_cap here.
                if "read_post" == cap_:
                    cap_ = post_type_.cap.cap_
                # end if
                break
            # end if
            status_obj_ = get_post_status_object(post_.post_status)
            if (not status_obj_):
                #// translators: 1: Post status, 2: Capability name.
                _doing_it_wrong(inspect.currentframe().f_code.co_name, php_sprintf(__("The post status %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post with that status."), post_.post_status, cap_), "5.4.0")
                caps_[-1] = "edit_others_posts"
                break
            # end if
            if status_obj_.public:
                caps_[-1] = post_type_.cap.read
                break
            # end if
            if post_.post_author and user_id_ == post_.post_author:
                caps_[-1] = post_type_.cap.read
            elif status_obj_.private:
                caps_[-1] = post_type_.cap.read_private_posts
            else:
                caps_ = map_meta_cap("edit_post", user_id_, post_.ID)
            # end if
            break
        # end if
        if case("publish_post"):
            post_ = get_post(args_[0])
            if (not post_):
                caps_[-1] = "do_not_allow"
                break
            # end if
            post_type_ = get_post_type_object(post_.post_type)
            if (not post_type_):
                #// translators: 1: Post type, 2: Capability name.
                _doing_it_wrong(inspect.currentframe().f_code.co_name, php_sprintf(__("The post type %1$s is not registered, so it may not be reliable to check the capability \"%2$s\" against a post of that type."), post_.post_type, cap_), "4.4.0")
                caps_[-1] = "edit_others_posts"
                break
            # end if
            caps_[-1] = post_type_.cap.publish_posts
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
            __, object_type_, __ = php_explode("_", cap_)
            object_id_ = php_int(args_[0])
            object_subtype_ = get_object_subtype(object_type_, object_id_)
            if php_empty(lambda : object_subtype_):
                caps_[-1] = "do_not_allow"
                break
            # end if
            caps_ = map_meta_cap(str("edit_") + str(object_type_), user_id_, object_id_)
            meta_key_ = args_[1] if (php_isset(lambda : args_[1])) else False
            if meta_key_:
                allowed_ = (not is_protected_meta(meta_key_, object_type_))
                if (not php_empty(lambda : object_subtype_)) and has_filter(str("auth_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_)):
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
                    allowed_ = apply_filters(str("auth_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_), allowed_, meta_key_, object_id_, user_id_, cap_, caps_)
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
                    allowed_ = apply_filters(str("auth_") + str(object_type_) + str("_meta_") + str(meta_key_), allowed_, meta_key_, object_id_, user_id_, cap_, caps_)
                # end if
                if (not php_empty(lambda : object_subtype_)):
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
                    allowed_ = apply_filters_deprecated(str("auth_") + str(object_type_) + str("_") + str(object_subtype_) + str("_meta_") + str(meta_key_), Array(allowed_, meta_key_, object_id_, user_id_, cap_, caps_), "4.9.8", str("auth_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_))
                # end if
                if (not allowed_):
                    caps_[-1] = cap_
                # end if
            # end if
            break
        # end if
        if case("edit_comment"):
            comment_ = get_comment(args_[0])
            if (not comment_):
                caps_[-1] = "do_not_allow"
                break
            # end if
            post_ = get_post(comment_.comment_post_ID)
            #// 
            #// If the post doesn't exist, we have an orphaned comment.
            #// Fall back to the edit_posts capability, instead.
            #//
            if post_:
                caps_ = map_meta_cap("edit_post", user_id_, post_.ID)
            else:
                caps_ = map_meta_cap("edit_posts", user_id_)
            # end if
            break
        # end if
        if case("unfiltered_upload"):
            if php_defined("ALLOW_UNFILTERED_UPLOADS") and ALLOW_UNFILTERED_UPLOADS and (not is_multisite()) or is_super_admin(user_id_):
                caps_[-1] = cap_
            else:
                caps_[-1] = "do_not_allow"
            # end if
            break
        # end if
        if case("edit_css"):
            pass
        # end if
        if case("unfiltered_html"):
            #// Disallow unfiltered_html for all users, even admins and super admins.
            if php_defined("DISALLOW_UNFILTERED_HTML") and DISALLOW_UNFILTERED_HTML:
                caps_[-1] = "do_not_allow"
            elif is_multisite() and (not is_super_admin(user_id_)):
                caps_[-1] = "do_not_allow"
            else:
                caps_[-1] = "unfiltered_html"
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
                caps_[-1] = "do_not_allow"
            elif (not wp_is_file_mod_allowed("capability_edit_themes")):
                caps_[-1] = "do_not_allow"
            elif is_multisite() and (not is_super_admin(user_id_)):
                caps_[-1] = "do_not_allow"
            else:
                caps_[-1] = cap_
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
                caps_[-1] = "do_not_allow"
            elif is_multisite() and (not is_super_admin(user_id_)):
                caps_[-1] = "do_not_allow"
            elif "upload_themes" == cap_:
                caps_[-1] = "install_themes"
            elif "upload_plugins" == cap_:
                caps_[-1] = "install_plugins"
            else:
                caps_[-1] = cap_
            # end if
            break
        # end if
        if case("install_languages"):
            pass
        # end if
        if case("update_languages"):
            if (not wp_is_file_mod_allowed("can_install_language_pack")):
                caps_[-1] = "do_not_allow"
            elif is_multisite() and (not is_super_admin(user_id_)):
                caps_[-1] = "do_not_allow"
            else:
                caps_[-1] = "install_languages"
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
            caps_[-1] = "activate_plugins"
            if is_multisite():
                #// update_, install_, and delete_ are handled above with is_super_admin().
                menu_perms_ = get_site_option("menu_items", Array())
                if php_empty(lambda : menu_perms_["plugins"]):
                    caps_[-1] = "manage_network_plugins"
                # end if
            # end if
            break
        # end if
        if case("resume_plugin"):
            caps_[-1] = "resume_plugins"
            break
        # end if
        if case("resume_theme"):
            caps_[-1] = "resume_themes"
            break
        # end if
        if case("delete_user"):
            pass
        # end if
        if case("delete_users"):
            #// If multisite only super admins can delete users.
            if is_multisite() and (not is_super_admin(user_id_)):
                caps_[-1] = "do_not_allow"
            else:
                caps_[-1] = "delete_users"
                pass
            # end if
            break
        # end if
        if case("create_users"):
            if (not is_multisite()):
                caps_[-1] = cap_
            elif is_super_admin(user_id_) or get_site_option("add_new_users"):
                caps_[-1] = cap_
            else:
                caps_[-1] = "do_not_allow"
            # end if
            break
        # end if
        if case("manage_links"):
            if get_option("link_manager_enabled"):
                caps_[-1] = cap_
            else:
                caps_[-1] = "do_not_allow"
            # end if
            break
        # end if
        if case("customize"):
            caps_[-1] = "edit_theme_options"
            break
        # end if
        if case("delete_site"):
            if is_multisite():
                caps_[-1] = "manage_options"
            else:
                caps_[-1] = "do_not_allow"
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
            term_id_ = php_int(args_[0])
            term_ = get_term(term_id_)
            if (not term_) or is_wp_error(term_):
                caps_[-1] = "do_not_allow"
                break
            # end if
            tax_ = get_taxonomy(term_.taxonomy)
            if (not tax_):
                caps_[-1] = "do_not_allow"
                break
            # end if
            if "delete_term" == cap_ and get_option("default_" + term_.taxonomy) == term_.term_id:
                caps_[-1] = "do_not_allow"
                break
            # end if
            taxo_cap_ = cap_ + "s"
            caps_ = map_meta_cap(tax_.cap.taxo_cap_, user_id_, term_id_)
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
            caps_[-1] = "manage_categories"
            break
        # end if
        if case("assign_categories"):
            pass
        # end if
        if case("assign_post_tags"):
            caps_[-1] = "edit_posts"
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
            caps_[-1] = cap_
            break
        # end if
        if case("setup_network"):
            if is_multisite():
                caps_[-1] = "manage_network_options"
            else:
                caps_[-1] = "manage_options"
            # end if
            break
        # end if
        if case("update_php"):
            if is_multisite() and (not is_super_admin(user_id_)):
                caps_[-1] = "do_not_allow"
            else:
                caps_[-1] = "update_core"
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
            caps_[-1] = "manage_network" if is_multisite() else "manage_options"
            break
        # end if
        if case():
            #// Handle meta capabilities for custom post types.
            global post_type_meta_caps_
            php_check_if_defined("post_type_meta_caps_")
            if (php_isset(lambda : post_type_meta_caps_[cap_])):
                return map_meta_cap(post_type_meta_caps_[cap_], user_id_, args_)
            # end if
            #// Block capabilities map to their post equivalent.
            block_caps_ = Array("edit_blocks", "edit_others_blocks", "publish_blocks", "read_private_blocks", "delete_blocks", "delete_private_blocks", "delete_published_blocks", "delete_others_blocks", "edit_private_blocks", "edit_published_blocks")
            if php_in_array(cap_, block_caps_, True):
                cap_ = php_str_replace("_blocks", "_posts", cap_)
            # end if
            #// If no meta caps match, return the original cap.
            caps_[-1] = cap_
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
    return apply_filters("map_meta_cap", caps_, cap_, user_id_, args_)
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
def current_user_can(capability_=None, *args_):
    
    
    current_user_ = wp_get_current_user()
    if php_empty(lambda : current_user_):
        return False
    # end if
    return current_user_.has_cap(capability_, args_)
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
def current_user_can_for_blog(blog_id_=None, capability_=None, *args_):
    
    
    switched_ = switch_to_blog(blog_id_) if is_multisite() else False
    current_user_ = wp_get_current_user()
    if php_empty(lambda : current_user_):
        if switched_:
            restore_current_blog()
        # end if
        return False
    # end if
    can_ = current_user_.has_cap(capability_, args_)
    if switched_:
        restore_current_blog()
    # end if
    return can_
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
def author_can(post_=None, capability_=None, *args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    author_ = get_userdata(post_.post_author)
    if (not author_):
        return False
    # end if
    return author_.has_cap(capability_, args_)
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
def user_can(user_=None, capability_=None, *args_):
    
    
    if (not php_is_object(user_)):
        user_ = get_userdata(user_)
    # end if
    if (not user_) or (not user_.exists()):
        return False
    # end if
    return user_.has_cap(capability_, args_)
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
def wp_roles(*_args_):
    
    
    global wp_roles_
    php_check_if_defined("wp_roles_")
    if (not (php_isset(lambda : wp_roles_))):
        wp_roles_ = php_new_class("WP_Roles", lambda : WP_Roles())
    # end if
    return wp_roles_
# end def wp_roles
#// 
#// Retrieve role object.
#// 
#// @since 2.0.0
#// 
#// @param string $role Role name.
#// @return WP_Role|null WP_Role object if found, null if the role does not exist.
#//
def get_role(role_=None, *_args_):
    
    
    return wp_roles().get_role(role_)
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
def add_role(role_=None, display_name_=None, capabilities_=None, *_args_):
    if capabilities_ is None:
        capabilities_ = Array()
    # end if
    
    if php_empty(lambda : role_):
        return
    # end if
    return wp_roles().add_role(role_, display_name_, capabilities_)
# end def add_role
#// 
#// Remove role, if it exists.
#// 
#// @since 2.0.0
#// 
#// @param string $role Role name.
#//
def remove_role(role_=None, *_args_):
    
    
    wp_roles().remove_role(role_)
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
def get_super_admins(*_args_):
    
    
    global super_admins_
    php_check_if_defined("super_admins_")
    if (php_isset(lambda : super_admins_)):
        return super_admins_
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
def is_super_admin(user_id_=None, *_args_):
    if user_id_ is None:
        user_id_ = False
    # end if
    
    if (not user_id_) or get_current_user_id() == user_id_:
        user_ = wp_get_current_user()
    else:
        user_ = get_userdata(user_id_)
    # end if
    if (not user_) or (not user_.exists()):
        return False
    # end if
    if is_multisite():
        super_admins_ = get_super_admins()
        if php_is_array(super_admins_) and php_in_array(user_.user_login, super_admins_):
            return True
        # end if
    else:
        if user_.has_cap("delete_users"):
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
def grant_super_admin(user_id_=None, *_args_):
    
    
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
    do_action("grant_super_admin", user_id_)
    #// Directly fetch site_admins instead of using get_super_admins().
    super_admins_ = get_site_option("site_admins", Array("admin"))
    user_ = get_userdata(user_id_)
    if user_ and (not php_in_array(user_.user_login, super_admins_)):
        super_admins_[-1] = user_.user_login
        update_site_option("site_admins", super_admins_)
        #// 
        #// Fires after the user is granted Super Admin privileges.
        #// 
        #// @since 3.0.0
        #// 
        #// @param int $user_id ID of the user that was granted Super Admin privileges.
        #//
        do_action("granted_super_admin", user_id_)
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
def revoke_super_admin(user_id_=None, *_args_):
    
    
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
    do_action("revoke_super_admin", user_id_)
    #// Directly fetch site_admins instead of using get_super_admins().
    super_admins_ = get_site_option("site_admins", Array("admin"))
    user_ = get_userdata(user_id_)
    if user_ and 0 != strcasecmp(user_.user_email, get_site_option("admin_email")):
        key_ = php_array_search(user_.user_login, super_admins_)
        if False != key_:
            super_admins_[key_] = None
            update_site_option("site_admins", super_admins_)
            #// 
            #// Fires after the user's Super Admin privileges are revoked.
            #// 
            #// @since 3.0.0
            #// 
            #// @param int $user_id ID of the user Super Admin privileges were revoked from.
            #//
            do_action("revoked_super_admin", user_id_)
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
def wp_maybe_grant_install_languages_cap(allcaps_=None, *_args_):
    
    
    if (not php_empty(lambda : allcaps_["update_core"])) or (not php_empty(lambda : allcaps_["install_plugins"])) or (not php_empty(lambda : allcaps_["install_themes"])):
        allcaps_["install_languages"] = True
    # end if
    return allcaps_
# end def wp_maybe_grant_install_languages_cap
#// 
#// Filters the user capabilities to grant the 'resume_plugins' and 'resume_themes' capabilities as necessary.
#// 
#// @since 5.2.0
#// 
#// @param bool[] $allcaps An array of all the user's capabilities.
#// @return bool[] Filtered array of the user's capabilities.
#//
def wp_maybe_grant_resume_extensions_caps(allcaps_=None, *_args_):
    
    
    #// Even in a multisite, regular administrators should be able to resume plugins.
    if (not php_empty(lambda : allcaps_["activate_plugins"])):
        allcaps_["resume_plugins"] = True
    # end if
    #// Even in a multisite, regular administrators should be able to resume themes.
    if (not php_empty(lambda : allcaps_["switch_themes"])):
        allcaps_["resume_themes"] = True
    # end if
    return allcaps_
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
def wp_maybe_grant_site_health_caps(allcaps_=None, caps_=None, args_=None, user_=None, *_args_):
    
    
    if (not php_empty(lambda : allcaps_["install_plugins"])) and (not is_multisite()) or is_super_admin(user_.ID):
        allcaps_["view_site_health_checks"] = True
    # end if
    return allcaps_
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
