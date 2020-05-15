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
menu[2] = Array(__("Dashboard"), "read", "index.php", "", "menu-top menu-top-first menu-icon-dashboard", "menu-dashboard", "dashicons-dashboard")
submenu["index.php"][0] = Array(__("Home"), "read", "index.php")
if is_multisite():
    submenu["index.php"][5] = Array(__("My Sites"), "read", "my-sites.php")
# end if
if (not is_multisite()) or current_user_can("update_core"):
    update_data = wp_get_update_data()
# end if
if (not is_multisite()):
    if current_user_can("update_core"):
        cap = "update_core"
    elif current_user_can("update_plugins"):
        cap = "update_plugins"
    elif current_user_can("update_themes"):
        cap = "update_themes"
    else:
        cap = "update_languages"
    # end if
    submenu["index.php"][10] = Array(php_sprintf(__("Updates %s"), php_sprintf("<span class=\"update-plugins count-%s\"><span class=\"update-count\">%s</span></span>", update_data["counts"]["total"], number_format_i18n(update_data["counts"]["total"]))), cap, "update-core.php")
    cap = None
# end if
menu[4] = Array("", "read", "separator1", "", "wp-menu-separator")
#// $menu[5] = Posts.
menu[10] = Array(__("Media"), "upload_files", "upload.php", "", "menu-top menu-icon-media", "menu-media", "dashicons-admin-media")
submenu["upload.php"][5] = Array(__("Library"), "upload_files", "upload.php")
#// translators: Add new file.
submenu["upload.php"][10] = Array(_x("Add New", "file"), "upload_files", "media-new.php")
i = 15
for tax in get_taxonomies_for_attachments("objects"):
    if (not tax.show_ui) or (not tax.show_in_menu):
        continue
    # end if
    submenu["upload.php"][i] = Array(esc_attr(tax.labels.menu_name), tax.cap.manage_terms, "edit-tags.php?taxonomy=" + tax.name + "&amp;post_type=attachment")
    i += 1
# end for
tax = None
i = None
menu[15] = Array(__("Links"), "manage_links", "link-manager.php", "", "menu-top menu-icon-links", "menu-links", "dashicons-admin-links")
submenu["link-manager.php"][5] = Array(_x("All Links", "admin menu"), "manage_links", "link-manager.php")
#// translators: Add new links.
submenu["link-manager.php"][10] = Array(_x("Add New", "link"), "manage_links", "link-add.php")
submenu["link-manager.php"][15] = Array(__("Link Categories"), "manage_categories", "edit-tags.php?taxonomy=link_category")
#// $menu[20] = Pages.
#// Avoid the comment count query for users who cannot edit_posts.
if current_user_can("edit_posts"):
    awaiting_mod = wp_count_comments()
    awaiting_mod = awaiting_mod.moderated
    awaiting_mod_i18n = number_format_i18n(awaiting_mod)
    #// translators: %s: Number of comments.
    awaiting_mod_text = php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", awaiting_mod), awaiting_mod_i18n)
    menu[25] = Array(php_sprintf(__("Comments %s"), "<span class=\"awaiting-mod count-" + absint(awaiting_mod) + "\"><span class=\"pending-count\" aria-hidden=\"true\">" + awaiting_mod_i18n + "</span><span class=\"comments-in-moderation-text screen-reader-text\">" + awaiting_mod_text + "</span></span>"), "edit_posts", "edit-comments.php", "", "menu-top menu-icon-comments", "menu-comments", "dashicons-admin-comments")
    awaiting_mod = None
# end if
submenu["edit-comments.php"][0] = Array(__("All Comments"), "edit_posts", "edit-comments.php")
_wp_last_object_menu = 25
#// The index of the last top-level menu in the object menu group.
types = get_post_types(Array({"show_ui": True, "_builtin": False, "show_in_menu": True}))
builtin = Array("post", "page")
for ptype in php_array_merge(builtin, types):
    ptype_obj = get_post_type_object(ptype)
    #// Check if it should be a submenu.
    if True != ptype_obj.show_in_menu:
        continue
    # end if
    _wp_last_object_menu += 1
    ptype_menu_position = ptype_obj.menu_position if php_is_int(ptype_obj.menu_position) else _wp_last_object_menu
    #// If we're to use $_wp_last_object_menu, increment it first.
    ptype_for_id = sanitize_html_class(ptype)
    menu_icon = "dashicons-admin-post"
    if php_is_string(ptype_obj.menu_icon):
        #// Special handling for data:image/svg+xml and Dashicons.
        if 0 == php_strpos(ptype_obj.menu_icon, "data:image/svg+xml;base64,") or 0 == php_strpos(ptype_obj.menu_icon, "dashicons-"):
            menu_icon = ptype_obj.menu_icon
        else:
            menu_icon = esc_url(ptype_obj.menu_icon)
        # end if
    elif php_in_array(ptype, builtin):
        menu_icon = "dashicons-admin-" + ptype
    # end if
    menu_class = "menu-top menu-icon-" + ptype_for_id
    #// 'post' special case.
    if "post" == ptype:
        menu_class += " open-if-no-js"
        ptype_file = "edit.php"
        post_new_file = "post-new.php"
        edit_tags_file = "edit-tags.php?taxonomy=%s"
    else:
        ptype_file = str("edit.php?post_type=") + str(ptype)
        post_new_file = str("post-new.php?post_type=") + str(ptype)
        edit_tags_file = str("edit-tags.php?taxonomy=%s&amp;post_type=") + str(ptype)
    # end if
    if php_in_array(ptype, builtin):
        ptype_menu_id = "menu-" + ptype_for_id + "s"
    else:
        ptype_menu_id = "menu-posts-" + ptype_for_id
    # end if
    #// 
    #// If $ptype_menu_position is already populated or will be populated
    #// by a hard-coded value below, increment the position.
    #//
    core_menu_positions = Array(59, 60, 65, 70, 75, 80, 85, 99)
    while True:
        
        if not ((php_isset(lambda : menu[ptype_menu_position])) or php_in_array(ptype_menu_position, core_menu_positions)):
            break
        # end if
        ptype_menu_position += 1
    # end while
    menu[ptype_menu_position] = Array(esc_attr(ptype_obj.labels.menu_name), ptype_obj.cap.edit_posts, ptype_file, "", menu_class, ptype_menu_id, menu_icon)
    submenu[ptype_file][5] = Array(ptype_obj.labels.all_items, ptype_obj.cap.edit_posts, ptype_file)
    submenu[ptype_file][10] = Array(ptype_obj.labels.add_new, ptype_obj.cap.create_posts, post_new_file)
    i = 15
    for tax in get_taxonomies(Array(), "objects"):
        if (not tax.show_ui) or (not tax.show_in_menu) or (not php_in_array(ptype, tax.object_type, True)):
            continue
        # end if
        submenu[ptype_file][i] = Array(esc_attr(tax.labels.menu_name), tax.cap.manage_terms, php_sprintf(edit_tags_file, tax.name))
        i += 1
    # end for
# end for
ptype = None
ptype_obj = None
ptype_for_id = None
ptype_menu_position = None
menu_icon = None
i = None
tax = None
post_new_file = None
menu[59] = Array("", "read", "separator2", "", "wp-menu-separator")
appearance_cap = "switch_themes" if current_user_can("switch_themes") else "edit_theme_options"
menu[60] = Array(__("Appearance"), appearance_cap, "themes.php", "", "menu-top menu-icon-appearance", "menu-appearance", "dashicons-admin-appearance")
submenu["themes.php"][5] = Array(__("Themes"), appearance_cap, "themes.php")
customize_url = add_query_arg("return", urlencode(remove_query_arg(wp_removable_query_args(), wp_unslash(PHP_SERVER["REQUEST_URI"]))), "customize.php")
submenu["themes.php"][6] = Array(__("Customize"), "customize", esc_url(customize_url), "", "hide-if-no-customize")
if current_theme_supports("menus") or current_theme_supports("widgets"):
    submenu["themes.php"][10] = Array(__("Menus"), "edit_theme_options", "nav-menus.php")
# end if
if current_theme_supports("custom-header") and current_user_can("customize"):
    customize_header_url = add_query_arg(Array({"autofocus": Array({"control": "header_image"})}), customize_url)
    submenu["themes.php"][15] = Array(__("Header"), appearance_cap, esc_url(customize_header_url), "", "hide-if-no-customize")
# end if
if current_theme_supports("custom-background") and current_user_can("customize"):
    customize_background_url = add_query_arg(Array({"autofocus": Array({"control": "background_image"})}), customize_url)
    submenu["themes.php"][20] = Array(__("Background"), appearance_cap, esc_url(customize_background_url), "", "hide-if-no-customize")
# end if
customize_url = None
appearance_cap = None
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
def _add_themes_utility_last(*args_):
    
    #// Must use API on the admin_menu hook, direct modification is only possible on/before the _admin_menu hook.
    add_submenu_page("themes.php", __("Theme Editor"), __("Theme Editor"), "edit_themes", "theme-editor.php")
# end def _add_themes_utility_last
count = ""
if (not is_multisite()) and current_user_can("update_plugins"):
    if (not (php_isset(lambda : update_data))):
        update_data = wp_get_update_data()
    # end if
    count = php_sprintf("<span class=\"update-plugins count-%s\"><span class=\"plugin-count\">%s</span></span>", update_data["counts"]["plugins"], number_format_i18n(update_data["counts"]["plugins"]))
# end if
#// translators: %s: Number of pending plugin updates.
menu[65] = Array(php_sprintf(__("Plugins %s"), count), "activate_plugins", "plugins.php", "", "menu-top menu-icon-plugins", "menu-plugins", "dashicons-admin-plugins")
submenu["plugins.php"][5] = Array(__("Installed Plugins"), "activate_plugins", "plugins.php")
if (not is_multisite()):
    #// translators: Add new plugin.
    submenu["plugins.php"][10] = Array(_x("Add New", "plugin"), "install_plugins", "plugin-install.php")
    submenu["plugins.php"][15] = Array(__("Plugin Editor"), "edit_plugins", "plugin-editor.php")
# end if
update_data = None
if current_user_can("list_users"):
    menu[70] = Array(__("Users"), "list_users", "users.php", "", "menu-top menu-icon-users", "menu-users", "dashicons-admin-users")
else:
    menu[70] = Array(__("Profile"), "read", "profile.php", "", "menu-top menu-icon-users", "menu-users", "dashicons-admin-users")
# end if
if current_user_can("list_users"):
    _wp_real_parent_file["profile.php"] = "users.php"
    #// Back-compat for plugins adding submenus to profile.php.
    submenu["users.php"][5] = Array(__("All Users"), "list_users", "users.php")
    if current_user_can("create_users"):
        submenu["users.php"][10] = Array(_x("Add New", "user"), "create_users", "user-new.php")
    elif is_multisite():
        submenu["users.php"][10] = Array(_x("Add New", "user"), "promote_users", "user-new.php")
    # end if
    submenu["users.php"][15] = Array(__("Your Profile"), "read", "profile.php")
else:
    _wp_real_parent_file["users.php"] = "profile.php"
    submenu["profile.php"][5] = Array(__("Your Profile"), "read", "profile.php")
    if current_user_can("create_users"):
        submenu["profile.php"][10] = Array(__("Add New User"), "create_users", "user-new.php")
    elif is_multisite():
        submenu["profile.php"][10] = Array(__("Add New User"), "promote_users", "user-new.php")
    # end if
# end if
menu[75] = Array(__("Tools"), "edit_posts", "tools.php", "", "menu-top menu-icon-tools", "menu-tools", "dashicons-admin-tools")
submenu["tools.php"][5] = Array(__("Available Tools"), "edit_posts", "tools.php")
submenu["tools.php"][10] = Array(__("Import"), "import", "import.php")
submenu["tools.php"][15] = Array(__("Export"), "export", "export.php")
submenu["tools.php"][20] = Array(__("Site Health"), "view_site_health_checks", "site-health.php")
submenu["tools.php"][25] = Array(__("Export Personal Data"), "export_others_personal_data", "export-personal-data.php")
submenu["tools.php"][30] = Array(__("Erase Personal Data"), "erase_others_personal_data", "erase-personal-data.php")
if is_multisite() and (not is_main_site()):
    submenu["tools.php"][35] = Array(__("Delete Site"), "delete_site", "ms-delete-site.php")
# end if
if (not is_multisite()) and php_defined("WP_ALLOW_MULTISITE") and WP_ALLOW_MULTISITE:
    submenu["tools.php"][50] = Array(__("Network Setup"), "setup_network", "network.php")
# end if
menu[80] = Array(__("Settings"), "manage_options", "options-general.php", "", "menu-top menu-icon-settings", "menu-settings", "dashicons-admin-settings")
submenu["options-general.php"][10] = Array(_x("General", "settings screen"), "manage_options", "options-general.php")
submenu["options-general.php"][15] = Array(__("Writing"), "manage_options", "options-writing.php")
submenu["options-general.php"][20] = Array(__("Reading"), "manage_options", "options-reading.php")
submenu["options-general.php"][25] = Array(__("Discussion"), "manage_options", "options-discussion.php")
submenu["options-general.php"][30] = Array(__("Media"), "manage_options", "options-media.php")
submenu["options-general.php"][40] = Array(__("Permalinks"), "manage_options", "options-permalink.php")
submenu["options-general.php"][45] = Array(__("Privacy"), "manage_privacy_options", "options-privacy.php")
_wp_last_utility_menu = 80
#// The index of the last top-level menu in the utility menu group.
menu[99] = Array("", "read", "separator-last", "", "wp-menu-separator")
#// Back-compat for old top-levels.
_wp_real_parent_file["post.php"] = "edit.php"
_wp_real_parent_file["post-new.php"] = "edit.php"
_wp_real_parent_file["edit-pages.php"] = "edit.php?post_type=page"
_wp_real_parent_file["page-new.php"] = "edit.php?post_type=page"
_wp_real_parent_file["wpmu-admin.php"] = "tools.php"
_wp_real_parent_file["ms-admin.php"] = "tools.php"
#// Ensure backward compatibility.
compat = Array({"index": "dashboard", "edit": "posts", "post": "posts", "upload": "media", "link-manager": "links", "edit-pages": "pages", "page": "pages", "edit-comments": "comments", "options-general": "settings", "themes": "appearance"})
php_include_file(ABSPATH + "wp-admin/includes/menu.php", once=True)
