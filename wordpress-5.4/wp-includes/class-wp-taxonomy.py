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
    name = Array()
    label = Array()
    labels = Array()
    description = ""
    public = True
    publicly_queryable = True
    hierarchical = False
    show_ui = True
    show_in_menu = True
    show_in_nav_menus = True
    show_tagcloud = True
    show_in_quick_edit = True
    show_admin_column = False
    meta_box_cb = None
    meta_box_sanitize_cb = None
    object_type = None
    cap = Array()
    rewrite = Array()
    query_var = Array()
    update_count_callback = Array()
    show_in_rest = Array()
    rest_base = Array()
    rest_controller_class = Array()
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
    def __init__(self, taxonomy=None, object_type=None, args=Array()):
        
        self.name = taxonomy
        self.set_props(object_type, args)
    # end def __init__
    #// 
    #// Sets taxonomy properties.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array|string $object_type Name of the object type for the taxonomy object.
    #// @param array|string $args        Array or query string of arguments for registering a taxonomy.
    #//
    def set_props(self, object_type=None, args=None):
        
        args = wp_parse_args(args)
        #// 
        #// Filters the arguments for registering a taxonomy.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array    $args        Array of arguments for registering a taxonomy.
        #// @param string   $taxonomy    Taxonomy key.
        #// @param string[] $object_type Array of names of object types for the taxonomy.
        #//
        args = apply_filters("register_taxonomy_args", args, self.name, object_type)
        defaults = Array({"labels": Array(), "description": "", "public": True, "publicly_queryable": None, "hierarchical": False, "show_ui": None, "show_in_menu": None, "show_in_nav_menus": None, "show_tagcloud": None, "show_in_quick_edit": None, "show_admin_column": False, "meta_box_cb": None, "meta_box_sanitize_cb": None, "capabilities": Array(), "rewrite": True, "query_var": self.name, "update_count_callback": "", "show_in_rest": False, "rest_base": False, "rest_controller_class": False, "_builtin": False})
        args = php_array_merge(defaults, args)
        #// If not set, default to the setting for 'public'.
        if None == args["publicly_queryable"]:
            args["publicly_queryable"] = args["public"]
        # end if
        if False != args["query_var"] and is_admin() or False != args["publicly_queryable"]:
            if True == args["query_var"]:
                args["query_var"] = self.name
            else:
                args["query_var"] = sanitize_title_with_dashes(args["query_var"])
            # end if
        else:
            #// Force 'query_var' to false for non-public taxonomies.
            args["query_var"] = False
        # end if
        if False != args["rewrite"] and is_admin() or "" != get_option("permalink_structure"):
            args["rewrite"] = wp_parse_args(args["rewrite"], Array({"with_front": True, "hierarchical": False, "ep_mask": EP_NONE}))
            if php_empty(lambda : args["rewrite"]["slug"]):
                args["rewrite"]["slug"] = sanitize_title_with_dashes(self.name)
            # end if
        # end if
        #// If not set, default to the setting for 'public'.
        if None == args["show_ui"]:
            args["show_ui"] = args["public"]
        # end if
        #// If not set, default to the setting for 'show_ui'.
        if None == args["show_in_menu"] or (not args["show_ui"]):
            args["show_in_menu"] = args["show_ui"]
        # end if
        #// If not set, default to the setting for 'public'.
        if None == args["show_in_nav_menus"]:
            args["show_in_nav_menus"] = args["public"]
        # end if
        #// If not set, default to the setting for 'show_ui'.
        if None == args["show_tagcloud"]:
            args["show_tagcloud"] = args["show_ui"]
        # end if
        #// If not set, default to the setting for 'show_ui'.
        if None == args["show_in_quick_edit"]:
            args["show_in_quick_edit"] = args["show_ui"]
        # end if
        default_caps = Array({"manage_terms": "manage_categories", "edit_terms": "manage_categories", "delete_terms": "manage_categories", "assign_terms": "edit_posts"})
        args["cap"] = php_array_merge(default_caps, args["capabilities"])
        args["capabilities"] = None
        args["object_type"] = array_unique(object_type)
        #// If not set, use the default meta box.
        if None == args["meta_box_cb"]:
            if args["hierarchical"]:
                args["meta_box_cb"] = "post_categories_meta_box"
            else:
                args["meta_box_cb"] = "post_tags_meta_box"
            # end if
        # end if
        args["name"] = self.name
        #// Default meta box sanitization callback depends on the value of 'meta_box_cb'.
        if None == args["meta_box_sanitize_cb"]:
            for case in Switch(args["meta_box_cb"]):
                if case("post_categories_meta_box"):
                    args["meta_box_sanitize_cb"] = "taxonomy_meta_box_sanitize_cb_checkboxes"
                    break
                # end if
                if case("post_tags_meta_box"):
                    pass
                # end if
                if case():
                    args["meta_box_sanitize_cb"] = "taxonomy_meta_box_sanitize_cb_input"
                    break
                # end if
            # end for
        # end if
        for property_name,property_value in args:
            self.property_name = property_value
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
        global wp
        php_check_if_defined("wp")
        #// Non-publicly queryable taxonomies should not register query vars, except in the admin.
        if False != self.query_var and wp:
            wp.add_query_var(self.query_var)
        # end if
        if False != self.rewrite and is_admin() or "" != get_option("permalink_structure"):
            if self.hierarchical and self.rewrite["hierarchical"]:
                tag = "(.+?)"
            else:
                tag = "([^/]+)"
            # end if
            add_rewrite_tag(str("%") + str(self.name) + str("%"), tag, str(self.query_var) + str("=") if self.query_var else str("taxonomy=") + str(self.name) + str("&term="))
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
        global wp
        php_check_if_defined("wp")
        #// Remove query var.
        if False != self.query_var:
            wp.remove_query_var(self.query_var)
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
