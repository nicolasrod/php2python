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
#// Navigation Menu functions
#// 
#// @package WordPress
#// @subpackage Nav_Menus
#// @since 3.0.0
#// 
#// 
#// Returns a navigation menu object.
#// 
#// @since 3.0.0
#// 
#// @param int|string|WP_Term $menu Menu ID, slug, name, or object.
#// @return WP_Term|false False if $menu param isn't supplied or term does not exist, menu object if successful.
#//
def wp_get_nav_menu_object(menu=None, *args_):
    
    menu_obj = False
    if php_is_object(menu):
        menu_obj = menu
    # end if
    if menu and (not menu_obj):
        menu_obj = get_term(menu, "nav_menu")
        if (not menu_obj):
            menu_obj = get_term_by("slug", menu, "nav_menu")
        # end if
        if (not menu_obj):
            menu_obj = get_term_by("name", menu, "nav_menu")
        # end if
    # end if
    if (not menu_obj) or is_wp_error(menu_obj):
        menu_obj = False
    # end if
    #// 
    #// Filters the nav_menu term retrieved for wp_get_nav_menu_object().
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Term|false      $menu_obj Term from nav_menu taxonomy, or false if nothing had been found.
    #// @param int|string|WP_Term $menu     The menu ID, slug, name, or object passed to wp_get_nav_menu_object().
    #//
    return apply_filters("wp_get_nav_menu_object", menu_obj, menu)
# end def wp_get_nav_menu_object
#// 
#// Check if the given ID is a navigation menu.
#// 
#// Returns true if it is; false otherwise.
#// 
#// @since 3.0.0
#// 
#// @param int|string|WP_Term $menu Menu ID, slug, name, or object of menu to check.
#// @return bool Whether the menu exists.
#//
def is_nav_menu(menu=None, *args_):
    
    if (not menu):
        return False
    # end if
    menu_obj = wp_get_nav_menu_object(menu)
    if menu_obj and (not is_wp_error(menu_obj)) and (not php_empty(lambda : menu_obj.taxonomy)) and "nav_menu" == menu_obj.taxonomy:
        return True
    # end if
    return False
# end def is_nav_menu
#// 
#// Registers navigation menu locations for a theme.
#// 
#// @since 3.0.0
#// 
#// @global array $_wp_registered_nav_menus
#// 
#// @param array $locations Associative array of menu location identifiers (like a slug) and descriptive text.
#//
def register_nav_menus(locations=Array(), *args_):
    
    global _wp_registered_nav_menus
    php_check_if_defined("_wp_registered_nav_menus")
    add_theme_support("menus")
    for key,value in locations:
        if php_is_int(key):
            _doing_it_wrong(__FUNCTION__, __("Nav menu locations must be strings."), "5.3.0")
            break
        # end if
    # end for
    _wp_registered_nav_menus = php_array_merge(_wp_registered_nav_menus, locations)
# end def register_nav_menus
#// 
#// Unregisters a navigation menu location for a theme.
#// 
#// @since 3.1.0
#// @global array $_wp_registered_nav_menus
#// 
#// @param string $location The menu location identifier.
#// @return bool True on success, false on failure.
#//
def unregister_nav_menu(location=None, *args_):
    
    global _wp_registered_nav_menus
    php_check_if_defined("_wp_registered_nav_menus")
    if php_is_array(_wp_registered_nav_menus) and (php_isset(lambda : _wp_registered_nav_menus[location])):
        _wp_registered_nav_menus[location] = None
        if php_empty(lambda : _wp_registered_nav_menus):
            _remove_theme_support("menus")
        # end if
        return True
    # end if
    return False
# end def unregister_nav_menu
#// 
#// Registers a navigation menu location for a theme.
#// 
#// @since 3.0.0
#// 
#// @param string $location    Menu location identifier, like a slug.
#// @param string $description Menu location descriptive text.
#//
def register_nav_menu(location=None, description=None, *args_):
    
    register_nav_menus(Array({location: description}))
# end def register_nav_menu
#// 
#// Retrieves all registered navigation menu locations in a theme.
#// 
#// @since 3.0.0
#// 
#// @global array $_wp_registered_nav_menus
#// 
#// @return array Registered navigation menu locations. If none are registered, an empty array.
#//
def get_registered_nav_menus(*args_):
    
    global _wp_registered_nav_menus
    php_check_if_defined("_wp_registered_nav_menus")
    if (php_isset(lambda : _wp_registered_nav_menus)):
        return _wp_registered_nav_menus
    # end if
    return Array()
# end def get_registered_nav_menus
#// 
#// Retrieves all registered navigation menu locations and the menus assigned to them.
#// 
#// @since 3.0.0
#// 
#// @return array Registered navigation menu locations and the menus assigned them.
#// If none are registered, an empty array.
#//
def get_nav_menu_locations(*args_):
    
    locations = get_theme_mod("nav_menu_locations")
    return locations if php_is_array(locations) else Array()
# end def get_nav_menu_locations
#// 
#// Determines whether a registered nav menu location has a menu assigned to it.
#// 
#// @since 3.0.0
#// 
#// @param string $location Menu location identifier.
#// @return bool Whether location has a menu.
#//
def has_nav_menu(location=None, *args_):
    
    has_nav_menu = False
    registered_nav_menus = get_registered_nav_menus()
    if (php_isset(lambda : registered_nav_menus[location])):
        locations = get_nav_menu_locations()
        has_nav_menu = (not php_empty(lambda : locations[location]))
    # end if
    #// 
    #// Filters whether a nav menu is assigned to the specified location.
    #// 
    #// @since 4.3.0
    #// 
    #// @param bool   $has_nav_menu Whether there is a menu assigned to a location.
    #// @param string $location     Menu location.
    #//
    return apply_filters("has_nav_menu", has_nav_menu, location)
# end def has_nav_menu
#// 
#// Returns the name of a navigation menu.
#// 
#// @since 4.9.0
#// 
#// @param string $location Menu location identifier.
#// @return string Menu name.
#//
def wp_get_nav_menu_name(location=None, *args_):
    
    menu_name = ""
    locations = get_nav_menu_locations()
    if (php_isset(lambda : locations[location])):
        menu = wp_get_nav_menu_object(locations[location])
        if menu and menu.name:
            menu_name = menu.name
        # end if
    # end if
    #// 
    #// Filters the navigation menu name being returned.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $menu_name Menu name.
    #// @param string $location  Menu location identifier.
    #//
    return apply_filters("wp_get_nav_menu_name", menu_name, location)
# end def wp_get_nav_menu_name
#// 
#// Determines whether the given ID is a nav menu item.
#// 
#// @since 3.0.0
#// 
#// @param int $menu_item_id The ID of the potential nav menu item.
#// @return bool Whether the given ID is that of a nav menu item.
#//
def is_nav_menu_item(menu_item_id=0, *args_):
    
    return (not is_wp_error(menu_item_id)) and "nav_menu_item" == get_post_type(menu_item_id)
# end def is_nav_menu_item
#// 
#// Creates a navigation menu.
#// 
#// Note that `$menu_name` is expected to be pre-slashed.
#// 
#// @since 3.0.0
#// 
#// @param string $menu_name Menu name.
#// @return int|WP_Error Menu ID on success, WP_Error object on failure.
#//
def wp_create_nav_menu(menu_name=None, *args_):
    
    #// expected_slashed ($menu_name)
    return wp_update_nav_menu_object(0, Array({"menu-name": menu_name}))
# end def wp_create_nav_menu
#// 
#// Delete a Navigation Menu.
#// 
#// @since 3.0.0
#// 
#// @param int|string|WP_Term $menu Menu ID, slug, name, or object.
#// @return bool|WP_Error True on success, false or WP_Error object on failure.
#//
def wp_delete_nav_menu(menu=None, *args_):
    
    menu = wp_get_nav_menu_object(menu)
    if (not menu):
        return False
    # end if
    menu_objects = get_objects_in_term(menu.term_id, "nav_menu")
    if (not php_empty(lambda : menu_objects)):
        for item in menu_objects:
            wp_delete_post(item)
        # end for
    # end if
    result = wp_delete_term(menu.term_id, "nav_menu")
    #// Remove this menu from any locations.
    locations = get_nav_menu_locations()
    for location,menu_id in locations:
        if menu_id == menu.term_id:
            locations[location] = 0
        # end if
    # end for
    set_theme_mod("nav_menu_locations", locations)
    if result and (not is_wp_error(result)):
        #// 
        #// Fires after a navigation menu has been successfully deleted.
        #// 
        #// @since 3.0.0
        #// 
        #// @param int $term_id ID of the deleted menu.
        #//
        do_action("wp_delete_nav_menu", menu.term_id)
    # end if
    return result
# end def wp_delete_nav_menu
#// 
#// Save the properties of a menu or create a new menu with those properties.
#// 
#// Note that `$menu_data` is expected to be pre-slashed.
#// 
#// @since 3.0.0
#// 
#// @param int   $menu_id   The ID of the menu or "0" to create a new menu.
#// @param array $menu_data The array of menu data.
#// @return int|WP_Error Menu ID on success, WP_Error object on failure.
#//
def wp_update_nav_menu_object(menu_id=0, menu_data=Array(), *args_):
    
    #// expected_slashed ($menu_data)
    menu_id = php_int(menu_id)
    _menu = wp_get_nav_menu_object(menu_id)
    args = Array({"description": menu_data["description"] if (php_isset(lambda : menu_data["description"])) else "", "name": menu_data["menu-name"] if (php_isset(lambda : menu_data["menu-name"])) else "", "parent": php_int(menu_data["parent"]) if (php_isset(lambda : menu_data["parent"])) else 0, "slug": None})
    #// Double-check that we're not going to have one menu take the name of another.
    _possible_existing = get_term_by("name", menu_data["menu-name"], "nav_menu")
    if _possible_existing and (not is_wp_error(_possible_existing)) and (php_isset(lambda : _possible_existing.term_id)) and _possible_existing.term_id != menu_id:
        return php_new_class("WP_Error", lambda : WP_Error("menu_exists", php_sprintf(__("The menu name %s conflicts with another menu name. Please try another."), "<strong>" + esc_html(menu_data["menu-name"]) + "</strong>")))
    # end if
    #// Menu doesn't already exist, so create a new menu.
    if (not _menu) or is_wp_error(_menu):
        menu_exists = get_term_by("name", menu_data["menu-name"], "nav_menu")
        if menu_exists:
            return php_new_class("WP_Error", lambda : WP_Error("menu_exists", php_sprintf(__("The menu name %s conflicts with another menu name. Please try another."), "<strong>" + esc_html(menu_data["menu-name"]) + "</strong>")))
        # end if
        _menu = wp_insert_term(menu_data["menu-name"], "nav_menu", args)
        if is_wp_error(_menu):
            return _menu
        # end if
        #// 
        #// Fires after a navigation menu is successfully created.
        #// 
        #// @since 3.0.0
        #// 
        #// @param int   $term_id   ID of the new menu.
        #// @param array $menu_data An array of menu data.
        #//
        do_action("wp_create_nav_menu", _menu["term_id"], menu_data)
        return php_int(_menu["term_id"])
    # end if
    if (not _menu) or (not (php_isset(lambda : _menu.term_id))):
        return 0
    # end if
    menu_id = php_int(_menu.term_id)
    update_response = wp_update_term(menu_id, "nav_menu", args)
    if is_wp_error(update_response):
        return update_response
    # end if
    menu_id = php_int(update_response["term_id"])
    #// 
    #// Fires after a navigation menu has been successfully updated.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int   $menu_id   ID of the updated menu.
    #// @param array $menu_data An array of menu data.
    #//
    do_action("wp_update_nav_menu", menu_id, menu_data)
    return menu_id
# end def wp_update_nav_menu_object
#// 
#// Save the properties of a menu item or create a new one.
#// 
#// The menu-item-title, menu-item-description, and menu-item-attr-title are expected
#// to be pre-slashed since they are passed directly into `wp_insert_post()`.
#// 
#// @since 3.0.0
#// 
#// @param int   $menu_id         The ID of the menu. Required. If "0", makes the menu item a draft orphan.
#// @param int   $menu_item_db_id The ID of the menu item. If "0", creates a new menu item.
#// @param array $menu_item_data  The menu item's data.
#// @return int|WP_Error The menu item's database ID or WP_Error object on failure.
#//
def wp_update_nav_menu_item(menu_id=0, menu_item_db_id=0, menu_item_data=Array(), *args_):
    
    menu_id = php_int(menu_id)
    menu_item_db_id = php_int(menu_item_db_id)
    #// Make sure that we don't convert non-nav_menu_item objects into nav_menu_item objects.
    if (not php_empty(lambda : menu_item_db_id)) and (not is_nav_menu_item(menu_item_db_id)):
        return php_new_class("WP_Error", lambda : WP_Error("update_nav_menu_item_failed", __("The given object ID is not that of a menu item.")))
    # end if
    menu = wp_get_nav_menu_object(menu_id)
    if (not menu) and 0 != menu_id:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_menu_id", __("Invalid menu ID.")))
    # end if
    if is_wp_error(menu):
        return menu
    # end if
    defaults = Array({"menu-item-db-id": menu_item_db_id, "menu-item-object-id": 0, "menu-item-object": "", "menu-item-parent-id": 0, "menu-item-position": 0, "menu-item-type": "custom", "menu-item-title": "", "menu-item-url": "", "menu-item-description": "", "menu-item-attr-title": "", "menu-item-target": "", "menu-item-classes": "", "menu-item-xfn": "", "menu-item-status": ""})
    args = wp_parse_args(menu_item_data, defaults)
    if 0 == menu_id:
        args["menu-item-position"] = 1
    elif 0 == php_int(args["menu-item-position"]):
        menu_items = Array() if 0 == menu_id else wp_get_nav_menu_items(menu_id, Array({"post_status": "publish,draft"}))
        last_item = php_array_pop(menu_items)
        args["menu-item-position"] = 1 + last_item.menu_order if last_item and (php_isset(lambda : last_item.menu_order)) else php_count(menu_items)
    # end if
    original_parent = get_post_field("post_parent", menu_item_db_id) if 0 < menu_item_db_id else 0
    if "custom" == args["menu-item-type"]:
        #// If custom menu item, trim the URL.
        args["menu-item-url"] = php_trim(args["menu-item-url"])
    else:
        #// 
        #// If non-custom menu item, then:
        #// - use the original object's URL.
        #// - blank default title to sync with the original object's title.
        #//
        args["menu-item-url"] = ""
        original_title = ""
        if "taxonomy" == args["menu-item-type"]:
            original_parent = get_term_field("parent", args["menu-item-object-id"], args["menu-item-object"], "raw")
            original_title = get_term_field("name", args["menu-item-object-id"], args["menu-item-object"], "raw")
        elif "post_type" == args["menu-item-type"]:
            original_object = get_post(args["menu-item-object-id"])
            original_parent = php_int(original_object.post_parent)
            original_title = original_object.post_title
        elif "post_type_archive" == args["menu-item-type"]:
            original_object = get_post_type_object(args["menu-item-object"])
            if original_object:
                original_title = original_object.labels.archives
            # end if
        # end if
        if args["menu-item-title"] == original_title:
            args["menu-item-title"] = ""
        # end if
        #// Hack to get wp to create a post object when too many properties are empty.
        if "" == args["menu-item-title"] and "" == args["menu-item-description"]:
            args["menu-item-description"] = " "
        # end if
    # end if
    #// Populate the menu item object.
    post = Array({"menu_order": args["menu-item-position"], "ping_status": 0, "post_content": args["menu-item-description"], "post_excerpt": args["menu-item-attr-title"], "post_parent": original_parent, "post_title": args["menu-item-title"], "post_type": "nav_menu_item"})
    update = 0 != menu_item_db_id
    #// New menu item. Default is draft status.
    if (not update):
        post["ID"] = 0
        post["post_status"] = "publish" if "publish" == args["menu-item-status"] else "draft"
        menu_item_db_id = wp_insert_post(post)
        if (not menu_item_db_id) or is_wp_error(menu_item_db_id):
            return menu_item_db_id
        # end if
        #// 
        #// Fires immediately after a new navigation menu item has been added.
        #// 
        #// @since 4.4.0
        #// 
        #// @see wp_update_nav_menu_item()
        #// 
        #// @param int   $menu_id         ID of the updated menu.
        #// @param int   $menu_item_db_id ID of the new menu item.
        #// @param array $args            An array of arguments used to update/add the menu item.
        #//
        do_action("wp_add_nav_menu_item", menu_id, menu_item_db_id, args)
    # end if
    #// Associate the menu item with the menu term.
    #// Only set the menu term if it isn't set to avoid unnecessary wp_get_object_terms().
    if menu_id and (not update) or (not is_object_in_term(menu_item_db_id, "nav_menu", php_int(menu.term_id))):
        wp_set_object_terms(menu_item_db_id, Array(menu.term_id), "nav_menu")
    # end if
    if "custom" == args["menu-item-type"]:
        args["menu-item-object-id"] = menu_item_db_id
        args["menu-item-object"] = "custom"
    # end if
    menu_item_db_id = php_int(menu_item_db_id)
    update_post_meta(menu_item_db_id, "_menu_item_type", sanitize_key(args["menu-item-type"]))
    update_post_meta(menu_item_db_id, "_menu_item_menu_item_parent", php_strval(php_int(args["menu-item-parent-id"])))
    update_post_meta(menu_item_db_id, "_menu_item_object_id", php_strval(php_int(args["menu-item-object-id"])))
    update_post_meta(menu_item_db_id, "_menu_item_object", sanitize_key(args["menu-item-object"]))
    update_post_meta(menu_item_db_id, "_menu_item_target", sanitize_key(args["menu-item-target"]))
    args["menu-item-classes"] = php_array_map("sanitize_html_class", php_explode(" ", args["menu-item-classes"]))
    args["menu-item-xfn"] = php_implode(" ", php_array_map("sanitize_html_class", php_explode(" ", args["menu-item-xfn"])))
    update_post_meta(menu_item_db_id, "_menu_item_classes", args["menu-item-classes"])
    update_post_meta(menu_item_db_id, "_menu_item_xfn", args["menu-item-xfn"])
    update_post_meta(menu_item_db_id, "_menu_item_url", esc_url_raw(args["menu-item-url"]))
    if 0 == menu_id:
        update_post_meta(menu_item_db_id, "_menu_item_orphaned", php_str(time()))
    elif get_post_meta(menu_item_db_id, "_menu_item_orphaned"):
        delete_post_meta(menu_item_db_id, "_menu_item_orphaned")
    # end if
    #// Update existing menu item. Default is publish status.
    if update:
        post["ID"] = menu_item_db_id
        post["post_status"] = "draft" if "draft" == args["menu-item-status"] else "publish"
        wp_update_post(post)
    # end if
    #// 
    #// Fires after a navigation menu item has been updated.
    #// 
    #// @since 3.0.0
    #// 
    #// @see wp_update_nav_menu_item()
    #// 
    #// @param int   $menu_id         ID of the updated menu.
    #// @param int   $menu_item_db_id ID of the updated menu item.
    #// @param array $args            An array of arguments used to update a menu item.
    #//
    do_action("wp_update_nav_menu_item", menu_id, menu_item_db_id, args)
    return menu_item_db_id
# end def wp_update_nav_menu_item
#// 
#// Returns all navigation menu objects.
#// 
#// @since 3.0.0
#// @since 4.1.0 Default value of the 'orderby' argument was changed from 'none'
#// to 'name'.
#// 
#// @param array $args Optional. Array of arguments passed on to get_terms().
#// Default empty array.
#// @return WP_Term[] An array of menu objects.
#//
def wp_get_nav_menus(args=Array(), *args_):
    
    defaults = Array({"taxonomy": "nav_menu", "hide_empty": False, "orderby": "name"})
    args = wp_parse_args(args, defaults)
    #// 
    #// Filters the navigation menu objects being returned.
    #// 
    #// @since 3.0.0
    #// 
    #// @see get_terms()
    #// 
    #// @param WP_Term[] $menus An array of menu objects.
    #// @param array     $args  An array of arguments used to retrieve menu objects.
    #//
    return apply_filters("wp_get_nav_menus", get_terms(args), args)
# end def wp_get_nav_menus
#// 
#// Return if a menu item is valid.
#// 
#// @link https://core.trac.wordpress.org/ticket/13958
#// 
#// @since 3.2.0
#// @access private
#// 
#// @param object $item The menu item to check.
#// @return bool False if invalid, otherwise true.
#//
def _is_valid_nav_menu_item(item=None, *args_):
    
    return php_empty(lambda : item._invalid)
# end def _is_valid_nav_menu_item
#// 
#// Retrieves all menu items of a navigation menu.
#// 
#// Note: Most arguments passed to the `$args` parameter – save for 'output_key' – are
#// specifically for retrieving nav_menu_item posts from get_posts() and may only
#// indirectly affect the ultimate ordering and content of the resulting nav menu
#// items that get returned from this function.
#// 
#// @since 3.0.0
#// 
#// @staticvar array $fetched
#// 
#// @param int|string|WP_Term $menu Menu ID, slug, name, or object.
#// @param array              $args {
#// Optional. Arguments to pass to get_posts().
#// 
#// @type string $order       How to order nav menu items as queried with get_posts(). Will be ignored
#// if 'output' is ARRAY_A. Default 'ASC'.
#// @type string $orderby     Field to order menu items by as retrieved from get_posts(). Supply an orderby
#// field via 'output_key' to affect the output order of nav menu items.
#// Default 'menu_order'.
#// @type string $post_type   Menu items post type. Default 'nav_menu_item'.
#// @type string $post_status Menu items post status. Default 'publish'.
#// @type string $output      How to order outputted menu items. Default ARRAY_A.
#// @type string $output_key  Key to use for ordering the actual menu items that get returned. Note that
#// that is not a get_posts() argument and will only affect output of menu items
#// processed in this function. Default 'menu_order'.
#// @type bool   $nopaging    Whether to retrieve all menu items (true) or paginate (false). Default true.
#// }
#// @return array|false $items Array of menu items, otherwise false.
#//
def wp_get_nav_menu_items(menu=None, args=Array(), *args_):
    
    menu = wp_get_nav_menu_object(menu)
    if (not menu):
        return False
    # end if
    wp_get_nav_menu_items.fetched = Array()
    items = get_objects_in_term(menu.term_id, "nav_menu")
    if is_wp_error(items):
        return False
    # end if
    defaults = Array({"order": "ASC", "orderby": "menu_order", "post_type": "nav_menu_item", "post_status": "publish", "output": ARRAY_A, "output_key": "menu_order", "nopaging": True})
    args = wp_parse_args(args, defaults)
    args["include"] = items
    if (not php_empty(lambda : items)):
        items = get_posts(args)
    else:
        items = Array()
    # end if
    #// Get all posts and terms at once to prime the caches.
    if php_empty(lambda : wp_get_nav_menu_items.fetched[menu.term_id]) and (not wp_using_ext_object_cache()):
        wp_get_nav_menu_items.fetched[menu.term_id] = True
        posts = Array()
        terms = Array()
        for item in items:
            object_id = get_post_meta(item.ID, "_menu_item_object_id", True)
            object = get_post_meta(item.ID, "_menu_item_object", True)
            type = get_post_meta(item.ID, "_menu_item_type", True)
            if "post_type" == type:
                posts[object][-1] = object_id
            elif "taxonomy" == type:
                terms[object][-1] = object_id
            # end if
        # end for
        if (not php_empty(lambda : posts)):
            for post_type in php_array_keys(posts):
                get_posts(Array({"post__in": posts[post_type], "post_type": post_type, "nopaging": True, "update_post_term_cache": False}))
            # end for
        # end if
        posts = None
        if (not php_empty(lambda : terms)):
            for taxonomy in php_array_keys(terms):
                get_terms(Array({"taxonomy": taxonomy, "include": terms[taxonomy], "hierarchical": False}))
            # end for
        # end if
        terms = None
    # end if
    items = php_array_map("wp_setup_nav_menu_item", items)
    if (not is_admin()):
        #// Remove invalid items only on front end.
        items = php_array_filter(items, "_is_valid_nav_menu_item")
    # end if
    if ARRAY_A == args["output"]:
        items = wp_list_sort(items, Array({args["output_key"]: "ASC"}))
        i = 1
        for k,item in items:
            items[k].args["output_key"] = i
            i += 1
        # end for
    # end if
    #// 
    #// Filters the navigation menu items being returned.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array  $items An array of menu item post objects.
    #// @param object $menu  The menu object.
    #// @param array  $args  An array of arguments used to retrieve menu item objects.
    #//
    return apply_filters("wp_get_nav_menu_items", items, menu, args)
# end def wp_get_nav_menu_items
#// 
#// Decorates a menu item object with the shared navigation menu item properties.
#// 
#// Properties:
#// - ID:               The term_id if the menu item represents a taxonomy term.
#// - attr_title:       The title attribute of the link element for this menu item.
#// - classes:          The array of class attribute values for the link element of this menu item.
#// - db_id:            The DB ID of this item as a nav_menu_item object, if it exists (0 if it doesn't exist).
#// - description:      The description of this menu item.
#// - menu_item_parent: The DB ID of the nav_menu_item that is this item's menu parent, if any. 0 otherwise.
#// - object:           The type of object originally represented, such as 'category', 'post', or 'attachment'.
#// - object_id:        The DB ID of the original object this menu item represents, e.g. ID for posts and term_id for categories.
#// - post_parent:      The DB ID of the original object's parent object, if any (0 otherwise).
#// - post_title:       A "no title" label if menu item represents a post that lacks a title.
#// - target:           The target attribute of the link element for this menu item.
#// - title:            The title of this menu item.
#// - type:             The family of objects originally represented, such as 'post_type' or 'taxonomy'.
#// - type_label:       The singular label used to describe this type of menu item.
#// - url:              The URL to which this menu item points.
#// - xfn:              The XFN relationship expressed in the link of this menu item.
#// - _invalid:         Whether the menu item represents an object that no longer exists.
#// 
#// @since 3.0.0
#// 
#// @param object $menu_item The menu item to modify.
#// @return object $menu_item The menu item with standard menu item properties.
#//
def wp_setup_nav_menu_item(menu_item=None, *args_):
    
    if (php_isset(lambda : menu_item.post_type)):
        if "nav_menu_item" == menu_item.post_type:
            menu_item.db_id = php_int(menu_item.ID)
            menu_item.menu_item_parent = get_post_meta(menu_item.ID, "_menu_item_menu_item_parent", True) if (not (php_isset(lambda : menu_item.menu_item_parent))) else menu_item.menu_item_parent
            menu_item.object_id = get_post_meta(menu_item.ID, "_menu_item_object_id", True) if (not (php_isset(lambda : menu_item.object_id))) else menu_item.object_id
            menu_item.object = get_post_meta(menu_item.ID, "_menu_item_object", True) if (not (php_isset(lambda : menu_item.object))) else menu_item.object
            menu_item.type = get_post_meta(menu_item.ID, "_menu_item_type", True) if (not (php_isset(lambda : menu_item.type))) else menu_item.type
            if "post_type" == menu_item.type:
                object = get_post_type_object(menu_item.object)
                if object:
                    menu_item.type_label = object.labels.singular_name
                    #// Use post states for special pages (only in the admin).
                    if php_function_exists("get_post_states"):
                        menu_post = get_post(menu_item.object_id)
                        post_states = get_post_states(menu_post)
                        if post_states:
                            menu_item.type_label = wp_strip_all_tags(php_implode(", ", post_states))
                        # end if
                    # end if
                else:
                    menu_item.type_label = menu_item.object
                    menu_item._invalid = True
                # end if
                if "trash" == get_post_status(menu_item.object_id):
                    menu_item._invalid = True
                # end if
                original_object = get_post(menu_item.object_id)
                if original_object:
                    menu_item.url = get_permalink(original_object.ID)
                    #// This filter is documented in wp-includes/post-template.php
                    original_title = apply_filters("the_title", original_object.post_title, original_object.ID)
                else:
                    menu_item.url = ""
                    original_title = ""
                    menu_item._invalid = True
                # end if
                if "" == original_title:
                    #// translators: %d: ID of a post.
                    original_title = php_sprintf(__("#%d (no title)"), menu_item.object_id)
                # end if
                menu_item.title = original_title if "" == menu_item.post_title else menu_item.post_title
            elif "post_type_archive" == menu_item.type:
                object = get_post_type_object(menu_item.object)
                if object:
                    menu_item.title = object.labels.archives if "" == menu_item.post_title else menu_item.post_title
                    post_type_description = object.description
                else:
                    post_type_description = ""
                    menu_item._invalid = True
                # end if
                menu_item.type_label = __("Post Type Archive")
                post_content = wp_trim_words(menu_item.post_content, 200)
                post_type_description = post_type_description if "" == post_content else post_content
                menu_item.url = get_post_type_archive_link(menu_item.object)
            elif "taxonomy" == menu_item.type:
                object = get_taxonomy(menu_item.object)
                if object:
                    menu_item.type_label = object.labels.singular_name
                else:
                    menu_item.type_label = menu_item.object
                    menu_item._invalid = True
                # end if
                original_object = get_term(php_int(menu_item.object_id), menu_item.object)
                if original_object and (not is_wp_error(original_object)):
                    menu_item.url = get_term_link(php_int(menu_item.object_id), menu_item.object)
                    original_title = original_object.name
                else:
                    menu_item.url = ""
                    original_title = ""
                    menu_item._invalid = True
                # end if
                if "" == original_title:
                    #// translators: %d: ID of a term.
                    original_title = php_sprintf(__("#%d (no title)"), menu_item.object_id)
                # end if
                menu_item.title = original_title if "" == menu_item.post_title else menu_item.post_title
            else:
                menu_item.type_label = __("Custom Link")
                menu_item.title = menu_item.post_title
                menu_item.url = get_post_meta(menu_item.ID, "_menu_item_url", True) if (not (php_isset(lambda : menu_item.url))) else menu_item.url
            # end if
            menu_item.target = get_post_meta(menu_item.ID, "_menu_item_target", True) if (not (php_isset(lambda : menu_item.target))) else menu_item.target
            #// 
            #// Filters a navigation menu item's title attribute.
            #// 
            #// @since 3.0.0
            #// 
            #// @param string $item_title The menu item title attribute.
            #//
            menu_item.attr_title = apply_filters("nav_menu_attr_title", menu_item.post_excerpt) if (not (php_isset(lambda : menu_item.attr_title))) else menu_item.attr_title
            if (not (php_isset(lambda : menu_item.description))):
                #// 
                #// Filters a navigation menu item's description.
                #// 
                #// @since 3.0.0
                #// 
                #// @param string $description The menu item description.
                #//
                menu_item.description = apply_filters("nav_menu_description", wp_trim_words(menu_item.post_content, 200))
            # end if
            menu_item.classes = get_post_meta(menu_item.ID, "_menu_item_classes", True) if (not (php_isset(lambda : menu_item.classes))) else menu_item.classes
            menu_item.xfn = get_post_meta(menu_item.ID, "_menu_item_xfn", True) if (not (php_isset(lambda : menu_item.xfn))) else menu_item.xfn
        else:
            menu_item.db_id = 0
            menu_item.menu_item_parent = 0
            menu_item.object_id = php_int(menu_item.ID)
            menu_item.type = "post_type"
            object = get_post_type_object(menu_item.post_type)
            menu_item.object = object.name
            menu_item.type_label = object.labels.singular_name
            if "" == menu_item.post_title:
                #// translators: %d: ID of a post.
                menu_item.post_title = php_sprintf(__("#%d (no title)"), menu_item.ID)
            # end if
            menu_item.title = menu_item.post_title
            menu_item.url = get_permalink(menu_item.ID)
            menu_item.target = ""
            #// This filter is documented in wp-includes/nav-menu.php
            menu_item.attr_title = apply_filters("nav_menu_attr_title", "")
            #// This filter is documented in wp-includes/nav-menu.php
            menu_item.description = apply_filters("nav_menu_description", "")
            menu_item.classes = Array()
            menu_item.xfn = ""
        # end if
    elif (php_isset(lambda : menu_item.taxonomy)):
        menu_item.ID = menu_item.term_id
        menu_item.db_id = 0
        menu_item.menu_item_parent = 0
        menu_item.object_id = php_int(menu_item.term_id)
        menu_item.post_parent = php_int(menu_item.parent)
        menu_item.type = "taxonomy"
        object = get_taxonomy(menu_item.taxonomy)
        menu_item.object = object.name
        menu_item.type_label = object.labels.singular_name
        menu_item.title = menu_item.name
        menu_item.url = get_term_link(menu_item, menu_item.taxonomy)
        menu_item.target = ""
        menu_item.attr_title = ""
        menu_item.description = get_term_field("description", menu_item.term_id, menu_item.taxonomy)
        menu_item.classes = Array()
        menu_item.xfn = ""
    # end if
    #// 
    #// Filters a navigation menu item object.
    #// 
    #// @since 3.0.0
    #// 
    #// @param object $menu_item The menu item object.
    #//
    return apply_filters("wp_setup_nav_menu_item", menu_item)
# end def wp_setup_nav_menu_item
#// 
#// Get the menu items associated with a particular object.
#// 
#// @since 3.0.0
#// 
#// @param int    $object_id   The ID of the original object.
#// @param string $object_type The type of object, such as 'taxonomy' or 'post_type'.
#// @param string $taxonomy    If $object_type is 'taxonomy', $taxonomy is the name of the tax
#// that $object_id belongs to.
#// @return int[] The array of menu item IDs; empty array if none;
#//
def wp_get_associated_nav_menu_items(object_id=0, object_type="post_type", taxonomy="", *args_):
    
    object_id = php_int(object_id)
    menu_item_ids = Array()
    query = php_new_class("WP_Query", lambda : WP_Query())
    menu_items = query.query(Array({"meta_key": "_menu_item_object_id", "meta_value": object_id, "post_status": "any", "post_type": "nav_menu_item", "posts_per_page": -1}))
    for menu_item in menu_items:
        if (php_isset(lambda : menu_item.ID)) and is_nav_menu_item(menu_item.ID):
            menu_item_type = get_post_meta(menu_item.ID, "_menu_item_type", True)
            if "post_type" == object_type and "post_type" == menu_item_type:
                menu_item_ids[-1] = php_int(menu_item.ID)
            elif "taxonomy" == object_type and "taxonomy" == menu_item_type and get_post_meta(menu_item.ID, "_menu_item_object", True) == taxonomy:
                menu_item_ids[-1] = php_int(menu_item.ID)
            # end if
        # end if
    # end for
    return array_unique(menu_item_ids)
# end def wp_get_associated_nav_menu_items
#// 
#// Callback for handling a menu item when its original object is deleted.
#// 
#// @since 3.0.0
#// @access private
#// 
#// @param int $object_id The ID of the original object being trashed.
#//
def _wp_delete_post_menu_item(object_id=0, *args_):
    
    object_id = php_int(object_id)
    menu_item_ids = wp_get_associated_nav_menu_items(object_id, "post_type")
    for menu_item_id in menu_item_ids:
        wp_delete_post(menu_item_id, True)
    # end for
# end def _wp_delete_post_menu_item
#// 
#// Serves as a callback for handling a menu item when its original object is deleted.
#// 
#// @since 3.0.0
#// @access private
#// 
#// @param int    $object_id Optional. The ID of the original object being trashed. Default 0.
#// @param int    $tt_id     Term taxonomy ID. Unused.
#// @param string $taxonomy  Taxonomy slug.
#//
def _wp_delete_tax_menu_item(object_id=0, tt_id=None, taxonomy=None, *args_):
    
    object_id = php_int(object_id)
    menu_item_ids = wp_get_associated_nav_menu_items(object_id, "taxonomy", taxonomy)
    for menu_item_id in menu_item_ids:
        wp_delete_post(menu_item_id, True)
    # end for
# end def _wp_delete_tax_menu_item
#// 
#// Automatically add newly published page objects to menus with that as an option.
#// 
#// @since 3.0.0
#// @access private
#// 
#// @param string  $new_status The new status of the post object.
#// @param string  $old_status The old status of the post object.
#// @param WP_Post $post       The post object being transitioned from one status to another.
#//
def _wp_auto_add_pages_to_menu(new_status=None, old_status=None, post=None, *args_):
    
    if "publish" != new_status or "publish" == old_status or "page" != post.post_type:
        return
    # end if
    if (not php_empty(lambda : post.post_parent)):
        return
    # end if
    auto_add = get_option("nav_menu_options")
    if php_empty(lambda : auto_add) or (not php_is_array(auto_add)) or (not (php_isset(lambda : auto_add["auto_add"]))):
        return
    # end if
    auto_add = auto_add["auto_add"]
    if php_empty(lambda : auto_add) or (not php_is_array(auto_add)):
        return
    # end if
    args = Array({"menu-item-object-id": post.ID, "menu-item-object": post.post_type, "menu-item-type": "post_type", "menu-item-status": "publish"})
    for menu_id in auto_add:
        items = wp_get_nav_menu_items(menu_id, Array({"post_status": "publish,draft"}))
        if (not php_is_array(items)):
            continue
        # end if
        for item in items:
            if post.ID == item.object_id:
                continue
            # end if
        # end for
        wp_update_nav_menu_item(menu_id, 0, args)
    # end for
# end def _wp_auto_add_pages_to_menu
#// 
#// Delete auto-draft posts associated with the supplied changeset.
#// 
#// @since 4.8.0
#// @access private
#// 
#// @param int $post_id Post ID for the customize_changeset.
#//
def _wp_delete_customize_changeset_dependent_auto_drafts(post_id=None, *args_):
    
    post = get_post(post_id)
    if (not post) or "customize_changeset" != post.post_type:
        return
    # end if
    data = php_json_decode(post.post_content, True)
    if php_empty(lambda : data["nav_menus_created_posts"]["value"]):
        return
    # end if
    remove_action("delete_post", "_wp_delete_customize_changeset_dependent_auto_drafts")
    for stub_post_id in data["nav_menus_created_posts"]["value"]:
        if php_empty(lambda : stub_post_id):
            continue
        # end if
        if "auto-draft" == get_post_status(stub_post_id):
            wp_delete_post(stub_post_id, True)
        elif "draft" == get_post_status(stub_post_id):
            wp_trash_post(stub_post_id)
            delete_post_meta(stub_post_id, "_customize_changeset_uuid")
        # end if
    # end for
    add_action("delete_post", "_wp_delete_customize_changeset_dependent_auto_drafts")
# end def _wp_delete_customize_changeset_dependent_auto_drafts
#// 
#// Handle menu config after theme change.
#// 
#// @access private
#// @since 4.9.0
#//
def _wp_menus_changed(*args_):
    
    old_nav_menu_locations = get_option("theme_switch_menu_locations", Array())
    new_nav_menu_locations = get_nav_menu_locations()
    mapped_nav_menu_locations = wp_map_nav_menu_locations(new_nav_menu_locations, old_nav_menu_locations)
    set_theme_mod("nav_menu_locations", mapped_nav_menu_locations)
    delete_option("theme_switch_menu_locations")
# end def _wp_menus_changed
#// 
#// Maps nav menu locations according to assignments in previously active theme.
#// 
#// @since 4.9.0
#// 
#// @param array $new_nav_menu_locations New nav menu locations assignments.
#// @param array $old_nav_menu_locations Old nav menu locations assignments.
#// @return array Nav menus mapped to new nav menu locations.
#//
def wp_map_nav_menu_locations(new_nav_menu_locations=None, old_nav_menu_locations=None, *args_):
    
    registered_nav_menus = get_registered_nav_menus()
    new_nav_menu_locations = php_array_intersect_key(new_nav_menu_locations, registered_nav_menus)
    #// Short-circuit if there are no old nav menu location assignments to map.
    if php_empty(lambda : old_nav_menu_locations):
        return new_nav_menu_locations
    # end if
    #// If old and new theme have just one location, map it and we're done.
    if 1 == php_count(old_nav_menu_locations) and 1 == php_count(registered_nav_menus):
        new_nav_menu_locations[key(registered_nav_menus)] = php_array_pop(old_nav_menu_locations)
        return new_nav_menu_locations
    # end if
    old_locations = php_array_keys(old_nav_menu_locations)
    #// Map locations with the same slug.
    for location,name in registered_nav_menus:
        if php_in_array(location, old_locations, True):
            new_nav_menu_locations[location] = old_nav_menu_locations[location]
            old_nav_menu_locations[location] = None
        # end if
    # end for
    #// If there are no old nav menu locations left, then we're done.
    if php_empty(lambda : old_nav_menu_locations):
        return new_nav_menu_locations
    # end if
    #// 
    #// If old and new theme both have locations that contain phrases
    #// from within the same group, make an educated guess and map it.
    #//
    common_slug_groups = Array(Array("primary", "menu-1", "main", "header", "navigation", "top"), Array("secondary", "menu-2", "footer", "subsidiary", "bottom"), Array("social"))
    #// Go through each group...
    for slug_group in common_slug_groups:
        #// ...and see if any of these slugs...
        for slug in slug_group:
            #// ...and any of the new menu locations...
            for new_location,name in registered_nav_menus:
                #// ...actually match!
                if php_is_string(new_location) and False == php_stripos(new_location, slug) and False == php_stripos(slug, new_location):
                    continue
                elif php_is_numeric(new_location) and new_location != slug:
                    continue
                # end if
                #// Then see if any of the old locations...
                for location,menu_id in old_nav_menu_locations:
                    #// ...and any slug in the same group...
                    for slug in slug_group:
                        #// ... have a match as well.
                        if php_is_string(location) and False == php_stripos(location, slug) and False == php_stripos(slug, location):
                            continue
                        elif php_is_numeric(location) and location != slug:
                            continue
                        # end if
                        #// Make sure this location wasn't mapped and removed previously.
                        if (not php_empty(lambda : old_nav_menu_locations[location])):
                            #// We have a match that can be mapped!
                            new_nav_menu_locations[new_location] = old_nav_menu_locations[location]
                            old_nav_menu_locations[location] = None
                            continue
                        # end if
                    # end for
                    pass
                # end for
                pass
            # end for
            pass
        # end for
        pass
    # end for
    #// End foreach ( $common_slug_groups as $slug_group ).
    return new_nav_menu_locations
# end def wp_map_nav_menu_locations
