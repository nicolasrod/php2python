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
    #// 
    #// Root ID for all widgets of this type.
    #// 
    #// @since 2.8.0
    #// @var mixed|string
    #//
    id_base = Array()
    #// 
    #// Name for this widget type.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    name = Array()
    #// 
    #// Option name for this widget type.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    option_name = Array()
    #// 
    #// Alt option name for this widget type.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    alt_option_name = Array()
    #// 
    #// Option array passed to wp_register_sidebar_widget().
    #// 
    #// @since 2.8.0
    #// @var array
    #//
    widget_options = Array()
    #// 
    #// Option array passed to wp_register_widget_control().
    #// 
    #// @since 2.8.0
    #// @var array
    #//
    control_options = Array()
    #// 
    #// Unique ID number of the current instance.
    #// 
    #// @since 2.8.0
    #// @var bool|int
    #//
    number = False
    #// 
    #// Unique ID string of the current instance (id_base-number).
    #// 
    #// @since 2.8.0
    #// @var bool|string
    #//
    id = False
    #// 
    #// Whether the widget data has been updated.
    #// 
    #// Set to true when the data is updated after a POST submit - ensures it does
    #// not happen twice.
    #// 
    #// @since 2.8.0
    #// @var bool
    #//
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
    def widget(self, args_=None, instance_=None):
        
        
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
    def update(self, new_instance_=None, old_instance_=None):
        
        
        return new_instance_
    # end def update
    #// 
    #// Outputs the settings update form.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #// @return string Default return is 'noform'.
    #//
    def form(self, instance_=None):
        
        
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
    def __init__(self, id_base_=None, name_=None, widget_options_=None, control_options_=None):
        if widget_options_ is None:
            widget_options_ = Array()
        # end if
        if control_options_ is None:
            control_options_ = Array()
        # end if
        
        self.id_base = php_preg_replace("/(wp_)?widget_/", "", php_strtolower(get_class(self))) if php_empty(lambda : id_base_) else php_strtolower(id_base_)
        self.name = name_
        self.option_name = "widget_" + self.id_base
        self.widget_options = wp_parse_args(widget_options_, Array({"classname": self.option_name, "customize_selective_refresh": False}))
        self.control_options = wp_parse_args(control_options_, Array({"id_base": self.id_base}))
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
    def wp_widget(self, id_base_=None, name_=None, widget_options_=None, control_options_=None):
        if widget_options_ is None:
            widget_options_ = Array()
        # end if
        if control_options_ is None:
            control_options_ = Array()
        # end if
        
        _deprecated_constructor("WP_Widget", "4.3.0", get_class(self))
        WP_Widget.__init__(id_base_, name_, widget_options_, control_options_)
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
    def get_field_name(self, field_name_=None):
        
        
        pos_ = php_strpos(field_name_, "[")
        if False == pos_:
            return "widget-" + self.id_base + "[" + self.number + "][" + field_name_ + "]"
        else:
            return "widget-" + self.id_base + "[" + self.number + "][" + php_substr_replace(field_name_, "][", pos_, php_strlen("["))
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
    def get_field_id(self, field_name_=None):
        
        
        return "widget-" + self.id_base + "-" + self.number + "-" + php_trim(php_str_replace(Array("[]", "[", "]"), Array("", "-", ""), field_name_), "-")
    # end def get_field_id
    #// 
    #// Register all widget instances of this widget class.
    #// 
    #// @since 2.8.0
    #//
    def _register(self):
        
        
        settings_ = self.get_settings()
        empty_ = True
        #// When $settings is an array-like object, get an intrinsic array for use with array_keys().
        if type(settings_).__name__ == "ArrayObject" or type(settings_).__name__ == "ArrayIterator":
            settings_ = settings_.getarraycopy()
        # end if
        if php_is_array(settings_):
            for number_ in php_array_keys(settings_):
                if php_is_numeric(number_):
                    self._set(number_)
                    self._register_one(number_)
                    empty_ = False
                # end if
            # end for
        # end if
        if empty_:
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
    def _set(self, number_=None):
        
        
        self.number = number_
        self.id = self.id_base + "-" + number_
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
        
        
        global wp_customize_
        php_check_if_defined("wp_customize_")
        return (php_isset(lambda : wp_customize_)) and wp_customize_.is_preview()
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
    def display_callback(self, args_=None, widget_args_=1):
        
        
        if php_is_numeric(widget_args_):
            widget_args_ = Array({"number": widget_args_})
        # end if
        widget_args_ = wp_parse_args(widget_args_, Array({"number": -1}))
        self._set(widget_args_["number"])
        instances_ = self.get_settings()
        if php_array_key_exists(self.number, instances_):
            instance_ = instances_[self.number]
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
            instance_ = apply_filters("widget_display_callback", instance_, self, args_)
            if False == instance_:
                return
            # end if
            was_cache_addition_suspended_ = wp_suspend_cache_addition()
            if self.is_preview() and (not was_cache_addition_suspended_):
                wp_suspend_cache_addition(True)
            # end if
            self.widget(args_, instance_)
            if self.is_preview():
                wp_suspend_cache_addition(was_cache_addition_suspended_)
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
    def update_callback(self, deprecated_=1):
        
        
        global wp_registered_widgets_
        php_check_if_defined("wp_registered_widgets_")
        all_instances_ = self.get_settings()
        #// We need to update the data.
        if self.updated:
            return
        # end if
        if (php_isset(lambda : PHP_POST["delete_widget"])) and PHP_POST["delete_widget"]:
            #// Delete the settings for this instance of the widget.
            if (php_isset(lambda : PHP_POST["the-widget-id"])):
                del_id_ = PHP_POST["the-widget-id"]
            else:
                return
            # end if
            if (php_isset(lambda : wp_registered_widgets_[del_id_]["params"][0]["number"])):
                number_ = wp_registered_widgets_[del_id_]["params"][0]["number"]
                if self.id_base + "-" + number_ == del_id_:
                    all_instances_[number_] = None
                # end if
            # end if
        else:
            if (php_isset(lambda : PHP_POST["widget-" + self.id_base])) and php_is_array(PHP_POST["widget-" + self.id_base]):
                settings_ = PHP_POST["widget-" + self.id_base]
            elif (php_isset(lambda : PHP_POST["id_base"])) and PHP_POST["id_base"] == self.id_base:
                num_ = php_int(PHP_POST["multi_number"]) if PHP_POST["multi_number"] else php_int(PHP_POST["widget_number"])
                settings_ = Array({num_: Array()})
            else:
                return
            # end if
            for number_,new_instance_ in settings_:
                new_instance_ = stripslashes_deep(new_instance_)
                self._set(number_)
                old_instance_ = all_instances_[number_] if (php_isset(lambda : all_instances_[number_])) else Array()
                was_cache_addition_suspended_ = wp_suspend_cache_addition()
                if self.is_preview() and (not was_cache_addition_suspended_):
                    wp_suspend_cache_addition(True)
                # end if
                instance_ = self.update(new_instance_, old_instance_)
                if self.is_preview():
                    wp_suspend_cache_addition(was_cache_addition_suspended_)
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
                instance_ = apply_filters("widget_update_callback", instance_, new_instance_, old_instance_, self)
                if False != instance_:
                    all_instances_[number_] = instance_
                # end if
                break
                pass
            # end for
        # end if
        self.save_settings(all_instances_)
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
    def form_callback(self, widget_args_=1):
        
        
        if php_is_numeric(widget_args_):
            widget_args_ = Array({"number": widget_args_})
        # end if
        widget_args_ = wp_parse_args(widget_args_, Array({"number": -1}))
        all_instances_ = self.get_settings()
        if -1 == widget_args_["number"]:
            #// We echo out a form where 'number' can be set later.
            self._set("__i__")
            instance_ = Array()
        else:
            self._set(widget_args_["number"])
            instance_ = all_instances_[widget_args_["number"]]
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
        instance_ = apply_filters("widget_form_callback", instance_, self)
        return_ = None
        if False != instance_:
            return_ = self.form(instance_)
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
            do_action_ref_array("in_widget_form", Array(self, return_, instance_))
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
    def _register_one(self, number_=None):
        if number_ is None:
            number_ = -1
        # end if
        
        wp_register_sidebar_widget(self.id, self.name, self._get_display_callback(), self.widget_options, Array({"number": number_}))
        _register_widget_update_callback(self.id_base, self._get_update_callback(), self.control_options, Array({"number": -1}))
        _register_widget_form_callback(self.id, self.name, self._get_form_callback(), self.control_options, Array({"number": number_}))
    # end def _register_one
    #// 
    #// Saves the settings for all instances of the widget class.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $settings Multi-dimensional array of widget instance settings.
    #//
    def save_settings(self, settings_=None):
        
        
        settings_["_multiwidget"] = 1
        update_option(self.option_name, settings_)
    # end def save_settings
    #// 
    #// Retrieves the settings for all instances of the widget class.
    #// 
    #// @since 2.8.0
    #// 
    #// @return array Multi-dimensional array of widget instance settings.
    #//
    def get_settings(self):
        
        
        settings_ = get_option(self.option_name)
        if False == settings_:
            if (php_isset(lambda : self.alt_option_name)):
                settings_ = get_option(self.alt_option_name)
            else:
                #// Save an option so it can be autoloaded next time.
                self.save_settings(Array())
            # end if
        # end if
        if (not php_is_array(settings_)) and (not type(settings_).__name__ == "ArrayObject" or type(settings_).__name__ == "ArrayIterator"):
            settings_ = Array()
        # end if
        if (not php_empty(lambda : settings_)) and (not (php_isset(lambda : settings_["_multiwidget"]))):
            #// Old format, convert if single widget.
            settings_ = wp_convert_widget_settings(self.id_base, self.option_name, settings_)
        # end if
        settings_["_multiwidget"] = None
        settings_["__i__"] = None
        return settings_
    # end def get_settings
# end class WP_Widget
