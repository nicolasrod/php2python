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
#// Core Navigation Menu API
#// 
#// @package WordPress
#// @subpackage Nav_Menus
#// @since 3.0.0
#// 
#// Walker_Nav_Menu_Edit class
php_include_file(ABSPATH + "wp-admin/includes/class-walker-nav-menu-edit.php", once=True)
#// Walker_Nav_Menu_Checklist class
php_include_file(ABSPATH + "wp-admin/includes/class-walker-nav-menu-checklist.php", once=True)
#// 
#// Prints the appropriate response to a menu quick search.
#// 
#// @since 3.0.0
#// 
#// @param array $request The unsanitized request values.
#//
def _wp_ajax_menu_quick_search(request_=None, *_args_):
    if request_ is None:
        request_ = Array()
    # end if
    
    args_ = Array()
    type_ = request_["type"] if (php_isset(lambda : request_["type"])) else ""
    object_type_ = request_["object_type"] if (php_isset(lambda : request_["object_type"])) else ""
    query_ = request_["q"] if (php_isset(lambda : request_["q"])) else ""
    response_format_ = request_["response-format"] if (php_isset(lambda : request_["response-format"])) and php_in_array(request_["response-format"], Array("json", "markup")) else "json"
    if "markup" == response_format_:
        args_["walker"] = php_new_class("Walker_Nav_Menu_Checklist", lambda : Walker_Nav_Menu_Checklist())
    # end if
    if "get-post-item" == type_:
        if post_type_exists(object_type_):
            if (php_isset(lambda : request_["ID"])):
                object_id_ = php_int(request_["ID"])
                if "markup" == response_format_:
                    php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", Array(get_post(object_id_))), 0, args_))
                elif "json" == response_format_:
                    php_print(wp_json_encode(Array({"ID": object_id_, "post_title": get_the_title(object_id_), "post_type": get_post_type(object_id_)})))
                    php_print("\n")
                # end if
            # end if
        elif taxonomy_exists(object_type_):
            if (php_isset(lambda : request_["ID"])):
                object_id_ = php_int(request_["ID"])
                if "markup" == response_format_:
                    php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", Array(get_term(object_id_, object_type_))), 0, args_))
                elif "json" == response_format_:
                    post_obj_ = get_term(object_id_, object_type_)
                    php_print(wp_json_encode(Array({"ID": object_id_, "post_title": post_obj_.name, "post_type": object_type_})))
                    php_print("\n")
                # end if
            # end if
        # end if
    elif php_preg_match("/quick-search-(posttype|taxonomy)-([a-zA-Z_-]*\\b)/", type_, matches_):
        if "posttype" == matches_[1] and get_post_type_object(matches_[2]):
            post_type_obj_ = _wp_nav_menu_meta_box_object(get_post_type_object(matches_[2]))
            args_ = php_array_merge(args_, Array({"no_found_rows": True, "update_post_meta_cache": False, "update_post_term_cache": False, "posts_per_page": 10, "post_type": matches_[2], "s": query_}))
            if (php_isset(lambda : post_type_obj_._default_query)):
                args_ = php_array_merge(args_, post_type_obj_._default_query)
            # end if
            search_results_query_ = php_new_class("WP_Query", lambda : WP_Query(args_))
            if (not search_results_query_.have_posts()):
                return
            # end if
            while True:
                
                if not (search_results_query_.have_posts()):
                    break
                # end if
                post_ = search_results_query_.next_post()
                if "markup" == response_format_:
                    var_by_ref_ = post_.ID
                    php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", Array(get_post(var_by_ref_))), 0, args_))
                elif "json" == response_format_:
                    php_print(wp_json_encode(Array({"ID": post_.ID, "post_title": get_the_title(post_.ID), "post_type": matches_[2]})))
                    php_print("\n")
                # end if
            # end while
        elif "taxonomy" == matches_[1]:
            terms_ = get_terms(Array({"taxonomy": matches_[2], "name__like": query_, "number": 10}))
            if php_empty(lambda : terms_) or is_wp_error(terms_):
                return
            # end if
            for term_ in terms_:
                if "markup" == response_format_:
                    php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", Array(term_)), 0, args_))
                elif "json" == response_format_:
                    php_print(wp_json_encode(Array({"ID": term_.term_id, "post_title": term_.name, "post_type": matches_[2]})))
                    php_print("\n")
                # end if
            # end for
        # end if
    # end if
# end def _wp_ajax_menu_quick_search
#// 
#// Register nav menu meta boxes and advanced menu items.
#// 
#// @since 3.0.0
#//
def wp_nav_menu_setup(*_args_):
    
    
    #// Register meta boxes.
    wp_nav_menu_post_type_meta_boxes()
    add_meta_box("add-custom-links", __("Custom Links"), "wp_nav_menu_item_link_meta_box", "nav-menus", "side", "default")
    wp_nav_menu_taxonomy_meta_boxes()
    #// Register advanced menu items (columns).
    add_filter("manage_nav-menus_columns", "wp_nav_menu_manage_columns")
    #// If first time editing, disable advanced items by default.
    if False == get_user_option("managenav-menuscolumnshidden"):
        user_ = wp_get_current_user()
        update_user_option(user_.ID, "managenav-menuscolumnshidden", Array({0: "link-target", 1: "css-classes", 2: "xfn", 3: "description", 4: "title-attribute"}), True)
    # end if
# end def wp_nav_menu_setup
#// 
#// Limit the amount of meta boxes to pages, posts, links, and categories for first time users.
#// 
#// @since 3.0.0
#// 
#// @global array $wp_meta_boxes
#//
def wp_initial_nav_menu_meta_boxes(*_args_):
    
    
    global wp_meta_boxes_
    php_check_if_defined("wp_meta_boxes_")
    if get_user_option("metaboxhidden_nav-menus") != False or (not php_is_array(wp_meta_boxes_)):
        return
    # end if
    initial_meta_boxes_ = Array("add-post-type-page", "add-post-type-post", "add-custom-links", "add-category")
    hidden_meta_boxes_ = Array()
    for context_ in php_array_keys(wp_meta_boxes_["nav-menus"]):
        for priority_ in php_array_keys(wp_meta_boxes_["nav-menus"][context_]):
            for box_ in wp_meta_boxes_["nav-menus"][context_][priority_]:
                if php_in_array(box_["id"], initial_meta_boxes_):
                    box_["id"] = None
                else:
                    hidden_meta_boxes_[-1] = box_["id"]
                # end if
            # end for
        # end for
    # end for
    user_ = wp_get_current_user()
    update_user_option(user_.ID, "metaboxhidden_nav-menus", hidden_meta_boxes_, True)
# end def wp_initial_nav_menu_meta_boxes
#// 
#// Creates meta boxes for any post type menu item..
#// 
#// @since 3.0.0
#//
def wp_nav_menu_post_type_meta_boxes(*_args_):
    
    
    post_types_ = get_post_types(Array({"show_in_nav_menus": True}), "object")
    if (not post_types_):
        return
    # end if
    for post_type_ in post_types_:
        #// 
        #// Filters whether a menu items meta box will be added for the current
        #// object type.
        #// 
        #// If a falsey value is returned instead of an object, the menu items
        #// meta box for the current meta box object will not be added.
        #// 
        #// @since 3.0.0
        #// 
        #// @param WP_Post_Type|false $post_type The current object to add a menu items
        #// meta box for.
        #//
        post_type_ = apply_filters("nav_menu_meta_box_object", post_type_)
        if post_type_:
            id_ = post_type_.name
            #// Give pages a higher priority.
            priority_ = "core" if "page" == post_type_.name else "default"
            add_meta_box(str("add-post-type-") + str(id_), post_type_.labels.name, "wp_nav_menu_item_post_type_meta_box", "nav-menus", "side", priority_, post_type_)
        # end if
    # end for
# end def wp_nav_menu_post_type_meta_boxes
#// 
#// Creates meta boxes for any taxonomy menu item.
#// 
#// @since 3.0.0
#//
def wp_nav_menu_taxonomy_meta_boxes(*_args_):
    
    
    taxonomies_ = get_taxonomies(Array({"show_in_nav_menus": True}), "object")
    if (not taxonomies_):
        return
    # end if
    for tax_ in taxonomies_:
        #// This filter is documented in wp-admin/includes/nav-menu.php
        tax_ = apply_filters("nav_menu_meta_box_object", tax_)
        if tax_:
            id_ = tax_.name
            add_meta_box(str("add-") + str(id_), tax_.labels.name, "wp_nav_menu_item_taxonomy_meta_box", "nav-menus", "side", "default", tax_)
        # end if
    # end for
# end def wp_nav_menu_taxonomy_meta_boxes
#// 
#// Check whether to disable the Menu Locations meta box submit button and inputs.
#// 
#// @since 3.6.0
#// @since 5.3.1 The `$echo` parameter was added.
#// 
#// @global bool $one_theme_location_no_menus to determine if no menus exist
#// 
#// @param int|string $nav_menu_selected_id ID, name, or slug of the currently selected menu.
#// @param bool       $echo                 Whether to echo or just return the string.
#// @return string|false Disabled attribute if at least one menu exists, false if not.
#//
def wp_nav_menu_disabled_check(nav_menu_selected_id_=None, echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    global one_theme_location_no_menus_
    php_check_if_defined("one_theme_location_no_menus_")
    if one_theme_location_no_menus_:
        return False
    # end if
    return disabled(nav_menu_selected_id_, 0, echo_)
# end def wp_nav_menu_disabled_check
#// 
#// Displays a meta box for the custom links menu item.
#// 
#// @since 3.0.0
#// 
#// @global int        $_nav_menu_placeholder
#// @global int|string $nav_menu_selected_id
#//
def wp_nav_menu_item_link_meta_box(*_args_):
    
    
    global _nav_menu_placeholder_
    global nav_menu_selected_id_
    php_check_if_defined("_nav_menu_placeholder_","nav_menu_selected_id_")
    _nav_menu_placeholder_ = _nav_menu_placeholder_ - 1 if 0 > _nav_menu_placeholder_ else -1
    php_print(" <div class=\"customlinkdiv\" id=\"customlinkdiv\">\n        <input type=\"hidden\" value=\"custom\" name=\"menu-item[")
    php_print(_nav_menu_placeholder_)
    php_print("][menu-item-type]\" />\n     <p id=\"menu-item-url-wrap\" class=\"wp-clearfix\">\n           <label class=\"howto\" for=\"custom-menu-item-url\">")
    _e("URL")
    php_print("</label>\n           <input id=\"custom-menu-item-url\" name=\"menu-item[")
    php_print(_nav_menu_placeholder_)
    php_print("][menu-item-url]\" type=\"text\"")
    wp_nav_menu_disabled_check(nav_menu_selected_id_)
    php_print(""" class=\"code menu-item-textbox\" placeholder=\"https://\" />
    </p>
    <p id=\"menu-item-name-wrap\" class=\"wp-clearfix\">
    <label class=\"howto\" for=\"custom-menu-item-name\">""")
    _e("Link Text")
    php_print("</label>\n           <input id=\"custom-menu-item-name\" name=\"menu-item[")
    php_print(_nav_menu_placeholder_)
    php_print("][menu-item-title]\" type=\"text\"")
    wp_nav_menu_disabled_check(nav_menu_selected_id_)
    php_print(""" class=\"regular-text menu-item-textbox\" />
    </p>
    <p class=\"button-controls wp-clearfix\">
    <span class=\"add-to-menu\">
    <input type=\"submit\"""")
    wp_nav_menu_disabled_check(nav_menu_selected_id_)
    php_print(" class=\"button submit-add-to-menu right\" value=\"")
    esc_attr_e("Add to Menu")
    php_print("""\" name=\"add-custom-menu-item\" id=\"submit-customlinkdiv\" />
    <span class=\"spinner\"></span>
    </span>
    </p>
    </div><!-- /.customlinkdiv -->
    """)
# end def wp_nav_menu_item_link_meta_box
#// 
#// Displays a meta box for a post type menu item.
#// 
#// @since 3.0.0
#// 
#// @global int        $_nav_menu_placeholder
#// @global int|string $nav_menu_selected_id
#// 
#// @param string $object Not used.
#// @param array  $box {
#// Post type menu item meta box arguments.
#// 
#// @type string       $id       Meta box 'id' attribute.
#// @type string       $title    Meta box title.
#// @type string       $callback Meta box display callback.
#// @type WP_Post_Type $args     Extra meta box arguments (the post type object for this meta box).
#// }
#//
def wp_nav_menu_item_post_type_meta_box(object_=None, box_=None, *_args_):
    
    
    global _nav_menu_placeholder_
    global nav_menu_selected_id_
    php_check_if_defined("_nav_menu_placeholder_","nav_menu_selected_id_")
    post_type_name_ = box_["args"].name
    post_type_ = get_post_type_object(post_type_name_)
    #// Paginate browsing for large numbers of post objects.
    per_page_ = 50
    pagenum_ = absint(PHP_REQUEST["paged"]) if (php_isset(lambda : PHP_REQUEST[post_type_name_ + "-tab"])) and (php_isset(lambda : PHP_REQUEST["paged"])) else 1
    offset_ = per_page_ * pagenum_ - 1 if 0 < pagenum_ else 0
    args_ = Array({"offset": offset_, "order": "ASC", "orderby": "title", "posts_per_page": per_page_, "post_type": post_type_name_, "suppress_filters": True, "update_post_term_cache": False, "update_post_meta_cache": False})
    if (php_isset(lambda : box_["args"]._default_query)):
        args_ = php_array_merge(args_, box_["args"]._default_query)
    # end if
    #// 
    #// If we're dealing with pages, let's prioritize the Front Page,
    #// Posts Page and Privacy Policy Page at the top of the list.
    #//
    important_pages_ = Array()
    if "page" == post_type_name_:
        suppress_page_ids_ = Array()
        #// Insert Front Page or custom Home link.
        front_page_ = php_int(get_option("page_on_front")) if "page" == get_option("show_on_front") else 0
        front_page_obj_ = None
        if (not php_empty(lambda : front_page_)):
            front_page_obj_ = get_post(front_page_)
            front_page_obj_.front_or_home = True
            important_pages_[-1] = front_page_obj_
            suppress_page_ids_[-1] = front_page_obj_.ID
        else:
            _nav_menu_placeholder_ = php_intval(_nav_menu_placeholder_) - 1 if 0 > _nav_menu_placeholder_ else -1
            front_page_obj_ = Array({"front_or_home": True, "ID": 0, "object_id": _nav_menu_placeholder_, "post_content": "", "post_excerpt": "", "post_parent": "", "post_title": _x("Home", "nav menu home label"), "post_type": "nav_menu_item", "type": "custom", "url": home_url("/")})
            important_pages_[-1] = front_page_obj_
        # end if
        #// Insert Posts Page.
        posts_page_ = php_int(get_option("page_for_posts")) if "page" == get_option("show_on_front") else 0
        if (not php_empty(lambda : posts_page_)):
            posts_page_obj_ = get_post(posts_page_)
            posts_page_obj_.posts_page = True
            important_pages_[-1] = posts_page_obj_
            suppress_page_ids_[-1] = posts_page_obj_.ID
        # end if
        #// Insert Privacy Policy Page.
        privacy_policy_page_id_ = php_int(get_option("wp_page_for_privacy_policy"))
        if (not php_empty(lambda : privacy_policy_page_id_)):
            privacy_policy_page_ = get_post(privacy_policy_page_id_)
            if type(privacy_policy_page_).__name__ == "WP_Post" and "publish" == privacy_policy_page_.post_status:
                privacy_policy_page_.privacy_policy_page = True
                important_pages_[-1] = privacy_policy_page_
                suppress_page_ids_[-1] = privacy_policy_page_.ID
            # end if
        # end if
        #// Add suppression array to arguments for WP_Query.
        if (not php_empty(lambda : suppress_page_ids_)):
            args_["post__not_in"] = suppress_page_ids_
        # end if
    # end if
    #// @todo Transient caching of these results with proper invalidation on updating of a post of this type.
    get_posts_ = php_new_class("WP_Query", lambda : WP_Query())
    posts_ = get_posts_.query(args_)
    #// Only suppress and insert when more than just suppression pages available.
    if (not get_posts_.post_count):
        if (not php_empty(lambda : suppress_page_ids_)):
            args_["post__not_in"] = None
            get_posts_ = php_new_class("WP_Query", lambda : WP_Query())
            posts_ = get_posts_.query(args_)
        else:
            php_print("<p>" + __("No items.") + "</p>")
            return
        # end if
    elif (not php_empty(lambda : important_pages_)):
        posts_ = php_array_merge(important_pages_, posts_)
    # end if
    num_pages_ = get_posts_.max_num_pages
    page_links_ = paginate_links(Array({"base": add_query_arg(Array({post_type_name_ + "-tab": "all", "paged": "%#%", "item-type": "post_type", "item-object": post_type_name_}))}, {"format": "", "prev_text": "<span aria-label=\"" + esc_attr__("Previous page") + "\">" + __("&laquo;") + "</span>", "next_text": "<span aria-label=\"" + esc_attr__("Next page") + "\">" + __("&raquo;") + "</span>", "before_page_number": "<span class=\"screen-reader-text\">" + __("Page") + "</span> ", "total": num_pages_, "current": pagenum_}))
    db_fields_ = False
    if is_post_type_hierarchical(post_type_name_):
        db_fields_ = Array({"parent": "post_parent", "id": "ID"})
    # end if
    walker_ = php_new_class("Walker_Nav_Menu_Checklist", lambda : Walker_Nav_Menu_Checklist(db_fields_))
    current_tab_ = "most-recent"
    if (php_isset(lambda : PHP_REQUEST[post_type_name_ + "-tab"])) and php_in_array(PHP_REQUEST[post_type_name_ + "-tab"], Array("all", "search")):
        current_tab_ = PHP_REQUEST[post_type_name_ + "-tab"]
    # end if
    if (not php_empty(lambda : PHP_REQUEST["quick-search-posttype-" + post_type_name_])):
        current_tab_ = "search"
    # end if
    removed_args_ = Array("action", "customlink-tab", "edit-menu-item", "menu-item", "page-tab", "_wpnonce")
    most_recent_url_ = ""
    view_all_url_ = ""
    search_url_ = ""
    if nav_menu_selected_id_:
        most_recent_url_ = esc_url(add_query_arg(post_type_name_ + "-tab", "most-recent", remove_query_arg(removed_args_)))
        view_all_url_ = esc_url(add_query_arg(post_type_name_ + "-tab", "all", remove_query_arg(removed_args_)))
        search_url_ = esc_url(add_query_arg(post_type_name_ + "-tab", "search", remove_query_arg(removed_args_)))
    # end if
    php_print(" <div id=\"posttype-")
    php_print(post_type_name_)
    php_print("\" class=\"posttypediv\">\n      <ul id=\"posttype-")
    php_print(post_type_name_)
    php_print("-tabs\" class=\"posttype-tabs add-menu-item-tabs\">\n            <li ")
    php_print(" class=\"tabs\"" if "most-recent" == current_tab_ else "")
    php_print(">\n              <a class=\"nav-tab-link\" data-type=\"tabs-panel-posttype-")
    php_print(esc_attr(post_type_name_))
    php_print("-most-recent\" href=\"")
    php_print(most_recent_url_)
    php_print("#tabs-panel-posttype-")
    php_print(post_type_name_)
    php_print("-most-recent\">\n                    ")
    _e("Most Recent")
    php_print("             </a>\n          </li>\n         <li ")
    php_print(" class=\"tabs\"" if "all" == current_tab_ else "")
    php_print(">\n              <a class=\"nav-tab-link\" data-type=\"")
    php_print(esc_attr(post_type_name_))
    php_print("-all\" href=\"")
    php_print(view_all_url_)
    php_print("#")
    php_print(post_type_name_)
    php_print("-all\">\n                    ")
    _e("View All")
    php_print("             </a>\n          </li>\n         <li ")
    php_print(" class=\"tabs\"" if "search" == current_tab_ else "")
    php_print(">\n              <a class=\"nav-tab-link\" data-type=\"tabs-panel-posttype-")
    php_print(esc_attr(post_type_name_))
    php_print("-search\" href=\"")
    php_print(search_url_)
    php_print("#tabs-panel-posttype-")
    php_print(post_type_name_)
    php_print("-search\">\n                 ")
    _e("Search")
    php_print("""               </a>
    </li>
    </ul><!-- .posttype-tabs -->
    <div id=\"tabs-panel-posttype-""")
    php_print(post_type_name_)
    php_print("-most-recent\" class=\"tabs-panel ")
    php_print("tabs-panel-active" if "most-recent" == current_tab_ else "tabs-panel-inactive")
    php_print("\" role=\"region\" aria-label=\"")
    _e("Most Recent")
    php_print("\" tabindex=\"0\">\n         <ul id=\"")
    php_print(post_type_name_)
    php_print("checklist-most-recent\" class=\"categorychecklist form-no-clear\">\n             ")
    recent_args_ = php_array_merge(args_, Array({"orderby": "post_date", "order": "DESC", "posts_per_page": 15}))
    most_recent_ = get_posts_.query(recent_args_)
    args_["walker"] = walker_
    #// 
    #// Filters the posts displayed in the 'Most Recent' tab of the current
    #// post type's menu items meta box.
    #// 
    #// The dynamic portion of the hook name, `$post_type_name`, refers to the post type name.
    #// 
    #// @since 4.3.0
    #// @since 4.9.0 Added the `$recent_args` parameter.
    #// 
    #// @param WP_Post[] $most_recent An array of post objects being listed.
    #// @param array     $args        An array of `WP_Query` arguments for the meta box.
    #// @param array     $box         Arguments passed to `wp_nav_menu_item_post_type_meta_box()`.
    #// @param array     $recent_args An array of `WP_Query` arguments for 'Most Recent' tab.
    #//
    most_recent_ = apply_filters(str("nav_menu_items_") + str(post_type_name_) + str("_recent"), most_recent_, args_, box_, recent_args_)
    php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", most_recent_), 0, args_))
    php_print("""           </ul>
    </div><!-- /.tabs-panel -->
    <div class=\"tabs-panel """)
    php_print("tabs-panel-active" if "search" == current_tab_ else "tabs-panel-inactive")
    php_print("\" id=\"tabs-panel-posttype-")
    php_print(post_type_name_)
    php_print("-search\" role=\"region\" aria-label=\"")
    php_print(post_type_.labels.search_items)
    php_print("\" tabindex=\"0\">\n         ")
    if (php_isset(lambda : PHP_REQUEST["quick-search-posttype-" + post_type_name_])):
        searched_ = esc_attr(PHP_REQUEST["quick-search-posttype-" + post_type_name_])
        search_results_ = get_posts(Array({"s": searched_, "post_type": post_type_name_, "fields": "all", "order": "DESC"}))
    else:
        searched_ = ""
        search_results_ = Array()
    # end if
    php_print("         <p class=\"quick-search-wrap\">\n               <label for=\"quick-search-posttype-")
    php_print(post_type_name_)
    php_print("\" class=\"screen-reader-text\">")
    _e("Search")
    php_print("</label>\n               <input type=\"search\"")
    wp_nav_menu_disabled_check(nav_menu_selected_id_)
    php_print(" class=\"quick-search\" value=\"")
    php_print(searched_)
    php_print("\" name=\"quick-search-posttype-")
    php_print(post_type_name_)
    php_print("\" id=\"quick-search-posttype-")
    php_print(post_type_name_)
    php_print("\" />\n              <span class=\"spinner\"></span>\n               ")
    submit_button(__("Search"), "small quick-search-submit hide-if-js", "submit", False, Array({"id": "submit-quick-search-posttype-" + post_type_name_}))
    php_print("         </p>\n\n            <ul id=\"")
    php_print(post_type_name_)
    php_print("-search-checklist\" data-wp-lists=\"list:")
    php_print(post_type_name_)
    php_print("\" class=\"categorychecklist form-no-clear\">\n          ")
    if (not php_empty(lambda : search_results_)) and (not is_wp_error(search_results_)):
        php_print("             ")
        args_["walker"] = walker_
        php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", search_results_), 0, args_))
        php_print("         ")
    elif is_wp_error(search_results_):
        php_print("             <li>")
        php_print(search_results_.get_error_message())
        php_print("</li>\n          ")
    elif (not php_empty(lambda : searched_)):
        php_print("             <li>")
        _e("No results found.")
        php_print("</li>\n          ")
    # end if
    php_print("""           </ul>
    </div><!-- /.tabs-panel -->
    <div id=\"""")
    php_print(post_type_name_)
    php_print("-all\" class=\"tabs-panel tabs-panel-view-all ")
    php_print("tabs-panel-active" if "all" == current_tab_ else "tabs-panel-inactive")
    php_print("\" role=\"region\" aria-label=\"")
    php_print(post_type_.labels.all_items)
    php_print("\" tabindex=\"0\">\n         ")
    if (not php_empty(lambda : page_links_)):
        php_print("             <div class=\"add-menu-item-pagelinks\">\n                   ")
        php_print(page_links_)
        php_print("             </div>\n            ")
    # end if
    php_print("         <ul id=\"")
    php_print(post_type_name_)
    php_print("checklist\" data-wp-lists=\"list:")
    php_print(post_type_name_)
    php_print("\" class=\"categorychecklist form-no-clear\">\n              ")
    args_["walker"] = walker_
    if post_type_.has_archive:
        _nav_menu_placeholder_ = php_intval(_nav_menu_placeholder_) - 1 if 0 > _nav_menu_placeholder_ else -1
        array_unshift(posts_, Array({"ID": 0, "object_id": _nav_menu_placeholder_, "object": post_type_name_, "post_content": "", "post_excerpt": "", "post_title": post_type_.labels.archives, "post_type": "nav_menu_item", "type": "post_type_archive", "url": get_post_type_archive_link(post_type_name_)}))
    # end if
    #// 
    #// Filters the posts displayed in the 'View All' tab of the current
    #// post type's menu items meta box.
    #// 
    #// The dynamic portion of the hook name, `$post_type_name`, refers
    #// to the slug of the current post type.
    #// 
    #// @since 3.2.0
    #// @since 4.6.0 Converted the `$post_type` parameter to accept a WP_Post_Type object.
    #// 
    #// @see WP_Query::query()
    #// 
    #// @param object[]     $posts     The posts for the current post type. Mostly `WP_Post` objects, but
    #// can also contain "fake" post objects to represent other menu items.
    #// @param array        $args      An array of `WP_Query` arguments.
    #// @param WP_Post_Type $post_type The current post type object for this menu item meta box.
    #//
    posts_ = apply_filters(str("nav_menu_items_") + str(post_type_name_), posts_, args_, post_type_)
    checkbox_items_ = walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", posts_), 0, args_)
    php_print(checkbox_items_)
    php_print("         </ul>\n         ")
    if (not php_empty(lambda : page_links_)):
        php_print("             <div class=\"add-menu-item-pagelinks\">\n                   ")
        php_print(page_links_)
        php_print("             </div>\n            ")
    # end if
    php_print("     </div><!-- /.tabs-panel -->\n\n     <p class=\"button-controls wp-clearfix\" data-items-type=\"posttype-")
    php_print(esc_attr(post_type_name_))
    php_print("\">\n            <span class=\"list-controls hide-if-no-js\">\n              <input type=\"checkbox\"")
    wp_nav_menu_disabled_check(nav_menu_selected_id_)
    php_print(" id=\"")
    php_print(esc_attr(post_type_name_ + "-tab"))
    php_print("\" class=\"select-all\" />\n             <label for=\"")
    php_print(esc_attr(post_type_name_ + "-tab"))
    php_print("\">")
    _e("Select All")
    php_print("""</label>
    </span>
    <span class=\"add-to-menu\">
    <input type=\"submit\"""")
    wp_nav_menu_disabled_check(nav_menu_selected_id_)
    php_print(" class=\"button submit-add-to-menu right\" value=\"")
    esc_attr_e("Add to Menu")
    php_print("\" name=\"add-post-type-menu-item\" id=\"")
    php_print(esc_attr("submit-posttype-" + post_type_name_))
    php_print("""\" />
    <span class=\"spinner\"></span>
    </span>
    </p>
    </div><!-- /.posttypediv -->
    """)
# end def wp_nav_menu_item_post_type_meta_box
#// 
#// Displays a meta box for a taxonomy menu item.
#// 
#// @since 3.0.0
#// 
#// @global int|string $nav_menu_selected_id
#// 
#// @param string $object Not used.
#// @param array  $box {
#// Taxonomy menu item meta box arguments.
#// 
#// @type string $id       Meta box 'id' attribute.
#// @type string $title    Meta box title.
#// @type string $callback Meta box display callback.
#// @type object $args     Extra meta box arguments (the taxonomy object for this meta box).
#// }
#//
def wp_nav_menu_item_taxonomy_meta_box(object_=None, box_=None, *_args_):
    
    
    global nav_menu_selected_id_
    php_check_if_defined("nav_menu_selected_id_")
    taxonomy_name_ = box_["args"].name
    taxonomy_ = get_taxonomy(taxonomy_name_)
    #// Paginate browsing for large numbers of objects.
    per_page_ = 50
    pagenum_ = absint(PHP_REQUEST["paged"]) if (php_isset(lambda : PHP_REQUEST[taxonomy_name_ + "-tab"])) and (php_isset(lambda : PHP_REQUEST["paged"])) else 1
    offset_ = per_page_ * pagenum_ - 1 if 0 < pagenum_ else 0
    args_ = Array({"taxonomy": taxonomy_name_, "child_of": 0, "exclude": "", "hide_empty": False, "hierarchical": 1, "include": "", "number": per_page_, "offset": offset_, "order": "ASC", "orderby": "name", "pad_counts": False})
    terms_ = get_terms(args_)
    if (not terms_) or is_wp_error(terms_):
        php_print("<p>" + __("No items.") + "</p>")
        return
    # end if
    num_pages_ = ceil(wp_count_terms(taxonomy_name_, php_array_merge(args_, Array({"number": "", "offset": ""}))) / per_page_)
    page_links_ = paginate_links(Array({"base": add_query_arg(Array({taxonomy_name_ + "-tab": "all", "paged": "%#%", "item-type": "taxonomy", "item-object": taxonomy_name_}))}, {"format": "", "prev_text": "<span aria-label=\"" + esc_attr__("Previous page") + "\">" + __("&laquo;") + "</span>", "next_text": "<span aria-label=\"" + esc_attr__("Next page") + "\">" + __("&raquo;") + "</span>", "before_page_number": "<span class=\"screen-reader-text\">" + __("Page") + "</span> ", "total": num_pages_, "current": pagenum_}))
    db_fields_ = False
    if is_taxonomy_hierarchical(taxonomy_name_):
        db_fields_ = Array({"parent": "parent", "id": "term_id"})
    # end if
    walker_ = php_new_class("Walker_Nav_Menu_Checklist", lambda : Walker_Nav_Menu_Checklist(db_fields_))
    current_tab_ = "most-used"
    if (php_isset(lambda : PHP_REQUEST[taxonomy_name_ + "-tab"])) and php_in_array(PHP_REQUEST[taxonomy_name_ + "-tab"], Array("all", "most-used", "search")):
        current_tab_ = PHP_REQUEST[taxonomy_name_ + "-tab"]
    # end if
    if (not php_empty(lambda : PHP_REQUEST["quick-search-taxonomy-" + taxonomy_name_])):
        current_tab_ = "search"
    # end if
    removed_args_ = Array("action", "customlink-tab", "edit-menu-item", "menu-item", "page-tab", "_wpnonce")
    most_used_url_ = ""
    view_all_url_ = ""
    search_url_ = ""
    if nav_menu_selected_id_:
        most_used_url_ = esc_url(add_query_arg(taxonomy_name_ + "-tab", "most-used", remove_query_arg(removed_args_)))
        view_all_url_ = esc_url(add_query_arg(taxonomy_name_ + "-tab", "all", remove_query_arg(removed_args_)))
        search_url_ = esc_url(add_query_arg(taxonomy_name_ + "-tab", "search", remove_query_arg(removed_args_)))
    # end if
    php_print(" <div id=\"taxonomy-")
    php_print(taxonomy_name_)
    php_print("\" class=\"taxonomydiv\">\n      <ul id=\"taxonomy-")
    php_print(taxonomy_name_)
    php_print("-tabs\" class=\"taxonomy-tabs add-menu-item-tabs\">\n            <li ")
    php_print(" class=\"tabs\"" if "most-used" == current_tab_ else "")
    php_print(">\n              <a class=\"nav-tab-link\" data-type=\"tabs-panel-")
    php_print(esc_attr(taxonomy_name_))
    php_print("-pop\" href=\"")
    php_print(most_used_url_)
    php_print("#tabs-panel-")
    php_print(taxonomy_name_)
    php_print("-pop\">\n                    ")
    php_print(esc_html(taxonomy_.labels.most_used))
    php_print("             </a>\n          </li>\n         <li ")
    php_print(" class=\"tabs\"" if "all" == current_tab_ else "")
    php_print(">\n              <a class=\"nav-tab-link\" data-type=\"tabs-panel-")
    php_print(esc_attr(taxonomy_name_))
    php_print("-all\" href=\"")
    php_print(view_all_url_)
    php_print("#tabs-panel-")
    php_print(taxonomy_name_)
    php_print("-all\">\n                    ")
    _e("View All")
    php_print("             </a>\n          </li>\n         <li ")
    php_print(" class=\"tabs\"" if "search" == current_tab_ else "")
    php_print(">\n              <a class=\"nav-tab-link\" data-type=\"tabs-panel-search-taxonomy-")
    php_print(esc_attr(taxonomy_name_))
    php_print("\" href=\"")
    php_print(search_url_)
    php_print("#tabs-panel-search-taxonomy-")
    php_print(taxonomy_name_)
    php_print("\">\n                    ")
    _e("Search")
    php_print("""               </a>
    </li>
    </ul><!-- .taxonomy-tabs -->
    <div id=\"tabs-panel-""")
    php_print(taxonomy_name_)
    php_print("-pop\" class=\"tabs-panel ")
    php_print("tabs-panel-active" if "most-used" == current_tab_ else "tabs-panel-inactive")
    php_print("\" role=\"region\" aria-label=\"")
    php_print(taxonomy_.labels.most_used)
    php_print("\" tabindex=\"0\">\n         <ul id=\"")
    php_print(taxonomy_name_)
    php_print("checklist-pop\" class=\"categorychecklist form-no-clear\" >\n                ")
    popular_terms_ = get_terms(Array({"taxonomy": taxonomy_name_, "orderby": "count", "order": "DESC", "number": 10, "hierarchical": False}))
    args_["walker"] = walker_
    php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", popular_terms_), 0, args_))
    php_print("""           </ul>
    </div><!-- /.tabs-panel -->
    <div id=\"tabs-panel-""")
    php_print(taxonomy_name_)
    php_print("-all\" class=\"tabs-panel tabs-panel-view-all ")
    php_print("tabs-panel-active" if "all" == current_tab_ else "tabs-panel-inactive")
    php_print("\" role=\"region\" aria-label=\"")
    php_print(taxonomy_.labels.all_items)
    php_print("\" tabindex=\"0\">\n         ")
    if (not php_empty(lambda : page_links_)):
        php_print("             <div class=\"add-menu-item-pagelinks\">\n                   ")
        php_print(page_links_)
        php_print("             </div>\n            ")
    # end if
    php_print("         <ul id=\"")
    php_print(taxonomy_name_)
    php_print("checklist\" data-wp-lists=\"list:")
    php_print(taxonomy_name_)
    php_print("\" class=\"categorychecklist form-no-clear\">\n              ")
    args_["walker"] = walker_
    php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", terms_), 0, args_))
    php_print("         </ul>\n         ")
    if (not php_empty(lambda : page_links_)):
        php_print("             <div class=\"add-menu-item-pagelinks\">\n                   ")
        php_print(page_links_)
        php_print("             </div>\n            ")
    # end if
    php_print("     </div><!-- /.tabs-panel -->\n\n     <div class=\"tabs-panel ")
    php_print("tabs-panel-active" if "search" == current_tab_ else "tabs-panel-inactive")
    php_print("\" id=\"tabs-panel-search-taxonomy-")
    php_print(taxonomy_name_)
    php_print("\" role=\"region\" aria-label=\"")
    php_print(taxonomy_.labels.search_items)
    php_print("\" tabindex=\"0\">\n         ")
    if (php_isset(lambda : PHP_REQUEST["quick-search-taxonomy-" + taxonomy_name_])):
        searched_ = esc_attr(PHP_REQUEST["quick-search-taxonomy-" + taxonomy_name_])
        search_results_ = get_terms(Array({"taxonomy": taxonomy_name_, "name__like": searched_, "fields": "all", "orderby": "count", "order": "DESC", "hierarchical": False}))
    else:
        searched_ = ""
        search_results_ = Array()
    # end if
    php_print("         <p class=\"quick-search-wrap\">\n               <label for=\"quick-search-taxonomy-")
    php_print(taxonomy_name_)
    php_print("\" class=\"screen-reader-text\">")
    _e("Search")
    php_print("</label>\n               <input type=\"search\" class=\"quick-search\" value=\"")
    php_print(searched_)
    php_print("\" name=\"quick-search-taxonomy-")
    php_print(taxonomy_name_)
    php_print("\" id=\"quick-search-taxonomy-")
    php_print(taxonomy_name_)
    php_print("\" />\n              <span class=\"spinner\"></span>\n               ")
    submit_button(__("Search"), "small quick-search-submit hide-if-js", "submit", False, Array({"id": "submit-quick-search-taxonomy-" + taxonomy_name_}))
    php_print("         </p>\n\n            <ul id=\"")
    php_print(taxonomy_name_)
    php_print("-search-checklist\" data-wp-lists=\"list:")
    php_print(taxonomy_name_)
    php_print("\" class=\"categorychecklist form-no-clear\">\n          ")
    if (not php_empty(lambda : search_results_)) and (not is_wp_error(search_results_)):
        php_print("             ")
        args_["walker"] = walker_
        php_print(walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", search_results_), 0, args_))
        php_print("         ")
    elif is_wp_error(search_results_):
        php_print("             <li>")
        php_print(search_results_.get_error_message())
        php_print("</li>\n          ")
    elif (not php_empty(lambda : searched_)):
        php_print("             <li>")
        _e("No results found.")
        php_print("</li>\n          ")
    # end if
    php_print("""           </ul>
    </div><!-- /.tabs-panel -->
    <p class=\"button-controls wp-clearfix\" data-items-type=\"taxonomy-""")
    php_print(esc_attr(taxonomy_name_))
    php_print("\">\n            <span class=\"list-controls hide-if-no-js\">\n              <input type=\"checkbox\"")
    wp_nav_menu_disabled_check(nav_menu_selected_id_)
    php_print(" id=\"")
    php_print(esc_attr(taxonomy_name_ + "-tab"))
    php_print("\" class=\"select-all\" />\n             <label for=\"")
    php_print(esc_attr(taxonomy_name_ + "-tab"))
    php_print("\">")
    _e("Select All")
    php_print("""</label>
    </span>
    <span class=\"add-to-menu\">
    <input type=\"submit\"""")
    wp_nav_menu_disabled_check(nav_menu_selected_id_)
    php_print(" class=\"button submit-add-to-menu right\" value=\"")
    esc_attr_e("Add to Menu")
    php_print("\" name=\"add-taxonomy-menu-item\" id=\"")
    php_print(esc_attr("submit-taxonomy-" + taxonomy_name_))
    php_print("""\" />
    <span class=\"spinner\"></span>
    </span>
    </p>
    </div><!-- /.taxonomydiv -->
    """)
# end def wp_nav_menu_item_taxonomy_meta_box
#// 
#// Save posted nav menu item data.
#// 
#// @since 3.0.0
#// 
#// @param int     $menu_id   The menu ID for which to save this item. Value of 0 makes a draft, orphaned menu item. Default 0.
#// @param array[] $menu_data The unsanitized POSTed menu item data.
#// @return int[] The database IDs of the items saved
#//
def wp_save_nav_menu_items(menu_id_=0, menu_data_=None, *_args_):
    if menu_data_ is None:
        menu_data_ = Array()
    # end if
    
    menu_id_ = php_int(menu_id_)
    items_saved_ = Array()
    if 0 == menu_id_ or is_nav_menu(menu_id_):
        #// Loop through all the menu items' POST values.
        for _possible_db_id_,_item_object_data_ in menu_data_.items():
            if php_empty(lambda : _item_object_data_["menu-item-object-id"]) and (not (php_isset(lambda : _item_object_data_["menu-item-type"]))) or php_in_array(_item_object_data_["menu-item-url"], Array("https://", "http://", "")) or (not "custom" == _item_object_data_["menu-item-type"] and (not (php_isset(lambda : _item_object_data_["menu-item-db-id"])))) or (not php_empty(lambda : _item_object_data_["menu-item-db-id"])):
                continue
            # end if
            #// If this possible menu item doesn't actually have a menu database ID yet.
            if php_empty(lambda : _item_object_data_["menu-item-db-id"]) or 0 > _possible_db_id_ or _possible_db_id_ != _item_object_data_["menu-item-db-id"]:
                _actual_db_id_ = 0
            else:
                _actual_db_id_ = php_int(_item_object_data_["menu-item-db-id"])
            # end if
            args_ = Array({"menu-item-db-id": _item_object_data_["menu-item-db-id"] if (php_isset(lambda : _item_object_data_["menu-item-db-id"])) else "", "menu-item-object-id": _item_object_data_["menu-item-object-id"] if (php_isset(lambda : _item_object_data_["menu-item-object-id"])) else "", "menu-item-object": _item_object_data_["menu-item-object"] if (php_isset(lambda : _item_object_data_["menu-item-object"])) else "", "menu-item-parent-id": _item_object_data_["menu-item-parent-id"] if (php_isset(lambda : _item_object_data_["menu-item-parent-id"])) else "", "menu-item-position": _item_object_data_["menu-item-position"] if (php_isset(lambda : _item_object_data_["menu-item-position"])) else "", "menu-item-type": _item_object_data_["menu-item-type"] if (php_isset(lambda : _item_object_data_["menu-item-type"])) else "", "menu-item-title": _item_object_data_["menu-item-title"] if (php_isset(lambda : _item_object_data_["menu-item-title"])) else "", "menu-item-url": _item_object_data_["menu-item-url"] if (php_isset(lambda : _item_object_data_["menu-item-url"])) else "", "menu-item-description": _item_object_data_["menu-item-description"] if (php_isset(lambda : _item_object_data_["menu-item-description"])) else "", "menu-item-attr-title": _item_object_data_["menu-item-attr-title"] if (php_isset(lambda : _item_object_data_["menu-item-attr-title"])) else "", "menu-item-target": _item_object_data_["menu-item-target"] if (php_isset(lambda : _item_object_data_["menu-item-target"])) else "", "menu-item-classes": _item_object_data_["menu-item-classes"] if (php_isset(lambda : _item_object_data_["menu-item-classes"])) else "", "menu-item-xfn": _item_object_data_["menu-item-xfn"] if (php_isset(lambda : _item_object_data_["menu-item-xfn"])) else ""})
            items_saved_[-1] = wp_update_nav_menu_item(menu_id_, _actual_db_id_, args_)
        # end for
    # end if
    return items_saved_
# end def wp_save_nav_menu_items
#// 
#// Adds custom arguments to some of the meta box object types.
#// 
#// @since 3.0.0
#// 
#// @access private
#// 
#// @param object $object The post type or taxonomy meta-object.
#// @return object The post type or taxonomy object.
#//
def _wp_nav_menu_meta_box_object(object_=None, *_args_):
    if object_ is None:
        object_ = None
    # end if
    
    if (php_isset(lambda : object_.name)):
        if "page" == object_.name:
            object_._default_query = Array({"orderby": "menu_order title", "post_status": "publish"})
            pass
        elif "post" == object_.name:
            object_._default_query = Array({"post_status": "publish"})
            pass
        elif "category" == object_.name:
            object_._default_query = Array({"orderby": "id", "order": "DESC"})
            pass
        else:
            object_._default_query = Array({"post_status": "publish"})
        # end if
    # end if
    return object_
# end def _wp_nav_menu_meta_box_object
#// 
#// Returns the menu formatted to edit.
#// 
#// @since 3.0.0
#// 
#// @param int $menu_id Optional. The ID of the menu to format. Default 0.
#// @return string|WP_Error $output The menu formatted to edit or error object on failure.
#//
def wp_get_nav_menu_to_edit(menu_id_=0, *_args_):
    
    
    menu_ = wp_get_nav_menu_object(menu_id_)
    #// If the menu exists, get its items.
    if is_nav_menu(menu_):
        menu_items_ = wp_get_nav_menu_items(menu_.term_id, Array({"post_status": "any"}))
        result_ = "<div id=\"menu-instructions\" class=\"post-body-plain"
        result_ += " menu-instructions-inactive\">" if (not php_empty(lambda : menu_items_)) else "\">"
        result_ += "<p>" + __("Add menu items from the column on the left.") + "</p>"
        result_ += "</div>"
        if php_empty(lambda : menu_items_):
            return result_ + " <ul class=\"menu\" id=\"menu-to-edit\"> </ul>"
        # end if
        #// 
        #// Filters the Walker class used when adding nav menu items.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $class   The walker class to use. Default 'Walker_Nav_Menu_Edit'.
        #// @param int    $menu_id ID of the menu being rendered.
        #//
        walker_class_name_ = apply_filters("wp_edit_nav_menu_walker", "Walker_Nav_Menu_Edit", menu_id_)
        if php_class_exists(walker_class_name_):
            walker_ = php_new_class(walker_class_name_, lambda : {**locals(), **globals()}[walker_class_name_]())
        else:
            return php_new_class("WP_Error", lambda : WP_Error("menu_walker_not_exist", php_sprintf(__("The Walker class named %s does not exist."), "<strong>" + walker_class_name_ + "</strong>")))
        # end if
        some_pending_menu_items_ = False
        some_invalid_menu_items_ = False
        for menu_item_ in menu_items_:
            if (php_isset(lambda : menu_item_.post_status)) and "draft" == menu_item_.post_status:
                some_pending_menu_items_ = True
            # end if
            if (not php_empty(lambda : menu_item_._invalid)):
                some_invalid_menu_items_ = True
            # end if
        # end for
        if some_pending_menu_items_:
            result_ += "<div class=\"notice notice-info notice-alt inline\"><p>" + __("Click Save Menu to make pending menu items public.") + "</p></div>"
        # end if
        if some_invalid_menu_items_:
            result_ += "<div class=\"notice notice-error notice-alt inline\"><p>" + __("There are some invalid menu items. Please check or delete them.") + "</p></div>"
        # end if
        result_ += "<ul class=\"menu\" id=\"menu-to-edit\"> "
        result_ += walk_nav_menu_tree(php_array_map("wp_setup_nav_menu_item", menu_items_), 0, Array({"walker": walker_}))
        result_ += " </ul> "
        return result_
    elif is_wp_error(menu_):
        return menu_
    # end if
# end def wp_get_nav_menu_to_edit
#// 
#// Returns the columns for the nav menus page.
#// 
#// @since 3.0.0
#// 
#// @return string[] Array of column titles keyed by their column name.
#//
def wp_nav_menu_manage_columns(*_args_):
    
    
    return Array({"_title": __("Show advanced menu properties"), "cb": "<input type=\"checkbox\" />", "link-target": __("Link Target"), "title-attribute": __("Title Attribute"), "css-classes": __("CSS Classes"), "xfn": __("Link Relationship (XFN)"), "description": __("Description")})
# end def wp_nav_menu_manage_columns
#// 
#// Deletes orphaned draft menu items
#// 
#// @access private
#// @since 3.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def _wp_delete_orphaned_draft_menu_items(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    delete_timestamp_ = time() - DAY_IN_SECONDS * EMPTY_TRASH_DAYS
    #// Delete orphaned draft menu items.
    menu_items_to_delete_ = wpdb_.get_col(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" AS p LEFT JOIN ") + str(wpdb_.postmeta) + str(" AS m ON p.ID = m.post_id WHERE post_type = 'nav_menu_item' AND post_status = 'draft' AND meta_key = '_menu_item_orphaned' AND meta_value < %d"), delete_timestamp_))
    for menu_item_id_ in menu_items_to_delete_:
        wp_delete_post(menu_item_id_, True)
    # end for
# end def _wp_delete_orphaned_draft_menu_items
#// 
#// Saves nav menu items
#// 
#// @since 3.6.0
#// 
#// @param int|string $nav_menu_selected_id (id, slug, or name ) of the currently-selected menu
#// @param string $nav_menu_selected_title Title of the currently-selected menu
#// @return array The menu updated message
#//
def wp_nav_menu_update_menu_items(nav_menu_selected_id_=None, nav_menu_selected_title_=None, *_args_):
    
    
    unsorted_menu_items_ = wp_get_nav_menu_items(nav_menu_selected_id_, Array({"orderby": "ID", "output": ARRAY_A, "output_key": "ID", "post_status": "draft,publish"}))
    messages_ = Array()
    menu_items_ = Array()
    #// Index menu items by DB ID.
    for _item_ in unsorted_menu_items_:
        menu_items_[_item_.db_id] = _item_
    # end for
    post_fields_ = Array("menu-item-db-id", "menu-item-object-id", "menu-item-object", "menu-item-parent-id", "menu-item-position", "menu-item-type", "menu-item-title", "menu-item-url", "menu-item-description", "menu-item-attr-title", "menu-item-target", "menu-item-classes", "menu-item-xfn")
    wp_defer_term_counting(True)
    #// Loop through all the menu items' POST variables.
    if (not php_empty(lambda : PHP_POST["menu-item-db-id"])):
        for _key_,k_ in PHP_POST["menu-item-db-id"].items():
            #// Menu item title can't be blank.
            if (not (php_isset(lambda : PHP_POST["menu-item-title"][_key_]))) or "" == PHP_POST["menu-item-title"][_key_]:
                continue
            # end if
            args_ = Array()
            for field_ in post_fields_:
                args_[field_] = PHP_POST[field_][_key_] if (php_isset(lambda : PHP_POST[field_][_key_])) else ""
            # end for
            menu_item_db_id_ = wp_update_nav_menu_item(nav_menu_selected_id_, 0 if PHP_POST["menu-item-db-id"][_key_] != _key_ else _key_, args_)
            if is_wp_error(menu_item_db_id_):
                messages_[-1] = "<div id=\"message\" class=\"error\"><p>" + menu_item_db_id_.get_error_message() + "</p></div>"
            else:
                menu_items_[menu_item_db_id_] = None
            # end if
        # end for
    # end if
    #// Remove menu items from the menu that weren't in $_POST.
    if (not php_empty(lambda : menu_items_)):
        for menu_item_id_ in php_array_keys(menu_items_):
            if is_nav_menu_item(menu_item_id_):
                wp_delete_post(menu_item_id_)
            # end if
        # end for
    # end if
    #// Store 'auto-add' pages.
    auto_add_ = (not php_empty(lambda : PHP_POST["auto-add-pages"]))
    nav_menu_option_ = get_option("nav_menu_options")
    if (not (php_isset(lambda : nav_menu_option_["auto_add"]))):
        nav_menu_option_["auto_add"] = Array()
    # end if
    if auto_add_:
        if (not php_in_array(nav_menu_selected_id_, nav_menu_option_["auto_add"])):
            nav_menu_option_["auto_add"][-1] = nav_menu_selected_id_
        # end if
    else:
        key_ = php_array_search(nav_menu_selected_id_, nav_menu_option_["auto_add"])
        if False != key_:
            nav_menu_option_["auto_add"][key_] = None
        # end if
    # end if
    #// Remove non-existent/deleted menus.
    nav_menu_option_["auto_add"] = php_array_intersect(nav_menu_option_["auto_add"], wp_get_nav_menus(Array({"fields": "ids"})))
    update_option("nav_menu_options", nav_menu_option_)
    wp_defer_term_counting(False)
    #// This action is documented in wp-includes/nav-menu.php
    do_action("wp_update_nav_menu", nav_menu_selected_id_)
    messages_[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + php_sprintf(__("%s has been updated."), "<strong>" + nav_menu_selected_title_ + "</strong>") + "</p></div>"
    menu_items_ = None
    unsorted_menu_items_ = None
    return messages_
# end def wp_nav_menu_update_menu_items
#// 
#// If a JSON blob of navigation menu data is in POST data, expand it and inject
#// it into `$_POST` to avoid PHP `max_input_vars` limitations. See #14134.
#// 
#// @ignore
#// @since 4.5.3
#// @access private
#//
def _wp_expand_nav_menu_post_data(*_args_):
    
    global PHP_POST
    if (not (php_isset(lambda : PHP_POST["nav-menu-data"]))):
        return
    # end if
    data_ = php_json_decode(stripslashes(PHP_POST["nav-menu-data"]))
    if (not php_is_null(data_)) and data_:
        for post_input_data_ in data_:
            #// For input names that are arrays (e.g. `menu-item-db-id[3][4][5]`),
            #// derive the array path keys via regex and set the value in $_POST.
            php_preg_match("#([^\\[]*)(\\[(.+)\\])?#", post_input_data_.name, matches_)
            array_bits_ = Array(matches_[1])
            if (php_isset(lambda : matches_[3])):
                array_bits_ = php_array_merge(array_bits_, php_explode("][", matches_[3]))
            # end if
            new_post_data_ = Array()
            #// Build the new array value from leaf to trunk.
            i_ = php_count(array_bits_) - 1
            while i_ >= 0:
                
                if php_count(array_bits_) - 1 == i_:
                    new_post_data_[array_bits_[i_]] = wp_slash(post_input_data_.value)
                else:
                    new_post_data_ = Array({array_bits_[i_]: new_post_data_})
                # end if
                i_ -= 1
            # end while
            PHP_POST = array_replace_recursive(PHP_POST, new_post_data_)
        # end for
    # end if
# end def _wp_expand_nav_menu_post_data
