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
    #// 
    #// Post type key.
    #// 
    #// @since 4.6.0
    #// @var string $name
    #//
    name = Array()
    #// 
    #// Name of the post type shown in the menu. Usually plural.
    #// 
    #// @since 4.6.0
    #// @var string $label
    #//
    label = Array()
    #// 
    #// Labels object for this post type.
    #// 
    #// If not set, post labels are inherited for non-hierarchical types
    #// and page labels for hierarchical ones.
    #// 
    #// @see get_post_type_labels()
    #// 
    #// @since 4.6.0
    #// @var object $labels
    #//
    labels = Array()
    #// 
    #// A short descriptive summary of what the post type is.
    #// 
    #// Default empty.
    #// 
    #// @since 4.6.0
    #// @var string $description
    #//
    description = ""
    #// 
    #// Whether a post type is intended for use publicly either via the admin interface or by front-end users.
    #// 
    #// While the default settings of $exclude_from_search, $publicly_queryable, $show_ui, and $show_in_nav_menus
    #// are inherited from public, each does not rely on this relationship and controls a very specific intention.
    #// 
    #// Default false.
    #// 
    #// @since 4.6.0
    #// @var bool $public
    #//
    public = False
    #// 
    #// Whether the post type is hierarchical (e.g. page).
    #// 
    #// Default false.
    #// 
    #// @since 4.6.0
    #// @var bool $hierarchical
    #//
    hierarchical = False
    #// 
    #// Whether to exclude posts with this post type from front end search
    #// results.
    #// 
    #// Default is the opposite value of $public.
    #// 
    #// @since 4.6.0
    #// @var bool $exclude_from_search
    #//
    exclude_from_search = None
    #// 
    #// Whether queries can be performed on the front end for the post type as part of `parse_request()`.
    #// 
    #// Endpoints would include:
    #// - `?post_type={post_type_key}`
    #// - `?{post_type_key}={single_post_slug}`
    #// - `?{post_type_query_var}={single_post_slug}`
    #// 
    #// Default is the value of $public.
    #// 
    #// @since 4.6.0
    #// @var bool $publicly_queryable
    #//
    publicly_queryable = None
    #// 
    #// Whether to generate and allow a UI for managing this post type in the admin.
    #// 
    #// Default is the value of $public.
    #// 
    #// @since 4.6.0
    #// @var bool $show_ui
    #//
    show_ui = None
    #// 
    #// Where to show the post type in the admin menu.
    #// 
    #// To work, $show_ui must be true. If true, the post type is shown in its own top level menu. If false, no menu is
    #// shown. If a string of an existing top level menu (eg. 'tools.php' or 'edit.php?post_type=page'), the post type
    #// will be placed as a sub-menu of that.
    #// 
    #// Default is the value of $show_ui.
    #// 
    #// @since 4.6.0
    #// @var bool $show_in_menu
    #//
    show_in_menu = None
    #// 
    #// Makes this post type available for selection in navigation menus.
    #// 
    #// Default is the value $public.
    #// 
    #// @since 4.6.0
    #// @var bool $show_in_nav_menus
    #//
    show_in_nav_menus = None
    #// 
    #// Makes this post type available via the admin bar.
    #// 
    #// Default is the value of $show_in_menu.
    #// 
    #// @since 4.6.0
    #// @var bool $show_in_admin_bar
    #//
    show_in_admin_bar = None
    #// 
    #// The position in the menu order the post type should appear.
    #// 
    #// To work, $show_in_menu must be true. Default null (at the bottom).
    #// 
    #// @since 4.6.0
    #// @var int $menu_position
    #//
    menu_position = None
    #// 
    #// The URL to the icon to be used for this menu.
    #// 
    #// Pass a base64-encoded SVG using a data URI, which will be colored to match the color scheme.
    #// This should begin with 'data:image/svg+xml;base64,'. Pass the name of a Dashicons helper class
    #// to use a font icon, e.g. 'dashicons-chart-pie'. Pass 'none' to leave div.wp-menu-image empty
    #// so an icon can be added via CSS.
    #// 
    #// Defaults to use the posts icon.
    #// 
    #// @since 4.6.0
    #// @var string $menu_icon
    #//
    menu_icon = None
    #// 
    #// The string to use to build the read, edit, and delete capabilities.
    #// 
    #// May be passed as an array to allow for alternative plurals when using
    #// this argument as a base to construct the capabilities, e.g.
    #// array( 'story', 'stories' ). Default 'post'.
    #// 
    #// @since 4.6.0
    #// @var string $capability_type
    #//
    capability_type = "post"
    #// 
    #// Whether to use the internal default meta capability handling.
    #// 
    #// Default false.
    #// 
    #// @since 4.6.0
    #// @var bool $map_meta_cap
    #//
    map_meta_cap = False
    #// 
    #// Provide a callback function that sets up the meta boxes for the edit form.
    #// 
    #// Do `remove_meta_box()` and `add_meta_box()` calls in the callback. Default null.
    #// 
    #// @since 4.6.0
    #// @var string $register_meta_box_cb
    #//
    register_meta_box_cb = None
    #// 
    #// An array of taxonomy identifiers that will be registered for the post type.
    #// 
    #// Taxonomies can be registered later with `register_taxonomy()` or `register_taxonomy_for_object_type()`.
    #// 
    #// Default empty array.
    #// 
    #// @since 4.6.0
    #// @var array $taxonomies
    #//
    taxonomies = Array()
    #// 
    #// Whether there should be post type archives, or if a string, the archive slug to use.
    #// 
    #// Will generate the proper rewrite rules if $rewrite is enabled. Default false.
    #// 
    #// @since 4.6.0
    #// @var bool|string $has_archive
    #//
    has_archive = False
    #// 
    #// Sets the query_var key for this post type.
    #// 
    #// Defaults to $post_type key. If false, a post type cannot be loaded at `?{query_var}={post_slug}`.
    #// If specified as a string, the query `?{query_var_string}={post_slug}` will be valid.
    #// 
    #// @since 4.6.0
    #// @var string|bool $query_var
    #//
    query_var = Array()
    #// 
    #// Whether to allow this post type to be exported.
    #// 
    #// Default true.
    #// 
    #// @since 4.6.0
    #// @var bool $can_export
    #//
    can_export = True
    #// 
    #// Whether to delete posts of this type when deleting a user.
    #// 
    #// If true, posts of this type belonging to the user will be moved to Trash when then user is deleted.
    #// If false, posts of this type belonging to the user will *not* be trashed or deleted.
    #// If not set (the default), posts are trashed if post_type_supports( 'author' ).
    #// Otherwise posts are not trashed or deleted. Default null.
    #// 
    #// @since 4.6.0
    #// @var bool $delete_with_user
    #//
    delete_with_user = None
    #// 
    #// Whether this post type is a native or "built-in" post_type.
    #// 
    #// Default false.
    #// 
    #// @since 4.6.0
    #// @var bool $_builtin
    #//
    _builtin = False
    #// 
    #// URL segment to use for edit link of this post type.
    #// 
    #// Default 'post.php?post=%d'.
    #// 
    #// @since 4.6.0
    #// @var string $_edit_link
    #//
    _edit_link = "post.php?post=%d"
    #// 
    #// Post type capabilities.
    #// 
    #// @since 4.6.0
    #// @var object $cap
    #//
    cap = Array()
    #// 
    #// Triggers the handling of rewrites for this post type.
    #// 
    #// Defaults to true, using $post_type as slug.
    #// 
    #// @since 4.6.0
    #// @var array|false $rewrite
    #//
    rewrite = Array()
    #// 
    #// The features supported by the post type.
    #// 
    #// @since 4.6.0
    #// @var array|bool $supports
    #//
    supports = Array()
    #// 
    #// Whether this post type should appear in the REST API.
    #// 
    #// Default false. If true, standard endpoints will be registered with
    #// respect to $rest_base and $rest_controller_class.
    #// 
    #// @since 4.7.4
    #// @var bool $show_in_rest
    #//
    show_in_rest = Array()
    #// 
    #// The base path for this post type's REST API endpoints.
    #// 
    #// @since 4.7.4
    #// @var string|bool $rest_base
    #//
    rest_base = Array()
    #// 
    #// The controller for this post type's REST API endpoints.
    #// 
    #// Custom controllers must extend WP_REST_Controller.
    #// 
    #// @since 4.7.4
    #// @var string|bool $rest_controller_class
    #//
    rest_controller_class = Array()
    #// 
    #// The controller instance for this post type's REST API endpoints.
    #// 
    #// Lazily computed. Should be accessed using {@see WP_Post_Type::get_rest_controller()}.
    #// 
    #// @since 5.3.0
    #// @var WP_REST_Controller $rest_controller
    #//
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
    def __init__(self, post_type_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        self.name = post_type_
        self.set_props(args_)
    # end def __init__
    #// 
    #// Sets post type properties.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array|string $args Array or string of arguments for registering a post type.
    #//
    def set_props(self, args_=None):
        
        
        args_ = wp_parse_args(args_)
        #// 
        #// Filters the arguments for registering a post type.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array  $args      Array of arguments for registering a post type.
        #// @param string $post_type Post type key.
        #//
        args_ = apply_filters("register_post_type_args", args_, self.name)
        has_edit_link_ = (not php_empty(lambda : args_["_edit_link"]))
        #// Args prefixed with an underscore are reserved for internal use.
        defaults_ = Array({"labels": Array(), "description": "", "public": False, "hierarchical": False, "exclude_from_search": None, "publicly_queryable": None, "show_ui": None, "show_in_menu": None, "show_in_nav_menus": None, "show_in_admin_bar": None, "menu_position": None, "menu_icon": None, "capability_type": "post", "capabilities": Array(), "map_meta_cap": None, "supports": Array(), "register_meta_box_cb": None, "taxonomies": Array(), "has_archive": False, "rewrite": True, "query_var": True, "can_export": True, "delete_with_user": None, "show_in_rest": False, "rest_base": False, "rest_controller_class": False, "_builtin": False, "_edit_link": "post.php?post=%d"})
        args_ = php_array_merge(defaults_, args_)
        args_["name"] = self.name
        #// If not set, default to the setting for 'public'.
        if None == args_["publicly_queryable"]:
            args_["publicly_queryable"] = args_["public"]
        # end if
        #// If not set, default to the setting for 'public'.
        if None == args_["show_ui"]:
            args_["show_ui"] = args_["public"]
        # end if
        #// If not set, default to the setting for 'show_ui'.
        if None == args_["show_in_menu"] or (not args_["show_ui"]):
            args_["show_in_menu"] = args_["show_ui"]
        # end if
        #// If not set, default to the setting for 'show_in_menu'.
        if None == args_["show_in_admin_bar"]:
            args_["show_in_admin_bar"] = php_bool(args_["show_in_menu"])
        # end if
        #// If not set, default to the setting for 'public'.
        if None == args_["show_in_nav_menus"]:
            args_["show_in_nav_menus"] = args_["public"]
        # end if
        #// If not set, default to true if not public, false if public.
        if None == args_["exclude_from_search"]:
            args_["exclude_from_search"] = (not args_["public"])
        # end if
        #// Back compat with quirky handling in version 3.0. #14122.
        if php_empty(lambda : args_["capabilities"]) and None == args_["map_meta_cap"] and php_in_array(args_["capability_type"], Array("post", "page")):
            args_["map_meta_cap"] = True
        # end if
        #// If not set, default to false.
        if None == args_["map_meta_cap"]:
            args_["map_meta_cap"] = False
        # end if
        #// If there's no specified edit link and no UI, remove the edit link.
        if (not args_["show_ui"]) and (not has_edit_link_):
            args_["_edit_link"] = ""
        # end if
        self.cap = get_post_type_capabilities(args_)
        args_["capabilities"] = None
        if php_is_array(args_["capability_type"]):
            args_["capability_type"] = args_["capability_type"][0]
        # end if
        if False != args_["query_var"]:
            if True == args_["query_var"]:
                args_["query_var"] = self.name
            else:
                args_["query_var"] = sanitize_title_with_dashes(args_["query_var"])
            # end if
        # end if
        if False != args_["rewrite"] and is_admin() or "" != get_option("permalink_structure"):
            if (not php_is_array(args_["rewrite"])):
                args_["rewrite"] = Array()
            # end if
            if php_empty(lambda : args_["rewrite"]["slug"]):
                args_["rewrite"]["slug"] = self.name
            # end if
            if (not (php_isset(lambda : args_["rewrite"]["with_front"]))):
                args_["rewrite"]["with_front"] = True
            # end if
            if (not (php_isset(lambda : args_["rewrite"]["pages"]))):
                args_["rewrite"]["pages"] = True
            # end if
            if (not (php_isset(lambda : args_["rewrite"]["feeds"]))) or (not args_["has_archive"]):
                args_["rewrite"]["feeds"] = php_bool(args_["has_archive"])
            # end if
            if (not (php_isset(lambda : args_["rewrite"]["ep_mask"]))):
                if (php_isset(lambda : args_["permalink_epmask"])):
                    args_["rewrite"]["ep_mask"] = args_["permalink_epmask"]
                else:
                    args_["rewrite"]["ep_mask"] = EP_PERMALINK
                # end if
            # end if
        # end if
        for property_name_,property_value_ in args_:
            self.property_name_ = property_value_
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
            for feature_,args_ in self.supports:
                if php_is_array(args_):
                    add_post_type_support(self.name, feature_, args_)
                else:
                    add_post_type_support(self.name, args_)
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
        
        
        global wp_rewrite_
        global wp_
        php_check_if_defined("wp_rewrite_","wp_")
        if False != self.query_var and wp_ and is_post_type_viewable(self):
            wp_.add_query_var(self.query_var)
        # end if
        if False != self.rewrite and is_admin() or "" != get_option("permalink_structure"):
            if self.hierarchical:
                add_rewrite_tag(str("%") + str(self.name) + str("%"), "(.+?)", str(self.query_var) + str("=") if self.query_var else str("post_type=") + str(self.name) + str("&pagename="))
            else:
                add_rewrite_tag(str("%") + str(self.name) + str("%"), "([^/]+)", str(self.query_var) + str("=") if self.query_var else str("post_type=") + str(self.name) + str("&name="))
            # end if
            if self.has_archive:
                archive_slug_ = self.rewrite["slug"] if True == self.has_archive else self.has_archive
                if self.rewrite["with_front"]:
                    archive_slug_ = php_substr(wp_rewrite_.front, 1) + archive_slug_
                else:
                    archive_slug_ = wp_rewrite_.root + archive_slug_
                # end if
                add_rewrite_rule(str(archive_slug_) + str("/?$"), str("index.php?post_type=") + str(self.name), "top")
                if self.rewrite["feeds"] and wp_rewrite_.feeds:
                    feeds_ = "(" + php_trim(php_implode("|", wp_rewrite_.feeds)) + ")"
                    add_rewrite_rule(str(archive_slug_) + str("/feed/") + str(feeds_) + str("/?$"), str("index.php?post_type=") + str(self.name) + "&feed=$matches[1]", "top")
                    add_rewrite_rule(str(archive_slug_) + str("/") + str(feeds_) + str("/?$"), str("index.php?post_type=") + str(self.name) + "&feed=$matches[1]", "top")
                # end if
                if self.rewrite["pages"]:
                    add_rewrite_rule(str(archive_slug_) + str("/") + str(wp_rewrite_.pagination_base) + str("/([0-9]{1,})/?$"), str("index.php?post_type=") + str(self.name) + "&paged=$matches[1]", "top")
                # end if
            # end if
            permastruct_args_ = self.rewrite
            permastruct_args_["feed"] = permastruct_args_["feeds"]
            add_permastruct(self.name, str(self.rewrite["slug"]) + str("/%") + str(self.name) + str("%"), permastruct_args_)
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
        
        
        for taxonomy_ in self.taxonomies:
            register_taxonomy_for_object_type(taxonomy_, self.name)
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
        
        
        global _wp_post_type_features_
        php_check_if_defined("_wp_post_type_features_")
        _wp_post_type_features_[self.name] = None
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
        
        
        global wp_
        global wp_rewrite_
        global post_type_meta_caps_
        php_check_if_defined("wp_","wp_rewrite_","post_type_meta_caps_")
        #// Remove query var.
        if False != self.query_var:
            wp_.remove_query_var(self.query_var)
        # end if
        #// Remove any rewrite rules, permastructs, and rules.
        if False != self.rewrite:
            remove_rewrite_tag(str("%") + str(self.name) + str("%"))
            remove_permastruct(self.name)
            for regex_,query_ in wp_rewrite_.extra_rules_top:
                if False != php_strpos(query_, str("index.php?post_type=") + str(self.name)):
                    wp_rewrite_.extra_rules_top[regex_] = None
                # end if
            # end for
        # end if
        #// Remove registered custom meta capabilities.
        for cap_ in self.cap:
            post_type_meta_caps_[cap_] = None
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
        
        
        for taxonomy_ in get_object_taxonomies(self.name):
            unregister_taxonomy_for_object_type(taxonomy_, self.name)
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
