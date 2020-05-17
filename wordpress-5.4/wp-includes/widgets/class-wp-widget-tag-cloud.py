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
#// Widget API: WP_Widget_Tag_Cloud class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a Tag cloud widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Tag_Cloud(WP_Widget):
    #// 
    #// Sets up a new Tag Cloud widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        
        widget_ops_ = Array({"description": __("A cloud of your most used tags."), "customize_selective_refresh": True})
        super().__init__("tag_cloud", __("Tag Cloud"), widget_ops_)
    # end def __init__
    #// 
    #// Outputs the content for the current Tag Cloud widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Tag Cloud widget instance.
    #//
    def widget(self, args_=None, instance_=None):
        
        
        current_taxonomy_ = self._get_current_taxonomy(instance_)
        if (not php_empty(lambda : instance_["title"])):
            title_ = instance_["title"]
        else:
            if "post_tag" == current_taxonomy_:
                title_ = __("Tags")
            else:
                tax_ = get_taxonomy(current_taxonomy_)
                title_ = tax_.labels.name
            # end if
        # end if
        show_count_ = (not php_empty(lambda : instance_["count"]))
        tag_cloud_ = wp_tag_cloud(apply_filters("widget_tag_cloud_args", Array({"taxonomy": current_taxonomy_, "echo": False, "show_count": show_count_}), instance_))
        if php_empty(lambda : tag_cloud_):
            return
        # end if
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title_ = apply_filters("widget_title", title_, instance_, self.id_base)
        php_print(args_["before_widget"])
        if title_:
            php_print(args_["before_title"] + title_ + args_["after_title"])
        # end if
        php_print("<div class=\"tagcloud\">")
        php_print(tag_cloud_)
        php_print("</div>\n")
        php_print(args_["after_widget"])
    # end def widget
    #// 
    #// Handles updating settings for the current Tag Cloud widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Settings to save or bool false to cancel saving.
    #//
    def update(self, new_instance_=None, old_instance_=None):
        
        
        instance_ = Array()
        instance_["title"] = sanitize_text_field(new_instance_["title"])
        instance_["count"] = 1 if (not php_empty(lambda : new_instance_["count"])) else 0
        instance_["taxonomy"] = stripslashes(new_instance_["taxonomy"])
        return instance_
    # end def update
    #// 
    #// Outputs the Tag Cloud widget settings form.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance_=None):
        
        
        current_taxonomy_ = self._get_current_taxonomy(instance_)
        title_id_ = self.get_field_id("title")
        count_ = php_bool(instance_["count"]) if (php_isset(lambda : instance_["count"])) else False
        instance_["title"] = esc_attr(instance_["title"]) if (not php_empty(lambda : instance_["title"])) else ""
        php_print("<p><label for=\"" + title_id_ + "\">" + __("Title:") + "</label>\n           <input type=\"text\" class=\"widefat\" id=\"" + title_id_ + "\" name=\"" + self.get_field_name("title") + "\" value=\"" + instance_["title"] + "\" />\n     </p>")
        taxonomies_ = get_taxonomies(Array({"show_tagcloud": True}), "object")
        id_ = self.get_field_id("taxonomy")
        name_ = self.get_field_name("taxonomy")
        input_ = "<input type=\"hidden\" id=\"" + id_ + "\" name=\"" + name_ + "\" value=\"%s\" />"
        count_checkbox_ = php_sprintf("<p><input type=\"checkbox\" class=\"checkbox\" id=\"%1$s\" name=\"%2$s\"%3$s /> <label for=\"%1$s\">%4$s</label></p>", self.get_field_id("count"), self.get_field_name("count"), checked(count_, True, False), __("Show tag counts"))
        for case in Switch(php_count(taxonomies_)):
            if case(0):
                php_print("<p>" + __("The tag cloud will not be displayed since there are no taxonomies that support the tag cloud widget.") + "</p>")
                printf(input_, "")
                break
            # end if
            if case(1):
                keys_ = php_array_keys(taxonomies_)
                taxonomy_ = reset(keys_)
                printf(input_, esc_attr(taxonomy_))
                php_print(count_checkbox_)
                break
            # end if
            if case():
                printf("<p><label for=\"%1$s\">%2$s</label>" + "<select class=\"widefat\" id=\"%1$s\" name=\"%3$s\">", id_, __("Taxonomy:"), name_)
                for taxonomy_,tax_ in taxonomies_:
                    printf("<option value=\"%s\"%s>%s</option>", esc_attr(taxonomy_), selected(taxonomy_, current_taxonomy_, False), tax_.labels.name)
                # end for
                php_print("</select></p>" + count_checkbox_)
            # end if
        # end for
    # end def form
    #// 
    #// Retrieves the taxonomy for the current Tag cloud widget instance.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $instance Current settings.
    #// @return string Name of the current taxonomy if set, otherwise 'post_tag'.
    #//
    def _get_current_taxonomy(self, instance_=None):
        
        
        if (not php_empty(lambda : instance_["taxonomy"])) and taxonomy_exists(instance_["taxonomy"]):
            return instance_["taxonomy"]
        # end if
        return "post_tag"
    # end def _get_current_taxonomy
# end class WP_Widget_Tag_Cloud
