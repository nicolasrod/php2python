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
    #// 
    #// Customize control type.
    #// 
    #// @since 3.9.0
    #// @var string
    #//
    type = "widget_form"
    #// 
    #// Widget ID.
    #// 
    #// @since 3.9.0
    #// @var string
    #//
    widget_id = Array()
    #// 
    #// Widget ID base.
    #// 
    #// @since 3.9.0
    #// @var string
    #//
    widget_id_base = Array()
    #// 
    #// Sidebar ID.
    #// 
    #// @since 3.9.0
    #// @var string
    #//
    sidebar_id = Array()
    #// 
    #// Widget status.
    #// 
    #// @since 3.9.0
    #// @var bool True if new, false otherwise. Default false.
    #//
    is_new = False
    #// 
    #// Widget width.
    #// 
    #// @since 3.9.0
    #// @var int
    #//
    width = Array()
    #// 
    #// Widget height.
    #// 
    #// @since 3.9.0
    #// @var int
    #//
    height = Array()
    #// 
    #// Widget mode.
    #// 
    #// @since 3.9.0
    #// @var bool True if wide, false otherwise. Default false.
    #//
    is_wide = False
    #// 
    #// Gather control params for exporting to JavaScript.
    #// 
    #// @since 3.9.0
    #// 
    #// @global array $wp_registered_widgets
    #//
    def to_json(self):
        
        
        global wp_registered_widgets_
        php_check_if_defined("wp_registered_widgets_")
        super().to_json()
        exported_properties_ = Array("widget_id", "widget_id_base", "sidebar_id", "width", "height", "is_wide")
        for key_ in exported_properties_:
            self.json[key_] = self.key_
        # end for
        #// Get the widget_control and widget_content.
        php_include_file(ABSPATH + "wp-admin/includes/widgets.php", once=True)
        widget_ = wp_registered_widgets_[self.widget_id]
        if (not (php_isset(lambda : widget_["params"][0]))):
            widget_["params"][0] = Array()
        # end if
        args_ = Array({"widget_id": widget_["id"], "widget_name": widget_["name"]})
        args_ = wp_list_widget_controls_dynamic_sidebar(Array({0: args_, 1: widget_["params"][0]}))
        widget_control_parts_ = self.manager.widgets.get_widget_control_parts(args_)
        self.json["widget_control"] = widget_control_parts_["control"]
        self.json["widget_content"] = widget_control_parts_["content"]
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
