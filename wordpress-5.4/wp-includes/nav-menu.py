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
def wp_get_nav_menu_object(menu_=None, *_args_):
    
    
    menu_obj_ = False
    if php_is_object(menu_):
        menu_obj_ = menu_
    # end if
    if menu_ and (not menu_obj_):
        menu_obj_ = get_term(menu_, "nav_menu")
        if (not menu_obj_):
            menu_obj_ = get_term_by("slug", menu_, "nav_menu")
        # end if
        if (not menu_obj_):
            menu_obj_ = get_term_by("name", menu_, "nav_menu")
        # end if
    # end if
    if (not menu_obj_) or is_wp_error(menu_obj_):
        menu_obj_ = False
    # end if
    #// 
    #// Filters the nav_menu term retrieved for wp_get_nav_menu_object().
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Term|false      $menu_obj Term from nav_menu taxonomy, or false if nothing had been found.
    #// @param int|string|WP_Term $menu     The menu ID, slug, name, or object passed to wp_get_nav_menu_object().
    #//
    return apply_filters("wp_get_nav_menu_object", menu_obj_, menu_)
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
def is_nav_menu(menu_=None, *_args_):
    
    
    if (not menu_):
        return False
    # end if
    menu_obj_ = wp_get_nav_menu_object(menu_)
    if menu_obj_ and (not is_wp_error(menu_obj_)) and (not php_empty(lambda : menu_obj_.taxonomy)) and "nav_menu" == menu_obj_.taxonomy:
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
def register_nav_menus(locations_=None, *_args_):
    if locations_ is None:
        locations_ = Array()
    # end if
    
    global _wp_registered_nav_menus_
    php_check_if_defined("_wp_registered_nav_menus_")
    add_theme_support("menus")
    for key_,value_ in locations_:
        if php_is_int(key_):
            _doing_it_wrong(__FUNCTION__, __("Nav menu locations must be strings."), "5.3.0")
            break
        # end if
    # end for
    _wp_registered_nav_menus_ = php_array_merge(_wp_registered_nav_menus_, locations_)
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
def unregister_nav_menu(location_=None, *_args_):
    
    
    global _wp_registered_nav_menus_
    php_check_if_defined("_wp_registered_nav_menus_")
    if php_is_array(_wp_registered_nav_menus_) and (php_isset(lambda : _wp_registered_nav_menus_[location_])):
        _wp_registered_nav_menus_[location_] = None
        if php_empty(lambda : _wp_registered_nav_menus_):
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
def register_nav_menu(location_=None, description_=None, *_args_):
    
    
    register_nav_menus(Array({location_: description_}))
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
def get_registered_nav_menus(*_args_):
    
    
    global _wp_registered_nav_menus_
    php_check_if_defined("_wp_registered_nav_menus_")
    if (php_isset(lambda : _wp_registered_nav_menus_)):
        return _wp_registered_nav_menus_
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
def get_nav_menu_locations(*_args_):
    
    
    locations_ = get_theme_mod("nav_menu_locations")
    return locations_ if php_is_array(locations_) else Array()
# end def get_nav_menu_locations
#// 
#// Determines whether a registered nav menu location has a menu assigned to it.
#// 
#// @since 3.0.0
#// 
#// @param string $location Menu location identifier.
#// @return bool Whether location has a menu.
#//
def has_nav_menu(location_=None, *_args_):
    
    
    has_nav_menu_ = False
    registered_nav_menus_ = get_registered_nav_menus()
    if (php_isset(lambda : registered_nav_menus_[location_])):
        locations_ = get_nav_menu_locations()
        has_nav_menu_ = (not php_empty(lambda : locations_[location_]))
    # end if
    #// 
    #// Filters whether a nav menu is assigned to the specified location.
    #// 
    #// @since 4.3.0
    #// 
    #// @param bool   $has_nav_menu Whether there is a menu assigned to a location.
    #// @param string $location     Menu location.
    #//
    return apply_filters("has_nav_menu", has_nav_menu_, location_)
# end def has_nav_menu
#// 
#// Returns the name of a navigation menu.
#// 
#// @since 4.9.0
#// 
#// @param string $location Menu location identifier.
#// @return string Menu name.
#//
def wp_get_nav_menu_name(location_=None, *_args_):
    
    
    menu_name_ = ""
    locations_ = get_nav_menu_locations()
    if (php_isset(lambda : locations_[location_])):
        menu_ = wp_get_nav_menu_object(locations_[location_])
        if menu_ and menu_.name:
            menu_name_ = menu_.name
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
    return apply_filters("wp_get_nav_menu_name", menu_name_, location_)
# end def wp_get_nav_menu_name
#// 
#// Determines whether the given ID is a nav menu item.
#// 
#// @since 3.0.0
#// 
#// @param int $menu_item_id The ID of the potential nav menu item.
#// @return bool Whether the given ID is that of a nav menu item.
#//
def is_nav_menu_item(menu_item_id_=0, *_args_):
    
    
    return (not is_wp_error(menu_item_id_)) and "nav_menu_item" == get_post_type(menu_item_id_)
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
def wp_create_nav_menu(menu_name_=None, *_args_):
    
    
    #// expected_slashed ($menu_name)
    return wp_update_nav_menu_object(0, Array({"menu-name": menu_name_}))
# end def wp_create_nav_menu
#// 
#// Delete a Navigation Menu.
#// 
#// @since 3.0.0
#// 
#// @param int|string|WP_Term $menu Menu ID, slug, name, or object.
#// @return bool|WP_Error True on success, false or WP_Error object on failure.
#//
def wp_delete_nav_menu(menu_=None, *_args_):
    
    
    menu_ = wp_get_nav_menu_object(menu_)
    if (not menu_):
        return False
    # end if
    menu_objects_ = get_objects_in_term(menu_.term_id, "nav_menu")
    if (not php_empty(lambda : menu_objects_)):
        for item_ in menu_objects_:
            wp_delete_post(item_)
        # end for
    # end if
    result_ = wp_delete_term(menu_.term_id, "nav_menu")
    #// Remove this menu from any locations.
    locations_ = get_nav_menu_locations()
    for location_,menu_id_ in locations_:
        if menu_id_ == menu_.term_id:
            locations_[location_] = 0
        # end if
    # end for
    set_theme_mod("nav_menu_locations", locations_)
    if result_ and (not is_wp_error(result_)):
        #// 
        #// Fires after a navigation menu has been successfully deleted.
        #// 
        #// @since 3.0.0
        #// 
        #// @param int $term_id ID of the deleted menu.
        #//
        do_action("wp_delete_nav_menu", menu_.term_id)
    # end if
    return result_
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
def wp_update_nav_menu_object(menu_id_=0, menu_data_=None, *_args_):
    if menu_data_ is None:
        menu_data_ = Array()
    # end if
    
    #// expected_slashed ($menu_data)
    menu_id_ = php_int(menu_id_)
    _menu_ = wp_get_nav_menu_object(menu_id_)
    args_ = Array({"description": menu_data_["description"] if (php_isset(lambda : menu_data_["description"])) else "", "name": menu_data_["menu-name"] if (php_isset(lambda : menu_data_["menu-name"])) else "", "parent": php_int(menu_data_["parent"]) if (php_isset(lambda : menu_data_["parent"])) else 0, "slug": None})
    #// Double-check that we're not going to have one menu take the name of another.
    _possible_existing_ = get_term_by("name", menu_data_["menu-name"], "nav_menu")
    if _possible_existing_ and (not is_wp_error(_possible_existing_)) and (php_isset(lambda : _possible_existing_.term_id)) and _possible_existing_.term_id != menu_id_:
        return php_new_class("WP_Error", lambda : WP_Error("menu_exists", php_sprintf(__("The menu name %s conflicts with another menu name. Please try another."), "<strong>" + esc_html(menu_data_["menu-name"]) + "</strong>")))
    # end if
    #// Menu doesn't already exist, so create a new menu.
    if (not _menu_) or is_wp_error(_menu_):
        menu_exists_ = get_term_by("name", menu_data_["menu-name"], "nav_menu")
        if menu_exists_:
            return php_new_class("WP_Error", lambda : WP_Error("menu_exists", php_sprintf(__("The menu name %s conflicts with another menu name. Please try another."), "<strong>" + esc_html(menu_data_["menu-name"]) + "</strong>")))
        # end if
        _menu_ = wp_insert_term(menu_data_["menu-name"], "nav_menu", args_)
        if is_wp_error(_menu_):
            return _menu_
        # end if
        #// 
        #// Fires after a navigation menu is successfully created.
        #// 
        #// @since 3.0.0
        #// 
        #// @param int   $term_id   ID of the new menu.
        #// @param array $menu_data An array of menu data.
        #//
        do_action("wp_create_nav_menu", _menu_["term_id"], menu_data_)
        return php_int(_menu_["term_id"])
    # end if
    if (not _menu_) or (not (php_isset(lambda : _menu_.term_id))):
        return 0
    # end if
    menu_id_ = php_int(_menu_.term_id)
    update_response_ = wp_update_term(menu_id_, "nav_menu", args_)
    if is_wp_error(update_response_):
        return update_response_
    # end if
    menu_id_ = php_int(update_response_["term_id"])
    #// 
    #// Fires after a navigation menu has been successfully updated.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int   $menu_id   ID of the updated menu.
    #// @param array $menu_data An array of menu data.
    #//
    do_action("wp_update_nav_menu", menu_id_, menu_data_)
    return menu_id_
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
def wp_update_nav_menu_item(menu_id_=0, menu_item_db_id_=0, menu_item_data_=None, *_args_):
    if menu_item_data_ is None:
        menu_item_data_ = Array()
    # end if
    
    menu_id_ = php_int(menu_id_)
    menu_item_db_id_ = php_int(menu_item_db_id_)
    #// Make sure that we don't convert non-nav_menu_item objects into nav_menu_item objects.
    if (not php_empty(lambda : menu_item_db_id_)) and (not is_nav_menu_item(menu_item_db_id_)):
        return php_new_class("WP_Error", lambda : WP_Error("update_nav_menu_item_failed", __("The given object ID is not that of a menu item.")))
    # end if
    menu_ = wp_get_nav_menu_object(menu_id_)
    if (not menu_) and 0 != menu_id_:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_menu_id", __("Invalid menu ID.")))
    # end if
    if is_wp_error(menu_):
        return menu_
    # end if
    defaults_ = Array({"menu-item-db-id": menu_item_db_id_, "menu-item-object-id": 0, "menu-item-object": "", "menu-item-parent-id": 0, "menu-item-position": 0, "menu-item-type": "custom", "menu-item-title": "", "menu-item-url": "", "menu-item-description": "", "menu-item-attr-title": "", "menu-item-target": "", "menu-item-classes": "", "menu-item-xfn": "", "menu-item-status": ""})
    args_ = wp_parse_args(menu_item_data_, defaults_)
    if 0 == menu_id_:
        args_["menu-item-position"] = 1
    elif 0 == php_int(args_["menu-item-position"]):
        menu_items_ = Array() if 0 == menu_id_ else wp_get_nav_menu_items(menu_id_, Array({"post_status": "publish,draft"}))
        last_item_ = php_array_pop(menu_items_)
        args_["menu-item-position"] = 1 + last_item_.menu_order if last_item_ and (php_isset(lambda : last_item_.menu_order)) else php_count(menu_items_)
    # end if
    original_parent_ = get_post_field("post_parent", menu_item_db_id_) if 0 < menu_item_db_id_ else 0
    if "custom" == args_["menu-item-type"]:
        #// If custom menu item, trim the URL.
        args_["menu-item-url"] = php_trim(args_["menu-item-url"])
    else:
        #// 
        #// If non-custom menu item, then:
        #// - use the original object's URL.
        #// - blank default title to sync with the original object's title.
        #//
        args_["menu-item-url"] = ""
        original_title_ = ""
        if "taxonomy" == args_["menu-item-type"]:
            original_parent_ = get_term_field("parent", args_["menu-item-object-id"], args_["menu-item-object"], "raw")
            original_title_ = get_term_field("name", args_["menu-item-object-id"], args_["menu-item-object"], "raw")
        elif "post_type" == args_["menu-item-type"]:
            original_object_ = get_post(args_["menu-item-object-id"])
            original_parent_ = php_int(original_object_.post_parent)
            original_title_ = original_object_.post_title
        elif "post_type_archive" == args_["menu-item-type"]:
            original_object_ = get_post_type_object(args_["menu-item-object"])
            if original_object_:
                original_title_ = original_object_.labels.archives
            # end if
        # end if
        if args_["menu-item-title"] == original_title_:
            args_["menu-item-title"] = ""
        # end if
        #// Hack to get wp to create a post object when too many properties are empty.
        if "" == args_["menu-item-title"] and "" == args_["menu-item-description"]:
            args_["menu-item-description"] = " "
        # end if
    # end if
    #// Populate the menu item object.
    post_ = Array({"menu_order": args_["menu-item-position"], "ping_status": 0, "post_content": args_["menu-item-description"], "post_excerpt": args_["menu-item-attr-title"], "post_parent": original_parent_, "post_title": args_["menu-item-title"], "post_type": "nav_menu_item"})
    update_ = 0 != menu_item_db_id_
    #// New menu item. Default is draft status.
    if (not update_):
        post_["ID"] = 0
        post_["post_status"] = "publish" if "publish" == args_["menu-item-status"] else "draft"
        menu_item_db_id_ = wp_insert_post(post_)
        if (not menu_item_db_id_) or is_wp_error(menu_item_db_id_):
            return menu_item_db_id_
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
        do_action("wp_add_nav_menu_item", menu_id_, menu_item_db_id_, args_)
    # end if
    #// Associate the menu item with the menu term.
    #// Only set the menu term if it isn't set to avoid unnecessary wp_get_object_terms().
    if menu_id_ and (not update_) or (not is_object_in_term(menu_item_db_id_, "nav_menu", php_int(menu_.term_id))):
        wp_set_object_terms(menu_item_db_id_, Array(menu_.term_id), "nav_menu")
    # end if
    if "custom" == args_["menu-item-type"]:
        args_["menu-item-object-id"] = menu_item_db_id_
        args_["menu-item-object"] = "custom"
    # end if
    menu_item_db_id_ = php_int(menu_item_db_id_)
    update_post_meta(menu_item_db_id_, "_menu_item_type", sanitize_key(args_["menu-item-type"]))
    update_post_meta(menu_item_db_id_, "_menu_item_menu_item_parent", php_strval(php_int(args_["menu-item-parent-id"])))
    update_post_meta(menu_item_db_id_, "_menu_item_object_id", php_strval(php_int(args_["menu-item-object-id"])))
    update_post_meta(menu_item_db_id_, "_menu_item_object", sanitize_key(args_["menu-item-object"]))
    update_post_meta(menu_item_db_id_, "_menu_item_target", sanitize_key(args_["menu-item-target"]))
    args_["menu-item-classes"] = php_array_map("sanitize_html_class", php_explode(" ", args_["menu-item-classes"]))
    args_["menu-item-xfn"] = php_implode(" ", php_array_map("sanitize_html_class", php_explode(" ", args_["menu-item-xfn"])))
    update_post_meta(menu_item_db_id_, "_menu_item_classes", args_["menu-item-classes"])
    update_post_meta(menu_item_db_id_, "_menu_item_xfn", args_["menu-item-xfn"])
    update_post_meta(menu_item_db_id_, "_menu_item_url", esc_url_raw(args_["menu-item-url"]))
    if 0 == menu_id_:
        update_post_meta(menu_item_db_id_, "_menu_item_orphaned", php_str(time()))
    elif get_post_meta(menu_item_db_id_, "_menu_item_orphaned"):
        delete_post_meta(menu_item_db_id_, "_menu_item_orphaned")
    # end if
    #// Update existing menu item. Default is publish status.
    if update_:
        post_["ID"] = menu_item_db_id_
        post_["post_status"] = "draft" if "draft" == args_["menu-item-status"] else "publish"
        wp_update_post(post_)
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
    do_action("wp_update_nav_menu_item", menu_id_, menu_item_db_id_, args_)
    return menu_item_db_id_
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
def wp_get_nav_menus(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"taxonomy": "nav_menu", "hide_empty": False, "orderby": "name"})
    args_ = wp_parse_args(args_, defaults_)
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
    return apply_filters("wp_get_nav_menus", get_terms(args_), args_)
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
def _is_valid_nav_menu_item(item_=None, *_args_):
    
    
    return php_empty(lambda : item_._invalid)
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
def wp_get_nav_menu_items(menu_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    menu_ = wp_get_nav_menu_object(menu_)
    if (not menu_):
        return False
    # end if
    fetched_ = Array()
    items_ = get_objects_in_term(menu_.term_id, "nav_menu")
    if is_wp_error(items_):
        return False
    # end if
    defaults_ = Array({"order": "ASC", "orderby": "menu_order", "post_type": "nav_menu_item", "post_status": "publish", "output": ARRAY_A, "output_key": "menu_order", "nopaging": True})
    args_ = wp_parse_args(args_, defaults_)
    args_["include"] = items_
    if (not php_empty(lambda : items_)):
        items_ = get_posts(args_)
    else:
        items_ = Array()
    # end if
    #// Get all posts and terms at once to prime the caches.
    if php_empty(lambda : fetched_[menu_.term_id]) and (not wp_using_ext_object_cache()):
        fetched_[menu_.term_id] = True
        posts_ = Array()
        terms_ = Array()
        for item_ in items_:
            object_id_ = get_post_meta(item_.ID, "_menu_item_object_id", True)
            object_ = get_post_meta(item_.ID, "_menu_item_object", True)
            type_ = get_post_meta(item_.ID, "_menu_item_type", True)
            if "post_type" == type_:
                posts_[object_][-1] = object_id_
            elif "taxonomy" == type_:
                terms_[object_][-1] = object_id_
            # end if
        # end for
        if (not php_empty(lambda : posts_)):
            for post_type_ in php_array_keys(posts_):
                get_posts(Array({"post__in": posts_[post_type_], "post_type": post_type_, "nopaging": True, "update_post_term_cache": False}))
            # end for
        # end if
        posts_ = None
        if (not php_empty(lambda : terms_)):
            for taxonomy_ in php_array_keys(terms_):
                get_terms(Array({"taxonomy": taxonomy_, "include": terms_[taxonomy_], "hierarchical": False}))
            # end for
        # end if
        terms_ = None
    # end if
    items_ = php_array_map("wp_setup_nav_menu_item", items_)
    if (not is_admin()):
        #// Remove invalid items only on front end.
        items_ = php_array_filter(items_, "_is_valid_nav_menu_item")
    # end if
    if ARRAY_A == args_["output"]:
        items_ = wp_list_sort(items_, Array({args_["output_key"]: "ASC"}))
        i_ = 1
        for k_,item_ in items_:
            items_[k_].args_["output_key"] = i_
            i_ += 1
            i_ += 1
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
    return apply_filters("wp_get_nav_menu_items", items_, menu_, args_)
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
def wp_setup_nav_menu_item(menu_item_=None, *_args_):
    
    
    if (php_isset(lambda : menu_item_.post_type)):
        if "nav_menu_item" == menu_item_.post_type:
            menu_item_.db_id = php_int(menu_item_.ID)
            menu_item_.menu_item_parent = get_post_meta(menu_item_.ID, "_menu_item_menu_item_parent", True) if (not (php_isset(lambda : menu_item_.menu_item_parent))) else menu_item_.menu_item_parent
            menu_item_.object_id = get_post_meta(menu_item_.ID, "_menu_item_object_id", True) if (not (php_isset(lambda : menu_item_.object_id))) else menu_item_.object_id
            menu_item_.object = get_post_meta(menu_item_.ID, "_menu_item_object", True) if (not (php_isset(lambda : menu_item_.object))) else menu_item_.object
            menu_item_.type = get_post_meta(menu_item_.ID, "_menu_item_type", True) if (not (php_isset(lambda : menu_item_.type))) else menu_item_.type
            if "post_type" == menu_item_.type:
                object_ = get_post_type_object(menu_item_.object)
                if object_:
                    menu_item_.type_label = object_.labels.singular_name
                    #// Use post states for special pages (only in the admin).
                    if php_function_exists("get_post_states"):
                        menu_post_ = get_post(menu_item_.object_id)
                        post_states_ = get_post_states(menu_post_)
                        if post_states_:
                            menu_item_.type_label = wp_strip_all_tags(php_implode(", ", post_states_))
                        # end if
                    # end if
                else:
                    menu_item_.type_label = menu_item_.object
                    menu_item_._invalid = True
                # end if
                if "trash" == get_post_status(menu_item_.object_id):
                    menu_item_._invalid = True
                # end if
                original_object_ = get_post(menu_item_.object_id)
                if original_object_:
                    menu_item_.url = get_permalink(original_object_.ID)
                    #// This filter is documented in wp-includes/post-template.php
                    original_title_ = apply_filters("the_title", original_object_.post_title, original_object_.ID)
                else:
                    menu_item_.url = ""
                    original_title_ = ""
                    menu_item_._invalid = True
                # end if
                if "" == original_title_:
                    #// translators: %d: ID of a post.
                    original_title_ = php_sprintf(__("#%d (no title)"), menu_item_.object_id)
                # end if
                menu_item_.title = original_title_ if "" == menu_item_.post_title else menu_item_.post_title
            elif "post_type_archive" == menu_item_.type:
                object_ = get_post_type_object(menu_item_.object)
                if object_:
                    menu_item_.title = object_.labels.archives if "" == menu_item_.post_title else menu_item_.post_title
                    post_type_description_ = object_.description
                else:
                    post_type_description_ = ""
                    menu_item_._invalid = True
                # end if
                menu_item_.type_label = __("Post Type Archive")
                post_content_ = wp_trim_words(menu_item_.post_content, 200)
                post_type_description_ = post_type_description_ if "" == post_content_ else post_content_
                menu_item_.url = get_post_type_archive_link(menu_item_.object)
            elif "taxonomy" == menu_item_.type:
                object_ = get_taxonomy(menu_item_.object)
                if object_:
                    menu_item_.type_label = object_.labels.singular_name
                else:
                    menu_item_.type_label = menu_item_.object
                    menu_item_._invalid = True
                # end if
                original_object_ = get_term(php_int(menu_item_.object_id), menu_item_.object)
                if original_object_ and (not is_wp_error(original_object_)):
                    menu_item_.url = get_term_link(php_int(menu_item_.object_id), menu_item_.object)
                    original_title_ = original_object_.name
                else:
                    menu_item_.url = ""
                    original_title_ = ""
                    menu_item_._invalid = True
                # end if
                if "" == original_title_:
                    #// translators: %d: ID of a term.
                    original_title_ = php_sprintf(__("#%d (no title)"), menu_item_.object_id)
                # end if
                menu_item_.title = original_title_ if "" == menu_item_.post_title else menu_item_.post_title
            else:
                menu_item_.type_label = __("Custom Link")
                menu_item_.title = menu_item_.post_title
                menu_item_.url = get_post_meta(menu_item_.ID, "_menu_item_url", True) if (not (php_isset(lambda : menu_item_.url))) else menu_item_.url
            # end if
            menu_item_.target = get_post_meta(menu_item_.ID, "_menu_item_target", True) if (not (php_isset(lambda : menu_item_.target))) else menu_item_.target
            #// 
            #// Filters a navigation menu item's title attribute.
            #// 
            #// @since 3.0.0
            #// 
            #// @param string $item_title The menu item title attribute.
            #//
            menu_item_.attr_title = apply_filters("nav_menu_attr_title", menu_item_.post_excerpt) if (not (php_isset(lambda : menu_item_.attr_title))) else menu_item_.attr_title
            if (not (php_isset(lambda : menu_item_.description))):
                #// 
                #// Filters a navigation menu item's description.
                #// 
                #// @since 3.0.0
                #// 
                #// @param string $description The menu item description.
                #//
                menu_item_.description = apply_filters("nav_menu_description", wp_trim_words(menu_item_.post_content, 200))
            # end if
            menu_item_.classes = get_post_meta(menu_item_.ID, "_menu_item_classes", True) if (not (php_isset(lambda : menu_item_.classes))) else menu_item_.classes
            menu_item_.xfn = get_post_meta(menu_item_.ID, "_menu_item_xfn", True) if (not (php_isset(lambda : menu_item_.xfn))) else menu_item_.xfn
        else:
            menu_item_.db_id = 0
            menu_item_.menu_item_parent = 0
            menu_item_.object_id = php_int(menu_item_.ID)
            menu_item_.type = "post_type"
            object_ = get_post_type_object(menu_item_.post_type)
            menu_item_.object = object_.name
            menu_item_.type_label = object_.labels.singular_name
            if "" == menu_item_.post_title:
                #// translators: %d: ID of a post.
                menu_item_.post_title = php_sprintf(__("#%d (no title)"), menu_item_.ID)
            # end if
            menu_item_.title = menu_item_.post_title
            menu_item_.url = get_permalink(menu_item_.ID)
            menu_item_.target = ""
            #// This filter is documented in wp-includes/nav-menu.php
            menu_item_.attr_title = apply_filters("nav_menu_attr_title", "")
            #// This filter is documented in wp-includes/nav-menu.php
            menu_item_.description = apply_filters("nav_menu_description", "")
            menu_item_.classes = Array()
            menu_item_.xfn = ""
        # end if
    elif (php_isset(lambda : menu_item_.taxonomy)):
        menu_item_.ID = menu_item_.term_id
        menu_item_.db_id = 0
        menu_item_.menu_item_parent = 0
        menu_item_.object_id = php_int(menu_item_.term_id)
        menu_item_.post_parent = php_int(menu_item_.parent)
        menu_item_.type = "taxonomy"
        object_ = get_taxonomy(menu_item_.taxonomy)
        menu_item_.object = object_.name
        menu_item_.type_label = object_.labels.singular_name
        menu_item_.title = menu_item_.name
        menu_item_.url = get_term_link(menu_item_, menu_item_.taxonomy)
        menu_item_.target = ""
        menu_item_.attr_title = ""
        menu_item_.description = get_term_field("description", menu_item_.term_id, menu_item_.taxonomy)
        menu_item_.classes = Array()
        menu_item_.xfn = ""
    # end if
    #// 
    #// Filters a navigation menu item object.
    #// 
    #// @since 3.0.0
    #// 
    #// @param object $menu_item The menu item object.
    #//
    return apply_filters("wp_setup_nav_menu_item", menu_item_)
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
def wp_get_associated_nav_menu_items(object_id_=0, object_type_="post_type", taxonomy_="", *_args_):
    
    
    object_id_ = php_int(object_id_)
    menu_item_ids_ = Array()
    query_ = php_new_class("WP_Query", lambda : WP_Query())
    menu_items_ = query_.query(Array({"meta_key": "_menu_item_object_id", "meta_value": object_id_, "post_status": "any", "post_type": "nav_menu_item", "posts_per_page": -1}))
    for menu_item_ in menu_items_:
        if (php_isset(lambda : menu_item_.ID)) and is_nav_menu_item(menu_item_.ID):
            menu_item_type_ = get_post_meta(menu_item_.ID, "_menu_item_type", True)
            if "post_type" == object_type_ and "post_type" == menu_item_type_:
                menu_item_ids_[-1] = php_int(menu_item_.ID)
            elif "taxonomy" == object_type_ and "taxonomy" == menu_item_type_ and get_post_meta(menu_item_.ID, "_menu_item_object", True) == taxonomy_:
                menu_item_ids_[-1] = php_int(menu_item_.ID)
            # end if
        # end if
    # end for
    return array_unique(menu_item_ids_)
# end def wp_get_associated_nav_menu_items
#// 
#// Callback for handling a menu item when its original object is deleted.
#// 
#// @since 3.0.0
#// @access private
#// 
#// @param int $object_id The ID of the original object being trashed.
#//
def _wp_delete_post_menu_item(object_id_=0, *_args_):
    
    
    object_id_ = php_int(object_id_)
    menu_item_ids_ = wp_get_associated_nav_menu_items(object_id_, "post_type")
    for menu_item_id_ in menu_item_ids_:
        wp_delete_post(menu_item_id_, True)
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
def _wp_delete_tax_menu_item(object_id_=0, tt_id_=None, taxonomy_=None, *_args_):
    
    
    object_id_ = php_int(object_id_)
    menu_item_ids_ = wp_get_associated_nav_menu_items(object_id_, "taxonomy", taxonomy_)
    for menu_item_id_ in menu_item_ids_:
        wp_delete_post(menu_item_id_, True)
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
def _wp_auto_add_pages_to_menu(new_status_=None, old_status_=None, post_=None, *_args_):
    
    
    if "publish" != new_status_ or "publish" == old_status_ or "page" != post_.post_type:
        return
    # end if
    if (not php_empty(lambda : post_.post_parent)):
        return
    # end if
    auto_add_ = get_option("nav_menu_options")
    if php_empty(lambda : auto_add_) or (not php_is_array(auto_add_)) or (not (php_isset(lambda : auto_add_["auto_add"]))):
        return
    # end if
    auto_add_ = auto_add_["auto_add"]
    if php_empty(lambda : auto_add_) or (not php_is_array(auto_add_)):
        return
    # end if
    args_ = Array({"menu-item-object-id": post_.ID, "menu-item-object": post_.post_type, "menu-item-type": "post_type", "menu-item-status": "publish"})
    for menu_id_ in auto_add_:
        items_ = wp_get_nav_menu_items(menu_id_, Array({"post_status": "publish,draft"}))
        if (not php_is_array(items_)):
            continue
        # end if
        for item_ in items_:
            if post_.ID == item_.object_id:
                continue
            # end if
        # end for
        wp_update_nav_menu_item(menu_id_, 0, args_)
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
def _wp_delete_customize_changeset_dependent_auto_drafts(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_) or "customize_changeset" != post_.post_type:
        return
    # end if
    data_ = php_json_decode(post_.post_content, True)
    if php_empty(lambda : data_["nav_menus_created_posts"]["value"]):
        return
    # end if
    remove_action("delete_post", "_wp_delete_customize_changeset_dependent_auto_drafts")
    for stub_post_id_ in data_["nav_menus_created_posts"]["value"]:
        if php_empty(lambda : stub_post_id_):
            continue
        # end if
        if "auto-draft" == get_post_status(stub_post_id_):
            wp_delete_post(stub_post_id_, True)
        elif "draft" == get_post_status(stub_post_id_):
            wp_trash_post(stub_post_id_)
            delete_post_meta(stub_post_id_, "_customize_changeset_uuid")
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
def _wp_menus_changed(*_args_):
    
    
    old_nav_menu_locations_ = get_option("theme_switch_menu_locations", Array())
    new_nav_menu_locations_ = get_nav_menu_locations()
    mapped_nav_menu_locations_ = wp_map_nav_menu_locations(new_nav_menu_locations_, old_nav_menu_locations_)
    set_theme_mod("nav_menu_locations", mapped_nav_menu_locations_)
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
def wp_map_nav_menu_locations(new_nav_menu_locations_=None, old_nav_menu_locations_=None, *_args_):
    
    
    registered_nav_menus_ = get_registered_nav_menus()
    new_nav_menu_locations_ = php_array_intersect_key(new_nav_menu_locations_, registered_nav_menus_)
    #// Short-circuit if there are no old nav menu location assignments to map.
    if php_empty(lambda : old_nav_menu_locations_):
        return new_nav_menu_locations_
    # end if
    #// If old and new theme have just one location, map it and we're done.
    if 1 == php_count(old_nav_menu_locations_) and 1 == php_count(registered_nav_menus_):
        new_nav_menu_locations_[key(registered_nav_menus_)] = php_array_pop(old_nav_menu_locations_)
        return new_nav_menu_locations_
    # end if
    old_locations_ = php_array_keys(old_nav_menu_locations_)
    #// Map locations with the same slug.
    for location_,name_ in registered_nav_menus_:
        if php_in_array(location_, old_locations_, True):
            new_nav_menu_locations_[location_] = old_nav_menu_locations_[location_]
            old_nav_menu_locations_[location_] = None
        # end if
    # end for
    #// If there are no old nav menu locations left, then we're done.
    if php_empty(lambda : old_nav_menu_locations_):
        return new_nav_menu_locations_
    # end if
    #// 
    #// If old and new theme both have locations that contain phrases
    #// from within the same group, make an educated guess and map it.
    #//
    common_slug_groups_ = Array(Array("primary", "menu-1", "main", "header", "navigation", "top"), Array("secondary", "menu-2", "footer", "subsidiary", "bottom"), Array("social"))
    #// Go through each group...
    for slug_group_ in common_slug_groups_:
        #// ...and see if any of these slugs...
        for slug_ in slug_group_:
            #// ...and any of the new menu locations...
            for new_location_,name_ in registered_nav_menus_:
                #// ...actually match!
                if php_is_string(new_location_) and False == php_stripos(new_location_, slug_) and False == php_stripos(slug_, new_location_):
                    continue
                elif php_is_numeric(new_location_) and new_location_ != slug_:
                    continue
                # end if
                #// Then see if any of the old locations...
                for location_,menu_id_ in old_nav_menu_locations_:
                    #// ...and any slug in the same group...
                    for slug_ in slug_group_:
                        #// ... have a match as well.
                        if php_is_string(location_) and False == php_stripos(location_, slug_) and False == php_stripos(slug_, location_):
                            continue
                        elif php_is_numeric(location_) and location_ != slug_:
                            continue
                        # end if
                        #// Make sure this location wasn't mapped and removed previously.
                        if (not php_empty(lambda : old_nav_menu_locations_[location_])):
                            #// We have a match that can be mapped!
                            new_nav_menu_locations_[new_location_] = old_nav_menu_locations_[location_]
                            old_nav_menu_locations_[location_] = None
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
    return new_nav_menu_locations_
# end def wp_map_nav_menu_locations
