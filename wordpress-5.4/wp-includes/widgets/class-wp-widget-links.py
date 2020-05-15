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
        
        widget_ops = Array({"description": __("Your blogroll"), "customize_selective_refresh": True})
        super().__init__("links", __("Links"), widget_ops)
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
    def widget(self, args=None, instance=None):
        
        show_description = instance["description"] if (php_isset(lambda : instance["description"])) else False
        show_name = instance["name"] if (php_isset(lambda : instance["name"])) else False
        show_rating = instance["rating"] if (php_isset(lambda : instance["rating"])) else False
        show_images = instance["images"] if (php_isset(lambda : instance["images"])) else True
        category = instance["category"] if (php_isset(lambda : instance["category"])) else False
        orderby = instance["orderby"] if (php_isset(lambda : instance["orderby"])) else "name"
        order = "DESC" if "rating" == orderby else "ASC"
        limit = instance["limit"] if (php_isset(lambda : instance["limit"])) else -1
        before_widget = php_preg_replace("/id=\"[^\"]*\"/", "id=\"%id\"", args["before_widget"])
        widget_links_args = Array({"title_before": args["before_title"], "title_after": args["after_title"], "category_before": before_widget, "category_after": args["after_widget"], "show_images": show_images, "show_description": show_description, "show_name": show_name, "show_rating": show_rating, "category": category, "class": "linkcat widget", "orderby": orderby, "order": order, "limit": limit})
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
        wp_list_bookmarks(apply_filters("widget_links_args", widget_links_args, instance))
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
    def update(self, new_instance=None, old_instance=None):
        
        new_instance = new_instance
        instance = Array({"images": 0, "name": 0, "description": 0, "rating": 0})
        for field,val in instance:
            if (php_isset(lambda : new_instance[field])):
                instance[field] = 1
            # end if
        # end for
        instance["orderby"] = "name"
        if php_in_array(new_instance["orderby"], Array("name", "rating", "id", "rand")):
            instance["orderby"] = new_instance["orderby"]
        # end if
        instance["category"] = php_intval(new_instance["category"])
        instance["limit"] = php_intval(new_instance["limit"]) if (not php_empty(lambda : new_instance["limit"])) else -1
        return instance
    # end def update
    #// 
    #// Outputs the settings form for the Links widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        #// Defaults.
        instance = wp_parse_args(instance, Array({"images": True, "name": True, "description": False, "rating": False, "category": False, "orderby": "name", "limit": -1}))
        link_cats = get_terms(Array({"taxonomy": "link_category"}))
        limit = php_intval(instance["limit"])
        if (not limit):
            limit = -1
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
        for link_cat in link_cats:
            php_print("<option value=\"" + php_intval(link_cat.term_id) + "\"" + selected(instance["category"], link_cat.term_id, False) + ">" + link_cat.name + "</option>\n")
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
        selected(instance["orderby"], "name")
        php_print(">")
        _e("Link title")
        php_print("</option>\n          <option value=\"rating\"")
        selected(instance["orderby"], "rating")
        php_print(">")
        _e("Link rating")
        php_print("</option>\n          <option value=\"id\"")
        selected(instance["orderby"], "id")
        php_print(">")
        _e("Link ID")
        php_print("</option>\n          <option value=\"rand\"")
        selected(instance["orderby"], "rand")
        php_print(">")
        _ex("Random", "Links widget")
        php_print("""</option>
        </select>
        </p>
        <p>
        <input class=\"checkbox\" type=\"checkbox\"""")
        checked(instance["images"], True)
        php_print(" id=\"")
        php_print(self.get_field_id("images"))
        php_print("\" name=\"")
        php_print(self.get_field_name("images"))
        php_print("\" />\n      <label for=\"")
        php_print(self.get_field_id("images"))
        php_print("\">")
        _e("Show Link Image")
        php_print("</label><br />\n     <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance["name"], True)
        php_print(" id=\"")
        php_print(self.get_field_id("name"))
        php_print("\" name=\"")
        php_print(self.get_field_name("name"))
        php_print("\" />\n      <label for=\"")
        php_print(self.get_field_id("name"))
        php_print("\">")
        _e("Show Link Name")
        php_print("</label><br />\n     <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance["description"], True)
        php_print(" id=\"")
        php_print(self.get_field_id("description"))
        php_print("\" name=\"")
        php_print(self.get_field_name("description"))
        php_print("\" />\n      <label for=\"")
        php_print(self.get_field_id("description"))
        php_print("\">")
        _e("Show Link Description")
        php_print("</label><br />\n     <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance["rating"], True)
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
        php_print(php_intval(limit) if -1 != limit else "")
        php_print("\" size=\"3\" />\n       </p>\n      ")
    # end def form
# end class WP_Widget_Links
