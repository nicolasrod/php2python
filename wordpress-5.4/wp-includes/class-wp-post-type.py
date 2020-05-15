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
#// Post API: WP_Post_Type class
#// 
#// @package WordPress
#// @subpackage Post
#// @since 4.6.0
#// 
#// 
#// Core class used for interacting with post types.
#// 
#// @since 4.6.0
#// 
#// @see register_post_type()
#//
class WP_Post_Type():
    name = Array()
    label = Array()
    labels = Array()
    description = ""
    public = False
    hierarchical = False
    exclude_from_search = None
    publicly_queryable = None
    show_ui = None
    show_in_menu = None
    show_in_nav_menus = None
    show_in_admin_bar = None
    menu_position = None
    menu_icon = None
    capability_type = "post"
    map_meta_cap = False
    register_meta_box_cb = None
    taxonomies = Array()
    has_archive = False
    query_var = Array()
    can_export = True
    delete_with_user = None
    _builtin = False
    _edit_link = "post.php?post=%d"
    cap = Array()
    rewrite = Array()
    supports = Array()
    show_in_rest = Array()
    rest_base = Array()
    rest_controller_class = Array()
    rest_controller = Array()
    #// 
    #// Constructor.
    #// 
    #// Will populate object properties from the provided arguments and assign other
    #// default properties based on that information.
    #// 
    #// @since 4.6.0
    #// 
    #// @see register_post_type()
    #// 
    #// @param string       $post_type Post type key.
    #// @param array|string $args      Optional. Array or string of arguments for registering a post type.
    #// Default empty array.
    #//
    def __init__(self, post_type=None, args=Array()):
        
        self.name = post_type
        self.set_props(args)
    # end def __init__
    #// 
    #// Sets post type properties.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array|string $args Array or string of arguments for registering a post type.
    #//
    def set_props(self, args=None):
        
        args = wp_parse_args(args)
        #// 
        #// Filters the arguments for registering a post type.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array  $args      Array of arguments for registering a post type.
        #// @param string $post_type Post type key.
        #//
        args = apply_filters("register_post_type_args", args, self.name)
        has_edit_link = (not php_empty(lambda : args["_edit_link"]))
        #// Args prefixed with an underscore are reserved for internal use.
        defaults = Array({"labels": Array(), "description": "", "public": False, "hierarchical": False, "exclude_from_search": None, "publicly_queryable": None, "show_ui": None, "show_in_menu": None, "show_in_nav_menus": None, "show_in_admin_bar": None, "menu_position": None, "menu_icon": None, "capability_type": "post", "capabilities": Array(), "map_meta_cap": None, "supports": Array(), "register_meta_box_cb": None, "taxonomies": Array(), "has_archive": False, "rewrite": True, "query_var": True, "can_export": True, "delete_with_user": None, "show_in_rest": False, "rest_base": False, "rest_controller_class": False, "_builtin": False, "_edit_link": "post.php?post=%d"})
        args = php_array_merge(defaults, args)
        args["name"] = self.name
        #// If not set, default to the setting for 'public'.
        if None == args["publicly_queryable"]:
            args["publicly_queryable"] = args["public"]
        # end if
        #// If not set, default to the setting for 'public'.
        if None == args["show_ui"]:
            args["show_ui"] = args["public"]
        # end if
        #// If not set, default to the setting for 'show_ui'.
        if None == args["show_in_menu"] or (not args["show_ui"]):
            args["show_in_menu"] = args["show_ui"]
        # end if
        #// If not set, default to the setting for 'show_in_menu'.
        if None == args["show_in_admin_bar"]:
            args["show_in_admin_bar"] = bool(args["show_in_menu"])
        # end if
        #// If not set, default to the setting for 'public'.
        if None == args["show_in_nav_menus"]:
            args["show_in_nav_menus"] = args["public"]
        # end if
        #// If not set, default to true if not public, false if public.
        if None == args["exclude_from_search"]:
            args["exclude_from_search"] = (not args["public"])
        # end if
        #// Back compat with quirky handling in version 3.0. #14122.
        if php_empty(lambda : args["capabilities"]) and None == args["map_meta_cap"] and php_in_array(args["capability_type"], Array("post", "page")):
            args["map_meta_cap"] = True
        # end if
        #// If not set, default to false.
        if None == args["map_meta_cap"]:
            args["map_meta_cap"] = False
        # end if
        #// If there's no specified edit link and no UI, remove the edit link.
        if (not args["show_ui"]) and (not has_edit_link):
            args["_edit_link"] = ""
        # end if
        self.cap = get_post_type_capabilities(args)
        args["capabilities"] = None
        if php_is_array(args["capability_type"]):
            args["capability_type"] = args["capability_type"][0]
        # end if
        if False != args["query_var"]:
            if True == args["query_var"]:
                args["query_var"] = self.name
            else:
                args["query_var"] = sanitize_title_with_dashes(args["query_var"])
            # end if
        # end if
        if False != args["rewrite"] and is_admin() or "" != get_option("permalink_structure"):
            if (not php_is_array(args["rewrite"])):
                args["rewrite"] = Array()
            # end if
            if php_empty(lambda : args["rewrite"]["slug"]):
                args["rewrite"]["slug"] = self.name
            # end if
            if (not (php_isset(lambda : args["rewrite"]["with_front"]))):
                args["rewrite"]["with_front"] = True
            # end if
            if (not (php_isset(lambda : args["rewrite"]["pages"]))):
                args["rewrite"]["pages"] = True
            # end if
            if (not (php_isset(lambda : args["rewrite"]["feeds"]))) or (not args["has_archive"]):
                args["rewrite"]["feeds"] = bool(args["has_archive"])
            # end if
            if (not (php_isset(lambda : args["rewrite"]["ep_mask"]))):
                if (php_isset(lambda : args["permalink_epmask"])):
                    args["rewrite"]["ep_mask"] = args["permalink_epmask"]
                else:
                    args["rewrite"]["ep_mask"] = EP_PERMALINK
                # end if
            # end if
        # end if
        for property_name,property_value in args:
            self.property_name = property_value
        # end for
        self.labels = get_post_type_labels(self)
        self.label = self.labels.name
    # end def set_props
    #// 
    #// Sets the features support for the post type.
    #// 
    #// @since 4.6.0
    #//
    def add_supports(self):
        
        if (not php_empty(lambda : self.supports)):
            for feature,args in self.supports:
                if php_is_array(args):
                    add_post_type_support(self.name, feature, args)
                else:
                    add_post_type_support(self.name, args)
                # end if
            # end for
            self.supports = None
        elif False != self.supports:
            #// Add default features.
            add_post_type_support(self.name, Array("title", "editor"))
        # end if
    # end def add_supports
    #// 
    #// Adds the necessary rewrite rules for the post type.
    #// 
    #// @since 4.6.0
    #// 
    #// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
    #// @global WP         $wp         Current WordPress environment instance.
    #//
    def add_rewrite_rules(self):
        
        global wp_rewrite,wp
        php_check_if_defined("wp_rewrite","wp")
        if False != self.query_var and wp and is_post_type_viewable(self):
            wp.add_query_var(self.query_var)
        # end if
        if False != self.rewrite and is_admin() or "" != get_option("permalink_structure"):
            if self.hierarchical:
                add_rewrite_tag(str("%") + str(self.name) + str("%"), "(.+?)", str(self.query_var) + str("=") if self.query_var else str("post_type=") + str(self.name) + str("&pagename="))
            else:
                add_rewrite_tag(str("%") + str(self.name) + str("%"), "([^/]+)", str(self.query_var) + str("=") if self.query_var else str("post_type=") + str(self.name) + str("&name="))
            # end if
            if self.has_archive:
                archive_slug = self.rewrite["slug"] if True == self.has_archive else self.has_archive
                if self.rewrite["with_front"]:
                    archive_slug = php_substr(wp_rewrite.front, 1) + archive_slug
                else:
                    archive_slug = wp_rewrite.root + archive_slug
                # end if
                add_rewrite_rule(str(archive_slug) + str("/?$"), str("index.php?post_type=") + str(self.name), "top")
                if self.rewrite["feeds"] and wp_rewrite.feeds:
                    feeds = "(" + php_trim(php_implode("|", wp_rewrite.feeds)) + ")"
                    add_rewrite_rule(str(archive_slug) + str("/feed/") + str(feeds) + str("/?$"), str("index.php?post_type=") + str(self.name) + "&feed=$matches[1]", "top")
                    add_rewrite_rule(str(archive_slug) + str("/") + str(feeds) + str("/?$"), str("index.php?post_type=") + str(self.name) + "&feed=$matches[1]", "top")
                # end if
                if self.rewrite["pages"]:
                    add_rewrite_rule(str(archive_slug) + str("/") + str(wp_rewrite.pagination_base) + str("/([0-9]{1,})/?$"), str("index.php?post_type=") + str(self.name) + "&paged=$matches[1]", "top")
                # end if
            # end if
            permastruct_args = self.rewrite
            permastruct_args["feed"] = permastruct_args["feeds"]
            add_permastruct(self.name, str(self.rewrite["slug"]) + str("/%") + str(self.name) + str("%"), permastruct_args)
        # end if
    # end def add_rewrite_rules
    #// 
    #// Registers the post type meta box if a custom callback was specified.
    #// 
    #// @since 4.6.0
    #//
    def register_meta_boxes(self):
        
        if self.register_meta_box_cb:
            add_action("add_meta_boxes_" + self.name, self.register_meta_box_cb, 10, 1)
        # end if
    # end def register_meta_boxes
    #// 
    #// Adds the future post hook action for the post type.
    #// 
    #// @since 4.6.0
    #//
    def add_hooks(self):
        
        add_action("future_" + self.name, "_future_post_hook", 5, 2)
    # end def add_hooks
    #// 
    #// Registers the taxonomies for the post type.
    #// 
    #// @since 4.6.0
    #//
    def register_taxonomies(self):
        
        for taxonomy in self.taxonomies:
            register_taxonomy_for_object_type(taxonomy, self.name)
        # end for
    # end def register_taxonomies
    #// 
    #// Removes the features support for the post type.
    #// 
    #// @since 4.6.0
    #// 
    #// @global array $_wp_post_type_features Post type features.
    #//
    def remove_supports(self):
        
        global _wp_post_type_features
        php_check_if_defined("_wp_post_type_features")
        _wp_post_type_features[self.name] = None
    # end def remove_supports
    #// 
    #// Removes any rewrite rules, permastructs, and rules for the post type.
    #// 
    #// @since 4.6.0
    #// 
    #// @global WP_Rewrite $wp_rewrite          WordPress rewrite component.
    #// @global WP         $wp                  Current WordPress environment instance.
    #// @global array      $post_type_meta_caps Used to remove meta capabilities.
    #//
    def remove_rewrite_rules(self):
        
        global wp,wp_rewrite,post_type_meta_caps
        php_check_if_defined("wp","wp_rewrite","post_type_meta_caps")
        #// Remove query var.
        if False != self.query_var:
            wp.remove_query_var(self.query_var)
        # end if
        #// Remove any rewrite rules, permastructs, and rules.
        if False != self.rewrite:
            remove_rewrite_tag(str("%") + str(self.name) + str("%"))
            remove_permastruct(self.name)
            for regex,query in wp_rewrite.extra_rules_top:
                if False != php_strpos(query, str("index.php?post_type=") + str(self.name)):
                    wp_rewrite.extra_rules_top[regex] = None
                # end if
            # end for
        # end if
        #// Remove registered custom meta capabilities.
        for cap in self.cap:
            post_type_meta_caps[cap] = None
        # end for
    # end def remove_rewrite_rules
    #// 
    #// Unregisters the post type meta box if a custom callback was specified.
    #// 
    #// @since 4.6.0
    #//
    def unregister_meta_boxes(self):
        
        if self.register_meta_box_cb:
            remove_action("add_meta_boxes_" + self.name, self.register_meta_box_cb, 10)
        # end if
    # end def unregister_meta_boxes
    #// 
    #// Removes the post type from all taxonomies.
    #// 
    #// @since 4.6.0
    #//
    def unregister_taxonomies(self):
        
        for taxonomy in get_object_taxonomies(self.name):
            unregister_taxonomy_for_object_type(taxonomy, self.name)
        # end for
    # end def unregister_taxonomies
    #// 
    #// Removes the future post hook action for the post type.
    #// 
    #// @since 4.6.0
    #//
    def remove_hooks(self):
        
        remove_action("future_" + self.name, "_future_post_hook", 5)
    # end def remove_hooks
    #// 
    #// Gets the REST API controller for this post type.
    #// 
    #// Will only instantiate the controller class once per request.
    #// 
    #// @since 5.3.0
    #// 
    #// @return WP_REST_Controller|null The controller instance, or null if the post type
    #// is set not to show in rest.
    #//
    def get_rest_controller(self):
        
        if (not self.show_in_rest):
            return None
        # end if
        class_ = self.rest_controller_class if self.rest_controller_class else WP_REST_Posts_Controller.class_
        if (not php_class_exists(class_)):
            return None
        # end if
        if (not is_subclass_of(class_, WP_REST_Controller.class_)):
            return None
        # end if
        if (not self.rest_controller):
            self.rest_controller = php_new_class(class_, lambda : {**locals(), **globals()}[class_](self.name))
        # end if
        if (not type(self.rest_controller).__name__ == "class_"):
            return None
        # end if
        return self.rest_controller
    # end def get_rest_controller
# end class WP_Post_Type
