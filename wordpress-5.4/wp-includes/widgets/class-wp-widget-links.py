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
#// Widget API: WP_Widget_Links class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a Links widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Links(WP_Widget):
    #// 
    #// Sets up a new Links widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        
        widget_ops_ = Array({"description": __("Your blogroll"), "customize_selective_refresh": True})
        super().__init__("links", __("Links"), widget_ops_)
    # end def __init__
    #// 
    #// Outputs the content for the current Links widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Links widget instance.
    #//
    def widget(self, args_=None, instance_=None):
        
        
        show_description_ = instance_["description"] if (php_isset(lambda : instance_["description"])) else False
        show_name_ = instance_["name"] if (php_isset(lambda : instance_["name"])) else False
        show_rating_ = instance_["rating"] if (php_isset(lambda : instance_["rating"])) else False
        show_images_ = instance_["images"] if (php_isset(lambda : instance_["images"])) else True
        category_ = instance_["category"] if (php_isset(lambda : instance_["category"])) else False
        orderby_ = instance_["orderby"] if (php_isset(lambda : instance_["orderby"])) else "name"
        order_ = "DESC" if "rating" == orderby_ else "ASC"
        limit_ = instance_["limit"] if (php_isset(lambda : instance_["limit"])) else -1
        before_widget_ = php_preg_replace("/id=\"[^\"]*\"/", "id=\"%id\"", args_["before_widget"])
        widget_links_args_ = Array({"title_before": args_["before_title"], "title_after": args_["after_title"], "category_before": before_widget_, "category_after": args_["after_widget"], "show_images": show_images_, "show_description": show_description_, "show_name": show_name_, "show_rating": show_rating_, "category": category_, "class": "linkcat widget", "orderby": orderby_, "order": order_, "limit": limit_})
        #// 
        #// Filters the arguments for the Links widget.
        #// 
        #// @since 2.6.0
        #// @since 4.4.0 Added the `$instance` parameter.
        #// 
        #// @see wp_list_bookmarks()
        #// 
        #// @param array $widget_links_args An array of arguments to retrieve the links list.
        #// @param array $instance          The settings for the particular instance of the widget.
        #//
        wp_list_bookmarks(apply_filters("widget_links_args", widget_links_args_, instance_))
    # end def widget
    #// 
    #// Handles updating settings for the current Links widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Updated settings to save.
    #//
    def update(self, new_instance_=None, old_instance_=None):
        
        
        new_instance_ = new_instance_
        instance_ = Array({"images": 0, "name": 0, "description": 0, "rating": 0})
        for field_,val_ in instance_:
            if (php_isset(lambda : new_instance_[field_])):
                instance_[field_] = 1
            # end if
        # end for
        instance_["orderby"] = "name"
        if php_in_array(new_instance_["orderby"], Array("name", "rating", "id", "rand")):
            instance_["orderby"] = new_instance_["orderby"]
        # end if
        instance_["category"] = php_intval(new_instance_["category"])
        instance_["limit"] = php_intval(new_instance_["limit"]) if (not php_empty(lambda : new_instance_["limit"])) else -1
        return instance_
    # end def update
    #// 
    #// Outputs the settings form for the Links widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance_=None):
        
        
        #// Defaults.
        instance_ = wp_parse_args(instance_, Array({"images": True, "name": True, "description": False, "rating": False, "category": False, "orderby": "name", "limit": -1}))
        link_cats_ = get_terms(Array({"taxonomy": "link_category"}))
        limit_ = php_intval(instance_["limit"])
        if (not limit_):
            limit_ = -1
        # end if
        php_print("     <p>\n       <label for=\"")
        php_print(self.get_field_id("category"))
        php_print("\">")
        _e("Select Link Category:")
        php_print("</label>\n       <select class=\"widefat\" id=\"")
        php_print(self.get_field_id("category"))
        php_print("\" name=\"")
        php_print(self.get_field_name("category"))
        php_print("\">\n        <option value=\"\">")
        _ex("All Links", "links widget")
        php_print("</option>\n      ")
        for link_cat_ in link_cats_:
            php_print("<option value=\"" + php_intval(link_cat_.term_id) + "\"" + selected(instance_["category"], link_cat_.term_id, False) + ">" + link_cat_.name + "</option>\n")
        # end for
        php_print("     </select>\n     <label for=\"")
        php_print(self.get_field_id("orderby"))
        php_print("\">")
        _e("Sort by:")
        php_print("</label>\n       <select name=\"")
        php_print(self.get_field_name("orderby"))
        php_print("\" id=\"")
        php_print(self.get_field_id("orderby"))
        php_print("\" class=\"widefat\">\n          <option value=\"name\"")
        selected(instance_["orderby"], "name")
        php_print(">")
        _e("Link title")
        php_print("</option>\n          <option value=\"rating\"")
        selected(instance_["orderby"], "rating")
        php_print(">")
        _e("Link rating")
        php_print("</option>\n          <option value=\"id\"")
        selected(instance_["orderby"], "id")
        php_print(">")
        _e("Link ID")
        php_print("</option>\n          <option value=\"rand\"")
        selected(instance_["orderby"], "rand")
        php_print(">")
        _ex("Random", "Links widget")
        php_print("""</option>
        </select>
        </p>
        <p>
        <input class=\"checkbox\" type=\"checkbox\"""")
        checked(instance_["images"], True)
        php_print(" id=\"")
        php_print(self.get_field_id("images"))
        php_print("\" name=\"")
        php_print(self.get_field_name("images"))
        php_print("\" />\n      <label for=\"")
        php_print(self.get_field_id("images"))
        php_print("\">")
        _e("Show Link Image")
        php_print("</label><br />\n     <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance_["name"], True)
        php_print(" id=\"")
        php_print(self.get_field_id("name"))
        php_print("\" name=\"")
        php_print(self.get_field_name("name"))
        php_print("\" />\n      <label for=\"")
        php_print(self.get_field_id("name"))
        php_print("\">")
        _e("Show Link Name")
        php_print("</label><br />\n     <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance_["description"], True)
        php_print(" id=\"")
        php_print(self.get_field_id("description"))
        php_print("\" name=\"")
        php_print(self.get_field_name("description"))
        php_print("\" />\n      <label for=\"")
        php_print(self.get_field_id("description"))
        php_print("\">")
        _e("Show Link Description")
        php_print("</label><br />\n     <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance_["rating"], True)
        php_print(" id=\"")
        php_print(self.get_field_id("rating"))
        php_print("\" name=\"")
        php_print(self.get_field_name("rating"))
        php_print("\" />\n      <label for=\"")
        php_print(self.get_field_id("rating"))
        php_print("\">")
        _e("Show Link Rating")
        php_print("""</label>
        </p>
        <p>
        <label for=\"""")
        php_print(self.get_field_id("limit"))
        php_print("\">")
        _e("Number of links to show:")
        php_print("</label>\n       <input id=\"")
        php_print(self.get_field_id("limit"))
        php_print("\" name=\"")
        php_print(self.get_field_name("limit"))
        php_print("\" type=\"text\" value=\"")
        php_print(php_intval(limit_) if -1 != limit_ else "")
        php_print("\" size=\"3\" />\n       </p>\n      ")
    # end def form
# end class WP_Widget_Links
