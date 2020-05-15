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
#// Widget API: WP_Widget base class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core base class extended to register widgets.
#// 
#// This class must be extended for each widget, and WP_Widget::widget() must be overridden.
#// 
#// If adding widget options, WP_Widget::update() and WP_Widget::form() should also be overridden.
#// 
#// @since 2.8.0
#// @since 4.4.0 Moved to its own file from wp-includes/widgets.php
#//
class WP_Widget():
    id_base = Array()
    name = Array()
    option_name = Array()
    alt_option_name = Array()
    widget_options = Array()
    control_options = Array()
    number = False
    id = False
    updated = False
    #// 
    #// Member functions that must be overridden by subclasses.
    #// 
    #// 
    #// Echoes the widget content.
    #// 
    #// Subclasses should override this function to generate their widget code.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance The settings for the particular instance of the widget.
    #//
    def widget(self, args=None, instance=None):
        
        php_print("function WP_Widget::widget() must be overridden in a subclass.")
        php_exit()
    # end def widget
    #// 
    #// Updates a particular instance of a widget.
    #// 
    #// This function should check that `$new_instance` is set correctly. The newly-calculated
    #// value of `$instance` should be returned. If false is returned, the instance won't be
    #// saved/updated.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Settings to save or bool false to cancel saving.
    #//
    def update(self, new_instance=None, old_instance=None):
        
        return new_instance
    # end def update
    #// 
    #// Outputs the settings update form.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #// @return string Default return is 'noform'.
    #//
    def form(self, instance=None):
        
        php_print("<p class=\"no-options-widget\">" + __("There are no options for this widget.") + "</p>")
        return "noform"
    # end def form
    #// Functions you'll need to call.
    #// 
    #// PHP5 constructor.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $id_base         Optional Base ID for the widget, lowercase and unique. If left empty,
    #// a portion of the widget's class name will be used Has to be unique.
    #// @param string $name            Name for the widget displayed on the configuration page.
    #// @param array  $widget_options  Optional. Widget options. See wp_register_sidebar_widget() for information
    #// on accepted arguments. Default empty array.
    #// @param array  $control_options Optional. Widget control options. See wp_register_widget_control() for
    #// information on accepted arguments. Default empty array.
    #//
    def __init__(self, id_base=None, name=None, widget_options=Array(), control_options=Array()):
        
        self.id_base = php_preg_replace("/(wp_)?widget_/", "", php_strtolower(get_class(self))) if php_empty(lambda : id_base) else php_strtolower(id_base)
        self.name = name
        self.option_name = "widget_" + self.id_base
        self.widget_options = wp_parse_args(widget_options, Array({"classname": self.option_name, "customize_selective_refresh": False}))
        self.control_options = wp_parse_args(control_options, Array({"id_base": self.id_base}))
    # end def __init__
    #// 
    #// PHP4 constructor.
    #// 
    #// @since 2.8.0
    #// @deprecated 4.3.0 Use __construct() instead.
    #// 
    #// @see WP_Widget::__construct()
    #// 
    #// @param string $id_base         Optional Base ID for the widget, lowercase and unique. If left empty,
    #// a portion of the widget's class name will be used Has to be unique.
    #// @param string $name            Name for the widget displayed on the configuration page.
    #// @param array  $widget_options  Optional. Widget options. See wp_register_sidebar_widget() for information
    #// on accepted arguments. Default empty array.
    #// @param array  $control_options Optional. Widget control options. See wp_register_widget_control() for
    #// information on accepted arguments. Default empty array.
    #//
    def wp_widget(self, id_base=None, name=None, widget_options=Array(), control_options=Array()):
        
        _deprecated_constructor("WP_Widget", "4.3.0", get_class(self))
        WP_Widget.__init__(id_base, name, widget_options, control_options)
    # end def wp_widget
    #// 
    #// Constructs name attributes for use in form() fields
    #// 
    #// This function should be used in form() methods to create name attributes for fields
    #// to be saved by update()
    #// 
    #// @since 2.8.0
    #// @since 4.4.0 Array format field names are now accepted.
    #// 
    #// @param string $field_name Field name
    #// @return string Name attribute for $field_name
    #//
    def get_field_name(self, field_name=None):
        
        pos = php_strpos(field_name, "[")
        if False == pos:
            return "widget-" + self.id_base + "[" + self.number + "][" + field_name + "]"
        else:
            return "widget-" + self.id_base + "[" + self.number + "][" + php_substr_replace(field_name, "][", pos, php_strlen("["))
        # end if
    # end def get_field_name
    #// 
    #// Constructs id attributes for use in WP_Widget::form() fields.
    #// 
    #// This function should be used in form() methods to create id attributes
    #// for fields to be saved by WP_Widget::update().
    #// 
    #// @since 2.8.0
    #// @since 4.4.0 Array format field IDs are now accepted.
    #// 
    #// @param string $field_name Field name.
    #// @return string ID attribute for `$field_name`.
    #//
    def get_field_id(self, field_name=None):
        
        return "widget-" + self.id_base + "-" + self.number + "-" + php_trim(php_str_replace(Array("[]", "[", "]"), Array("", "-", ""), field_name), "-")
    # end def get_field_id
    #// 
    #// Register all widget instances of this widget class.
    #// 
    #// @since 2.8.0
    #//
    def _register(self):
        
        settings = self.get_settings()
        empty = True
        #// When $settings is an array-like object, get an intrinsic array for use with array_keys().
        if type(settings).__name__ == "ArrayObject" or type(settings).__name__ == "ArrayIterator":
            settings = settings.getarraycopy()
        # end if
        if php_is_array(settings):
            for number in php_array_keys(settings):
                if php_is_numeric(number):
                    self._set(number)
                    self._register_one(number)
                    empty = False
                # end if
            # end for
        # end if
        if empty:
            #// If there are none, we register the widget's existence with a generic template.
            self._set(1)
            self._register_one()
        # end if
    # end def _register
    #// 
    #// Sets the internal order number for the widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param int $number The unique order number of this widget instance compared to other
    #// instances of the same class.
    #//
    def _set(self, number=None):
        
        self.number = number
        self.id = self.id_base + "-" + number
    # end def _set
    #// 
    #// Retrieves the widget display callback.
    #// 
    #// @since 2.8.0
    #// 
    #// @return callable Display callback.
    #//
    def _get_display_callback(self):
        
        return Array(self, "display_callback")
    # end def _get_display_callback
    #// 
    #// Retrieves the widget update callback.
    #// 
    #// @since 2.8.0
    #// 
    #// @return callable Update callback.
    #//
    def _get_update_callback(self):
        
        return Array(self, "update_callback")
    # end def _get_update_callback
    #// 
    #// Retrieves the form callback.
    #// 
    #// @since 2.8.0
    #// 
    #// @return callable Form callback.
    #//
    def _get_form_callback(self):
        
        return Array(self, "form_callback")
    # end def _get_form_callback
    #// 
    #// Determines whether the current request is inside the Customizer preview.
    #// 
    #// If true -- the current request is inside the Customizer preview, then
    #// the object cache gets suspended and widgets should check this to decide
    #// whether they should store anything persistently to the object cache,
    #// to transients, or anywhere else.
    #// 
    #// @since 3.9.0
    #// 
    #// @global WP_Customize_Manager $wp_customize
    #// 
    #// @return bool True if within the Customizer preview, false if not.
    #//
    def is_preview(self):
        
        global wp_customize
        php_check_if_defined("wp_customize")
        return (php_isset(lambda : wp_customize)) and wp_customize.is_preview()
    # end def is_preview
    #// 
    #// Generates the actual widget content (Do NOT override).
    #// 
    #// Finds the instance and calls WP_Widget::widget().
    #// 
    #// @since 2.8.0
    #// 
    #// @param array     $args        Display arguments. See WP_Widget::widget() for information
    #// on accepted arguments.
    #// @param int|array $widget_args {
    #// Optional. Internal order number of the widget instance, or array of multi-widget arguments.
    #// Default 1.
    #// 
    #// @type int $number Number increment used for multiples of the same widget.
    #// }
    #//
    def display_callback(self, args=None, widget_args=1):
        
        if php_is_numeric(widget_args):
            widget_args = Array({"number": widget_args})
        # end if
        widget_args = wp_parse_args(widget_args, Array({"number": -1}))
        self._set(widget_args["number"])
        instances = self.get_settings()
        if php_array_key_exists(self.number, instances):
            instance = instances[self.number]
            #// 
            #// Filters the settings for a particular widget instance.
            #// 
            #// Returning false will effectively short-circuit display of the widget.
            #// 
            #// @since 2.8.0
            #// 
            #// @param array     $instance The current widget instance's settings.
            #// @param WP_Widget $this     The current widget instance.
            #// @param array     $args     An array of default widget arguments.
            #//
            instance = apply_filters("widget_display_callback", instance, self, args)
            if False == instance:
                return
            # end if
            was_cache_addition_suspended = wp_suspend_cache_addition()
            if self.is_preview() and (not was_cache_addition_suspended):
                wp_suspend_cache_addition(True)
            # end if
            self.widget(args, instance)
            if self.is_preview():
                wp_suspend_cache_addition(was_cache_addition_suspended)
            # end if
        # end if
    # end def display_callback
    #// 
    #// Handles changed settings (Do NOT override).
    #// 
    #// @since 2.8.0
    #// 
    #// @global array $wp_registered_widgets
    #// 
    #// @param int $deprecated Not used.
    #//
    def update_callback(self, deprecated=1):
        
        global wp_registered_widgets
        php_check_if_defined("wp_registered_widgets")
        all_instances = self.get_settings()
        #// We need to update the data.
        if self.updated:
            return
        # end if
        if (php_isset(lambda : PHP_POST["delete_widget"])) and PHP_POST["delete_widget"]:
            #// Delete the settings for this instance of the widget.
            if (php_isset(lambda : PHP_POST["the-widget-id"])):
                del_id = PHP_POST["the-widget-id"]
            else:
                return
            # end if
            if (php_isset(lambda : wp_registered_widgets[del_id]["params"][0]["number"])):
                number = wp_registered_widgets[del_id]["params"][0]["number"]
                if self.id_base + "-" + number == del_id:
                    all_instances[number] = None
                # end if
            # end if
        else:
            if (php_isset(lambda : PHP_POST["widget-" + self.id_base])) and php_is_array(PHP_POST["widget-" + self.id_base]):
                settings = PHP_POST["widget-" + self.id_base]
            elif (php_isset(lambda : PHP_POST["id_base"])) and PHP_POST["id_base"] == self.id_base:
                num = int(PHP_POST["multi_number"]) if PHP_POST["multi_number"] else int(PHP_POST["widget_number"])
                settings = Array({num: Array()})
            else:
                return
            # end if
            for number,new_instance in settings:
                new_instance = stripslashes_deep(new_instance)
                self._set(number)
                old_instance = all_instances[number] if (php_isset(lambda : all_instances[number])) else Array()
                was_cache_addition_suspended = wp_suspend_cache_addition()
                if self.is_preview() and (not was_cache_addition_suspended):
                    wp_suspend_cache_addition(True)
                # end if
                instance = self.update(new_instance, old_instance)
                if self.is_preview():
                    wp_suspend_cache_addition(was_cache_addition_suspended)
                # end if
                #// 
                #// Filters a widget's settings before saving.
                #// 
                #// Returning false will effectively short-circuit the widget's ability
                #// to update settings.
                #// 
                #// @since 2.8.0
                #// 
                #// @param array     $instance     The current widget instance's settings.
                #// @param array     $new_instance Array of new widget settings.
                #// @param array     $old_instance Array of old widget settings.
                #// @param WP_Widget $this         The current widget instance.
                #//
                instance = apply_filters("widget_update_callback", instance, new_instance, old_instance, self)
                if False != instance:
                    all_instances[number] = instance
                # end if
                break
                pass
            # end for
        # end if
        self.save_settings(all_instances)
        self.updated = True
    # end def update_callback
    #// 
    #// Generates the widget control form (Do NOT override).
    #// 
    #// @since 2.8.0
    #// 
    #// @param int|array $widget_args {
    #// Optional. Internal order number of the widget instance, or array of multi-widget arguments.
    #// Default 1.
    #// 
    #// @type int $number Number increment used for multiples of the same widget.
    #// }
    #// @return string|null
    #//
    def form_callback(self, widget_args=1):
        
        if php_is_numeric(widget_args):
            widget_args = Array({"number": widget_args})
        # end if
        widget_args = wp_parse_args(widget_args, Array({"number": -1}))
        all_instances = self.get_settings()
        if -1 == widget_args["number"]:
            #// We echo out a form where 'number' can be set later.
            self._set("__i__")
            instance = Array()
        else:
            self._set(widget_args["number"])
            instance = all_instances[widget_args["number"]]
        # end if
        #// 
        #// Filters the widget instance's settings before displaying the control form.
        #// 
        #// Returning false effectively short-circuits display of the control form.
        #// 
        #// @since 2.8.0
        #// 
        #// @param array     $instance The current widget instance's settings.
        #// @param WP_Widget $this     The current widget instance.
        #//
        instance = apply_filters("widget_form_callback", instance, self)
        return_ = None
        if False != instance:
            return_ = self.form(instance)
            #// 
            #// Fires at the end of the widget control form.
            #// 
            #// Use this hook to add extra fields to the widget form. The hook
            #// is only fired if the value passed to the 'widget_form_callback'
            #// hook is not false.
            #// 
            #// Note: If the widget has no form, the text echoed from the default
            #// form method can be hidden using CSS.
            #// 
            #// @since 2.8.0
            #// 
            #// @param WP_Widget $this     The widget instance (passed by reference).
            #// @param null      $return   Return null if new fields are added.
            #// @param array     $instance An array of the widget's settings.
            #//
            do_action_ref_array("in_widget_form", Array(self, return_, instance))
        # end if
        return return_
    # end def form_callback
    #// 
    #// Registers an instance of the widget class.
    #// 
    #// @since 2.8.0
    #// 
    #// @param integer $number Optional. The unique order number of this widget instance
    #// compared to other instances of the same class. Default -1.
    #//
    def _register_one(self, number=-1):
        
        wp_register_sidebar_widget(self.id, self.name, self._get_display_callback(), self.widget_options, Array({"number": number}))
        _register_widget_update_callback(self.id_base, self._get_update_callback(), self.control_options, Array({"number": -1}))
        _register_widget_form_callback(self.id, self.name, self._get_form_callback(), self.control_options, Array({"number": number}))
    # end def _register_one
    #// 
    #// Saves the settings for all instances of the widget class.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $settings Multi-dimensional array of widget instance settings.
    #//
    def save_settings(self, settings=None):
        
        settings["_multiwidget"] = 1
        update_option(self.option_name, settings)
    # end def save_settings
    #// 
    #// Retrieves the settings for all instances of the widget class.
    #// 
    #// @since 2.8.0
    #// 
    #// @return array Multi-dimensional array of widget instance settings.
    #//
    def get_settings(self):
        
        settings = get_option(self.option_name)
        if False == settings:
            if (php_isset(lambda : self.alt_option_name)):
                settings = get_option(self.alt_option_name)
            else:
                #// Save an option so it can be autoloaded next time.
                self.save_settings(Array())
            # end if
        # end if
        if (not php_is_array(settings)) and (not type(settings).__name__ == "ArrayObject" or type(settings).__name__ == "ArrayIterator"):
            settings = Array()
        # end if
        if (not php_empty(lambda : settings)) and (not (php_isset(lambda : settings["_multiwidget"]))):
            #// Old format, convert if single widget.
            settings = wp_convert_widget_settings(self.id_base, self.option_name, settings)
        # end if
        settings["_multiwidget"] = None
        settings["__i__"] = None
        return settings
    # end def get_settings
# end class WP_Widget
