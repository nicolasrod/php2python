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
#// WordPress Customize Nav Menus classes
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.3.0
#// 
#// 
#// Customize Nav Menus class.
#// 
#// Implements menu management in the Customizer.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Manager
#//
class WP_Customize_Nav_Menus():
    manager = Array()
    original_nav_menu_locations = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #//
    def __init__(self, manager=None):
        
        self.manager = manager
        self.original_nav_menu_locations = get_nav_menu_locations()
        #// See https://github.com/xwp/wp-customize-snapshots/blob/962586659688a5b1fd9ae93618b7ce2d4e7a421c/php/class-customize-snapshot-manager.php#L469-L499
        add_action("customize_register", Array(self, "customize_register"), 11)
        add_filter("customize_dynamic_setting_args", Array(self, "filter_dynamic_setting_args"), 10, 2)
        add_filter("customize_dynamic_setting_class", Array(self, "filter_dynamic_setting_class"), 10, 3)
        add_action("customize_save_nav_menus_created_posts", Array(self, "save_nav_menus_created_posts"))
        #// Skip remaining hooks when the user can't manage nav menus anyway.
        if (not current_user_can("edit_theme_options")):
            return
        # end if
        add_filter("customize_refresh_nonces", Array(self, "filter_nonces"))
        add_action("wp_ajax_load-available-menu-items-customizer", Array(self, "ajax_load_available_items"))
        add_action("wp_ajax_search-available-menu-items-customizer", Array(self, "ajax_search_available_items"))
        add_action("wp_ajax_customize-nav-menus-insert-auto-draft", Array(self, "ajax_insert_auto_draft_post"))
        add_action("customize_controls_enqueue_scripts", Array(self, "enqueue_scripts"))
        add_action("customize_controls_print_footer_scripts", Array(self, "print_templates"))
        add_action("customize_controls_print_footer_scripts", Array(self, "available_items_template"))
        add_action("customize_preview_init", Array(self, "customize_preview_init"))
        add_action("customize_preview_init", Array(self, "make_auto_draft_status_previewable"))
        #// Selective Refresh partials.
        add_filter("customize_dynamic_partial_args", Array(self, "customize_dynamic_partial_args"), 10, 2)
    # end def __init__
    #// 
    #// Adds a nonce for customizing menus.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string[] $nonces Array of nonces.
    #// @return string[] $nonces Modified array of nonces.
    #//
    def filter_nonces(self, nonces=None):
        
        nonces["customize-menus"] = wp_create_nonce("customize-menus")
        return nonces
    # end def filter_nonces
    #// 
    #// Ajax handler for loading available menu items.
    #// 
    #// @since 4.3.0
    #//
    def ajax_load_available_items(self):
        
        check_ajax_referer("customize-menus", "customize-menus-nonce")
        if (not current_user_can("edit_theme_options")):
            wp_die(-1)
        # end if
        all_items = Array()
        item_types = Array()
        if (php_isset(lambda : PHP_POST["item_types"])) and php_is_array(PHP_POST["item_types"]):
            item_types = wp_unslash(PHP_POST["item_types"])
        elif (php_isset(lambda : PHP_POST["type"])) and (php_isset(lambda : PHP_POST["object"])):
            #// Back compat.
            item_types[-1] = Array({"type": wp_unslash(PHP_POST["type"]), "object": wp_unslash(PHP_POST["object"]), "page": 0 if php_empty(lambda : PHP_POST["page"]) else absint(PHP_POST["page"])})
        else:
            wp_send_json_error("nav_menus_missing_type_or_object_parameter")
        # end if
        for item_type in item_types:
            if php_empty(lambda : item_type["type"]) or php_empty(lambda : item_type["object"]):
                wp_send_json_error("nav_menus_missing_type_or_object_parameter")
            # end if
            type = sanitize_key(item_type["type"])
            object = sanitize_key(item_type["object"])
            page = 0 if php_empty(lambda : item_type["page"]) else absint(item_type["page"])
            items = self.load_available_items_query(type, object, page)
            if is_wp_error(items):
                wp_send_json_error(items.get_error_code())
            # end if
            all_items[item_type["type"] + ":" + item_type["object"]] = items
        # end for
        wp_send_json_success(Array({"items": all_items}))
    # end def ajax_load_available_items
    #// 
    #// Performs the post_type and taxonomy queries for loading available menu items.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string $type   Optional. Accepts any custom object type and has built-in support for
    #// 'post_type' and 'taxonomy'. Default is 'post_type'.
    #// @param string $object Optional. Accepts any registered taxonomy or post type name. Default is 'page'.
    #// @param int    $page   Optional. The page number used to generate the query offset. Default is '0'.
    #// @return array|WP_Error An array of menu items on success, a WP_Error object on failure.
    #//
    def load_available_items_query(self, type="post_type", object="page", page=0):
        
        items = Array()
        if "post_type" == type:
            post_type = get_post_type_object(object)
            if (not post_type):
                return php_new_class("WP_Error", lambda : WP_Error("nav_menus_invalid_post_type"))
            # end if
            if 0 == page and "page" == object:
                #// Add "Home" link. Treat as a page, but switch to custom on add.
                items[-1] = Array({"id": "home", "title": _x("Home", "nav menu home label"), "type": "custom", "type_label": __("Custom Link"), "object": "", "url": home_url()})
            elif "post" != object and 0 == page and post_type.has_archive:
                #// Add a post type archive link.
                items[-1] = Array({"id": object + "-archive", "title": post_type.labels.archives, "type": "post_type_archive", "type_label": __("Post Type Archive"), "object": object, "url": get_post_type_archive_link(object)})
            # end if
            #// Prepend posts with nav_menus_created_posts on first page.
            posts = Array()
            if 0 == page and self.manager.get_setting("nav_menus_created_posts"):
                for post_id in self.manager.get_setting("nav_menus_created_posts").value():
                    auto_draft_post = get_post(post_id)
                    if post_type.name == auto_draft_post.post_type:
                        posts[-1] = auto_draft_post
                    # end if
                # end for
            # end if
            posts = php_array_merge(posts, get_posts(Array({"numberposts": 10, "offset": 10 * page, "orderby": "date", "order": "DESC", "post_type": object})))
            for post in posts:
                post_title = post.post_title
                if "" == post_title:
                    #// translators: %d: ID of a post.
                    post_title = php_sprintf(__("#%d (no title)"), post.ID)
                # end if
                items[-1] = Array({"id": str("post-") + str(post.ID), "title": html_entity_decode(post_title, ENT_QUOTES, get_bloginfo("charset")), "type": "post_type", "type_label": get_post_type_object(post.post_type).labels.singular_name, "object": post.post_type, "object_id": php_intval(post.ID), "url": get_permalink(php_intval(post.ID))})
            # end for
        elif "taxonomy" == type:
            terms = get_terms(Array({"taxonomy": object, "child_of": 0, "exclude": "", "hide_empty": False, "hierarchical": 1, "include": "", "number": 10, "offset": 10 * page, "order": "DESC", "orderby": "count", "pad_counts": False}))
            if is_wp_error(terms):
                return terms
            # end if
            for term in terms:
                items[-1] = Array({"id": str("term-") + str(term.term_id), "title": html_entity_decode(term.name, ENT_QUOTES, get_bloginfo("charset")), "type": "taxonomy", "type_label": get_taxonomy(term.taxonomy).labels.singular_name, "object": term.taxonomy, "object_id": php_intval(term.term_id), "url": get_term_link(php_intval(term.term_id), term.taxonomy)})
            # end for
        # end if
        #// 
        #// Filters the available menu items.
        #// 
        #// @since 4.3.0
        #// 
        #// @param array  $items  The array of menu items.
        #// @param string $type   The object type.
        #// @param string $object The object name.
        #// @param int    $page   The current page number.
        #//
        items = apply_filters("customize_nav_menu_available_items", items, type, object, page)
        return items
    # end def load_available_items_query
    #// 
    #// Ajax handler for searching available menu items.
    #// 
    #// @since 4.3.0
    #//
    def ajax_search_available_items(self):
        
        check_ajax_referer("customize-menus", "customize-menus-nonce")
        if (not current_user_can("edit_theme_options")):
            wp_die(-1)
        # end if
        if php_empty(lambda : PHP_POST["search"]):
            wp_send_json_error("nav_menus_missing_search_parameter")
        # end if
        p = absint(PHP_POST["page"]) if (php_isset(lambda : PHP_POST["page"])) else 0
        if p < 1:
            p = 1
        # end if
        s = sanitize_text_field(wp_unslash(PHP_POST["search"]))
        items = self.search_available_items_query(Array({"pagenum": p, "s": s}))
        if php_empty(lambda : items):
            wp_send_json_error(Array({"message": __("No results found.")}))
        else:
            wp_send_json_success(Array({"items": items}))
        # end if
    # end def ajax_search_available_items
    #// 
    #// Performs post queries for available-item searching.
    #// 
    #// Based on WP_Editor::wp_link_query().
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $args Optional. Accepts 'pagenum' and 's' (search) arguments.
    #// @return array Menu items.
    #//
    def search_available_items_query(self, args=Array()):
        
        items = Array()
        post_type_objects = get_post_types(Array({"show_in_nav_menus": True}), "objects")
        query = Array({"post_type": php_array_keys(post_type_objects), "suppress_filters": True, "update_post_term_cache": False, "update_post_meta_cache": False, "post_status": "publish", "posts_per_page": 20})
        args["pagenum"] = absint(args["pagenum"]) if (php_isset(lambda : args["pagenum"])) else 1
        query["offset"] = query["posts_per_page"] * args["pagenum"] - 1 if args["pagenum"] > 1 else 0
        if (php_isset(lambda : args["s"])):
            query["s"] = args["s"]
        # end if
        posts = Array()
        #// Prepend list of posts with nav_menus_created_posts search results on first page.
        nav_menus_created_posts_setting = self.manager.get_setting("nav_menus_created_posts")
        if 1 == args["pagenum"] and nav_menus_created_posts_setting and php_count(nav_menus_created_posts_setting.value()) > 0:
            stub_post_query = php_new_class("WP_Query", lambda : WP_Query(php_array_merge(query, Array({"post_status": "auto-draft", "post__in": nav_menus_created_posts_setting.value(), "posts_per_page": -1}))))
            posts = php_array_merge(posts, stub_post_query.posts)
        # end if
        #// Query posts.
        get_posts = php_new_class("WP_Query", lambda : WP_Query(query))
        posts = php_array_merge(posts, get_posts.posts)
        #// Create items for posts.
        for post in posts:
            post_title = post.post_title
            if "" == post_title:
                #// translators: %d: ID of a post.
                post_title = php_sprintf(__("#%d (no title)"), post.ID)
            # end if
            items[-1] = Array({"id": "post-" + post.ID, "title": html_entity_decode(post_title, ENT_QUOTES, get_bloginfo("charset")), "type": "post_type", "type_label": post_type_objects[post.post_type].labels.singular_name, "object": post.post_type, "object_id": php_intval(post.ID), "url": get_permalink(php_intval(post.ID))})
        # end for
        #// Query taxonomy terms.
        taxonomies = get_taxonomies(Array({"show_in_nav_menus": True}), "names")
        terms = get_terms(Array({"taxonomies": taxonomies, "name__like": args["s"], "number": 20, "offset": 20 * args["pagenum"] - 1}))
        #// Check if any taxonomies were found.
        if (not php_empty(lambda : terms)):
            for term in terms:
                items[-1] = Array({"id": "term-" + term.term_id, "title": html_entity_decode(term.name, ENT_QUOTES, get_bloginfo("charset")), "type": "taxonomy", "type_label": get_taxonomy(term.taxonomy).labels.singular_name, "object": term.taxonomy, "object_id": php_intval(term.term_id), "url": get_term_link(php_intval(term.term_id), term.taxonomy)})
            # end for
        # end if
        #// Add "Home" link if search term matches. Treat as a page, but switch to custom on add.
        if (php_isset(lambda : args["s"])):
            title = _x("Home", "nav menu home label")
            matches = False != php_mb_stripos(title, args["s"]) if php_function_exists("mb_stripos") else False != php_stripos(title, args["s"])
            if matches:
                items[-1] = Array({"id": "home", "title": title, "type": "custom", "type_label": __("Custom Link"), "object": "", "url": home_url()})
            # end if
        # end if
        #// 
        #// Filters the available menu items during a search request.
        #// 
        #// @since 4.5.0
        #// 
        #// @param array $items The array of menu items.
        #// @param array $args  Includes 'pagenum' and 's' (search) arguments.
        #//
        items = apply_filters("customize_nav_menu_searched_items", items, args)
        return items
    # end def search_available_items_query
    #// 
    #// Enqueue scripts and styles for Customizer pane.
    #// 
    #// @since 4.3.0
    #//
    def enqueue_scripts(self):
        
        wp_enqueue_style("customize-nav-menus")
        wp_enqueue_script("customize-nav-menus")
        temp_nav_menu_setting = php_new_class("WP_Customize_Nav_Menu_Setting", lambda : WP_Customize_Nav_Menu_Setting(self.manager, "nav_menu[-1]"))
        temp_nav_menu_item_setting = php_new_class("WP_Customize_Nav_Menu_Item_Setting", lambda : WP_Customize_Nav_Menu_Item_Setting(self.manager, "nav_menu_item[-1]"))
        num_locations = php_count(get_registered_nav_menus())
        if 1 == num_locations:
            locations_description = __("Your theme can display menus in one location.")
        else:
            #// translators: %s: Number of menu locations.
            locations_description = php_sprintf(_n("Your theme can display menus in %s location.", "Your theme can display menus in %s locations.", num_locations), number_format_i18n(num_locations))
        # end if
        #// Pass data to JS.
        settings = Array({"allMenus": wp_get_nav_menus(), "itemTypes": self.available_item_types(), "l10n": Array({"untitled": _x("(no label)", "missing menu item navigation label"), "unnamed": _x("(unnamed)", "Missing menu name."), "custom_label": __("Custom Link"), "page_label": get_post_type_object("page").labels.singular_name, "menuLocation": _x("(Currently set to: %s)", "menu"), "locationsTitle": __("Menu Location") if 1 == num_locations else __("Menu Locations"), "locationsDescription": locations_description, "menuNameLabel": __("Menu Name"), "newMenuNameDescription": __("If your theme has multiple menus, giving them clear names will help you manage them."), "itemAdded": __("Menu item added"), "itemDeleted": __("Menu item deleted"), "menuAdded": __("Menu created"), "menuDeleted": __("Menu deleted"), "movedUp": __("Menu item moved up"), "movedDown": __("Menu item moved down"), "movedLeft": __("Menu item moved out of submenu"), "movedRight": __("Menu item is now a sub-item"), "customizingMenus": php_sprintf(__("Customizing &#9656; %s"), esc_html(self.manager.get_panel("nav_menus").title)), "invalidTitleTpl": __("%s (Invalid)"), "pendingTitleTpl": __("%s (Pending)"), "itemsFound": __("Number of items found: %d"), "itemsFoundMore": __("Additional items found: %d"), "itemsLoadingMore": __("Loading more results... please wait."), "reorderModeOn": __("Reorder mode enabled"), "reorderModeOff": __("Reorder mode closed"), "reorderLabelOn": esc_attr__("Reorder menu items"), "reorderLabelOff": esc_attr__("Close reorder mode")})}, {"settingTransport": "postMessage", "phpIntMax": PHP_INT_MAX, "defaultSettingValues": Array({"nav_menu": temp_nav_menu_setting.default, "nav_menu_item": temp_nav_menu_item_setting.default})}, {"locationSlugMappedToName": get_registered_nav_menus()})
        data = php_sprintf("var _wpCustomizeNavMenusSettings = %s;", wp_json_encode(settings))
        wp_scripts().add_data("customize-nav-menus", "data", data)
        #// This is copied from nav-menus.php, and it has an unfortunate object name of `menus`.
        nav_menus_l10n = Array({"oneThemeLocationNoMenus": None, "moveUp": __("Move up one"), "moveDown": __("Move down one"), "moveToTop": __("Move to the top"), "moveUnder": __("Move under %s"), "moveOutFrom": __("Move out from under %s"), "under": __("Under %s"), "outFrom": __("Out from under %s"), "menuFocus": __("%1$s. Menu item %2$d of %3$d."), "subMenuFocus": __("%1$s. Sub item number %2$d under %3$s.")})
        wp_localize_script("nav-menu", "menus", nav_menus_l10n)
    # end def enqueue_scripts
    #// 
    #// Filters a dynamic setting's constructor args.
    #// 
    #// For a dynamic setting to be registered, this filter must be employed
    #// to override the default false value with an array of args to pass to
    #// the WP_Customize_Setting constructor.
    #// 
    #// @since 4.3.0
    #// 
    #// @param false|array $setting_args The arguments to the WP_Customize_Setting constructor.
    #// @param string      $setting_id   ID for dynamic setting, usually coming from `$_POST['customized']`.
    #// @return array|false
    #//
    def filter_dynamic_setting_args(self, setting_args=None, setting_id=None):
        
        if php_preg_match(WP_Customize_Nav_Menu_Setting.ID_PATTERN, setting_id):
            setting_args = Array({"type": WP_Customize_Nav_Menu_Setting.TYPE, "transport": "postMessage"})
        elif php_preg_match(WP_Customize_Nav_Menu_Item_Setting.ID_PATTERN, setting_id):
            setting_args = Array({"type": WP_Customize_Nav_Menu_Item_Setting.TYPE, "transport": "postMessage"})
        # end if
        return setting_args
    # end def filter_dynamic_setting_args
    #// 
    #// Allow non-statically created settings to be constructed with custom WP_Customize_Setting subclass.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string $setting_class WP_Customize_Setting or a subclass.
    #// @param string $setting_id    ID for dynamic setting, usually coming from `$_POST['customized']`.
    #// @param array  $setting_args  WP_Customize_Setting or a subclass.
    #// @return string
    #//
    def filter_dynamic_setting_class(self, setting_class=None, setting_id=None, setting_args=None):
        
        setting_id = None
        if (not php_empty(lambda : setting_args["type"])) and WP_Customize_Nav_Menu_Setting.TYPE == setting_args["type"]:
            setting_class = "WP_Customize_Nav_Menu_Setting"
        elif (not php_empty(lambda : setting_args["type"])) and WP_Customize_Nav_Menu_Item_Setting.TYPE == setting_args["type"]:
            setting_class = "WP_Customize_Nav_Menu_Item_Setting"
        # end if
        return setting_class
    # end def filter_dynamic_setting_class
    #// 
    #// Add the customizer settings and controls.
    #// 
    #// @since 4.3.0
    #//
    def customize_register(self):
        
        changeset = self.manager.unsanitized_post_values()
        #// Preview settings for nav menus early so that the sections and controls will be added properly.
        nav_menus_setting_ids = Array()
        for setting_id in php_array_keys(changeset):
            if php_preg_match("/^(nav_menu_locations|nav_menu|nav_menu_item)\\[/", setting_id):
                nav_menus_setting_ids[-1] = setting_id
            # end if
        # end for
        settings = self.manager.add_dynamic_settings(nav_menus_setting_ids)
        if self.manager.settings_previewed():
            for setting in settings:
                setting.preview()
            # end for
        # end if
        #// Require JS-rendered control types.
        self.manager.register_panel_type("WP_Customize_Nav_Menus_Panel")
        self.manager.register_control_type("WP_Customize_Nav_Menu_Control")
        self.manager.register_control_type("WP_Customize_Nav_Menu_Name_Control")
        self.manager.register_control_type("WP_Customize_Nav_Menu_Locations_Control")
        self.manager.register_control_type("WP_Customize_Nav_Menu_Auto_Add_Control")
        self.manager.register_control_type("WP_Customize_Nav_Menu_Item_Control")
        #// Create a panel for Menus.
        description = "<p>" + __("This panel is used for managing navigation menus for content you have already published on your site. You can create menus and add items for existing content such as pages, posts, categories, tags, formats, or custom links.") + "</p>"
        if current_theme_supports("widgets"):
            description += "<p>" + php_sprintf(__("Menus can be displayed in locations defined by your theme or in <a href=\"%s\">widget areas</a> by adding a &#8220;Navigation Menu&#8221; widget."), "javascript:wp.customize.panel( 'widgets' ).focus();") + "</p>"
        else:
            description += "<p>" + __("Menus can be displayed in locations defined by your theme.") + "</p>"
        # end if
        #// 
        #// Once multiple theme supports are allowed in WP_Customize_Panel,
        #// this panel can be restricted to themes that support menus or widgets.
        #//
        self.manager.add_panel(php_new_class("WP_Customize_Nav_Menus_Panel", lambda : WP_Customize_Nav_Menus_Panel(self.manager, "nav_menus", Array({"title": __("Menus"), "description": description, "priority": 100}))))
        menus = wp_get_nav_menus()
        #// Menu locations.
        locations = get_registered_nav_menus()
        num_locations = php_count(locations)
        if 1 == num_locations:
            description = "<p>" + __("Your theme can display menus in one location. Select which menu you would like to use.") + "</p>"
        else:
            #// translators: %s: Number of menu locations.
            description = "<p>" + php_sprintf(_n("Your theme can display menus in %s location. Select which menu you would like to use.", "Your theme can display menus in %s locations. Select which menu appears in each location.", num_locations), number_format_i18n(num_locations)) + "</p>"
        # end if
        if current_theme_supports("widgets"):
            #// translators: URL to the Widgets panel of the Customizer.
            description += "<p>" + php_sprintf(__("If your theme has widget areas, you can also add menus there. Visit the <a href=\"%s\">Widgets panel</a> and add a &#8220;Navigation Menu widget&#8221; to display a menu in a sidebar or footer."), "javascript:wp.customize.panel( 'widgets' ).focus();") + "</p>"
        # end if
        self.manager.add_section("menu_locations", Array({"title": _x("View Location", "menu locations") if 1 == num_locations else _x("View All Locations", "menu locations"), "panel": "nav_menus", "priority": 30, "description": description}))
        choices = Array({"0": __("&mdash; Select &mdash;")})
        for menu in menus:
            choices[menu.term_id] = wp_html_excerpt(menu.name, 40, "&hellip;")
        # end for
        #// Attempt to re-map the nav menu location assignments when previewing a theme switch.
        mapped_nav_menu_locations = Array()
        if (not self.manager.is_theme_active()):
            theme_mods = get_option("theme_mods_" + self.manager.get_stylesheet(), Array())
            #// If there is no data from a previous activation, start fresh.
            if php_empty(lambda : theme_mods["nav_menu_locations"]):
                theme_mods["nav_menu_locations"] = Array()
            # end if
            mapped_nav_menu_locations = wp_map_nav_menu_locations(theme_mods["nav_menu_locations"], self.original_nav_menu_locations)
        # end if
        for location,description in locations:
            setting_id = str("nav_menu_locations[") + str(location) + str("]")
            setting = self.manager.get_setting(setting_id)
            if setting:
                setting.transport = "postMessage"
                remove_filter(str("customize_sanitize_") + str(setting_id), "absint")
                add_filter(str("customize_sanitize_") + str(setting_id), Array(self, "intval_base10"))
            else:
                self.manager.add_setting(setting_id, Array({"sanitize_callback": Array(self, "intval_base10"), "theme_supports": "menus", "type": "theme_mod", "transport": "postMessage", "default": 0}))
            # end if
            #// Override the assigned nav menu location if mapped during previewed theme switch.
            if php_empty(lambda : changeset[setting_id]) and (php_isset(lambda : mapped_nav_menu_locations[location])):
                self.manager.set_post_value(setting_id, mapped_nav_menu_locations[location])
            # end if
            self.manager.add_control(php_new_class("WP_Customize_Nav_Menu_Location_Control", lambda : WP_Customize_Nav_Menu_Location_Control(self.manager, setting_id, Array({"label": description, "location_id": location, "section": "menu_locations", "choices": choices}))))
        # end for
        #// Register each menu as a Customizer section, and add each menu item to each menu.
        for menu in menus:
            menu_id = menu.term_id
            #// Create a section for each menu.
            section_id = "nav_menu[" + menu_id + "]"
            self.manager.add_section(php_new_class("WP_Customize_Nav_Menu_Section", lambda : WP_Customize_Nav_Menu_Section(self.manager, section_id, Array({"title": html_entity_decode(menu.name, ENT_QUOTES, get_bloginfo("charset")), "priority": 10, "panel": "nav_menus"}))))
            nav_menu_setting_id = "nav_menu[" + menu_id + "]"
            self.manager.add_setting(php_new_class("WP_Customize_Nav_Menu_Setting", lambda : WP_Customize_Nav_Menu_Setting(self.manager, nav_menu_setting_id, Array({"transport": "postMessage"}))))
            #// Add the menu contents.
            menu_items = wp_get_nav_menu_items(menu_id)
            for i,item in php_array_values(menu_items):
                #// Create a setting for each menu item (which doesn't actually manage data, currently).
                menu_item_setting_id = "nav_menu_item[" + item.ID + "]"
                value = item
                if php_empty(lambda : value["post_title"]):
                    value["title"] = ""
                # end if
                value["nav_menu_term_id"] = menu_id
                self.manager.add_setting(php_new_class("WP_Customize_Nav_Menu_Item_Setting", lambda : WP_Customize_Nav_Menu_Item_Setting(self.manager, menu_item_setting_id, Array({"value": value, "transport": "postMessage"}))))
                #// Create a control for each menu item.
                self.manager.add_control(php_new_class("WP_Customize_Nav_Menu_Item_Control", lambda : WP_Customize_Nav_Menu_Item_Control(self.manager, menu_item_setting_id, Array({"label": item.title, "section": section_id, "priority": 10 + i}))))
            # end for
            pass
        # end for
        #// Add the add-new-menu section and controls.
        self.manager.add_section("add_menu", Array({"type": "new_menu", "title": __("New Menu"), "panel": "nav_menus", "priority": 20}))
        self.manager.add_setting(php_new_class("WP_Customize_Filter_Setting", lambda : WP_Customize_Filter_Setting(self.manager, "nav_menus_created_posts", Array({"transport": "postMessage", "type": "option", "default": Array(), "sanitize_callback": Array(self, "sanitize_nav_menus_created_posts")}))))
    # end def customize_register
    #// 
    #// Get the base10 intval.
    #// 
    #// This is used as a setting's sanitize_callback; we can't use just plain
    #// intval because the second argument is not what intval() expects.
    #// 
    #// @since 4.3.0
    #// 
    #// @param mixed $value Number to convert.
    #// @return int Integer.
    #//
    def intval_base10(self, value=None):
        
        return php_intval(value, 10)
    # end def intval_base10
    #// 
    #// Return an array of all the available item types.
    #// 
    #// @since 4.3.0
    #// @since 4.7.0  Each array item now includes a `$type_label` in addition to `$title`, `$type`, and `$object`.
    #// 
    #// @return array The available menu item types.
    #//
    def available_item_types(self):
        
        item_types = Array()
        post_types = get_post_types(Array({"show_in_nav_menus": True}), "objects")
        if post_types:
            for slug,post_type in post_types:
                item_types[-1] = Array({"title": post_type.labels.name, "type_label": post_type.labels.singular_name, "type": "post_type", "object": post_type.name})
            # end for
        # end if
        taxonomies = get_taxonomies(Array({"show_in_nav_menus": True}), "objects")
        if taxonomies:
            for slug,taxonomy in taxonomies:
                if "post_format" == taxonomy and (not current_theme_supports("post-formats")):
                    continue
                # end if
                item_types[-1] = Array({"title": taxonomy.labels.name, "type_label": taxonomy.labels.singular_name, "type": "taxonomy", "object": taxonomy.name})
            # end for
        # end if
        #// 
        #// Filters the available menu item types.
        #// 
        #// @since 4.3.0
        #// @since 4.7.0  Each array item now includes a `$type_label` in addition to `$title`, `$type`, and `$object`.
        #// 
        #// @param array $item_types Navigation menu item types.
        #//
        item_types = apply_filters("customize_nav_menu_available_item_types", item_types)
        return item_types
    # end def available_item_types
    #// 
    #// Add a new `auto-draft` post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $postarr {
    #// Post array. Note that post_status is overridden to be `auto-draft`.
    #// 
    #// @var string $post_title   Post title. Required.
    #// @var string $post_type    Post type. Required.
    #// @var string $post_name    Post name.
    #// @var string $post_content Post content.
    #// }
    #// @return WP_Post|WP_Error Inserted auto-draft post object or error.
    #//
    def insert_auto_draft_post(self, postarr=None):
        
        if (not (php_isset(lambda : postarr["post_type"]))):
            return php_new_class("WP_Error", lambda : WP_Error("unknown_post_type", __("Invalid post type.")))
        # end if
        if php_empty(lambda : postarr["post_title"]):
            return php_new_class("WP_Error", lambda : WP_Error("empty_title", __("Empty title.")))
        # end if
        if (not php_empty(lambda : postarr["post_status"])):
            return php_new_class("WP_Error", lambda : WP_Error("status_forbidden", __("Status is forbidden.")))
        # end if
        #// 
        #// If the changeset is a draft, this will change to draft the next time the changeset
        #// is updated; otherwise, auto-draft will persist in autosave revisions, until save.
        #//
        postarr["post_status"] = "auto-draft"
        #// Auto-drafts are allowed to have empty post_names, so it has to be explicitly set.
        if php_empty(lambda : postarr["post_name"]):
            postarr["post_name"] = sanitize_title(postarr["post_title"])
        # end if
        if (not (php_isset(lambda : postarr["meta_input"]))):
            postarr["meta_input"] = Array()
        # end if
        postarr["meta_input"]["_customize_draft_post_name"] = postarr["post_name"]
        postarr["meta_input"]["_customize_changeset_uuid"] = self.manager.changeset_uuid()
        postarr["post_name"] = None
        add_filter("wp_insert_post_empty_content", "__return_false", 1000)
        r = wp_insert_post(wp_slash(postarr), True)
        remove_filter("wp_insert_post_empty_content", "__return_false", 1000)
        if is_wp_error(r):
            return r
        else:
            return get_post(r)
        # end if
    # end def insert_auto_draft_post
    #// 
    #// Ajax handler for adding a new auto-draft post.
    #// 
    #// @since 4.7.0
    #//
    def ajax_insert_auto_draft_post(self):
        
        if (not check_ajax_referer("customize-menus", "customize-menus-nonce", False)):
            wp_send_json_error("bad_nonce", 400)
        # end if
        if (not current_user_can("customize")):
            wp_send_json_error("customize_not_allowed", 403)
        # end if
        if php_empty(lambda : PHP_POST["params"]) or (not php_is_array(PHP_POST["params"])):
            wp_send_json_error("missing_params", 400)
        # end if
        params = wp_unslash(PHP_POST["params"])
        illegal_params = php_array_diff(php_array_keys(params), Array("post_type", "post_title"))
        if (not php_empty(lambda : illegal_params)):
            wp_send_json_error("illegal_params", 400)
        # end if
        params = php_array_merge(Array({"post_type": "", "post_title": ""}), params)
        if php_empty(lambda : params["post_type"]) or (not post_type_exists(params["post_type"])):
            status_header(400)
            wp_send_json_error("missing_post_type_param")
        # end if
        post_type_object = get_post_type_object(params["post_type"])
        if (not current_user_can(post_type_object.cap.create_posts)) or (not current_user_can(post_type_object.cap.publish_posts)):
            status_header(403)
            wp_send_json_error("insufficient_post_permissions")
        # end if
        params["post_title"] = php_trim(params["post_title"])
        if "" == params["post_title"]:
            status_header(400)
            wp_send_json_error("missing_post_title")
        # end if
        r = self.insert_auto_draft_post(params)
        if is_wp_error(r):
            error = r
            if (not php_empty(lambda : post_type_object.labels.singular_name)):
                singular_name = post_type_object.labels.singular_name
            else:
                singular_name = __("Post")
            # end if
            data = Array({"message": php_sprintf(__("%1$s could not be created: %2$s"), singular_name, error.get_error_message())})
            wp_send_json_error(data)
        else:
            post = r
            data = Array({"post_id": post.ID, "url": get_permalink(post.ID)})
            wp_send_json_success(data)
        # end if
    # end def ajax_insert_auto_draft_post
    #// 
    #// Print the JavaScript templates used to render Menu Customizer components.
    #// 
    #// Templates are imported into the JS use wp.template.
    #// 
    #// @since 4.3.0
    #//
    def print_templates(self):
        
        php_print("""       <script type=\"text/html\" id=\"tmpl-available-menu-item\">
        <li id=\"menu-item-tpl-{{ data.id }}\" class=\"menu-item-tpl\" data-menu-item-id=\"{{ data.id }}\">
        <div class=\"menu-item-bar\">
        <div class=\"menu-item-handle\">
        <span class=\"item-type\" aria-hidden=\"true\">{{ data.type_label }}</span>
        <span class=\"item-title\" aria-hidden=\"true\">
        <span class=\"menu-item-title<# if ( ! data.title ) { #> no-title<# } #>\">{{ data.title || wp.customize.Menus.data.l10n.untitled }}</span>
        </span>
        <button type=\"button\" class=\"button-link item-add\">
        <span class=\"screen-reader-text\">
        """)
        #// translators: 1: Title of a menu item, 2: Type of a menu item.
        printf(__("Add to menu: %1$s (%2$s)"), "{{ data.title || wp.customize.Menus.data.l10n.untitled }}", "{{ data.type_label }}")
        php_print("""                           </span>
        </button>
        </div>
        </div>
        </li>
        </script>
        <script type=\"text/html\" id=\"tmpl-menu-item-reorder-nav\">
        <div class=\"menu-item-reorder-nav\">
        """)
        printf("<button type=\"button\" class=\"menus-move-up\">%1$s</button><button type=\"button\" class=\"menus-move-down\">%2$s</button><button type=\"button\" class=\"menus-move-left\">%3$s</button><button type=\"button\" class=\"menus-move-right\">%4$s</button>", __("Move up"), __("Move down"), __("Move one level up"), __("Move one level down"))
        php_print("""           </div>
        </script>
        <script type=\"text/html\" id=\"tmpl-nav-menu-delete-button\">
        <div class=\"menu-delete-item\">
        <button type=\"button\" class=\"button-link button-link-delete\">
        """)
        _e("Delete Menu")
        php_print("""               </button>
        </div>
        </script>
        <script type=\"text/html\" id=\"tmpl-nav-menu-submit-new-button\">
        <p id=\"customize-new-menu-submit-description\">""")
        _e("Click &#8220;Next&#8221; to start adding links to your new menu.")
        php_print("</p>\n           <button id=\"customize-new-menu-submit\" type=\"button\" class=\"button\" aria-describedby=\"customize-new-menu-submit-description\">")
        _e("Next")
        php_print("""</button>
        </script>
        <script type=\"text/html\" id=\"tmpl-nav-menu-locations-header\">
        <span class=\"customize-control-title customize-section-title-menu_locations-heading\">{{ data.l10n.locationsTitle }}</span>
        <p class=\"customize-control-description customize-section-title-menu_locations-description\">{{ data.l10n.locationsDescription }}</p>
        </script>
        <script type=\"text/html\" id=\"tmpl-nav-menu-create-menu-section-title\">
        <p class=\"add-new-menu-notice\">
        """)
        _e("It doesn&#8217;t look like your site has any menus yet. Want to build one? Click the button to start.")
        php_print("         </p>\n          <p class=\"add-new-menu-notice\">\n             ")
        _e("You&#8217;ll create a menu, assign it a location, and add menu items like links to pages and categories. If your theme has multiple menu areas, you might need to create more than one.")
        php_print("""           </p>
        <h3>
        <button type=\"button\" class=\"button customize-add-menu-button\">
        """)
        _e("Create New Menu")
        php_print("""               </button>
        </h3>
        </script>
        """)
    # end def print_templates
    #// 
    #// Print the html template used to render the add-menu-item frame.
    #// 
    #// @since 4.3.0
    #//
    def available_items_template(self):
        
        php_print("""       <div id=\"available-menu-items\" class=\"accordion-container\">
        <div class=\"customize-section-title\">
        <button type=\"button\" class=\"customize-section-back\" tabindex=\"-1\">
        <span class=\"screen-reader-text\">""")
        _e("Back")
        php_print("""</span>
        </button>
        <h3>
        <span class=\"customize-action\">
        """)
        #// translators: &#9656; is the unicode right-pointing triangle. %s: Section title in the Customizer.
        printf(__("Customizing &#9656; %s"), esc_html(self.manager.get_panel("nav_menus").title))
        php_print("                 </span>\n                   ")
        _e("Add Menu Items")
        php_print("""               </h3>
        </div>
        <div id=\"available-menu-items-search\" class=\"accordion-section cannot-expand\">
        <div class=\"accordion-section-title\">
        <label class=\"screen-reader-text\" for=\"menu-items-search\">""")
        _e("Search Menu Items")
        php_print("</label>\n                   <input type=\"text\" id=\"menu-items-search\" placeholder=\"")
        esc_attr_e("Search menu items&hellip;")
        php_print("\" aria-describedby=\"menu-items-search-desc\" />\n                  <p class=\"screen-reader-text\" id=\"menu-items-search-desc\">")
        _e("The search results will be updated as you type.")
        php_print("""</p>
        <span class=\"spinner\"></span>
        </div>
        <div class=\"search-icon\" aria-hidden=\"true\"></div>
        <button type=\"button\" class=\"clear-results\"><span class=\"screen-reader-text\">""")
        _e("Clear Results")
        php_print("""</span></button>
        <ul class=\"accordion-section-content available-menu-items-list\" data-type=\"search\"></ul>
        </div>
        """)
        #// Ensure the page post type comes first in the list.
        item_types = self.available_item_types()
        page_item_type = None
        for i,item_type in item_types:
            if (php_isset(lambda : item_type["object"])) and "page" == item_type["object"]:
                page_item_type = item_type
                item_types[i] = None
            # end if
        # end for
        self.print_custom_links_available_menu_item()
        if page_item_type:
            self.print_post_type_container(page_item_type)
        # end if
        #// Containers for per-post-type item browsing; items are added with JS.
        for item_type in item_types:
            self.print_post_type_container(item_type)
        # end for
        php_print("     </div><!-- #available-menu-items -->\n      ")
    # end def available_items_template
    #// 
    #// Print the markup for new menu items.
    #// 
    #// To be used in the template #available-menu-items.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $available_item_type Menu item data to output, including title, type, and label.
    #// @return void
    #//
    def print_post_type_container(self, available_item_type=None):
        
        id = php_sprintf("available-menu-items-%s-%s", available_item_type["type"], available_item_type["object"])
        php_print("     <div id=\"")
        php_print(esc_attr(id))
        php_print("\" class=\"accordion-section\">\n            <h4 class=\"accordion-section-title\" role=\"presentation\">\n              ")
        php_print(esc_html(available_item_type["title"]))
        php_print("             <span class=\"spinner\"></span>\n               <span class=\"no-items\">")
        _e("No items")
        php_print("""</span>
        <button type=\"button\" class=\"button-link\" aria-expanded=\"false\">
        <span class=\"screen-reader-text\">
        """)
        #// translators: %s: Title of a section with menu items.
        printf(__("Toggle section: %s"), esc_html(available_item_type["title"]))
        php_print("""                       </span>
        <span class=\"toggle-indicator\" aria-hidden=\"true\"></span>
        </button>
        </h4>
        <div class=\"accordion-section-content\">
        """)
        if "post_type" == available_item_type["type"]:
            php_print("                 ")
            post_type_obj = get_post_type_object(available_item_type["object"])
            php_print("                 ")
            if current_user_can(post_type_obj.cap.create_posts) and current_user_can(post_type_obj.cap.publish_posts):
                php_print("                     <div class=\"new-content-item\">\n                          <label for=\"")
                php_print(esc_attr("create-item-input-" + available_item_type["object"]))
                php_print("\" class=\"screen-reader-text\">")
                php_print(esc_html(post_type_obj.labels.add_new_item))
                php_print("</label>\n                           <input type=\"text\" id=\"")
                php_print(esc_attr("create-item-input-" + available_item_type["object"]))
                php_print("\" class=\"create-item-input\" placeholder=\"")
                php_print(esc_attr(post_type_obj.labels.add_new_item))
                php_print("\">\n                            <button type=\"button\" class=\"button add-content\">")
                _e("Add")
                php_print("</button>\n                      </div>\n                    ")
            # end if
            php_print("             ")
        # end if
        php_print("             <ul class=\"available-menu-items-list\" data-type=\"")
        php_print(esc_attr(available_item_type["type"]))
        php_print("\" data-object=\"")
        php_print(esc_attr(available_item_type["object"]))
        php_print("\" data-type_label=\"")
        php_print(esc_attr(available_item_type["type_label"] if (php_isset(lambda : available_item_type["type_label"])) else available_item_type["type"]))
        php_print("""\"></ul>
        </div>
        </div>
        """)
    # end def print_post_type_container
    #// 
    #// Print the markup for available menu item custom links.
    #// 
    #// @since 4.7.0
    #// 
    #// @return void
    #//
    def print_custom_links_available_menu_item(self):
        
        php_print("     <div id=\"new-custom-menu-item\" class=\"accordion-section\">\n         <h4 class=\"accordion-section-title\" role=\"presentation\">\n              ")
        _e("Custom Links")
        php_print("             <button type=\"button\" class=\"button-link\" aria-expanded=\"false\">\n                    <span class=\"screen-reader-text\">")
        _e("Toggle section: Custom Links")
        php_print("""</span>
        <span class=\"toggle-indicator\" aria-hidden=\"true\"></span>
        </button>
        </h4>
        <div class=\"accordion-section-content customlinkdiv\">
        <input type=\"hidden\" value=\"custom\" id=\"custom-menu-item-type\" name=\"menu-item[-1][menu-item-type]\" />
        <p id=\"menu-item-url-wrap\" class=\"wp-clearfix\">
        <label class=\"howto\" for=\"custom-menu-item-url\">""")
        _e("URL")
        php_print("""</label>
        <input id=\"custom-menu-item-url\" name=\"menu-item[-1][menu-item-url]\" type=\"text\" class=\"code menu-item-textbox\" placeholder=\"https://\">
        </p>
        <p id=\"menu-item-name-wrap\" class=\"wp-clearfix\">
        <label class=\"howto\" for=\"custom-menu-item-name\">""")
        _e("Link Text")
        php_print("""</label>
        <input id=\"custom-menu-item-name\" name=\"menu-item[-1][menu-item-title]\" type=\"text\" class=\"regular-text menu-item-textbox\">
        </p>
        <p class=\"button-controls\">
        <span class=\"add-to-menu\">
        <input type=\"submit\" class=\"button submit-add-to-menu right\" value=\"""")
        esc_attr_e("Add to Menu")
        php_print("""\" name=\"add-custom-menu-item\" id=\"custom-menu-item-submit\">
        <span class=\"spinner\"></span>
        </span>
        </p>
        </div>
        </div>
        """)
    # end def print_custom_links_available_menu_item
    preview_nav_menu_instance_args = Array()
    #// 
    #// Filters arguments for dynamic nav_menu selective refresh partials.
    #// 
    #// @since 4.5.0
    #// 
    #// @param array|false $partial_args Partial args.
    #// @param string      $partial_id   Partial ID.
    #// @return array Partial args.
    #//
    def customize_dynamic_partial_args(self, partial_args=None, partial_id=None):
        
        if php_preg_match("/^nav_menu_instance\\[[0-9a-f]{32}\\]$/", partial_id):
            if False == partial_args:
                partial_args = Array()
            # end if
            partial_args = php_array_merge(partial_args, Array({"type": "nav_menu_instance", "render_callback": Array(self, "render_nav_menu_partial"), "container_inclusive": True, "settings": Array(), "capability": "edit_theme_options"}))
        # end if
        return partial_args
    # end def customize_dynamic_partial_args
    #// 
    #// Add hooks for the Customizer preview.
    #// 
    #// @since 4.3.0
    #//
    def customize_preview_init(self):
        
        add_action("wp_enqueue_scripts", Array(self, "customize_preview_enqueue_deps"))
        add_filter("wp_nav_menu_args", Array(self, "filter_wp_nav_menu_args"), 1000)
        add_filter("wp_nav_menu", Array(self, "filter_wp_nav_menu"), 10, 2)
        add_filter("wp_footer", Array(self, "export_preview_data"), 1)
        add_filter("customize_render_partials_response", Array(self, "export_partial_rendered_nav_menu_instances"))
    # end def customize_preview_init
    #// 
    #// Make the auto-draft status protected so that it can be queried.
    #// 
    #// @since 4.7.0
    #// 
    #// @global array $wp_post_statuses List of post statuses.
    #//
    def make_auto_draft_status_previewable(self):
        
        global wp_post_statuses
        php_check_if_defined("wp_post_statuses")
        wp_post_statuses["auto-draft"].protected = True
    # end def make_auto_draft_status_previewable
    #// 
    #// Sanitize post IDs for posts created for nav menu items to be published.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $value Post IDs.
    #// @return array Post IDs.
    #//
    def sanitize_nav_menus_created_posts(self, value=None):
        
        post_ids = Array()
        for post_id in wp_parse_id_list(value):
            if php_empty(lambda : post_id):
                continue
            # end if
            post = get_post(post_id)
            if "auto-draft" != post.post_status and "draft" != post.post_status:
                continue
            # end if
            post_type_obj = get_post_type_object(post.post_type)
            if (not post_type_obj):
                continue
            # end if
            if (not current_user_can(post_type_obj.cap.publish_posts)) or (not current_user_can(post_type_obj.cap.edit_post, post_id)):
                continue
            # end if
            post_ids[-1] = post.ID
        # end for
        return post_ids
    # end def sanitize_nav_menus_created_posts
    #// 
    #// Publish the auto-draft posts that were created for nav menu items.
    #// 
    #// The post IDs will have been sanitized by already by
    #// `WP_Customize_Nav_Menu_Items::sanitize_nav_menus_created_posts()` to
    #// remove any post IDs for which the user cannot publish or for which the
    #// post is not an auto-draft.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Customize_Setting $setting Customizer setting object.
    #//
    def save_nav_menus_created_posts(self, setting=None):
        
        post_ids = setting.post_value()
        if (not php_empty(lambda : post_ids)):
            for post_id in post_ids:
                #// Prevent overriding the status that a user may have prematurely updated the post to.
                current_status = get_post_status(post_id)
                if "auto-draft" != current_status and "draft" != current_status:
                    continue
                # end if
                target_status = "inherit" if "attachment" == get_post_type(post_id) else "publish"
                args = Array({"ID": post_id, "post_status": target_status})
                post_name = get_post_meta(post_id, "_customize_draft_post_name", True)
                if post_name:
                    args["post_name"] = post_name
                # end if
                #// Note that wp_publish_post() cannot be used because unique slugs need to be assigned.
                wp_update_post(wp_slash(args))
                delete_post_meta(post_id, "_customize_draft_post_name")
            # end for
        # end if
    # end def save_nav_menus_created_posts
    #// 
    #// Keep track of the arguments that are being passed to wp_nav_menu().
    #// 
    #// @since 4.3.0
    #// @see wp_nav_menu()
    #// @see WP_Customize_Widgets::filter_dynamic_sidebar_params()
    #// 
    #// @param array $args An array containing wp_nav_menu() arguments.
    #// @return array Arguments.
    #//
    def filter_wp_nav_menu_args(self, args=None):
        
        #// 
        #// The following conditions determine whether or not this instance of
        #// wp_nav_menu() can use selective refreshed. A wp_nav_menu() can be
        #// selective refreshed if...
        #//
        can_partial_refresh = (not php_empty(lambda : args["echo"])) and php_empty(lambda : args["fallback_cb"]) or php_is_string(args["fallback_cb"]) and php_empty(lambda : args["walker"]) or php_is_string(args["walker"]) and (not php_empty(lambda : args["theme_location"])) or (not php_empty(lambda : args["menu"])) and php_is_numeric(args["menu"]) or php_is_object(args["menu"]) and (not php_empty(lambda : args["container"])) or (php_isset(lambda : args["items_wrap"])) and "<" == php_substr(args["items_wrap"], 0, 1)
        args["can_partial_refresh"] = can_partial_refresh
        exported_args = args
        #// Empty out args which may not be JSON-serializable.
        if (not can_partial_refresh):
            exported_args["fallback_cb"] = ""
            exported_args["walker"] = ""
        # end if
        #// 
        #// Replace object menu arg with a term_id menu arg, as this exports better
        #// to JS and is easier to compare hashes.
        #//
        if (not php_empty(lambda : exported_args["menu"])) and php_is_object(exported_args["menu"]):
            exported_args["menu"] = exported_args["menu"].term_id
        # end if
        ksort(exported_args)
        exported_args["args_hmac"] = self.hash_nav_menu_args(exported_args)
        args["customize_preview_nav_menus_args"] = exported_args
        self.preview_nav_menu_instance_args[exported_args["args_hmac"]] = exported_args
        return args
    # end def filter_wp_nav_menu_args
    #// 
    #// Prepares wp_nav_menu() calls for partial refresh.
    #// 
    #// Injects attributes into container element.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_nav_menu()
    #// 
    #// @param string $nav_menu_content The HTML content for the navigation menu.
    #// @param object $args             An object containing wp_nav_menu() arguments.
    #// @return string Nav menu HTML with selective refresh attributes added if partial can be refreshed.
    #//
    def filter_wp_nav_menu(self, nav_menu_content=None, args=None):
        
        if (php_isset(lambda : args.customize_preview_nav_menus_args["can_partial_refresh"])) and args.customize_preview_nav_menus_args["can_partial_refresh"]:
            attributes = php_sprintf(" data-customize-partial-id=\"%s\"", esc_attr("nav_menu_instance[" + args.customize_preview_nav_menus_args["args_hmac"] + "]"))
            attributes += " data-customize-partial-type=\"nav_menu_instance\""
            attributes += php_sprintf(" data-customize-partial-placement-context=\"%s\"", esc_attr(wp_json_encode(args.customize_preview_nav_menus_args)))
            nav_menu_content = php_preg_replace("#^(<\\w+)#", "$1 " + php_str_replace("\\", "\\\\", attributes), nav_menu_content, 1)
        # end if
        return nav_menu_content
    # end def filter_wp_nav_menu
    #// 
    #// Hashes (hmac) the nav menu arguments to ensure they are not tampered with when
    #// submitted in the Ajax request.
    #// 
    #// Note that the array is expected to be pre-sorted.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $args The arguments to hash.
    #// @return string Hashed nav menu arguments.
    #//
    def hash_nav_menu_args(self, args=None):
        
        return wp_hash(serialize(args))
    # end def hash_nav_menu_args
    #// 
    #// Enqueue scripts for the Customizer preview.
    #// 
    #// @since 4.3.0
    #//
    def customize_preview_enqueue_deps(self):
        
        wp_enqueue_script("customize-preview-nav-menus")
        pass
    # end def customize_preview_enqueue_deps
    #// 
    #// Exports data from PHP to JS.
    #// 
    #// @since 4.3.0
    #//
    def export_preview_data(self):
        
        #// Why not wp_localize_script? Because we're not localizing, and it forces values into strings.
        exports = Array({"navMenuInstanceArgs": self.preview_nav_menu_instance_args})
        printf("<script>var _wpCustomizePreviewNavMenusExports = %s;</script>", wp_json_encode(exports))
    # end def export_preview_data
    #// 
    #// Export any wp_nav_menu() calls during the rendering of any partials.
    #// 
    #// @since 4.5.0
    #// 
    #// @param array $response Response.
    #// @return array Response.
    #//
    def export_partial_rendered_nav_menu_instances(self, response=None):
        
        response["nav_menu_instance_args"] = self.preview_nav_menu_instance_args
        return response
    # end def export_partial_rendered_nav_menu_instances
    #// 
    #// Render a specific menu via wp_nav_menu() using the supplied arguments.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_nav_menu()
    #// 
    #// @param WP_Customize_Partial $partial       Partial.
    #// @param array                $nav_menu_args Nav menu args supplied as container context.
    #// @return string|false
    #//
    def render_nav_menu_partial(self, partial=None, nav_menu_args=None):
        
        partial = None
        if (not (php_isset(lambda : nav_menu_args["args_hmac"]))):
            #// Error: missing_args_hmac.
            return False
        # end if
        nav_menu_args_hmac = nav_menu_args["args_hmac"]
        nav_menu_args["args_hmac"] = None
        ksort(nav_menu_args)
        if (not hash_equals(self.hash_nav_menu_args(nav_menu_args), nav_menu_args_hmac)):
            #// Error: args_hmac_mismatch.
            return False
        # end if
        ob_start()
        wp_nav_menu(nav_menu_args)
        content = ob_get_clean()
        return content
    # end def render_nav_menu_partial
# end class WP_Customize_Nav_Menus
