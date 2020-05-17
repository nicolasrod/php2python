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
def wp_nav_menu(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    menu_id_slugs_ = Array()
    defaults_ = Array({"menu": "", "container": "div", "container_class": "", "container_id": "", "menu_class": "menu", "menu_id": "", "echo": True, "fallback_cb": "wp_page_menu", "before": "", "after": "", "link_before": "", "link_after": "", "items_wrap": "<ul id=\"%1$s\" class=\"%2$s\">%3$s</ul>", "item_spacing": "preserve", "depth": 0, "walker": "", "theme_location": ""})
    args_ = wp_parse_args(args_, defaults_)
    if (not php_in_array(args_["item_spacing"], Array("preserve", "discard"), True)):
        #// Invalid value, fall back to default.
        args_["item_spacing"] = defaults_["item_spacing"]
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
    args_ = apply_filters("wp_nav_menu_args", args_)
    args_ = args_
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
    nav_menu_ = apply_filters("pre_wp_nav_menu", None, args_)
    if None != nav_menu_:
        if args_.echo:
            php_print(nav_menu_)
            return
        # end if
        return nav_menu_
    # end if
    #// Get the nav menu based on the requested menu.
    menu_ = wp_get_nav_menu_object(args_.menu)
    #// Get the nav menu based on the theme_location.
    locations_ = get_nav_menu_locations()
    if (not menu_) and args_.theme_location and locations_ and (php_isset(lambda : locations_[args_.theme_location])):
        menu_ = wp_get_nav_menu_object(locations_[args_.theme_location])
    # end if
    #// Get the first menu that has items if we still can't find a menu.
    if (not menu_) and (not args_.theme_location):
        menus_ = wp_get_nav_menus()
        for menu_maybe_ in menus_:
            menu_items_ = wp_get_nav_menu_items(menu_maybe_.term_id, Array({"update_post_term_cache": False}))
            if menu_items_:
                menu_ = menu_maybe_
                break
            # end if
        # end for
    # end if
    if php_empty(lambda : args_.menu):
        args_.menu = menu_
    # end if
    #// If the menu exists, get its items.
    if menu_ and (not is_wp_error(menu_)) and (not (php_isset(lambda : menu_items_))):
        menu_items_ = wp_get_nav_menu_items(menu_.term_id, Array({"update_post_term_cache": False}))
    # end if
    #// 
    #// If no menu was found:
    #// - Fall back (if one was specified), or bail.
    #// 
    #// If no menu items were found:
    #// - Fall back, but only if no theme location was specified.
    #// - Otherwise, bail.
    #//
    if (not menu_) or is_wp_error(menu_) or (php_isset(lambda : menu_items_)) and php_empty(lambda : menu_items_) and (not args_.theme_location) and (php_isset(lambda : args_.fallback_cb)) and args_.fallback_cb and php_is_callable(args_.fallback_cb):
        return php_call_user_func(args_.fallback_cb, args_)
    # end if
    if (not menu_) or is_wp_error(menu_):
        return False
    # end if
    nav_menu_ = ""
    items_ = ""
    show_container_ = False
    if args_.container:
        #// 
        #// Filters the list of HTML tags that are valid for use as menu containers.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $tags The acceptable HTML tags for use as menu containers.
        #// Default is array containing 'div' and 'nav'.
        #//
        allowed_tags_ = apply_filters("wp_nav_menu_container_allowedtags", Array("div", "nav"))
        if php_is_string(args_.container) and php_in_array(args_.container, allowed_tags_):
            show_container_ = True
            class_ = " class=\"" + esc_attr(args_.container_class) + "\"" if args_.container_class else " class=\"menu-" + menu_.slug + "-container\""
            id_ = " id=\"" + esc_attr(args_.container_id) + "\"" if args_.container_id else ""
            nav_menu_ += "<" + args_.container + id_ + class_ + ">"
        # end if
    # end if
    #// Set up the $menu_item variables.
    _wp_menu_item_classes_by_context(menu_items_)
    sorted_menu_items_ = Array()
    menu_items_with_children_ = Array()
    for menu_item_ in menu_items_:
        sorted_menu_items_[menu_item_.menu_order] = menu_item_
        if menu_item_.menu_item_parent:
            menu_items_with_children_[menu_item_.menu_item_parent] = True
        # end if
    # end for
    #// Add the menu-item-has-children class where applicable.
    if menu_items_with_children_:
        for menu_item_ in sorted_menu_items_:
            if (php_isset(lambda : menu_items_with_children_[menu_item_.ID])):
                menu_item_.classes[-1] = "menu-item-has-children"
            # end if
        # end for
    # end if
    menu_items_ = None
    menu_item_ = None
    #// 
    #// Filters the sorted list of menu item objects before generating the menu's HTML.
    #// 
    #// @since 3.1.0
    #// 
    #// @param array    $sorted_menu_items The menu items, sorted by each menu item's menu order.
    #// @param stdClass $args              An object containing wp_nav_menu() arguments.
    #//
    sorted_menu_items_ = apply_filters("wp_nav_menu_objects", sorted_menu_items_, args_)
    items_ += walk_nav_menu_tree(sorted_menu_items_, args_.depth, args_)
    sorted_menu_items_ = None
    #// Attributes.
    if (not php_empty(lambda : args_.menu_id)):
        wrap_id_ = args_.menu_id
    else:
        wrap_id_ = "menu-" + menu_.slug
        while True:
            
            if not (php_in_array(wrap_id_, menu_id_slugs_)):
                break
            # end if
            if php_preg_match("#-(\\d+)$#", wrap_id_, matches_):
                matches_[1] += 1
                matches_[1] += 1
                wrap_id_ = php_preg_replace("#-(\\d+)$#", "-" + matches_[1], wrap_id_)
            else:
                wrap_id_ = wrap_id_ + "-1"
            # end if
        # end while
    # end if
    menu_id_slugs_[-1] = wrap_id_
    wrap_class_ = args_.menu_class if args_.menu_class else ""
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
    items_ = apply_filters("wp_nav_menu_items", items_, args_)
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
    items_ = apply_filters(str("wp_nav_menu_") + str(menu_.slug) + str("_items"), items_, args_)
    #// Don't print any markup if there are no items at this point.
    if php_empty(lambda : items_):
        return False
    # end if
    nav_menu_ += php_sprintf(args_.items_wrap, esc_attr(wrap_id_), esc_attr(wrap_class_), items_)
    items_ = None
    if show_container_:
        nav_menu_ += "</" + args_.container + ">"
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
    nav_menu_ = apply_filters("wp_nav_menu", nav_menu_, args_)
    if args_.echo:
        php_print(nav_menu_)
    else:
        return nav_menu_
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
def _wp_menu_item_classes_by_context(menu_items_=None, *_args_):
    
    
    global wp_query_
    global wp_rewrite_
    php_check_if_defined("wp_query_","wp_rewrite_")
    queried_object_ = wp_query_.get_queried_object()
    queried_object_id_ = php_int(wp_query_.queried_object_id)
    active_object_ = ""
    active_ancestor_item_ids_ = Array()
    active_parent_item_ids_ = Array()
    active_parent_object_ids_ = Array()
    possible_taxonomy_ancestors_ = Array()
    possible_object_parents_ = Array()
    home_page_id_ = php_int(get_option("page_for_posts"))
    if wp_query_.is_singular and (not php_empty(lambda : queried_object_.post_type)) and (not is_post_type_hierarchical(queried_object_.post_type)):
        for taxonomy_ in get_object_taxonomies(queried_object_.post_type):
            if is_taxonomy_hierarchical(taxonomy_):
                term_hierarchy_ = _get_term_hierarchy(taxonomy_)
                terms_ = wp_get_object_terms(queried_object_id_, taxonomy_, Array({"fields": "ids"}))
                if php_is_array(terms_):
                    possible_object_parents_ = php_array_merge(possible_object_parents_, terms_)
                    term_to_ancestor_ = Array()
                    for anc_,descs_ in term_hierarchy_:
                        for desc_ in descs_:
                            term_to_ancestor_[desc_] = anc_
                        # end for
                    # end for
                    for desc_ in terms_:
                        while True:
                            possible_taxonomy_ancestors_[taxonomy_][-1] = desc_
                            if (php_isset(lambda : term_to_ancestor_[desc_])):
                                _desc_ = term_to_ancestor_[desc_]
                                term_to_ancestor_[desc_] = None
                                desc_ = _desc_
                            else:
                                desc_ = 0
                            # end if
                            
                            if (not php_empty(lambda : desc_)):
                                break
                            # end if
                        # end while
                    # end for
                # end if
            # end if
        # end for
    elif (not php_empty(lambda : queried_object_.taxonomy)) and is_taxonomy_hierarchical(queried_object_.taxonomy):
        term_hierarchy_ = _get_term_hierarchy(queried_object_.taxonomy)
        term_to_ancestor_ = Array()
        for anc_,descs_ in term_hierarchy_:
            for desc_ in descs_:
                term_to_ancestor_[desc_] = anc_
            # end for
        # end for
        desc_ = queried_object_.term_id
        while True:
            possible_taxonomy_ancestors_[queried_object_.taxonomy][-1] = desc_
            if (php_isset(lambda : term_to_ancestor_[desc_])):
                _desc_ = term_to_ancestor_[desc_]
                term_to_ancestor_[desc_] = None
                desc_ = _desc_
            else:
                desc_ = 0
            # end if
            
            if (not php_empty(lambda : desc_)):
                break
            # end if
        # end while
    # end if
    possible_object_parents_ = php_array_filter(possible_object_parents_)
    front_page_url_ = home_url()
    front_page_id_ = php_int(get_option("page_on_front"))
    privacy_policy_page_id_ = php_int(get_option("wp_page_for_privacy_policy"))
    for key_,menu_item_ in menu_items_:
        menu_items_[key_].current = False
        classes_ = menu_item_.classes
        classes_[-1] = "menu-item"
        classes_[-1] = "menu-item-type-" + menu_item_.type
        classes_[-1] = "menu-item-object-" + menu_item_.object
        #// This menu item is set as the 'Front Page'.
        if "post_type" == menu_item_.type and front_page_id_ == php_int(menu_item_.object_id):
            classes_[-1] = "menu-item-home"
        # end if
        #// This menu item is set as the 'Privacy Policy Page'.
        if "post_type" == menu_item_.type and privacy_policy_page_id_ == php_int(menu_item_.object_id):
            classes_[-1] = "menu-item-privacy-policy"
        # end if
        #// If the menu item corresponds to a taxonomy term for the currently queried non-hierarchical post object.
        if wp_query_.is_singular and "taxonomy" == menu_item_.type and php_in_array(menu_item_.object_id, possible_object_parents_):
            active_parent_object_ids_[-1] = php_int(menu_item_.object_id)
            active_parent_item_ids_[-1] = php_int(menu_item_.db_id)
            active_object_ = queried_object_.post_type
            pass
        elif menu_item_.object_id == queried_object_id_ and (not php_empty(lambda : home_page_id_)) and "post_type" == menu_item_.type and wp_query_.is_home and home_page_id_ == menu_item_.object_id or "post_type" == menu_item_.type and wp_query_.is_singular or "taxonomy" == menu_item_.type and wp_query_.is_category or wp_query_.is_tag or wp_query_.is_tax and queried_object_.taxonomy == menu_item_.object:
            classes_[-1] = "current-menu-item"
            menu_items_[key_].current = True
            _anc_id_ = php_int(menu_item_.db_id)
            while True:
                _anc_id_ = get_post_meta(_anc_id_, "_menu_item_menu_item_parent", True)
                if not (_anc_id_ and (not php_in_array(_anc_id_, active_ancestor_item_ids_))):
                    break
                # end if
                active_ancestor_item_ids_[-1] = _anc_id_
            # end while
            if "post_type" == menu_item_.type and "page" == menu_item_.object:
                #// Back compat classes for pages to match wp_page_menu().
                classes_[-1] = "page_item"
                classes_[-1] = "page-item-" + menu_item_.object_id
                classes_[-1] = "current_page_item"
            # end if
            active_parent_item_ids_[-1] = php_int(menu_item_.menu_item_parent)
            active_parent_object_ids_[-1] = php_int(menu_item_.post_parent)
            active_object_ = menu_item_.object
            pass
        elif "post_type_archive" == menu_item_.type and is_post_type_archive(Array(menu_item_.object)):
            classes_[-1] = "current-menu-item"
            menu_items_[key_].current = True
            _anc_id_ = php_int(menu_item_.db_id)
            while True:
                _anc_id_ = get_post_meta(_anc_id_, "_menu_item_menu_item_parent", True)
                if not (_anc_id_ and (not php_in_array(_anc_id_, active_ancestor_item_ids_))):
                    break
                # end if
                active_ancestor_item_ids_[-1] = _anc_id_
            # end while
            active_parent_item_ids_[-1] = php_int(menu_item_.menu_item_parent)
            pass
        elif "custom" == menu_item_.object and (php_isset(lambda : PHP_SERVER["HTTP_HOST"])):
            _root_relative_current_ = untrailingslashit(PHP_SERVER["REQUEST_URI"])
            #// If it's the customize page then it will strip the query var off the URL before entering the comparison block.
            if is_customize_preview():
                _root_relative_current_ = strtok(untrailingslashit(PHP_SERVER["REQUEST_URI"]), "?")
            # end if
            current_url_ = set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + _root_relative_current_)
            raw_item_url_ = php_substr(menu_item_.url, 0, php_strpos(menu_item_.url, "#")) if php_strpos(menu_item_.url, "#") else menu_item_.url
            item_url_ = set_url_scheme(untrailingslashit(raw_item_url_))
            _indexless_current_ = untrailingslashit(php_preg_replace("/" + preg_quote(wp_rewrite_.index, "/") + "$/", "", current_url_))
            matches_ = Array(current_url_, urldecode(current_url_), _indexless_current_, urldecode(_indexless_current_), _root_relative_current_, urldecode(_root_relative_current_))
            if raw_item_url_ and php_in_array(item_url_, matches_):
                classes_[-1] = "current-menu-item"
                menu_items_[key_].current = True
                _anc_id_ = php_int(menu_item_.db_id)
                while True:
                    _anc_id_ = get_post_meta(_anc_id_, "_menu_item_menu_item_parent", True)
                    if not (_anc_id_ and (not php_in_array(_anc_id_, active_ancestor_item_ids_))):
                        break
                    # end if
                    active_ancestor_item_ids_[-1] = _anc_id_
                # end while
                if php_in_array(home_url(), Array(untrailingslashit(current_url_), untrailingslashit(_indexless_current_))):
                    #// Back compat for home link to match wp_page_menu().
                    classes_[-1] = "current_page_item"
                # end if
                active_parent_item_ids_[-1] = php_int(menu_item_.menu_item_parent)
                active_parent_object_ids_[-1] = php_int(menu_item_.post_parent)
                active_object_ = menu_item_.object
                pass
            elif item_url_ == front_page_url_ and is_front_page():
                classes_[-1] = "current-menu-item"
            # end if
            if untrailingslashit(item_url_) == home_url():
                classes_[-1] = "menu-item-home"
            # end if
        # end if
        #// Back-compat with wp_page_menu(): add "current_page_parent" to static home page link for any non-page query.
        if (not php_empty(lambda : home_page_id_)) and "post_type" == menu_item_.type and php_empty(lambda : wp_query_.is_page) and home_page_id_ == menu_item_.object_id:
            classes_[-1] = "current_page_parent"
        # end if
        menu_items_[key_].classes = array_unique(classes_)
    # end for
    active_ancestor_item_ids_ = php_array_filter(array_unique(active_ancestor_item_ids_))
    active_parent_item_ids_ = php_array_filter(array_unique(active_parent_item_ids_))
    active_parent_object_ids_ = php_array_filter(array_unique(active_parent_object_ids_))
    #// Set parent's class.
    for key_,parent_item_ in menu_items_:
        classes_ = parent_item_.classes
        menu_items_[key_].current_item_ancestor = False
        menu_items_[key_].current_item_parent = False
        if (php_isset(lambda : parent_item_.type)) and "post_type" == parent_item_.type and (not php_empty(lambda : queried_object_.post_type)) and is_post_type_hierarchical(queried_object_.post_type) and php_in_array(parent_item_.object_id, queried_object_.ancestors) and parent_item_.object != queried_object_.ID or "taxonomy" == parent_item_.type and (php_isset(lambda : possible_taxonomy_ancestors_[parent_item_.object])) and php_in_array(parent_item_.object_id, possible_taxonomy_ancestors_[parent_item_.object]) and (not (php_isset(lambda : queried_object_.term_id))) or parent_item_.object_id != queried_object_.term_id:
            classes_[-1] = "current-" + queried_object_.post_type + "-ancestor" if php_empty(lambda : queried_object_.taxonomy) else "current-" + queried_object_.taxonomy + "-ancestor"
        # end if
        if php_in_array(php_intval(parent_item_.db_id), active_ancestor_item_ids_):
            classes_[-1] = "current-menu-ancestor"
            menu_items_[key_].current_item_ancestor = True
        # end if
        if php_in_array(parent_item_.db_id, active_parent_item_ids_):
            classes_[-1] = "current-menu-parent"
            menu_items_[key_].current_item_parent = True
        # end if
        if php_in_array(parent_item_.object_id, active_parent_object_ids_):
            classes_[-1] = "current-" + active_object_ + "-parent"
        # end if
        if "post_type" == parent_item_.type and "page" == parent_item_.object:
            #// Back compat classes for pages to match wp_page_menu().
            if php_in_array("current-menu-parent", classes_):
                classes_[-1] = "current_page_parent"
            # end if
            if php_in_array("current-menu-ancestor", classes_):
                classes_[-1] = "current_page_ancestor"
            # end if
        # end if
        menu_items_[key_].classes = array_unique(classes_)
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
def walk_nav_menu_tree(items_=None, depth_=None, r_=None, *_args_):
    
    
    walker_ = php_new_class("Walker_Nav_Menu", lambda : Walker_Nav_Menu()) if php_empty(lambda : r_.walker) else r_.walker
    return walker_.walk(items_, depth_, r_)
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
def _nav_menu_item_id_use_once(id_=None, item_=None, *_args_):
    
    
    _used_ids_ = Array()
    if php_in_array(item_.ID, _used_ids_):
        return ""
    # end if
    _used_ids_[-1] = item_.ID
    return id_
# end def _nav_menu_item_id_use_once
