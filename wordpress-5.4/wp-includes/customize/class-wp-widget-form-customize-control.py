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
#// Customize API: WP_Widget_Form_Customize_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Widget Form Customize Control class.
#// 
#// @since 3.9.0
#// 
#// @see WP_Customize_Control
#//
class WP_Widget_Form_Customize_Control(WP_Customize_Control):
    type = "widget_form"
    widget_id = Array()
    widget_id_base = Array()
    sidebar_id = Array()
    is_new = False
    width = Array()
    height = Array()
    is_wide = False
    #// 
    #// Gather control params for exporting to JavaScript.
    #// 
    #// @since 3.9.0
    #// 
    #// @global array $wp_registered_widgets
    #//
    def to_json(self):
        
        global wp_registered_widgets
        php_check_if_defined("wp_registered_widgets")
        super().to_json()
        exported_properties = Array("widget_id", "widget_id_base", "sidebar_id", "width", "height", "is_wide")
        for key in exported_properties:
            self.json[key] = self.key
        # end for
        #// Get the widget_control and widget_content.
        php_include_file(ABSPATH + "wp-admin/includes/widgets.php", once=True)
        widget = wp_registered_widgets[self.widget_id]
        if (not (php_isset(lambda : widget["params"][0]))):
            widget["params"][0] = Array()
        # end if
        args = Array({"widget_id": widget["id"], "widget_name": widget["name"]})
        args = wp_list_widget_controls_dynamic_sidebar(Array({0: args, 1: widget["params"][0]}))
        widget_control_parts = self.manager.widgets.get_widget_control_parts(args)
        self.json["widget_control"] = widget_control_parts["control"]
        self.json["widget_content"] = widget_control_parts["content"]
    # end def to_json
    #// 
    #// Override render_content to be no-op since content is exported via to_json for deferred embedding.
    #// 
    #// @since 3.9.0
    #//
    def render_content(self):
        
        pass
    # end def render_content
    #// 
    #// Whether the current widget is rendered on the page.
    #// 
    #// @since 4.0.0
    #// 
    #// @return bool Whether the widget is rendered.
    #//
    def active_callback(self):
        
        return self.manager.widgets.is_widget_rendered(self.widget_id)
    # end def active_callback
# end class WP_Widget_Form_Customize_Control
