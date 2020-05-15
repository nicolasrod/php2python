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
#// Nav Menu API: Template functions
#// 
#// @package WordPress
#// @subpackage Nav_Menus
#// @since 3.0.0
#// 
#// Walker_Nav_Menu class
php_include_file(ABSPATH + WPINC + "/class-walker-nav-menu.php", once=True)
#// 
#// Displays a navigation menu.
#// 
#// @since 3.0.0
#// @since 4.7.0 Added the `item_spacing` argument.
#// 
#// @staticvar array $menu_id_slugs
#// 
#// @param array $args {
#// Optional. Array of nav menu arguments.
#// 
#// @type int|string|WP_Term $menu            Desired menu. Accepts a menu ID, slug, name, or object. Default empty.
#// @type string             $menu_class      CSS class to use for the ul element which forms the menu. Default 'menu'.
#// @type string             $menu_id         The ID that is applied to the ul element which forms the menu.
#// Default is the menu slug, incremented.
#// @type string             $container       Whether to wrap the ul, and what to wrap it with. Default 'div'.
#// @type string             $container_class Class that is applied to the container. Default 'menu-{menu slug}-container'.
#// @type string             $container_id    The ID that is applied to the container. Default empty.
#// @type callable|bool      $fallback_cb     If the menu doesn't exist, a callback function will fire.
#// Default is 'wp_page_menu'. Set to false for no fallback.
#// @type string             $before          Text before the link markup. Default empty.
#// @type string             $after           Text after the link markup. Default empty.
#// @type string             $link_before     Text before the link text. Default empty.
#// @type string             $link_after      Text after the link text. Default empty.
#// @type bool               $echo            Whether to echo the menu or return it. Default true.
#// @type int                $depth           How many levels of the hierarchy are to be included. 0 means all. Default 0.
#// @type object             $walker          Instance of a custom walker class. Default empty.
#// @type string             $theme_location  Theme location to be used. Must be registered with register_nav_menu()
#// in order to be selectable by the user.
#// @type string             $items_wrap      How the list items should be wrapped. Default is a ul with an id and class.
#// Uses printf() format with numbered placeholders.
#// @type string             $item_spacing    Whether to preserve whitespace within the menu's HTML. Accepts 'preserve' or 'discard'. Default 'preserve'.
#// }
#// @return void|string|false Void if 'echo' argument is true, menu output if 'echo' is false.
#// False if there are no items or no menu was found.
#//
def wp_nav_menu(args=Array(), *args_):
    
    menu_id_slugs = Array()
    defaults = Array({"menu": "", "container": "div", "container_class": "", "container_id": "", "menu_class": "menu", "menu_id": "", "echo": True, "fallback_cb": "wp_page_menu", "before": "", "after": "", "link_before": "", "link_after": "", "items_wrap": "<ul id=\"%1$s\" class=\"%2$s\">%3$s</ul>", "item_spacing": "preserve", "depth": 0, "walker": "", "theme_location": ""})
    args = wp_parse_args(args, defaults)
    if (not php_in_array(args["item_spacing"], Array("preserve", "discard"), True)):
        #// Invalid value, fall back to default.
        args["item_spacing"] = defaults["item_spacing"]
    # end if
    #// 
    #// Filters the arguments used to display a navigation menu.
    #// 
    #// @since 3.0.0
    #// 
    #// @see wp_nav_menu()
    #// 
    #// @param array $args Array of wp_nav_menu() arguments.
    #//
    args = apply_filters("wp_nav_menu_args", args)
    args = args
    #// 
    #// Filters whether to short-circuit the wp_nav_menu() output.
    #// 
    #// Returning a non-null value to the filter will short-circuit
    #// wp_nav_menu(), echoing that value if $args->echo is true,
    #// returning that value otherwise.
    #// 
    #// @since 3.9.0
    #// 
    #// @see wp_nav_menu()
    #// 
    #// @param string|null $output Nav menu output to short-circuit with. Default null.
    #// @param stdClass    $args   An object containing wp_nav_menu() arguments.
    #//
    nav_menu = apply_filters("pre_wp_nav_menu", None, args)
    if None != nav_menu:
        if args.echo:
            php_print(nav_menu)
            return
        # end if
        return nav_menu
    # end if
    #// Get the nav menu based on the requested menu.
    menu = wp_get_nav_menu_object(args.menu)
    #// Get the nav menu based on the theme_location.
    locations = get_nav_menu_locations()
    if (not menu) and args.theme_location and locations and (php_isset(lambda : locations[args.theme_location])):
        menu = wp_get_nav_menu_object(locations[args.theme_location])
    # end if
    #// Get the first menu that has items if we still can't find a menu.
    if (not menu) and (not args.theme_location):
        menus = wp_get_nav_menus()
        for menu_maybe in menus:
            menu_items = wp_get_nav_menu_items(menu_maybe.term_id, Array({"update_post_term_cache": False}))
            if menu_items:
                menu = menu_maybe
                break
            # end if
        # end for
    # end if
    if php_empty(lambda : args.menu):
        args.menu = menu
    # end if
    #// If the menu exists, get its items.
    if menu and (not is_wp_error(menu)) and (not (php_isset(lambda : menu_items))):
        menu_items = wp_get_nav_menu_items(menu.term_id, Array({"update_post_term_cache": False}))
    # end if
    #// 
    #// If no menu was found:
    #// - Fall back (if one was specified), or bail.
    #// 
    #// If no menu items were found:
    #// - Fall back, but only if no theme location was specified.
    #// - Otherwise, bail.
    #//
    if (not menu) or is_wp_error(menu) or (php_isset(lambda : menu_items)) and php_empty(lambda : menu_items) and (not args.theme_location) and (php_isset(lambda : args.fallback_cb)) and args.fallback_cb and php_is_callable(args.fallback_cb):
        return php_call_user_func(args.fallback_cb, args)
    # end if
    if (not menu) or is_wp_error(menu):
        return False
    # end if
    nav_menu = ""
    items = ""
    show_container = False
    if args.container:
        #// 
        #// Filters the list of HTML tags that are valid for use as menu containers.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $tags The acceptable HTML tags for use as menu containers.
        #// Default is array containing 'div' and 'nav'.
        #//
        allowed_tags = apply_filters("wp_nav_menu_container_allowedtags", Array("div", "nav"))
        if php_is_string(args.container) and php_in_array(args.container, allowed_tags):
            show_container = True
            class_ = " class=\"" + esc_attr(args.container_class) + "\"" if args.container_class else " class=\"menu-" + menu.slug + "-container\""
            id = " id=\"" + esc_attr(args.container_id) + "\"" if args.container_id else ""
            nav_menu += "<" + args.container + id + class_ + ">"
        # end if
    # end if
    #// Set up the $menu_item variables.
    _wp_menu_item_classes_by_context(menu_items)
    sorted_menu_items = Array()
    menu_items_with_children = Array()
    for menu_item in menu_items:
        sorted_menu_items[menu_item.menu_order] = menu_item
        if menu_item.menu_item_parent:
            menu_items_with_children[menu_item.menu_item_parent] = True
        # end if
    # end for
    #// Add the menu-item-has-children class where applicable.
    if menu_items_with_children:
        for menu_item in sorted_menu_items:
            if (php_isset(lambda : menu_items_with_children[menu_item.ID])):
                menu_item.classes[-1] = "menu-item-has-children"
            # end if
        # end for
    # end if
    menu_items = None
    menu_item = None
    #// 
    #// Filters the sorted list of menu item objects before generating the menu's HTML.
    #// 
    #// @since 3.1.0
    #// 
    #// @param array    $sorted_menu_items The menu items, sorted by each menu item's menu order.
    #// @param stdClass $args              An object containing wp_nav_menu() arguments.
    #//
    sorted_menu_items = apply_filters("wp_nav_menu_objects", sorted_menu_items, args)
    items += walk_nav_menu_tree(sorted_menu_items, args.depth, args)
    sorted_menu_items = None
    #// Attributes.
    if (not php_empty(lambda : args.menu_id)):
        wrap_id = args.menu_id
    else:
        wrap_id = "menu-" + menu.slug
        while True:
            
            if not (php_in_array(wrap_id, menu_id_slugs)):
                break
            # end if
            if php_preg_match("#-(\\d+)$#", wrap_id, matches):
                matches[1] += 1
                wrap_id = php_preg_replace("#-(\\d+)$#", "-" + matches[1], wrap_id)
            else:
                wrap_id = wrap_id + "-1"
            # end if
        # end while
    # end if
    menu_id_slugs[-1] = wrap_id
    wrap_class = args.menu_class if args.menu_class else ""
    #// 
    #// Filters the HTML list content for navigation menus.
    #// 
    #// @since 3.0.0
    #// 
    #// @see wp_nav_menu()
    #// 
    #// @param string   $items The HTML list content for the menu items.
    #// @param stdClass $args  An object containing wp_nav_menu() arguments.
    #//
    items = apply_filters("wp_nav_menu_items", items, args)
    #// 
    #// Filters the HTML list content for a specific navigation menu.
    #// 
    #// @since 3.0.0
    #// 
    #// @see wp_nav_menu()
    #// 
    #// @param string   $items The HTML list content for the menu items.
    #// @param stdClass $args  An object containing wp_nav_menu() arguments.
    #//
    items = apply_filters(str("wp_nav_menu_") + str(menu.slug) + str("_items"), items, args)
    #// Don't print any markup if there are no items at this point.
    if php_empty(lambda : items):
        return False
    # end if
    nav_menu += php_sprintf(args.items_wrap, esc_attr(wrap_id), esc_attr(wrap_class), items)
    items = None
    if show_container:
        nav_menu += "</" + args.container + ">"
    # end if
    #// 
    #// Filters the HTML content for navigation menus.
    #// 
    #// @since 3.0.0
    #// 
    #// @see wp_nav_menu()
    #// 
    #// @param string   $nav_menu The HTML content for the navigation menu.
    #// @param stdClass $args     An object containing wp_nav_menu() arguments.
    #//
    nav_menu = apply_filters("wp_nav_menu", nav_menu, args)
    if args.echo:
        php_print(nav_menu)
    else:
        return nav_menu
    # end if
# end def wp_nav_menu
#// 
#// Add the class property classes for the current context, if applicable.
#// 
#// @access private
#// @since 3.0.0
#// 
#// @global WP_Query   $wp_query   WordPress Query object.
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param array $menu_items The current menu item objects to which to add the class property information.
#//
def _wp_menu_item_classes_by_context(menu_items=None, *args_):
    
    global wp_query,wp_rewrite
    php_check_if_defined("wp_query","wp_rewrite")
    queried_object = wp_query.get_queried_object()
    queried_object_id = int(wp_query.queried_object_id)
    active_object = ""
    active_ancestor_item_ids = Array()
    active_parent_item_ids = Array()
    active_parent_object_ids = Array()
    possible_taxonomy_ancestors = Array()
    possible_object_parents = Array()
    home_page_id = int(get_option("page_for_posts"))
    if wp_query.is_singular and (not php_empty(lambda : queried_object.post_type)) and (not is_post_type_hierarchical(queried_object.post_type)):
        for taxonomy in get_object_taxonomies(queried_object.post_type):
            if is_taxonomy_hierarchical(taxonomy):
                term_hierarchy = _get_term_hierarchy(taxonomy)
                terms = wp_get_object_terms(queried_object_id, taxonomy, Array({"fields": "ids"}))
                if php_is_array(terms):
                    possible_object_parents = php_array_merge(possible_object_parents, terms)
                    term_to_ancestor = Array()
                    for anc,descs in term_hierarchy:
                        for desc in descs:
                            term_to_ancestor[desc] = anc
                        # end for
                    # end for
                    for desc in terms:
                        while True:
                            possible_taxonomy_ancestors[taxonomy][-1] = desc
                            if (php_isset(lambda : term_to_ancestor[desc])):
                                _desc = term_to_ancestor[desc]
                                term_to_ancestor[desc] = None
                                desc = _desc
                            else:
                                desc = 0
                            # end if
                            
                            if (not php_empty(lambda : desc)):
                                break
                            # end if
                        # end while
                    # end for
                # end if
            # end if
        # end for
    elif (not php_empty(lambda : queried_object.taxonomy)) and is_taxonomy_hierarchical(queried_object.taxonomy):
        term_hierarchy = _get_term_hierarchy(queried_object.taxonomy)
        term_to_ancestor = Array()
        for anc,descs in term_hierarchy:
            for desc in descs:
                term_to_ancestor[desc] = anc
            # end for
        # end for
        desc = queried_object.term_id
        while True:
            possible_taxonomy_ancestors[queried_object.taxonomy][-1] = desc
            if (php_isset(lambda : term_to_ancestor[desc])):
                _desc = term_to_ancestor[desc]
                term_to_ancestor[desc] = None
                desc = _desc
            else:
                desc = 0
            # end if
            
            if (not php_empty(lambda : desc)):
                break
            # end if
        # end while
    # end if
    possible_object_parents = php_array_filter(possible_object_parents)
    front_page_url = home_url()
    front_page_id = int(get_option("page_on_front"))
    privacy_policy_page_id = int(get_option("wp_page_for_privacy_policy"))
    for key,menu_item in menu_items:
        menu_items[key].current = False
        classes = menu_item.classes
        classes[-1] = "menu-item"
        classes[-1] = "menu-item-type-" + menu_item.type
        classes[-1] = "menu-item-object-" + menu_item.object
        #// This menu item is set as the 'Front Page'.
        if "post_type" == menu_item.type and front_page_id == int(menu_item.object_id):
            classes[-1] = "menu-item-home"
        # end if
        #// This menu item is set as the 'Privacy Policy Page'.
        if "post_type" == menu_item.type and privacy_policy_page_id == int(menu_item.object_id):
            classes[-1] = "menu-item-privacy-policy"
        # end if
        #// If the menu item corresponds to a taxonomy term for the currently queried non-hierarchical post object.
        if wp_query.is_singular and "taxonomy" == menu_item.type and php_in_array(menu_item.object_id, possible_object_parents):
            active_parent_object_ids[-1] = int(menu_item.object_id)
            active_parent_item_ids[-1] = int(menu_item.db_id)
            active_object = queried_object.post_type
            pass
        elif menu_item.object_id == queried_object_id and (not php_empty(lambda : home_page_id)) and "post_type" == menu_item.type and wp_query.is_home and home_page_id == menu_item.object_id or "post_type" == menu_item.type and wp_query.is_singular or "taxonomy" == menu_item.type and wp_query.is_category or wp_query.is_tag or wp_query.is_tax and queried_object.taxonomy == menu_item.object:
            classes[-1] = "current-menu-item"
            menu_items[key].current = True
            _anc_id = int(menu_item.db_id)
            while True:
                _anc_id = get_post_meta(_anc_id, "_menu_item_menu_item_parent", True)
                if not (_anc_id and (not php_in_array(_anc_id, active_ancestor_item_ids))):
                    break
                # end if
                active_ancestor_item_ids[-1] = _anc_id
            # end while
            if "post_type" == menu_item.type and "page" == menu_item.object:
                #// Back compat classes for pages to match wp_page_menu().
                classes[-1] = "page_item"
                classes[-1] = "page-item-" + menu_item.object_id
                classes[-1] = "current_page_item"
            # end if
            active_parent_item_ids[-1] = int(menu_item.menu_item_parent)
            active_parent_object_ids[-1] = int(menu_item.post_parent)
            active_object = menu_item.object
            pass
        elif "post_type_archive" == menu_item.type and is_post_type_archive(Array(menu_item.object)):
            classes[-1] = "current-menu-item"
            menu_items[key].current = True
            _anc_id = int(menu_item.db_id)
            while True:
                _anc_id = get_post_meta(_anc_id, "_menu_item_menu_item_parent", True)
                if not (_anc_id and (not php_in_array(_anc_id, active_ancestor_item_ids))):
                    break
                # end if
                active_ancestor_item_ids[-1] = _anc_id
            # end while
            active_parent_item_ids[-1] = int(menu_item.menu_item_parent)
            pass
        elif "custom" == menu_item.object and (php_isset(lambda : PHP_SERVER["HTTP_HOST"])):
            _root_relative_current = untrailingslashit(PHP_SERVER["REQUEST_URI"])
            #// If it's the customize page then it will strip the query var off the URL before entering the comparison block.
            if is_customize_preview():
                _root_relative_current = strtok(untrailingslashit(PHP_SERVER["REQUEST_URI"]), "?")
            # end if
            current_url = set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + _root_relative_current)
            raw_item_url = php_substr(menu_item.url, 0, php_strpos(menu_item.url, "#")) if php_strpos(menu_item.url, "#") else menu_item.url
            item_url = set_url_scheme(untrailingslashit(raw_item_url))
            _indexless_current = untrailingslashit(php_preg_replace("/" + preg_quote(wp_rewrite.index, "/") + "$/", "", current_url))
            matches = Array(current_url, urldecode(current_url), _indexless_current, urldecode(_indexless_current), _root_relative_current, urldecode(_root_relative_current))
            if raw_item_url and php_in_array(item_url, matches):
                classes[-1] = "current-menu-item"
                menu_items[key].current = True
                _anc_id = int(menu_item.db_id)
                while True:
                    _anc_id = get_post_meta(_anc_id, "_menu_item_menu_item_parent", True)
                    if not (_anc_id and (not php_in_array(_anc_id, active_ancestor_item_ids))):
                        break
                    # end if
                    active_ancestor_item_ids[-1] = _anc_id
                # end while
                if php_in_array(home_url(), Array(untrailingslashit(current_url), untrailingslashit(_indexless_current))):
                    #// Back compat for home link to match wp_page_menu().
                    classes[-1] = "current_page_item"
                # end if
                active_parent_item_ids[-1] = int(menu_item.menu_item_parent)
                active_parent_object_ids[-1] = int(menu_item.post_parent)
                active_object = menu_item.object
                pass
            elif item_url == front_page_url and is_front_page():
                classes[-1] = "current-menu-item"
            # end if
            if untrailingslashit(item_url) == home_url():
                classes[-1] = "menu-item-home"
            # end if
        # end if
        #// Back-compat with wp_page_menu(): add "current_page_parent" to static home page link for any non-page query.
        if (not php_empty(lambda : home_page_id)) and "post_type" == menu_item.type and php_empty(lambda : wp_query.is_page) and home_page_id == menu_item.object_id:
            classes[-1] = "current_page_parent"
        # end if
        menu_items[key].classes = array_unique(classes)
    # end for
    active_ancestor_item_ids = php_array_filter(array_unique(active_ancestor_item_ids))
    active_parent_item_ids = php_array_filter(array_unique(active_parent_item_ids))
    active_parent_object_ids = php_array_filter(array_unique(active_parent_object_ids))
    #// Set parent's class.
    for key,parent_item in menu_items:
        classes = parent_item.classes
        menu_items[key].current_item_ancestor = False
        menu_items[key].current_item_parent = False
        if (php_isset(lambda : parent_item.type)) and "post_type" == parent_item.type and (not php_empty(lambda : queried_object.post_type)) and is_post_type_hierarchical(queried_object.post_type) and php_in_array(parent_item.object_id, queried_object.ancestors) and parent_item.object != queried_object.ID or "taxonomy" == parent_item.type and (php_isset(lambda : possible_taxonomy_ancestors[parent_item.object])) and php_in_array(parent_item.object_id, possible_taxonomy_ancestors[parent_item.object]) and (not (php_isset(lambda : queried_object.term_id))) or parent_item.object_id != queried_object.term_id:
            classes[-1] = "current-" + queried_object.post_type + "-ancestor" if php_empty(lambda : queried_object.taxonomy) else "current-" + queried_object.taxonomy + "-ancestor"
        # end if
        if php_in_array(php_intval(parent_item.db_id), active_ancestor_item_ids):
            classes[-1] = "current-menu-ancestor"
            menu_items[key].current_item_ancestor = True
        # end if
        if php_in_array(parent_item.db_id, active_parent_item_ids):
            classes[-1] = "current-menu-parent"
            menu_items[key].current_item_parent = True
        # end if
        if php_in_array(parent_item.object_id, active_parent_object_ids):
            classes[-1] = "current-" + active_object + "-parent"
        # end if
        if "post_type" == parent_item.type and "page" == parent_item.object:
            #// Back compat classes for pages to match wp_page_menu().
            if php_in_array("current-menu-parent", classes):
                classes[-1] = "current_page_parent"
            # end if
            if php_in_array("current-menu-ancestor", classes):
                classes[-1] = "current_page_ancestor"
            # end if
        # end if
        menu_items[key].classes = array_unique(classes)
    # end for
# end def _wp_menu_item_classes_by_context
#// 
#// Retrieve the HTML list content for nav menu items.
#// 
#// @uses Walker_Nav_Menu to create HTML list content.
#// @since 3.0.0
#// 
#// @param array    $items The menu items, sorted by each menu item's menu order.
#// @param int      $depth Depth of the item in reference to parents.
#// @param stdClass $r     An object containing wp_nav_menu() arguments.
#// @return string The HTML list content for the menu items.
#//
def walk_nav_menu_tree(items=None, depth=None, r=None, *args_):
    
    walker = php_new_class("Walker_Nav_Menu", lambda : Walker_Nav_Menu()) if php_empty(lambda : r.walker) else r.walker
    return walker.walk(items, depth, r)
# end def walk_nav_menu_tree
#// 
#// Prevents a menu item ID from being used more than once.
#// 
#// @since 3.0.1
#// @access private
#// 
#// @staticvar array $used_ids
#// @param string $id
#// @param object $item
#// @return string
#//
def _nav_menu_item_id_use_once(id=None, item=None, *args_):
    
    _used_ids = Array()
    if php_in_array(item.ID, _used_ids):
        return ""
    # end if
    _used_ids[-1] = item.ID
    return id
# end def _nav_menu_item_id_use_once
