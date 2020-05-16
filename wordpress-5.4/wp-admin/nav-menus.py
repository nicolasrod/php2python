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
#// WordPress Administration for Navigation Menus
#// Interface functions
#// 
#// @version 2.0.0
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
#// Load all the nav menu interface functions.
php_include_file(ABSPATH + "wp-admin/includes/nav-menu.php", once=True)
if (not current_theme_supports("menus")) and (not current_theme_supports("widgets")):
    wp_die(__("Your theme does not support navigation menus or widgets."))
# end if
#// Permissions check.
if (not current_user_can("edit_theme_options")):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to edit theme options on this site.") + "</p>", 403)
# end if
wp_enqueue_script("nav-menu")
if wp_is_mobile():
    wp_enqueue_script("jquery-touch-punch")
# end if
#// Container for any messages displayed to the user.
messages = Array()
#// Container that stores the name of the active menu.
nav_menu_selected_title = ""
#// The menu id of the current menu being edited.
nav_menu_selected_id = php_int(PHP_REQUEST["menu"]) if (php_isset(lambda : PHP_REQUEST["menu"])) else 0
#// Get existing menu locations assignments.
locations = get_registered_nav_menus()
menu_locations = get_nav_menu_locations()
num_locations = php_count(php_array_keys(locations))
#// Allowed actions: add, update, delete.
action = PHP_REQUEST["action"] if (php_isset(lambda : PHP_REQUEST["action"])) else "edit"
#// 
#// If a JSON blob of navigation menu data is found, expand it and inject it
#// into `$_POST` to avoid PHP `max_input_vars` limitations. See #14134.
#//
_wp_expand_nav_menu_post_data()
for case in Switch(action):
    if case("add-menu-item"):
        check_admin_referer("add-menu_item", "menu-settings-column-nonce")
        if (php_isset(lambda : PHP_REQUEST["nav-menu-locations"])):
            set_theme_mod("nav_menu_locations", php_array_map("absint", PHP_REQUEST["menu-locations"]))
        elif (php_isset(lambda : PHP_REQUEST["menu-item"])):
            wp_save_nav_menu_items(nav_menu_selected_id, PHP_REQUEST["menu-item"])
        # end if
        break
    # end if
    if case("move-down-menu-item"):
        #// Moving down a menu item is the same as moving up the next in order.
        check_admin_referer("move-menu_item")
        menu_item_id = php_int(PHP_REQUEST["menu-item"]) if (php_isset(lambda : PHP_REQUEST["menu-item"])) else 0
        if is_nav_menu_item(menu_item_id):
            menus = Array(php_int(PHP_REQUEST["menu"])) if (php_isset(lambda : PHP_REQUEST["menu"])) else wp_get_object_terms(menu_item_id, "nav_menu", Array({"fields": "ids"}))
            if (not is_wp_error(menus)) and (not php_empty(lambda : menus[0])):
                menu_id = php_int(menus[0])
                ordered_menu_items = wp_get_nav_menu_items(menu_id)
                menu_item_data = wp_setup_nav_menu_item(get_post(menu_item_id))
                #// Set up the data we need in one pass through the array of menu items.
                dbids_to_orders = Array()
                orders_to_dbids = Array()
                for ordered_menu_item_object in ordered_menu_items:
                    if (php_isset(lambda : ordered_menu_item_object.ID)):
                        if (php_isset(lambda : ordered_menu_item_object.menu_order)):
                            dbids_to_orders[ordered_menu_item_object.ID] = ordered_menu_item_object.menu_order
                            orders_to_dbids[ordered_menu_item_object.menu_order] = ordered_menu_item_object.ID
                        # end if
                    # end if
                # end for
                #// Get next in order.
                if (php_isset(lambda : orders_to_dbids[dbids_to_orders[menu_item_id] + 1])):
                    next_item_id = orders_to_dbids[dbids_to_orders[menu_item_id] + 1]
                    next_item_data = wp_setup_nav_menu_item(get_post(next_item_id))
                    #// If not siblings of same parent, bubble menu item up but keep order.
                    if (not php_empty(lambda : menu_item_data["menu_item_parent"])) and php_empty(lambda : next_item_data["menu_item_parent"]) or next_item_data["menu_item_parent"] != menu_item_data["menu_item_parent"]:
                        parent_db_id = php_int(menu_item_data["menu_item_parent"]) if php_in_array(menu_item_data["menu_item_parent"], orders_to_dbids) else 0
                        parent_object = wp_setup_nav_menu_item(get_post(parent_db_id))
                        if (not is_wp_error(parent_object)):
                            parent_data = parent_object
                            menu_item_data["menu_item_parent"] = parent_data["menu_item_parent"]
                            update_post_meta(menu_item_data["ID"], "_menu_item_menu_item_parent", php_int(menu_item_data["menu_item_parent"]))
                        # end if
                        pass
                    else:
                        next_item_data["menu_order"] = next_item_data["menu_order"] - 1
                        menu_item_data["menu_order"] = menu_item_data["menu_order"] + 1
                        menu_item_data["menu_item_parent"] = next_item_data["ID"]
                        update_post_meta(menu_item_data["ID"], "_menu_item_menu_item_parent", php_int(menu_item_data["menu_item_parent"]))
                        wp_update_post(menu_item_data)
                        wp_update_post(next_item_data)
                    # end if
                    pass
                elif (not php_empty(lambda : menu_item_data["menu_item_parent"])) and php_in_array(menu_item_data["menu_item_parent"], orders_to_dbids):
                    menu_item_data["menu_item_parent"] = php_int(get_post_meta(menu_item_data["menu_item_parent"], "_menu_item_menu_item_parent", True))
                    update_post_meta(menu_item_data["ID"], "_menu_item_menu_item_parent", php_int(menu_item_data["menu_item_parent"]))
                # end if
            # end if
        # end if
        break
    # end if
    if case("move-up-menu-item"):
        check_admin_referer("move-menu_item")
        menu_item_id = php_int(PHP_REQUEST["menu-item"]) if (php_isset(lambda : PHP_REQUEST["menu-item"])) else 0
        if is_nav_menu_item(menu_item_id):
            menus = Array(php_int(PHP_REQUEST["menu"])) if (php_isset(lambda : PHP_REQUEST["menu"])) else wp_get_object_terms(menu_item_id, "nav_menu", Array({"fields": "ids"}))
            if (not is_wp_error(menus)) and (not php_empty(lambda : menus[0])):
                menu_id = php_int(menus[0])
                ordered_menu_items = wp_get_nav_menu_items(menu_id)
                menu_item_data = wp_setup_nav_menu_item(get_post(menu_item_id))
                #// Set up the data we need in one pass through the array of menu items.
                dbids_to_orders = Array()
                orders_to_dbids = Array()
                for ordered_menu_item_object in ordered_menu_items:
                    if (php_isset(lambda : ordered_menu_item_object.ID)):
                        if (php_isset(lambda : ordered_menu_item_object.menu_order)):
                            dbids_to_orders[ordered_menu_item_object.ID] = ordered_menu_item_object.menu_order
                            orders_to_dbids[ordered_menu_item_object.menu_order] = ordered_menu_item_object.ID
                        # end if
                    # end if
                # end for
                #// If this menu item is not first.
                if (not php_empty(lambda : dbids_to_orders[menu_item_id])) and (not php_empty(lambda : orders_to_dbids[dbids_to_orders[menu_item_id] - 1])):
                    #// If this menu item is a child of the previous.
                    if (not php_empty(lambda : menu_item_data["menu_item_parent"])) and php_in_array(menu_item_data["menu_item_parent"], php_array_keys(dbids_to_orders)) and (php_isset(lambda : orders_to_dbids[dbids_to_orders[menu_item_id] - 1])) and menu_item_data["menu_item_parent"] == orders_to_dbids[dbids_to_orders[menu_item_id] - 1]:
                        parent_db_id = php_int(menu_item_data["menu_item_parent"]) if php_in_array(menu_item_data["menu_item_parent"], orders_to_dbids) else 0
                        parent_object = wp_setup_nav_menu_item(get_post(parent_db_id))
                        if (not is_wp_error(parent_object)):
                            parent_data = parent_object
                            #// 
                            #// If there is something before the parent and parent a child of it,
                            #// make menu item a child also of it.
                            #//
                            if (not php_empty(lambda : dbids_to_orders[parent_db_id])) and (not php_empty(lambda : orders_to_dbids[dbids_to_orders[parent_db_id] - 1])) and (not php_empty(lambda : parent_data["menu_item_parent"])):
                                menu_item_data["menu_item_parent"] = parent_data["menu_item_parent"]
                                pass
                            elif (not php_empty(lambda : dbids_to_orders[parent_db_id])) and (not php_empty(lambda : orders_to_dbids[dbids_to_orders[parent_db_id] - 1])):
                                _possible_parent_id = php_int(get_post_meta(orders_to_dbids[dbids_to_orders[parent_db_id] - 1], "_menu_item_menu_item_parent", True))
                                if php_in_array(_possible_parent_id, php_array_keys(dbids_to_orders)):
                                    menu_item_data["menu_item_parent"] = _possible_parent_id
                                else:
                                    menu_item_data["menu_item_parent"] = 0
                                # end if
                                pass
                            else:
                                menu_item_data["menu_item_parent"] = 0
                            # end if
                            #// Set former parent's [menu_order] to that of menu-item's.
                            parent_data["menu_order"] = parent_data["menu_order"] + 1
                            #// Set menu-item's [menu_order] to that of former parent.
                            menu_item_data["menu_order"] = menu_item_data["menu_order"] - 1
                            #// Save changes.
                            update_post_meta(menu_item_data["ID"], "_menu_item_menu_item_parent", php_int(menu_item_data["menu_item_parent"]))
                            wp_update_post(menu_item_data)
                            wp_update_post(parent_data)
                        # end if
                        pass
                    elif php_empty(lambda : menu_item_data["menu_order"]) or php_empty(lambda : menu_item_data["menu_item_parent"]) or (not php_in_array(menu_item_data["menu_item_parent"], php_array_keys(dbids_to_orders))) or php_empty(lambda : orders_to_dbids[dbids_to_orders[menu_item_id] - 1]) or orders_to_dbids[dbids_to_orders[menu_item_id] - 1] != menu_item_data["menu_item_parent"]:
                        #// Just make it a child of the previous; keep the order.
                        menu_item_data["menu_item_parent"] = php_int(orders_to_dbids[dbids_to_orders[menu_item_id] - 1])
                        update_post_meta(menu_item_data["ID"], "_menu_item_menu_item_parent", php_int(menu_item_data["menu_item_parent"]))
                        wp_update_post(menu_item_data)
                    # end if
                # end if
            # end if
        # end if
        break
    # end if
    if case("delete-menu-item"):
        menu_item_id = php_int(PHP_REQUEST["menu-item"])
        check_admin_referer("delete-menu_item_" + menu_item_id)
        if is_nav_menu_item(menu_item_id) and wp_delete_post(menu_item_id, True):
            messages[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("The menu item has been successfully deleted.") + "</p></div>"
        # end if
        break
    # end if
    if case("delete"):
        check_admin_referer("delete-nav_menu-" + nav_menu_selected_id)
        if is_nav_menu(nav_menu_selected_id):
            deletion = wp_delete_nav_menu(nav_menu_selected_id)
        else:
            #// Reset the selected menu.
            nav_menu_selected_id = 0
            PHP_REQUEST["menu"] = None
        # end if
        if (not (php_isset(lambda : deletion))):
            break
        # end if
        if is_wp_error(deletion):
            messages[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + deletion.get_error_message() + "</p></div>"
        else:
            messages[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("The menu has been successfully deleted.") + "</p></div>"
        # end if
        break
    # end if
    if case("delete_menus"):
        check_admin_referer("nav_menus_bulk_actions")
        for menu_id_to_delete in PHP_REQUEST["delete_menus"]:
            if (not is_nav_menu(menu_id_to_delete)):
                continue
            # end if
            deletion = wp_delete_nav_menu(menu_id_to_delete)
            if is_wp_error(deletion):
                messages[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + deletion.get_error_message() + "</p></div>"
                deletion_error = True
            # end if
        # end for
        if php_empty(lambda : deletion_error):
            messages[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("Selected menus have been successfully deleted.") + "</p></div>"
        # end if
        break
    # end if
    if case("update"):
        check_admin_referer("update-nav_menu", "update-nav-menu-nonce")
        #// Remove menu locations that have been unchecked.
        for location,description in locations:
            if php_empty(lambda : PHP_POST["menu-locations"]) or php_empty(lambda : PHP_POST["menu-locations"][location]) and (php_isset(lambda : menu_locations[location])) and menu_locations[location] == nav_menu_selected_id:
                menu_locations[location] = None
            # end if
        # end for
        #// Merge new and existing menu locations if any new ones are set.
        if (php_isset(lambda : PHP_POST["menu-locations"])):
            new_menu_locations = php_array_map("absint", PHP_POST["menu-locations"])
            menu_locations = php_array_merge(menu_locations, new_menu_locations)
        # end if
        #// Set menu locations.
        set_theme_mod("nav_menu_locations", menu_locations)
        #// Add Menu.
        if 0 == nav_menu_selected_id:
            new_menu_title = php_trim(esc_html(PHP_POST["menu-name"]))
            if new_menu_title:
                _nav_menu_selected_id = wp_update_nav_menu_object(0, Array({"menu-name": new_menu_title}))
                if is_wp_error(_nav_menu_selected_id):
                    messages[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + _nav_menu_selected_id.get_error_message() + "</p></div>"
                else:
                    _menu_object = wp_get_nav_menu_object(_nav_menu_selected_id)
                    nav_menu_selected_id = _nav_menu_selected_id
                    nav_menu_selected_title = _menu_object.name
                    if (php_isset(lambda : PHP_REQUEST["menu-item"])):
                        wp_save_nav_menu_items(nav_menu_selected_id, absint(PHP_REQUEST["menu-item"]))
                    # end if
                    if (php_isset(lambda : PHP_REQUEST["zero-menu-state"])):
                        #// If there are menu items, add them.
                        wp_nav_menu_update_menu_items(nav_menu_selected_id, nav_menu_selected_title)
                        #// Auto-save nav_menu_locations.
                        locations = get_nav_menu_locations()
                        for location,menu_id in locations:
                            locations[location] = nav_menu_selected_id
                            break
                            pass
                        # end for
                        set_theme_mod("nav_menu_locations", locations)
                    # end if
                    if (php_isset(lambda : PHP_REQUEST["use-location"])):
                        locations = get_registered_nav_menus()
                        menu_locations = get_nav_menu_locations()
                        if (php_isset(lambda : locations[PHP_REQUEST["use-location"]])):
                            menu_locations[PHP_REQUEST["use-location"]] = nav_menu_selected_id
                        # end if
                        set_theme_mod("nav_menu_locations", menu_locations)
                    # end if
                    #// $messages[] = '<div id="message" class="updated"><p>' . sprintf( __( '<strong>%s</strong> has been created.' ), $nav_menu_selected_title ) . '</p></div>';
                    wp_redirect(admin_url("nav-menus.php?menu=" + _nav_menu_selected_id))
                    php_exit(0)
                # end if
            else:
                messages[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("Please enter a valid menu name.") + "</p></div>"
            # end if
            pass
        else:
            _menu_object = wp_get_nav_menu_object(nav_menu_selected_id)
            menu_title = php_trim(esc_html(PHP_POST["menu-name"]))
            if (not menu_title):
                messages[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("Please enter a valid menu name.") + "</p></div>"
                menu_title = _menu_object.name
            # end if
            if (not is_wp_error(_menu_object)):
                _nav_menu_selected_id = wp_update_nav_menu_object(nav_menu_selected_id, Array({"menu-name": menu_title}))
                if is_wp_error(_nav_menu_selected_id):
                    _menu_object = _nav_menu_selected_id
                    messages[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + _nav_menu_selected_id.get_error_message() + "</p></div>"
                else:
                    _menu_object = wp_get_nav_menu_object(_nav_menu_selected_id)
                    nav_menu_selected_title = _menu_object.name
                # end if
            # end if
            #// Update menu items.
            if (not is_wp_error(_menu_object)):
                messages = php_array_merge(messages, wp_nav_menu_update_menu_items(_nav_menu_selected_id, nav_menu_selected_title))
                #// If the menu ID changed, redirect to the new URL.
                if nav_menu_selected_id != _nav_menu_selected_id:
                    wp_redirect(admin_url("nav-menus.php?menu=" + php_intval(_nav_menu_selected_id)))
                    php_exit(0)
                # end if
            # end if
        # end if
        break
    # end if
    if case("locations"):
        if (not num_locations):
            wp_redirect(admin_url("nav-menus.php"))
            php_exit(0)
        # end if
        add_filter("screen_options_show_screen", "__return_false")
        if (php_isset(lambda : PHP_POST["menu-locations"])):
            check_admin_referer("save-menu-locations")
            new_menu_locations = php_array_map("absint", PHP_POST["menu-locations"])
            menu_locations = php_array_merge(menu_locations, new_menu_locations)
            #// Set menu locations.
            set_theme_mod("nav_menu_locations", menu_locations)
            messages[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("Menu locations updated.") + "</p></div>"
        # end if
        break
    # end if
# end for
#// Get all nav menus.
nav_menus = wp_get_nav_menus()
menu_count = php_count(nav_menus)
#// Are we on the add new screen?
add_new_screen = True if (php_isset(lambda : PHP_REQUEST["menu"])) and 0 == PHP_REQUEST["menu"] else False
locations_screen = True if (php_isset(lambda : PHP_REQUEST["action"])) and "locations" == PHP_REQUEST["action"] else False
#// 
#// If we have one theme location, and zero menus, we take them right
#// into editing their first menu.
#//
page_count = wp_count_posts("page")
one_theme_location_no_menus = True if 1 == php_count(get_registered_nav_menus()) and (not add_new_screen) and php_empty(lambda : nav_menus) and (not php_empty(lambda : page_count.publish)) else False
nav_menus_l10n = Array({"oneThemeLocationNoMenus": one_theme_location_no_menus, "moveUp": __("Move up one"), "moveDown": __("Move down one"), "moveToTop": __("Move to the top"), "moveUnder": __("Move under %s"), "moveOutFrom": __("Move out from under %s"), "under": __("Under %s"), "outFrom": __("Out from under %s"), "menuFocus": __("%1$s. Menu item %2$d of %3$d."), "subMenuFocus": __("%1$s. Sub item number %2$d under %3$s.")})
wp_localize_script("nav-menu", "menus", nav_menus_l10n)
#// 
#// Redirect to add screen if there are no menus and this users has either zero,
#// or more than 1 theme locations.
#//
if 0 == menu_count and (not add_new_screen) and (not one_theme_location_no_menus):
    wp_redirect(admin_url("nav-menus.php?action=edit&menu=0"))
# end if
#// Get recently edited nav menu.
recently_edited = absint(get_user_option("nav_menu_recently_edited"))
if php_empty(lambda : recently_edited) and is_nav_menu(nav_menu_selected_id):
    recently_edited = nav_menu_selected_id
# end if
#// Use $recently_edited if none are selected.
if php_empty(lambda : nav_menu_selected_id) and (not (php_isset(lambda : PHP_REQUEST["menu"]))) and is_nav_menu(recently_edited):
    nav_menu_selected_id = recently_edited
# end if
#// On deletion of menu, if another menu exists, show it.
if (not add_new_screen) and 0 < menu_count and (php_isset(lambda : PHP_REQUEST["action"])) and "delete" == PHP_REQUEST["action"]:
    nav_menu_selected_id = nav_menus[0].term_id
# end if
#// Set $nav_menu_selected_id to 0 if no menus.
if one_theme_location_no_menus:
    nav_menu_selected_id = 0
elif php_empty(lambda : nav_menu_selected_id) and (not php_empty(lambda : nav_menus)) and (not add_new_screen):
    #// If we have no selection yet, and we have menus, set to the first one in the list.
    nav_menu_selected_id = nav_menus[0].term_id
# end if
#// Update the user's setting.
if nav_menu_selected_id != recently_edited and is_nav_menu(nav_menu_selected_id):
    update_user_meta(current_user.ID, "nav_menu_recently_edited", nav_menu_selected_id)
# end if
#// If there's a menu, get its name.
if (not nav_menu_selected_title) and is_nav_menu(nav_menu_selected_id):
    _menu_object = wp_get_nav_menu_object(nav_menu_selected_id)
    nav_menu_selected_title = _menu_object.name if (not is_wp_error(_menu_object)) else ""
# end if
#// Generate truncated menu names.
for key,_nav_menu in nav_menus:
    nav_menus[key].truncated_name = wp_html_excerpt(_nav_menu.name, 40, "&hellip;")
# end for
#// Retrieve menu locations.
if current_theme_supports("menus"):
    locations = get_registered_nav_menus()
    menu_locations = get_nav_menu_locations()
# end if
#// 
#// Ensure the user will be able to scroll horizontally
#// by adding a class for the max menu depth.
#// 
#// @global int $_wp_nav_menu_max_depth
#//
global _wp_nav_menu_max_depth
php_check_if_defined("_wp_nav_menu_max_depth")
_wp_nav_menu_max_depth = 0
#// Calling wp_get_nav_menu_to_edit generates $_wp_nav_menu_max_depth.
if is_nav_menu(nav_menu_selected_id):
    menu_items = wp_get_nav_menu_items(nav_menu_selected_id, Array({"post_status": "any"}))
    edit_markup = wp_get_nav_menu_to_edit(nav_menu_selected_id)
# end if
#// 
#// @global int $_wp_nav_menu_max_depth
#// 
#// @param string $classes
#// @return string
#//
def wp_nav_menu_max_depth(classes=None, *args_):
    
    global _wp_nav_menu_max_depth
    php_check_if_defined("_wp_nav_menu_max_depth")
    return str(classes) + str(" menu-max-depth-") + str(_wp_nav_menu_max_depth)
# end def wp_nav_menu_max_depth
add_filter("admin_body_class", "wp_nav_menu_max_depth")
wp_nav_menu_setup()
wp_initial_nav_menu_meta_boxes()
if (not current_theme_supports("menus")) and (not num_locations):
    messages[-1] = "<div id=\"message\" class=\"updated\"><p>" + php_sprintf(__("Your theme does not natively support menus, but you can use them in sidebars by adding a &#8220;Navigation Menu&#8221; widget on the <a href=\"%s\">Widgets</a> screen."), admin_url("widgets.php")) + "</p></div>"
# end if
if (not locations_screen):
    #// Main tab.
    overview = "<p>" + __("This screen is used for managing your navigation menus.") + "</p>"
    overview += "<p>" + php_sprintf(__("Menus can be displayed in locations defined by your theme, even used in sidebars by adding a &#8220;Navigation Menu&#8221; widget on the <a href=\"%1$s\">Widgets</a> screen. If your theme does not support the navigation menus feature (the default themes, %2$s and %3$s, do), you can learn about adding this support by following the Documentation link to the side."), admin_url("widgets.php"), "Twenty Nineteen", "Twenty Twenty") + "</p>"
    overview += "<p>" + __("From this screen you can:") + "</p>"
    overview += "<ul><li>" + __("Create, edit, and delete menus") + "</li>"
    overview += "<li>" + __("Add, organize, and modify individual menu items") + "</li></ul>"
    get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": overview}))
    menu_management = "<p>" + __("The menu management box at the top of the screen is used to control which menu is opened in the editor below.") + "</p>"
    menu_management += "<ul><li>" + __("To edit an existing menu, <strong>choose a menu from the drop down and click Select</strong>") + "</li>"
    menu_management += "<li>" + __("If you haven&#8217;t yet created any menus, <strong>click the &#8217;create a new menu&#8217; link</strong> to get started") + "</li></ul>"
    menu_management += "<p>" + __("You can assign theme locations to individual menus by <strong>selecting the desired settings</strong> at the bottom of the menu editor. To assign menus to all theme locations at once, <strong>visit the Manage Locations tab</strong> at the top of the screen.") + "</p>"
    get_current_screen().add_help_tab(Array({"id": "menu-management", "title": __("Menu Management"), "content": menu_management}))
    editing_menus = "<p>" + __("Each navigation menu may contain a mix of links to pages, categories, custom URLs or other content types. Menu links are added by selecting items from the expanding boxes in the left-hand column below.") + "</p>"
    editing_menus += "<p>" + __("<strong>Clicking the arrow to the right of any menu item</strong> in the editor will reveal a standard group of settings. Additional settings such as link target, CSS classes, link relationships, and link descriptions can be enabled and disabled via the Screen Options tab.") + "</p>"
    editing_menus += "<ul><li>" + __("Add one or several items at once by <strong>selecting the checkbox next to each item and clicking Add to Menu</strong>") + "</li>"
    editing_menus += "<li>" + __("To add a custom link, <strong>expand the Custom Links section, enter a URL and link text, and click Add to Menu</strong>") + "</li>"
    editing_menus += "<li>" + __("To reorganize menu items, <strong>drag and drop items with your mouse or use your keyboard</strong>. Drag or move a menu item a little to the right to make it a submenu") + "</li>"
    editing_menus += "<li>" + __("Delete a menu item by <strong>expanding it and clicking the Remove link</strong>") + "</li></ul>"
    get_current_screen().add_help_tab(Array({"id": "editing-menus", "title": __("Editing Menus"), "content": editing_menus}))
else:
    #// Locations tab.
    locations_overview = "<p>" + __("This screen is used for globally assigning menus to locations defined by your theme.") + "</p>"
    locations_overview += "<ul><li>" + __("To assign menus to one or more theme locations, <strong>select a menu from each location&#8217;s drop down.</strong> When you&#8217;re finished, <strong>click Save Changes</strong>") + "</li>"
    locations_overview += "<li>" + __("To edit a menu currently assigned to a theme location, <strong>click the adjacent &#8217;Edit&#8217; link</strong>") + "</li>"
    locations_overview += "<li>" + __("To add a new menu instead of assigning an existing one, <strong>click the &#8217;Use new menu&#8217; link</strong>. Your new menu will be automatically assigned to that theme location") + "</li></ul>"
    get_current_screen().add_help_tab(Array({"id": "locations-overview", "title": __("Overview"), "content": locations_overview}))
# end if
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/appearance-menus-screen/\">Documentation on Menus</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
#// Get the admin header.
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n   <h1 class=\"wp-heading-inline\">")
php_print(esc_html(__("Menus")))
php_print("</h1>\n  ")
if current_user_can("customize"):
    focus = Array({"section": "menu_locations"}) if locations_screen else Array({"panel": "nav_menus"})
    printf(" <a class=\"page-title-action hide-if-no-customize\" href=\"%1$s\">%2$s</a>", esc_url(add_query_arg(Array(Array({"autofocus": focus}), {"return": urlencode(remove_query_arg(wp_removable_query_args(), wp_unslash(PHP_SERVER["REQUEST_URI"])))}), admin_url("customize.php"))), __("Manage with Live Preview"))
# end if
nav_tab_active_class = ""
nav_aria_current = ""
if (not (php_isset(lambda : PHP_REQUEST["action"]))) or (php_isset(lambda : PHP_REQUEST["action"])) and "locations" != PHP_REQUEST["action"]:
    nav_tab_active_class = " nav-tab-active"
    nav_aria_current = " aria-current=\"page\""
# end if
php_print("""
<hr class=\"wp-header-end\">
<nav class=\"nav-tab-wrapper wp-clearfix\" aria-label=\"""")
esc_attr_e("Secondary menu")
php_print("\">\n        <a href=\"")
php_print(admin_url("nav-menus.php"))
php_print("\" class=\"nav-tab")
php_print(nav_tab_active_class)
php_print("\"")
php_print(nav_aria_current)
php_print(">")
esc_html_e("Edit Menus")
php_print("</a>\n       ")
if num_locations and menu_count:
    active_tab_class = ""
    aria_current = ""
    if locations_screen:
        active_tab_class = " nav-tab-active"
        aria_current = " aria-current=\"page\""
    # end if
    php_print("         <a href=\"")
    php_print(esc_url(add_query_arg(Array({"action": "locations"}), admin_url("nav-menus.php"))))
    php_print("\" class=\"nav-tab")
    php_print(active_tab_class)
    php_print("\"")
    php_print(aria_current)
    php_print(">")
    esc_html_e("Manage Locations")
    php_print("</a>\n           ")
# end if
php_print(" </nav>\n    ")
for message in messages:
    php_print(message + "\n")
# end for
php_print(" ")
if locations_screen:
    if 1 == num_locations:
        php_print("<p>" + __("Your theme supports one menu. Select which menu you would like to use.") + "</p>")
    else:
        php_print("<p>" + php_sprintf(_n("Your theme supports %s menu. Select which menu appears in each location.", "Your theme supports %s menus. Select which menu appears in each location.", num_locations), number_format_i18n(num_locations)) + "</p>")
    # end if
    php_print(" <div id=\"menu-locations-wrap\">\n      <form method=\"post\" action=\"")
    php_print(esc_url(add_query_arg(Array({"action": "locations"}), admin_url("nav-menus.php"))))
    php_print("""\">
    <table class=\"widefat fixed\" id=\"menu-locations-table\">
    <thead>
    <tr>
    <th scope=\"col\" class=\"manage-column column-locations\">""")
    _e("Theme Location")
    php_print("</th>\n                  <th scope=\"col\" class=\"manage-column column-menus\">")
    _e("Assigned Menu")
    php_print("""</th>
    </tr>
    </thead>
    <tbody class=\"menu-locations\">
    """)
    for _location,_name in locations:
        php_print("                 <tr class=\"menu-locations-row\">\n                     <td class=\"menu-location-title\"><label for=\"locations-")
        php_print(_location)
        php_print("\">")
        php_print(_name)
        php_print("</label></td>\n                      <td class=\"menu-location-menus\">\n                            <select name=\"menu-locations[")
        php_print(_location)
        php_print("]\" id=\"locations-")
        php_print(_location)
        php_print("\">\n                                <option value=\"0\">")
        printf("&mdash; %s &mdash;", esc_html__("Select a Menu"))
        php_print("</option>\n                              ")
        for menu in nav_menus:
            data_orig = ""
            selected = (php_isset(lambda : menu_locations[_location])) and menu_locations[_location] == menu.term_id
            if selected:
                data_orig = "data-orig=\"true\""
            # end if
            php_print("                                 <option ")
            php_print(data_orig)
            php_print(" ")
            selected(selected)
            php_print(" value=\"")
            php_print(menu.term_id)
            php_print("\">\n                                        ")
            php_print(wp_html_excerpt(menu.name, 40, "&hellip;"))
            php_print("                                 </option>\n                             ")
        # end for
        php_print("                         </select>\n                         <div class=\"locations-row-links\">\n                               ")
        if (php_isset(lambda : menu_locations[_location])) and 0 != menu_locations[_location]:
            php_print("                             <span class=\"locations-edit-menu-link\">\n                                 <a href=\"\n                                    ")
            php_print(esc_url(add_query_arg(Array({"action": "edit", "menu": menu_locations[_location]}), admin_url("nav-menus.php"))))
            php_print("                                 \">\n                                       <span aria-hidden=\"true\">")
            _ex("Edit", "menu")
            php_print("</span><span class=\"screen-reader-text\">")
            _e("Edit selected menu")
            php_print("""</span>
            </a>
            </span>
            """)
        # end if
        php_print("                             <span class=\"locations-add-menu-link\">\n                                  <a href=\"\n                                    ")
        php_print(esc_url(add_query_arg(Array({"action": "edit", "menu": 0, "use-location": _location}), admin_url("nav-menus.php"))))
        php_print("                                 \">\n                                       ")
        _ex("Use new menu", "menu")
        php_print("""                                   </a>
        </span>
        </div><!-- .locations-row-links -->
        </td><!-- .menu-location-menus -->
        </tr><!-- .menu-locations-row -->
        """)
    # end for
    pass
    php_print("             </tbody>\n          </table>\n          <p class=\"button-controls wp-clearfix\">")
    submit_button(__("Save Changes"), "primary left", "nav-menu-locations", False)
    php_print("</p>\n           ")
    wp_nonce_field("save-menu-locations")
    php_print("         <input type=\"hidden\" name=\"menu\" id=\"nav-menu-meta-object-id\" value=\"")
    php_print(esc_attr(nav_menu_selected_id))
    php_print("""\" />
    </form>
    </div><!-- #menu-locations-wrap -->
    """)
    #// 
    #// Fires after the menu locations table is displayed.
    #// 
    #// @since 3.6.0
    #//
    do_action("after_menu_locations_table")
    php_print(" ")
else:
    php_print(" <div class=\"manage-menus\">\n      ")
    if menu_count < 1:
        php_print("     <span class=\"first-menu-message\">\n           ")
        _e("Create your first menu below.")
        php_print("         <span class=\"screen-reader-text\">")
        _e("Fill in the Menu Name and click the Create Menu button to create your first menu.")
        php_print("</span>\n        </span><!-- /first-menu-message -->\n       ")
    elif menu_count < 2:
        php_print("     <span class=\"add-edit-menu-action\">\n         ")
        printf(__("Edit your menu below, or <a href=\"%s\">create a new menu</a>. Don&#8217;t forget to save your changes!"), esc_url(add_query_arg(Array({"action": "edit", "menu": 0}), admin_url("nav-menus.php"))))
        php_print("         <span class=\"screen-reader-text\">")
        _e("Click the Save Menu button to save your changes.")
        php_print("</span>\n        </span><!-- /add-edit-menu-action -->\n     ")
    else:
        php_print("         <form method=\"get\" action=\"")
        php_print(admin_url("nav-menus.php"))
        php_print("\">\n            <input type=\"hidden\" name=\"action\" value=\"edit\" />\n          <label for=\"select-menu-to-edit\" class=\"selected-menu\">")
        _e("Select a menu to edit:")
        php_print("</label>\n           <select name=\"menu\" id=\"select-menu-to-edit\">\n             ")
        if add_new_screen:
            php_print("                 <option value=\"0\" selected=\"selected\">")
            _e("&mdash; Select &mdash;")
            php_print("</option>\n              ")
        # end if
        php_print("             ")
        for _nav_menu in nav_menus:
            php_print("                 <option value=\"")
            php_print(esc_attr(_nav_menu.term_id))
            php_print("\" ")
            selected(_nav_menu.term_id, nav_menu_selected_id)
            php_print(">\n                      ")
            php_print(esc_html(_nav_menu.truncated_name))
            if (not php_empty(lambda : menu_locations)) and php_in_array(_nav_menu.term_id, menu_locations):
                locations_assigned_to_this_menu = Array()
                for menu_location_key in php_array_keys(menu_locations, _nav_menu.term_id):
                    if (php_isset(lambda : locations[menu_location_key])):
                        locations_assigned_to_this_menu[-1] = locations[menu_location_key]
                    # end if
                # end for
                #// 
                #// Filters the number of locations listed per menu in the drop-down select.
                #// 
                #// @since 3.6.0
                #// 
                #// @param int $locations Number of menu locations to list. Default 3.
                #//
                assigned_locations = php_array_slice(locations_assigned_to_this_menu, 0, absint(apply_filters("wp_nav_locations_listed_per_menu", 3)))
                #// Adds ellipses following the number of locations defined in $assigned_locations.
                if (not php_empty(lambda : assigned_locations)):
                    printf(" (%1$s%2$s)", php_implode(", ", assigned_locations), " &hellip;" if php_count(locations_assigned_to_this_menu) > php_count(assigned_locations) else "")
                # end if
            # end if
            php_print("                 </option>\n             ")
        # end for
        php_print("         </select>\n         <span class=\"submit-btn\"><input type=\"submit\" class=\"button\" value=\"")
        esc_attr_e("Select")
        php_print("\"></span>\n         <span class=\"add-new-menu-action\">\n              ")
        printf(__("or <a href=\"%s\">create a new menu</a>. Don&#8217;t forget to save your changes!"), esc_url(add_query_arg(Array({"action": "edit", "menu": 0}), admin_url("nav-menus.php"))))
        php_print("             <span class=\"screen-reader-text\">")
        _e("Click the Save Menu button to save your changes.")
        php_print("""</span>
        </span><!-- /add-new-menu-action -->
        </form>
        """)
    # end if
    metabox_holder_disabled_class = ""
    if (php_isset(lambda : PHP_REQUEST["menu"])) and "0" == PHP_REQUEST["menu"]:
        metabox_holder_disabled_class = " metabox-holder-disabled"
    # end if
    php_print(" </div><!-- /manage-menus -->\n  <div id=\"nav-menus-frame\" class=\"wp-clearfix\">\n    <div id=\"menu-settings-column\" class=\"metabox-holder")
    php_print(metabox_holder_disabled_class)
    php_print("""\">
    <div class=\"clear\"></div>
    <form id=\"nav-menu-meta\" class=\"nav-menu-meta\" method=\"post\" enctype=\"multipart/form-data\">
    <input type=\"hidden\" name=\"menu\" id=\"nav-menu-meta-object-id\" value=\"""")
    php_print(esc_attr(nav_menu_selected_id))
    php_print("\" />\n          <input type=\"hidden\" name=\"action\" value=\"add-menu-item\" />\n         ")
    wp_nonce_field("add-menu_item", "menu-settings-column-nonce")
    php_print("         <h2>")
    _e("Add menu items")
    php_print("</h2>\n          ")
    do_accordion_sections("nav-menus", "side", None)
    php_print("""       </form>
    </div><!-- /#menu-settings-column -->
    <div id=\"menu-management-liquid\">
    <div id=\"menu-management\">
    <form id=\"update-nav-menu\" method=\"post\" enctype=\"multipart/form-data\">
    """)
    new_screen_class = ""
    if add_new_screen:
        new_screen_class = "blank-slate"
    # end if
    php_print("             <h2>")
    _e("Menu structure")
    php_print("</h2>\n              <div class=\"menu-edit ")
    php_print(new_screen_class)
    php_print("\">\n                    <input type=\"hidden\" name=\"nav-menu-data\">\n                    ")
    wp_nonce_field("closedpostboxes", "closedpostboxesnonce", False)
    wp_nonce_field("meta-box-order", "meta-box-order-nonce", False)
    wp_nonce_field("update-nav_menu", "update-nav-menu-nonce")
    menu_name_aria_desc = " aria-describedby=\"menu-name-desc\"" if add_new_screen else ""
    if one_theme_location_no_menus:
        menu_name_val = "value=\"" + esc_attr("Menu 1") + "\""
        php_print("                     <input type=\"hidden\" name=\"zero-menu-state\" value=\"true\" />\n                     ")
    else:
        menu_name_val = "value=\"" + esc_attr(nav_menu_selected_title) + "\""
    # end if
    php_print("                 <input type=\"hidden\" name=\"action\" value=\"update\" />\n                    <input type=\"hidden\" name=\"menu\" id=\"menu\" value=\"")
    php_print(esc_attr(nav_menu_selected_id))
    php_print("""\" />
    <div id=\"nav-menu-header\">
    <div class=\"major-publishing-actions wp-clearfix\">
    <label class=\"menu-name-label\" for=\"menu-name\">""")
    _e("Menu Name")
    php_print("</label>\n                           <input name=\"menu-name\" id=\"menu-name\" type=\"text\" class=\"menu-name regular-text menu-item-textbox\" ")
    php_print(menu_name_val + menu_name_aria_desc)
    php_print(" />\n                            <div class=\"publishing-action\">\n                             ")
    submit_button(__("Create Menu") if php_empty(lambda : nav_menu_selected_id) else __("Save Menu"), "primary large menu-save", "save_menu", False, Array({"id": "save_menu_header"}))
    php_print("""                           </div><!-- END .publishing-action -->
    </div><!-- END .major-publishing-actions -->
    </div><!-- END .nav-menu-header -->
    <div id=\"post-body\">
    <div id=\"post-body-content\" class=\"wp-clearfix\">
    """)
    if (not add_new_screen):
        php_print("                             ")
        hide_style = ""
        if (php_isset(lambda : menu_items)) and 0 == php_count(menu_items):
            hide_style = "style=\"display: none;\""
        # end if
        if one_theme_location_no_menus:
            starter_copy = __("Edit your default menu by adding or removing items. Drag the items into the order you prefer. Click Create Menu to save your changes.")
        else:
            starter_copy = __("Drag the items into the order you prefer. Click the arrow on the right of the item to reveal additional configuration options.")
        # end if
        php_print("                         <div class=\"drag-instructions post-body-plain\" ")
        php_print(hide_style)
        php_print(">\n                              <p>")
        php_print(starter_copy)
        php_print("</p>\n                           </div>\n                                ")
        if (php_isset(lambda : edit_markup)) and (not is_wp_error(edit_markup)):
            php_print(edit_markup)
        else:
            php_print("                         <ul class=\"menu\" id=\"menu-to-edit\"></ul>\n                              ")
        # end if
        php_print("                         ")
    # end if
    php_print("                         ")
    if add_new_screen:
        php_print("                             <p class=\"post-body-plain\" id=\"menu-name-desc\">")
        _e("Give your menu a name, then click Create Menu.")
        php_print("</p>\n                               ")
        if (php_isset(lambda : PHP_REQUEST["use-location"])):
            php_print("                                 <input type=\"hidden\" name=\"use-location\" value=\"")
            php_print(esc_attr(PHP_REQUEST["use-location"]))
            php_print("\" />\n                              ")
        # end if
        php_print("                             ")
    # end if
    no_menus_style = ""
    if one_theme_location_no_menus:
        no_menus_style = "style=\"display: none;\""
    # end if
    php_print("                         <div class=\"menu-settings\" ")
    php_print(no_menus_style)
    php_print(">\n                              <h3>")
    _e("Menu Settings")
    php_print("</h3>\n                              ")
    if (not (php_isset(lambda : auto_add))):
        auto_add = get_option("nav_menu_options")
        if (not (php_isset(lambda : auto_add["auto_add"]))):
            auto_add = False
        elif False != php_array_search(nav_menu_selected_id, auto_add["auto_add"]):
            auto_add = True
        else:
            auto_add = False
        # end if
    # end if
    php_print("\n                               <fieldset class=\"menu-settings-group auto-add-pages\">\n                                   <legend class=\"menu-settings-group-name howto\">")
    _e("Auto add pages")
    php_print("</legend>\n                                  <div class=\"menu-settings-input checkbox-input\">\n                                        <input type=\"checkbox\"")
    checked(auto_add)
    php_print(" name=\"auto-add-pages\" id=\"auto-add-pages\" value=\"1\" /> <label for=\"auto-add-pages\">")
    printf(__("Automatically add new top-level pages to this menu"), esc_url(admin_url("edit.php?post_type=page")))
    php_print("""</label>
    </div>
    </fieldset>
    """)
    if current_theme_supports("menus"):
        php_print("\n                                   <fieldset class=\"menu-settings-group menu-theme-locations\">\n                                     <legend class=\"menu-settings-group-name howto\">")
        _e("Display location")
        php_print("</legend>\n                                      ")
        for location,description in locations:
            php_print("                                     <div class=\"menu-settings-input checkbox-input\">\n                                            <input type=\"checkbox\"")
            checked((php_isset(lambda : menu_locations[location])) and menu_locations[location] == nav_menu_selected_id)
            php_print(" name=\"menu-locations[")
            php_print(esc_attr(location))
            php_print("]\" id=\"locations-")
            php_print(esc_attr(location))
            php_print("\" value=\"")
            php_print(esc_attr(nav_menu_selected_id))
            php_print("\" />\n                                          <label for=\"locations-")
            php_print(esc_attr(location))
            php_print("\">")
            php_print(description)
            php_print("</label>\n                                           ")
            if (not php_empty(lambda : menu_locations[location])) and menu_locations[location] != nav_menu_selected_id:
                php_print("                                             <span class=\"theme-location-set\">\n                                               ")
                printf(_x("(Currently set to: %s)", "menu location"), wp_get_nav_menu_object(menu_locations[location]).name)
                php_print("                                             </span>\n                                           ")
            # end if
            php_print("                                     </div>\n                                        ")
        # end for
        php_print("                                 </fieldset>\n\n                             ")
    # end if
    php_print("""
    </div>
    </div><!-- /#post-body-content -->
    </div><!-- /#post-body -->
    <div id=\"nav-menu-footer\">
    <div class=\"major-publishing-actions wp-clearfix\">
    """)
    if 0 != menu_count and (not add_new_screen):
        php_print("                         <span class=\"delete-action\">\n                                <a class=\"submitdelete deletion menu-delete\" href=\"\n                                ")
        php_print(esc_url(wp_nonce_url(add_query_arg(Array({"action": "delete", "menu": nav_menu_selected_id}), admin_url("nav-menus.php")), "delete-nav_menu-" + nav_menu_selected_id)))
        php_print("                             \">")
        _e("Delete Menu")
        php_print("</a>\n                           </span><!-- END .delete-action -->\n                            ")
    # end if
    php_print("                         <div class=\"publishing-action\">\n                             ")
    submit_button(__("Create Menu") if php_empty(lambda : nav_menu_selected_id) else __("Save Menu"), "primary large menu-save", "save_menu", False, Array({"id": "save_menu_footer"}))
    php_print("""                           </div><!-- END .publishing-action -->
    </div><!-- END .major-publishing-actions -->
    </div><!-- /#nav-menu-footer -->
    </div><!-- /.menu-edit -->
    </form><!-- /#update-nav-menu -->
    </div><!-- /#menu-management -->
    </div><!-- /#menu-management-liquid -->
    </div><!-- /#nav-menus-frame -->
    """)
# end if
php_print("</div><!-- /.wrap-->\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
