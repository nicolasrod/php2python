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
#// Taxonomy API: WP_Taxonomy class
#// 
#// @package WordPress
#// @subpackage Taxonomy
#// @since 4.7.0
#// 
#// 
#// Core class used for interacting with taxonomies.
#// 
#// @since 4.7.0
#//
class WP_Taxonomy():
    #// 
    #// Taxonomy key.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    name = Array()
    #// 
    #// Name of the taxonomy shown in the menu. Usually plural.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    label = Array()
    #// 
    #// Labels object for this taxonomy.
    #// 
    #// If not set, tag labels are inherited for non-hierarchical types
    #// and category labels for hierarchical ones.
    #// 
    #// @see get_taxonomy_labels()
    #// 
    #// @since 4.7.0
    #// @var object
    #//
    labels = Array()
    #// 
    #// A short descriptive summary of what the taxonomy is for.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    description = ""
    #// 
    #// Whether a taxonomy is intended for use publicly either via the admin interface or by front-end users.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    public = True
    #// 
    #// Whether the taxonomy is publicly queryable.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    publicly_queryable = True
    #// 
    #// Whether the taxonomy is hierarchical.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    hierarchical = False
    #// 
    #// Whether to generate and allow a UI for managing terms in this taxonomy in the admin.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    show_ui = True
    #// 
    #// Whether to show the taxonomy in the admin menu.
    #// 
    #// If true, the taxonomy is shown as a submenu of the object type menu. If false, no menu is shown.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    show_in_menu = True
    #// 
    #// Whether the taxonomy is available for selection in navigation menus.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    show_in_nav_menus = True
    #// 
    #// Whether to list the taxonomy in the tag cloud widget controls.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    show_tagcloud = True
    #// 
    #// Whether to show the taxonomy in the quick/bulk edit panel.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    show_in_quick_edit = True
    #// 
    #// Whether to display a column for the taxonomy on its post type listing screens.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    show_admin_column = False
    #// 
    #// The callback function for the meta box display.
    #// 
    #// @since 4.7.0
    #// @var bool|callable
    #//
    meta_box_cb = None
    #// 
    #// The callback function for sanitizing taxonomy data saved from a meta box.
    #// 
    #// @since 5.1.0
    #// @var callable
    #//
    meta_box_sanitize_cb = None
    #// 
    #// An array of object types this taxonomy is registered for.
    #// 
    #// @since 4.7.0
    #// @var array
    #//
    object_type = None
    #// 
    #// Capabilities for this taxonomy.
    #// 
    #// @since 4.7.0
    #// @var object
    #//
    cap = Array()
    #// 
    #// Rewrites information for this taxonomy.
    #// 
    #// @since 4.7.0
    #// @var array|false
    #//
    rewrite = Array()
    #// 
    #// Query var string for this taxonomy.
    #// 
    #// @since 4.7.0
    #// @var string|false
    #//
    query_var = Array()
    #// 
    #// Function that will be called when the count is updated.
    #// 
    #// @since 4.7.0
    #// @var callable
    #//
    update_count_callback = Array()
    #// 
    #// Whether this taxonomy should appear in the REST API.
    #// 
    #// Default false. If true, standard endpoints will be registered with
    #// respect to $rest_base and $rest_controller_class.
    #// 
    #// @since 4.7.4
    #// @var bool $show_in_rest
    #//
    show_in_rest = Array()
    #// 
    #// The base path for this taxonomy's REST API endpoints.
    #// 
    #// @since 4.7.4
    #// @var string|bool $rest_base
    #//
    rest_base = Array()
    #// 
    #// The controller for this taxonomy's REST API endpoints.
    #// 
    #// Custom controllers must extend WP_REST_Controller.
    #// 
    #// @since 4.7.4
    #// @var string|bool $rest_controller_class
    #//
    rest_controller_class = Array()
    #// 
    #// Whether it is a built-in taxonomy.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
    _builtin = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @global WP $wp Current WordPress environment instance.
    #// 
    #// @param string       $taxonomy    Taxonomy key, must not exceed 32 characters.
    #// @param array|string $object_type Name of the object type for the taxonomy object.
    #// @param array|string $args        Optional. Array or query string of arguments for registering a taxonomy.
    #// Default empty array.
    #//
    def __init__(self, taxonomy_=None, object_type_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        self.name = taxonomy_
        self.set_props(object_type_, args_)
    # end def __init__
    #// 
    #// Sets taxonomy properties.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array|string $object_type Name of the object type for the taxonomy object.
    #// @param array|string $args        Array or query string of arguments for registering a taxonomy.
    #//
    def set_props(self, object_type_=None, args_=None):
        
        
        args_ = wp_parse_args(args_)
        #// 
        #// Filters the arguments for registering a taxonomy.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array    $args        Array of arguments for registering a taxonomy.
        #// @param string   $taxonomy    Taxonomy key.
        #// @param string[] $object_type Array of names of object types for the taxonomy.
        #//
        args_ = apply_filters("register_taxonomy_args", args_, self.name, object_type_)
        defaults_ = Array({"labels": Array(), "description": "", "public": True, "publicly_queryable": None, "hierarchical": False, "show_ui": None, "show_in_menu": None, "show_in_nav_menus": None, "show_tagcloud": None, "show_in_quick_edit": None, "show_admin_column": False, "meta_box_cb": None, "meta_box_sanitize_cb": None, "capabilities": Array(), "rewrite": True, "query_var": self.name, "update_count_callback": "", "show_in_rest": False, "rest_base": False, "rest_controller_class": False, "_builtin": False})
        args_ = php_array_merge(defaults_, args_)
        #// If not set, default to the setting for 'public'.
        if None == args_["publicly_queryable"]:
            args_["publicly_queryable"] = args_["public"]
        # end if
        if False != args_["query_var"] and is_admin() or False != args_["publicly_queryable"]:
            if True == args_["query_var"]:
                args_["query_var"] = self.name
            else:
                args_["query_var"] = sanitize_title_with_dashes(args_["query_var"])
            # end if
        else:
            #// Force 'query_var' to false for non-public taxonomies.
            args_["query_var"] = False
        # end if
        if False != args_["rewrite"] and is_admin() or "" != get_option("permalink_structure"):
            args_["rewrite"] = wp_parse_args(args_["rewrite"], Array({"with_front": True, "hierarchical": False, "ep_mask": EP_NONE}))
            if php_empty(lambda : args_["rewrite"]["slug"]):
                args_["rewrite"]["slug"] = sanitize_title_with_dashes(self.name)
            # end if
        # end if
        #// If not set, default to the setting for 'public'.
        if None == args_["show_ui"]:
            args_["show_ui"] = args_["public"]
        # end if
        #// If not set, default to the setting for 'show_ui'.
        if None == args_["show_in_menu"] or (not args_["show_ui"]):
            args_["show_in_menu"] = args_["show_ui"]
        # end if
        #// If not set, default to the setting for 'public'.
        if None == args_["show_in_nav_menus"]:
            args_["show_in_nav_menus"] = args_["public"]
        # end if
        #// If not set, default to the setting for 'show_ui'.
        if None == args_["show_tagcloud"]:
            args_["show_tagcloud"] = args_["show_ui"]
        # end if
        #// If not set, default to the setting for 'show_ui'.
        if None == args_["show_in_quick_edit"]:
            args_["show_in_quick_edit"] = args_["show_ui"]
        # end if
        default_caps_ = Array({"manage_terms": "manage_categories", "edit_terms": "manage_categories", "delete_terms": "manage_categories", "assign_terms": "edit_posts"})
        args_["cap"] = php_array_merge(default_caps_, args_["capabilities"])
        args_["capabilities"] = None
        args_["object_type"] = array_unique(object_type_)
        #// If not set, use the default meta box.
        if None == args_["meta_box_cb"]:
            if args_["hierarchical"]:
                args_["meta_box_cb"] = "post_categories_meta_box"
            else:
                args_["meta_box_cb"] = "post_tags_meta_box"
            # end if
        # end if
        args_["name"] = self.name
        #// Default meta box sanitization callback depends on the value of 'meta_box_cb'.
        if None == args_["meta_box_sanitize_cb"]:
            for case in Switch(args_["meta_box_cb"]):
                if case("post_categories_meta_box"):
                    args_["meta_box_sanitize_cb"] = "taxonomy_meta_box_sanitize_cb_checkboxes"
                    break
                # end if
                if case("post_tags_meta_box"):
                    pass
                # end if
                if case():
                    args_["meta_box_sanitize_cb"] = "taxonomy_meta_box_sanitize_cb_input"
                    break
                # end if
            # end for
        # end if
        for property_name_,property_value_ in args_.items():
            self.property_name_ = property_value_
        # end for
        self.labels = get_taxonomy_labels(self)
        self.label = self.labels.name
    # end def set_props
    #// 
    #// Adds the necessary rewrite rules for the taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @global WP $wp Current WordPress environment instance.
    #//
    def add_rewrite_rules(self):
        
        
        #// @var WP $wp
        global wp_
        php_check_if_defined("wp_")
        #// Non-publicly queryable taxonomies should not register query vars, except in the admin.
        if False != self.query_var and wp_:
            wp_.add_query_var(self.query_var)
        # end if
        if False != self.rewrite and is_admin() or "" != get_option("permalink_structure"):
            if self.hierarchical and self.rewrite["hierarchical"]:
                tag_ = "(.+?)"
            else:
                tag_ = "([^/]+)"
            # end if
            add_rewrite_tag(str("%") + str(self.name) + str("%"), tag_, str(self.query_var) + str("=") if self.query_var else str("taxonomy=") + str(self.name) + str("&term="))
            add_permastruct(self.name, str(self.rewrite["slug"]) + str("/%") + str(self.name) + str("%"), self.rewrite)
        # end if
    # end def add_rewrite_rules
    #// 
    #// Removes any rewrite rules, permastructs, and rules for the taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @global WP $wp Current WordPress environment instance.
    #//
    def remove_rewrite_rules(self):
        
        
        #// @var WP $wp
        global wp_
        php_check_if_defined("wp_")
        #// Remove query var.
        if False != self.query_var:
            wp_.remove_query_var(self.query_var)
        # end if
        #// Remove rewrite tags and permastructs.
        if False != self.rewrite:
            remove_rewrite_tag(str("%") + str(self.name) + str("%"))
            remove_permastruct(self.name)
        # end if
    # end def remove_rewrite_rules
    #// 
    #// Registers the ajax callback for the meta box.
    #// 
    #// @since 4.7.0
    #//
    def add_hooks(self):
        
        
        add_filter("wp_ajax_add-" + self.name, "_wp_ajax_add_hierarchical_term")
    # end def add_hooks
    #// 
    #// Removes the ajax callback for the meta box.
    #// 
    #// @since 4.7.0
    #//
    def remove_hooks(self):
        
        
        remove_filter("wp_ajax_add-" + self.name, "_wp_ajax_add_hierarchical_term")
    # end def remove_hooks
# end class WP_Taxonomy
