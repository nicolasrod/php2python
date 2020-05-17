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
#// Build Administration Menu.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Constructs the admin menu.
#// 
#// The elements in the array are :
#// 0: Menu item name
#// 1: Minimum level or capability required.
#// 2: The URL of the item's file
#// 3: Class
#// 4: ID
#// 5: Icon for top level menu
#// 
#// @global array $menu
#//
menu_[2] = Array(__("Dashboard"), "read", "index.php", "", "menu-top menu-top-first menu-icon-dashboard", "menu-dashboard", "dashicons-dashboard")
submenu_["index.php"][0] = Array(__("Home"), "read", "index.php")
if is_multisite():
    submenu_["index.php"][5] = Array(__("My Sites"), "read", "my-sites.php")
# end if
if (not is_multisite()) or current_user_can("update_core"):
    update_data_ = wp_get_update_data()
# end if
if (not is_multisite()):
    if current_user_can("update_core"):
        cap_ = "update_core"
    elif current_user_can("update_plugins"):
        cap_ = "update_plugins"
    elif current_user_can("update_themes"):
        cap_ = "update_themes"
    else:
        cap_ = "update_languages"
    # end if
    submenu_["index.php"][10] = Array(php_sprintf(__("Updates %s"), php_sprintf("<span class=\"update-plugins count-%s\"><span class=\"update-count\">%s</span></span>", update_data_["counts"]["total"], number_format_i18n(update_data_["counts"]["total"]))), cap_, "update-core.php")
    cap_ = None
# end if
menu_[4] = Array("", "read", "separator1", "", "wp-menu-separator")
#// $menu[5] = Posts.
menu_[10] = Array(__("Media"), "upload_files", "upload.php", "", "menu-top menu-icon-media", "menu-media", "dashicons-admin-media")
submenu_["upload.php"][5] = Array(__("Library"), "upload_files", "upload.php")
#// translators: Add new file.
submenu_["upload.php"][10] = Array(_x("Add New", "file"), "upload_files", "media-new.php")
i_ = 15
for tax_ in get_taxonomies_for_attachments("objects"):
    if (not tax_.show_ui) or (not tax_.show_in_menu):
        continue
    # end if
    submenu_["upload.php"][i_] = Array(esc_attr(tax_.labels.menu_name), tax_.cap.manage_terms, "edit-tags.php?taxonomy=" + tax_.name + "&amp;post_type=attachment")
    i_ += 1
# end for
tax_ = None
i_ = None
menu_[15] = Array(__("Links"), "manage_links", "link-manager.php", "", "menu-top menu-icon-links", "menu-links", "dashicons-admin-links")
submenu_["link-manager.php"][5] = Array(_x("All Links", "admin menu"), "manage_links", "link-manager.php")
#// translators: Add new links.
submenu_["link-manager.php"][10] = Array(_x("Add New", "link"), "manage_links", "link-add.php")
submenu_["link-manager.php"][15] = Array(__("Link Categories"), "manage_categories", "edit-tags.php?taxonomy=link_category")
#// $menu[20] = Pages.
#// Avoid the comment count query for users who cannot edit_posts.
if current_user_can("edit_posts"):
    awaiting_mod_ = wp_count_comments()
    awaiting_mod_ = awaiting_mod_.moderated
    awaiting_mod_i18n_ = number_format_i18n(awaiting_mod_)
    #// translators: %s: Number of comments.
    awaiting_mod_text_ = php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", awaiting_mod_), awaiting_mod_i18n_)
    menu_[25] = Array(php_sprintf(__("Comments %s"), "<span class=\"awaiting-mod count-" + absint(awaiting_mod_) + "\"><span class=\"pending-count\" aria-hidden=\"true\">" + awaiting_mod_i18n_ + "</span><span class=\"comments-in-moderation-text screen-reader-text\">" + awaiting_mod_text_ + "</span></span>"), "edit_posts", "edit-comments.php", "", "menu-top menu-icon-comments", "menu-comments", "dashicons-admin-comments")
    awaiting_mod_ = None
# end if
submenu_["edit-comments.php"][0] = Array(__("All Comments"), "edit_posts", "edit-comments.php")
_wp_last_object_menu_ = 25
#// The index of the last top-level menu in the object menu group.
types_ = get_post_types(Array({"show_ui": True, "_builtin": False, "show_in_menu": True}))
builtin_ = Array("post", "page")
for ptype_ in php_array_merge(builtin_, types_):
    ptype_obj_ = get_post_type_object(ptype_)
    #// Check if it should be a submenu.
    if True != ptype_obj_.show_in_menu:
        continue
    # end if
    _wp_last_object_menu_ += 1
    _wp_last_object_menu_ += 1
    ptype_menu_position_ = ptype_obj_.menu_position if php_is_int(ptype_obj_.menu_position) else _wp_last_object_menu_
    #// If we're to use $_wp_last_object_menu, increment it first.
    ptype_for_id_ = sanitize_html_class(ptype_)
    menu_icon_ = "dashicons-admin-post"
    if php_is_string(ptype_obj_.menu_icon):
        #// Special handling for data:image/svg+xml and Dashicons.
        if 0 == php_strpos(ptype_obj_.menu_icon, "data:image/svg+xml;base64,") or 0 == php_strpos(ptype_obj_.menu_icon, "dashicons-"):
            menu_icon_ = ptype_obj_.menu_icon
        else:
            menu_icon_ = esc_url(ptype_obj_.menu_icon)
        # end if
    elif php_in_array(ptype_, builtin_):
        menu_icon_ = "dashicons-admin-" + ptype_
    # end if
    menu_class_ = "menu-top menu-icon-" + ptype_for_id_
    #// 'post' special case.
    if "post" == ptype_:
        menu_class_ += " open-if-no-js"
        ptype_file_ = "edit.php"
        post_new_file_ = "post-new.php"
        edit_tags_file_ = "edit-tags.php?taxonomy=%s"
    else:
        ptype_file_ = str("edit.php?post_type=") + str(ptype_)
        post_new_file_ = str("post-new.php?post_type=") + str(ptype_)
        edit_tags_file_ = str("edit-tags.php?taxonomy=%s&amp;post_type=") + str(ptype_)
    # end if
    if php_in_array(ptype_, builtin_):
        ptype_menu_id_ = "menu-" + ptype_for_id_ + "s"
    else:
        ptype_menu_id_ = "menu-posts-" + ptype_for_id_
    # end if
    #// 
    #// If $ptype_menu_position is already populated or will be populated
    #// by a hard-coded value below, increment the position.
    #//
    core_menu_positions_ = Array(59, 60, 65, 70, 75, 80, 85, 99)
    while True:
        
        if not ((php_isset(lambda : menu_[ptype_menu_position_])) or php_in_array(ptype_menu_position_, core_menu_positions_)):
            break
        # end if
        ptype_menu_position_ += 1
    # end while
    menu_[ptype_menu_position_] = Array(esc_attr(ptype_obj_.labels.menu_name), ptype_obj_.cap.edit_posts, ptype_file_, "", menu_class_, ptype_menu_id_, menu_icon_)
    submenu_[ptype_file_][5] = Array(ptype_obj_.labels.all_items, ptype_obj_.cap.edit_posts, ptype_file_)
    submenu_[ptype_file_][10] = Array(ptype_obj_.labels.add_new, ptype_obj_.cap.create_posts, post_new_file_)
    i_ = 15
    for tax_ in get_taxonomies(Array(), "objects"):
        if (not tax_.show_ui) or (not tax_.show_in_menu) or (not php_in_array(ptype_, tax_.object_type, True)):
            continue
        # end if
        submenu_[ptype_file_][i_] = Array(esc_attr(tax_.labels.menu_name), tax_.cap.manage_terms, php_sprintf(edit_tags_file_, tax_.name))
        i_ += 1
    # end for
# end for
ptype_ = None
ptype_obj_ = None
ptype_for_id_ = None
ptype_menu_position_ = None
menu_icon_ = None
i_ = None
tax_ = None
post_new_file_ = None
menu_[59] = Array("", "read", "separator2", "", "wp-menu-separator")
appearance_cap_ = "switch_themes" if current_user_can("switch_themes") else "edit_theme_options"
menu_[60] = Array(__("Appearance"), appearance_cap_, "themes.php", "", "menu-top menu-icon-appearance", "menu-appearance", "dashicons-admin-appearance")
submenu_["themes.php"][5] = Array(__("Themes"), appearance_cap_, "themes.php")
customize_url_ = add_query_arg("return", urlencode(remove_query_arg(wp_removable_query_args(), wp_unslash(PHP_SERVER["REQUEST_URI"]))), "customize.php")
submenu_["themes.php"][6] = Array(__("Customize"), "customize", esc_url(customize_url_), "", "hide-if-no-customize")
if current_theme_supports("menus") or current_theme_supports("widgets"):
    submenu_["themes.php"][10] = Array(__("Menus"), "edit_theme_options", "nav-menus.php")
# end if
if current_theme_supports("custom-header") and current_user_can("customize"):
    customize_header_url_ = add_query_arg(Array({"autofocus": Array({"control": "header_image"})}), customize_url_)
    submenu_["themes.php"][15] = Array(__("Header"), appearance_cap_, esc_url(customize_header_url_), "", "hide-if-no-customize")
# end if
if current_theme_supports("custom-background") and current_user_can("customize"):
    customize_background_url_ = add_query_arg(Array({"autofocus": Array({"control": "background_image"})}), customize_url_)
    submenu_["themes.php"][20] = Array(__("Background"), appearance_cap_, esc_url(customize_background_url_), "", "hide-if-no-customize")
# end if
customize_url_ = None
appearance_cap_ = None
#// Add 'Editor' to the bottom of the Appearance menu.
if (not is_multisite()):
    add_action("admin_menu", "_add_themes_utility_last", 101)
# end if
#// 
#// Adds the (theme) 'Editor' link to the bottom of the Appearance menu.
#// 
#// @access private
#// @since 3.0.0
#//
def _add_themes_utility_last(*_args_):
    
    
    #// Must use API on the admin_menu hook, direct modification is only possible on/before the _admin_menu hook.
    add_submenu_page("themes.php", __("Theme Editor"), __("Theme Editor"), "edit_themes", "theme-editor.php")
# end def _add_themes_utility_last
count_ = ""
if (not is_multisite()) and current_user_can("update_plugins"):
    if (not (php_isset(lambda : update_data_))):
        update_data_ = wp_get_update_data()
    # end if
    count_ = php_sprintf("<span class=\"update-plugins count-%s\"><span class=\"plugin-count\">%s</span></span>", update_data_["counts"]["plugins"], number_format_i18n(update_data_["counts"]["plugins"]))
# end if
#// translators: %s: Number of pending plugin updates.
menu_[65] = Array(php_sprintf(__("Plugins %s"), count_), "activate_plugins", "plugins.php", "", "menu-top menu-icon-plugins", "menu-plugins", "dashicons-admin-plugins")
submenu_["plugins.php"][5] = Array(__("Installed Plugins"), "activate_plugins", "plugins.php")
if (not is_multisite()):
    #// translators: Add new plugin.
    submenu_["plugins.php"][10] = Array(_x("Add New", "plugin"), "install_plugins", "plugin-install.php")
    submenu_["plugins.php"][15] = Array(__("Plugin Editor"), "edit_plugins", "plugin-editor.php")
# end if
update_data_ = None
if current_user_can("list_users"):
    menu_[70] = Array(__("Users"), "list_users", "users.php", "", "menu-top menu-icon-users", "menu-users", "dashicons-admin-users")
else:
    menu_[70] = Array(__("Profile"), "read", "profile.php", "", "menu-top menu-icon-users", "menu-users", "dashicons-admin-users")
# end if
if current_user_can("list_users"):
    _wp_real_parent_file_["profile.php"] = "users.php"
    #// Back-compat for plugins adding submenus to profile.php.
    submenu_["users.php"][5] = Array(__("All Users"), "list_users", "users.php")
    if current_user_can("create_users"):
        submenu_["users.php"][10] = Array(_x("Add New", "user"), "create_users", "user-new.php")
    elif is_multisite():
        submenu_["users.php"][10] = Array(_x("Add New", "user"), "promote_users", "user-new.php")
    # end if
    submenu_["users.php"][15] = Array(__("Your Profile"), "read", "profile.php")
else:
    _wp_real_parent_file_["users.php"] = "profile.php"
    submenu_["profile.php"][5] = Array(__("Your Profile"), "read", "profile.php")
    if current_user_can("create_users"):
        submenu_["profile.php"][10] = Array(__("Add New User"), "create_users", "user-new.php")
    elif is_multisite():
        submenu_["profile.php"][10] = Array(__("Add New User"), "promote_users", "user-new.php")
    # end if
# end if
menu_[75] = Array(__("Tools"), "edit_posts", "tools.php", "", "menu-top menu-icon-tools", "menu-tools", "dashicons-admin-tools")
submenu_["tools.php"][5] = Array(__("Available Tools"), "edit_posts", "tools.php")
submenu_["tools.php"][10] = Array(__("Import"), "import", "import.php")
submenu_["tools.php"][15] = Array(__("Export"), "export", "export.php")
submenu_["tools.php"][20] = Array(__("Site Health"), "view_site_health_checks", "site-health.php")
submenu_["tools.php"][25] = Array(__("Export Personal Data"), "export_others_personal_data", "export-personal-data.php")
submenu_["tools.php"][30] = Array(__("Erase Personal Data"), "erase_others_personal_data", "erase-personal-data.php")
if is_multisite() and (not is_main_site()):
    submenu_["tools.php"][35] = Array(__("Delete Site"), "delete_site", "ms-delete-site.php")
# end if
if (not is_multisite()) and php_defined("WP_ALLOW_MULTISITE") and WP_ALLOW_MULTISITE:
    submenu_["tools.php"][50] = Array(__("Network Setup"), "setup_network", "network.php")
# end if
menu_[80] = Array(__("Settings"), "manage_options", "options-general.php", "", "menu-top menu-icon-settings", "menu-settings", "dashicons-admin-settings")
submenu_["options-general.php"][10] = Array(_x("General", "settings screen"), "manage_options", "options-general.php")
submenu_["options-general.php"][15] = Array(__("Writing"), "manage_options", "options-writing.php")
submenu_["options-general.php"][20] = Array(__("Reading"), "manage_options", "options-reading.php")
submenu_["options-general.php"][25] = Array(__("Discussion"), "manage_options", "options-discussion.php")
submenu_["options-general.php"][30] = Array(__("Media"), "manage_options", "options-media.php")
submenu_["options-general.php"][40] = Array(__("Permalinks"), "manage_options", "options-permalink.php")
submenu_["options-general.php"][45] = Array(__("Privacy"), "manage_privacy_options", "options-privacy.php")
_wp_last_utility_menu_ = 80
#// The index of the last top-level menu in the utility menu group.
menu_[99] = Array("", "read", "separator-last", "", "wp-menu-separator")
#// Back-compat for old top-levels.
_wp_real_parent_file_["post.php"] = "edit.php"
_wp_real_parent_file_["post-new.php"] = "edit.php"
_wp_real_parent_file_["edit-pages.php"] = "edit.php?post_type=page"
_wp_real_parent_file_["page-new.php"] = "edit.php?post_type=page"
_wp_real_parent_file_["wpmu-admin.php"] = "tools.php"
_wp_real_parent_file_["ms-admin.php"] = "tools.php"
#// Ensure backward compatibility.
compat_ = Array({"index": "dashboard", "edit": "posts", "post": "posts", "upload": "media", "link-manager": "links", "edit-pages": "pages", "page": "pages", "edit-comments": "comments", "options-general": "settings", "themes": "appearance"})
php_include_file(ABSPATH + "wp-admin/includes/menu.php", once=True)
