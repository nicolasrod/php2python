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
#// WordPress Customize Widgets classes
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 3.9.0
#// 
#// 
#// Customize Widgets class.
#// 
#// Implements widget management in the Customizer.
#// 
#// @since 3.9.0
#// 
#// @see WP_Customize_Manager
#//
class WP_Customize_Widgets():
    #// 
    #// WP_Customize_Manager instance.
    #// 
    #// @since 3.9.0
    #// @var WP_Customize_Manager
    #//
    manager = Array()
    #// 
    #// All id_bases for widgets defined in core.
    #// 
    #// @since 3.9.0
    #// @var array
    #//
    core_widget_id_bases = Array("archives", "calendar", "categories", "custom_html", "links", "media_audio", "media_image", "media_video", "meta", "nav_menu", "pages", "recent-comments", "recent-posts", "rss", "search", "tag_cloud", "text")
    #// 
    #// @since 3.9.0
    #// @var array
    #//
    rendered_sidebars = Array()
    #// 
    #// @since 3.9.0
    #// @var array
    #//
    rendered_widgets = Array()
    #// 
    #// @since 3.9.0
    #// @var array
    #//
    old_sidebars_widgets = Array()
    #// 
    #// Mapping of widget ID base to whether it supports selective refresh.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    selective_refreshable_widgets = Array()
    #// 
    #// Mapping of setting type to setting ID pattern.
    #// 
    #// @since 4.2.0
    #// @var array
    #//
    setting_id_patterns = Array({"widget_instance": "/^widget_(?P<id_base>.+?)(?:\\[(?P<widget_number>\\d+)\\])?$/", "sidebar_widgets": "/^sidebars_widgets\\[(?P<sidebar_id>.+?)\\]$/"})
    #// 
    #// Initial loader.
    #// 
    #// @since 3.9.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #//
    def __init__(self, manager_=None):
        
        
        self.manager = manager_
        #// See https://github.com/xwp/wp-customize-snapshots/blob/962586659688a5b1fd9ae93618b7ce2d4e7a421c/php/class-customize-snapshot-manager.php#L420-L449
        add_filter("customize_dynamic_setting_args", Array(self, "filter_customize_dynamic_setting_args"), 10, 2)
        add_action("widgets_init", Array(self, "register_settings"), 95)
        add_action("customize_register", Array(self, "schedule_customize_register"), 1)
        #// Skip remaining hooks when the user can't manage widgets anyway.
        if (not current_user_can("edit_theme_options")):
            return
        # end if
        add_action("wp_loaded", Array(self, "override_sidebars_widgets_for_theme_switch"))
        add_action("customize_controls_init", Array(self, "customize_controls_init"))
        add_action("customize_controls_enqueue_scripts", Array(self, "enqueue_scripts"))
        add_action("customize_controls_print_styles", Array(self, "print_styles"))
        add_action("customize_controls_print_scripts", Array(self, "print_scripts"))
        add_action("customize_controls_print_footer_scripts", Array(self, "print_footer_scripts"))
        add_action("customize_controls_print_footer_scripts", Array(self, "output_widget_control_templates"))
        add_action("customize_preview_init", Array(self, "customize_preview_init"))
        add_filter("customize_refresh_nonces", Array(self, "refresh_nonces"))
        add_action("dynamic_sidebar", Array(self, "tally_rendered_widgets"))
        add_filter("is_active_sidebar", Array(self, "tally_sidebars_via_is_active_sidebar_calls"), 10, 2)
        add_filter("dynamic_sidebar_has_widgets", Array(self, "tally_sidebars_via_dynamic_sidebar_calls"), 10, 2)
        #// Selective Refresh.
        add_filter("customize_dynamic_partial_args", Array(self, "customize_dynamic_partial_args"), 10, 2)
        add_action("customize_preview_init", Array(self, "selective_refresh_init"))
    # end def __init__
    #// 
    #// List whether each registered widget can be use selective refresh.
    #// 
    #// If the theme does not support the customize-selective-refresh-widgets feature,
    #// then this will always return an empty array.
    #// 
    #// @since 4.5.0
    #// 
    #// @global WP_Widget_Factory $wp_widget_factory
    #// 
    #// @return array Mapping of id_base to support. If theme doesn't support
    #// selective refresh, an empty array is returned.
    #//
    def get_selective_refreshable_widgets(self):
        
        
        global wp_widget_factory_
        php_check_if_defined("wp_widget_factory_")
        if (not current_theme_supports("customize-selective-refresh-widgets")):
            return Array()
        # end if
        if (not (php_isset(lambda : self.selective_refreshable_widgets))):
            self.selective_refreshable_widgets = Array()
            for wp_widget_ in wp_widget_factory_.widgets:
                self.selective_refreshable_widgets[wp_widget_.id_base] = (not php_empty(lambda : wp_widget_.widget_options["customize_selective_refresh"]))
            # end for
        # end if
        return self.selective_refreshable_widgets
    # end def get_selective_refreshable_widgets
    #// 
    #// Determines if a widget supports selective refresh.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $id_base Widget ID Base.
    #// @return bool Whether the widget can be selective refreshed.
    #//
    def is_widget_selective_refreshable(self, id_base_=None):
        
        
        selective_refreshable_widgets_ = self.get_selective_refreshable_widgets()
        return (not php_empty(lambda : selective_refreshable_widgets_[id_base_]))
    # end def is_widget_selective_refreshable
    #// 
    #// Retrieves the widget setting type given a setting ID.
    #// 
    #// @since 4.2.0
    #// 
    #// @staticvar array $cache
    #// 
    #// @param string $setting_id Setting ID.
    #// @return string|void Setting type.
    #//
    def get_setting_type(self, setting_id_=None):
        
        
        cache_ = Array()
        if (php_isset(lambda : cache_[setting_id_])):
            return cache_[setting_id_]
        # end if
        for type_,pattern_ in self.setting_id_patterns:
            if php_preg_match(pattern_, setting_id_):
                cache_[setting_id_] = type_
                return type_
            # end if
        # end for
    # end def get_setting_type
    #// 
    #// Inspects the incoming customized data for any widget settings, and dynamically adds
    #// them up-front so widgets will be initialized properly.
    #// 
    #// @since 4.2.0
    #//
    def register_settings(self):
        
        
        widget_setting_ids_ = Array()
        incoming_setting_ids_ = php_array_keys(self.manager.unsanitized_post_values())
        for setting_id_ in incoming_setting_ids_:
            if (not is_null(self.get_setting_type(setting_id_))):
                widget_setting_ids_[-1] = setting_id_
            # end if
        # end for
        if self.manager.doing_ajax("update-widget") and (php_isset(lambda : PHP_REQUEST["widget-id"])):
            widget_setting_ids_[-1] = self.get_setting_id(wp_unslash(PHP_REQUEST["widget-id"]))
        # end if
        settings_ = self.manager.add_dynamic_settings(array_unique(widget_setting_ids_))
        if self.manager.settings_previewed():
            for setting_ in settings_:
                setting_.preview()
            # end for
        # end if
    # end def register_settings
    #// 
    #// Determines the arguments for a dynamically-created setting.
    #// 
    #// @since 4.2.0
    #// 
    #// @param false|array $args       The arguments to the WP_Customize_Setting constructor.
    #// @param string      $setting_id ID for dynamic setting, usually coming from `$_POST['customized']`.
    #// @return array|false Setting arguments, false otherwise.
    #//
    def filter_customize_dynamic_setting_args(self, args_=None, setting_id_=None):
        
        
        if self.get_setting_type(setting_id_):
            args_ = self.get_setting_args(setting_id_)
        # end if
        return args_
    # end def filter_customize_dynamic_setting_args
    #// 
    #// Retrieves an unslashed post value or return a default.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $name    Post value.
    #// @param mixed  $default Default post value.
    #// @return mixed Unslashed post value or default value.
    #//
    def get_post_value(self, name_=None, default_=None):
        
        
        if (not (php_isset(lambda : PHP_POST[name_]))):
            return default_
        # end if
        return wp_unslash(PHP_POST[name_])
    # end def get_post_value
    #// 
    #// Override sidebars_widgets for theme switch.
    #// 
    #// When switching a theme via the Customizer, supply any previously-configured
    #// sidebars_widgets from the target theme as the initial sidebars_widgets
    #// setting. Also store the old theme's existing settings so that they can
    #// be passed along for storing in the sidebars_widgets theme_mod when the
    #// theme gets switched.
    #// 
    #// @since 3.9.0
    #// 
    #// @global array $sidebars_widgets
    #// @global array $_wp_sidebars_widgets
    #//
    def override_sidebars_widgets_for_theme_switch(self):
        
        
        global sidebars_widgets_
        php_check_if_defined("sidebars_widgets_")
        if self.manager.doing_ajax() or self.manager.is_theme_active():
            return
        # end if
        self.old_sidebars_widgets = wp_get_sidebars_widgets()
        add_filter("customize_value_old_sidebars_widgets_data", Array(self, "filter_customize_value_old_sidebars_widgets_data"))
        self.manager.set_post_value("old_sidebars_widgets_data", self.old_sidebars_widgets)
        #// Override any value cached in changeset.
        #// retrieve_widgets() looks at the global $sidebars_widgets.
        sidebars_widgets_ = self.old_sidebars_widgets
        sidebars_widgets_ = retrieve_widgets("customize")
        add_filter("option_sidebars_widgets", Array(self, "filter_option_sidebars_widgets_for_theme_switch"), 1)
        PHP_GLOBALS["_wp_sidebars_widgets"] = None
    # end def override_sidebars_widgets_for_theme_switch
    #// 
    #// Filters old_sidebars_widgets_data Customizer setting.
    #// 
    #// When switching themes, filter the Customizer setting old_sidebars_widgets_data
    #// to supply initial $sidebars_widgets before they were overridden by retrieve_widgets().
    #// The value for old_sidebars_widgets_data gets set in the old theme's sidebars_widgets
    #// theme_mod.
    #// 
    #// @since 3.9.0
    #// 
    #// @see WP_Customize_Widgets::handle_theme_switch()
    #// 
    #// @param array $old_sidebars_widgets
    #// @return array
    #//
    def filter_customize_value_old_sidebars_widgets_data(self, old_sidebars_widgets_=None):
        
        
        return self.old_sidebars_widgets
    # end def filter_customize_value_old_sidebars_widgets_data
    #// 
    #// Filters sidebars_widgets option for theme switch.
    #// 
    #// When switching themes, the retrieve_widgets() function is run when the Customizer initializes,
    #// and then the new sidebars_widgets here get supplied as the default value for the sidebars_widgets
    #// option.
    #// 
    #// @since 3.9.0
    #// 
    #// @see WP_Customize_Widgets::handle_theme_switch()
    #// @global array $sidebars_widgets
    #// 
    #// @param array $sidebars_widgets
    #// @return array
    #//
    def filter_option_sidebars_widgets_for_theme_switch(self, sidebars_widgets_=None):
        
        
        sidebars_widgets_ = PHP_GLOBALS["sidebars_widgets"]
        sidebars_widgets_["array_version"] = 3
        return sidebars_widgets_
    # end def filter_option_sidebars_widgets_for_theme_switch
    #// 
    #// Ensures all widgets get loaded into the Customizer.
    #// 
    #// Note: these actions are also fired in wp_ajax_update_widget().
    #// 
    #// @since 3.9.0
    #//
    def customize_controls_init(self):
        
        
        #// This action is documented in wp-admin/includes/ajax-actions.php
        do_action("load-widgets.php")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        #// This action is documented in wp-admin/includes/ajax-actions.php
        do_action("widgets.php")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        #// This action is documented in wp-admin/widgets.php
        do_action("sidebar_admin_setup")
    # end def customize_controls_init
    #// 
    #// Ensures widgets are available for all types of previews.
    #// 
    #// When in preview, hook to {@see 'customize_register'} for settings after WordPress is loaded
    #// so that all filters have been initialized (e.g. Widget Visibility).
    #// 
    #// @since 3.9.0
    #//
    def schedule_customize_register(self):
        
        
        if is_admin():
            self.customize_register()
        else:
            add_action("wp", Array(self, "customize_register"))
        # end if
    # end def schedule_customize_register
    #// 
    #// Registers Customizer settings and controls for all sidebars and widgets.
    #// 
    #// @since 3.9.0
    #// 
    #// @global array $wp_registered_widgets
    #// @global array $wp_registered_widget_controls
    #// @global array $wp_registered_sidebars
    #//
    def customize_register(self):
        
        
        global wp_registered_widgets_
        global wp_registered_widget_controls_
        global wp_registered_sidebars_
        php_check_if_defined("wp_registered_widgets_","wp_registered_widget_controls_","wp_registered_sidebars_")
        add_filter("sidebars_widgets", Array(self, "preview_sidebars_widgets"), 1)
        sidebars_widgets_ = php_array_merge(Array({"wp_inactive_widgets": Array()}), php_array_fill_keys(php_array_keys(wp_registered_sidebars_), Array()), wp_get_sidebars_widgets())
        new_setting_ids_ = Array()
        #// 
        #// Register a setting for all widgets, including those which are active,
        #// inactive, and orphaned since a widget may get suppressed from a sidebar
        #// via a plugin (like Widget Visibility).
        #//
        for widget_id_ in php_array_keys(wp_registered_widgets_):
            setting_id_ = self.get_setting_id(widget_id_)
            setting_args_ = self.get_setting_args(setting_id_)
            if (not self.manager.get_setting(setting_id_)):
                self.manager.add_setting(setting_id_, setting_args_)
            # end if
            new_setting_ids_[-1] = setting_id_
        # end for
        #// 
        #// Add a setting which will be supplied for the theme's sidebars_widgets
        #// theme_mod when the theme is switched.
        #//
        if (not self.manager.is_theme_active()):
            setting_id_ = "old_sidebars_widgets_data"
            setting_args_ = self.get_setting_args(setting_id_, Array({"type": "global_variable", "dirty": True}))
            self.manager.add_setting(setting_id_, setting_args_)
        # end if
        self.manager.add_panel("widgets", Array({"type": "widgets", "title": __("Widgets"), "description": __("Widgets are independent sections of content that can be placed into widgetized areas provided by your theme (commonly called sidebars)."), "priority": 110, "active_callback": Array(self, "is_panel_active"), "auto_expand_sole_section": True}))
        for sidebar_id_,sidebar_widget_ids_ in sidebars_widgets_:
            if php_empty(lambda : sidebar_widget_ids_):
                sidebar_widget_ids_ = Array()
            # end if
            is_registered_sidebar_ = is_registered_sidebar(sidebar_id_)
            is_inactive_widgets_ = "wp_inactive_widgets" == sidebar_id_
            is_active_sidebar_ = is_registered_sidebar_ and (not is_inactive_widgets_)
            #// Add setting for managing the sidebar's widgets.
            if is_registered_sidebar_ or is_inactive_widgets_:
                setting_id_ = php_sprintf("sidebars_widgets[%s]", sidebar_id_)
                setting_args_ = self.get_setting_args(setting_id_)
                if (not self.manager.get_setting(setting_id_)):
                    if (not self.manager.is_theme_active()):
                        setting_args_["dirty"] = True
                    # end if
                    self.manager.add_setting(setting_id_, setting_args_)
                # end if
                new_setting_ids_[-1] = setting_id_
                #// Add section to contain controls.
                section_id_ = php_sprintf("sidebar-widgets-%s", sidebar_id_)
                if is_active_sidebar_:
                    section_args_ = Array({"title": wp_registered_sidebars_[sidebar_id_]["name"], "description": wp_registered_sidebars_[sidebar_id_]["description"], "priority": php_array_search(sidebar_id_, php_array_keys(wp_registered_sidebars_)), "panel": "widgets", "sidebar_id": sidebar_id_})
                    #// 
                    #// Filters Customizer widget section arguments for a given sidebar.
                    #// 
                    #// @since 3.9.0
                    #// 
                    #// @param array      $section_args Array of Customizer widget section arguments.
                    #// @param string     $section_id   Customizer section ID.
                    #// @param int|string $sidebar_id   Sidebar ID.
                    #//
                    section_args_ = apply_filters("customizer_widgets_section_args", section_args_, section_id_, sidebar_id_)
                    section_ = php_new_class("WP_Customize_Sidebar_Section", lambda : WP_Customize_Sidebar_Section(self.manager, section_id_, section_args_))
                    self.manager.add_section(section_)
                    control_ = php_new_class("WP_Widget_Area_Customize_Control", lambda : WP_Widget_Area_Customize_Control(self.manager, setting_id_, Array({"section": section_id_, "sidebar_id": sidebar_id_, "priority": php_count(sidebar_widget_ids_)})))
                    new_setting_ids_[-1] = setting_id_
                    self.manager.add_control(control_)
                # end if
            # end if
            #// Add a control for each active widget (located in a sidebar).
            for i_,widget_id_ in sidebar_widget_ids_:
                #// Skip widgets that may have gone away due to a plugin being deactivated.
                if (not is_active_sidebar_) or (not (php_isset(lambda : wp_registered_widgets_[widget_id_]))):
                    continue
                # end if
                registered_widget_ = wp_registered_widgets_[widget_id_]
                setting_id_ = self.get_setting_id(widget_id_)
                id_base_ = wp_registered_widget_controls_[widget_id_]["id_base"]
                control_ = php_new_class("WP_Widget_Form_Customize_Control", lambda : WP_Widget_Form_Customize_Control(self.manager, setting_id_, Array({"label": registered_widget_["name"], "section": section_id_, "sidebar_id": sidebar_id_, "widget_id": widget_id_, "widget_id_base": id_base_, "priority": i_, "width": wp_registered_widget_controls_[widget_id_]["width"], "height": wp_registered_widget_controls_[widget_id_]["height"], "is_wide": self.is_wide_widget(widget_id_)})))
                self.manager.add_control(control_)
            # end for
        # end for
        if self.manager.settings_previewed():
            for new_setting_id_ in new_setting_ids_:
                self.manager.get_setting(new_setting_id_).preview()
            # end for
        # end if
    # end def customize_register
    #// 
    #// Determines whether the widgets panel is active, based on whether there are sidebars registered.
    #// 
    #// @since 4.4.0
    #// 
    #// @see WP_Customize_Panel::$active_callback
    #// 
    #// @global array $wp_registered_sidebars
    #// @return bool Active.
    #//
    def is_panel_active(self):
        
        
        global wp_registered_sidebars_
        php_check_if_defined("wp_registered_sidebars_")
        return (not php_empty(lambda : wp_registered_sidebars_))
    # end def is_panel_active
    #// 
    #// Converts a widget_id into its corresponding Customizer setting ID (option name).
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $widget_id Widget ID.
    #// @return string Maybe-parsed widget ID.
    #//
    def get_setting_id(self, widget_id_=None):
        
        
        parsed_widget_id_ = self.parse_widget_id(widget_id_)
        setting_id_ = php_sprintf("widget_%s", parsed_widget_id_["id_base"])
        if (not is_null(parsed_widget_id_["number"])):
            setting_id_ += php_sprintf("[%d]", parsed_widget_id_["number"])
        # end if
        return setting_id_
    # end def get_setting_id
    #// 
    #// Determines whether the widget is considered "wide".
    #// 
    #// Core widgets which may have controls wider than 250, but can still be shown
    #// in the narrow Customizer panel. The RSS and Text widgets in Core, for example,
    #// have widths of 400 and yet they still render fine in the Customizer panel.
    #// 
    #// This method will return all Core widgets as being not wide, but this can be
    #// overridden with the {@see 'is_wide_widget_in_customizer'} filter.
    #// 
    #// @since 3.9.0
    #// 
    #// @global $wp_registered_widget_controls
    #// 
    #// @param string $widget_id Widget ID.
    #// @return bool Whether or not the widget is a "wide" widget.
    #//
    def is_wide_widget(self, widget_id_=None):
        
        
        global wp_registered_widget_controls_
        php_check_if_defined("wp_registered_widget_controls_")
        parsed_widget_id_ = self.parse_widget_id(widget_id_)
        width_ = wp_registered_widget_controls_[widget_id_]["width"]
        is_core_ = php_in_array(parsed_widget_id_["id_base"], self.core_widget_id_bases)
        is_wide_ = width_ > 250 and (not is_core_)
        #// 
        #// Filters whether the given widget is considered "wide".
        #// 
        #// @since 3.9.0
        #// 
        #// @param bool   $is_wide   Whether the widget is wide, Default false.
        #// @param string $widget_id Widget ID.
        #//
        return apply_filters("is_wide_widget_in_customizer", is_wide_, widget_id_)
    # end def is_wide_widget
    #// 
    #// Converts a widget ID into its id_base and number components.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $widget_id Widget ID.
    #// @return array Array containing a widget's id_base and number components.
    #//
    def parse_widget_id(self, widget_id_=None):
        
        
        parsed_ = Array({"number": None, "id_base": None})
        if php_preg_match("/^(.+)-(\\d+)$/", widget_id_, matches_):
            parsed_["id_base"] = matches_[1]
            parsed_["number"] = php_intval(matches_[2])
        else:
            #// Likely an old single widget.
            parsed_["id_base"] = widget_id_
        # end if
        return parsed_
    # end def parse_widget_id
    #// 
    #// Converts a widget setting ID (option path) to its id_base and number components.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $setting_id Widget setting ID.
    #// @return array|WP_Error Array containing a widget's id_base and number components,
    #// or a WP_Error object.
    #//
    def parse_widget_setting_id(self, setting_id_=None):
        
        
        if (not php_preg_match("/^(widget_(.+?))(?:\\[(\\d+)\\])?$/", setting_id_, matches_)):
            return php_new_class("WP_Error", lambda : WP_Error("widget_setting_invalid_id"))
        # end if
        id_base_ = matches_[2]
        number_ = php_intval(matches_[3]) if (php_isset(lambda : matches_[3])) else None
        return php_compact("id_base", "number")
    # end def parse_widget_setting_id
    #// 
    #// Calls admin_print_styles-widgets.php and admin_print_styles hooks to
    #// allow custom styles from plugins.
    #// 
    #// @since 3.9.0
    #//
    def print_styles(self):
        
        
        #// This action is documented in wp-admin/admin-header.php
        do_action("admin_print_styles-widgets.php")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        #// This action is documented in wp-admin/admin-header.php
        do_action("admin_print_styles")
    # end def print_styles
    #// 
    #// Calls admin_print_scripts-widgets.php and admin_print_scripts hooks to
    #// allow custom scripts from plugins.
    #// 
    #// @since 3.9.0
    #//
    def print_scripts(self):
        
        
        #// This action is documented in wp-admin/admin-header.php
        do_action("admin_print_scripts-widgets.php")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        #// This action is documented in wp-admin/admin-header.php
        do_action("admin_print_scripts")
    # end def print_scripts
    #// 
    #// Enqueues scripts and styles for Customizer panel and export data to JavaScript.
    #// 
    #// @since 3.9.0
    #// 
    #// @global WP_Scripts $wp_scripts
    #// @global array $wp_registered_sidebars
    #// @global array $wp_registered_widgets
    #//
    def enqueue_scripts(self):
        
        
        global wp_scripts_
        global wp_registered_sidebars_
        global wp_registered_widgets_
        php_check_if_defined("wp_scripts_","wp_registered_sidebars_","wp_registered_widgets_")
        wp_enqueue_style("customize-widgets")
        wp_enqueue_script("customize-widgets")
        #// This action is documented in wp-admin/admin-header.php
        do_action("admin_enqueue_scripts", "widgets.php")
        #// 
        #// Export available widgets with control_tpl removed from model
        #// since plugins need templates to be in the DOM.
        #//
        available_widgets_ = Array()
        for available_widget_ in self.get_available_widgets():
            available_widget_["control_tpl"] = None
            available_widgets_[-1] = available_widget_
        # end for
        widget_reorder_nav_tpl_ = php_sprintf("<div class=\"widget-reorder-nav\"><span class=\"move-widget\" tabindex=\"0\">%1$s</span><span class=\"move-widget-down\" tabindex=\"0\">%2$s</span><span class=\"move-widget-up\" tabindex=\"0\">%3$s</span></div>", __("Move to another area&hellip;"), __("Move down"), __("Move up"))
        move_widget_area_tpl_ = php_str_replace(Array("{description}", "{btn}"), Array(__("Select an area to move this widget into:"), _x("Move", "Move widget")), """<div class=\"move-widget-area\">
        <p class=\"description\">{description}</p>
        <ul class=\"widget-area-select\">
        <% _.each( sidebars, function ( sidebar ){ %>
        <li class=\"\" data-id=\"<%- sidebar.id %>\" title=\"<%- sidebar.description %>\" tabindex=\"0\"><%- sidebar.name %></li>
        <% }); %>
        </ul>
        <div class=\"move-widget-actions\">
        <button class=\"move-widget-btn button\" type=\"button\">{btn}</button>
        </div>
        </div>""")
        #// 
        #// Gather all strings in PHP that may be needed by JS on the client.
        #// Once JS i18n is implemented (in #20491), this can be removed.
        #//
        some_non_rendered_areas_messages_ = Array()
        some_non_rendered_areas_messages_[1] = html_entity_decode(__("Your theme has 1 other widget area, but this particular page doesn&#8217;t display it."), ENT_QUOTES, get_bloginfo("charset"))
        registered_sidebar_count_ = php_count(wp_registered_sidebars_)
        non_rendered_count_ = 2
        while non_rendered_count_ < registered_sidebar_count_:
            
            some_non_rendered_areas_messages_[non_rendered_count_] = html_entity_decode(php_sprintf(_n("Your theme has %s other widget area, but this particular page doesn&#8217;t display it.", "Your theme has %s other widget areas, but this particular page doesn&#8217;t display them.", non_rendered_count_), number_format_i18n(non_rendered_count_)), ENT_QUOTES, get_bloginfo("charset"))
            non_rendered_count_ += 1
        # end while
        if 1 == registered_sidebar_count_:
            no_areas_shown_message_ = html_entity_decode(php_sprintf(__("Your theme has 1 widget area, but this particular page doesn&#8217;t display it.")), ENT_QUOTES, get_bloginfo("charset"))
        else:
            no_areas_shown_message_ = html_entity_decode(php_sprintf(_n("Your theme has %s widget area, but this particular page doesn&#8217;t display it.", "Your theme has %s widget areas, but this particular page doesn&#8217;t display them.", registered_sidebar_count_), number_format_i18n(registered_sidebar_count_)), ENT_QUOTES, get_bloginfo("charset"))
        # end if
        settings_ = Array({"registeredSidebars": php_array_values(wp_registered_sidebars_), "registeredWidgets": wp_registered_widgets_, "availableWidgets": available_widgets_, "l10n": Array({"saveBtnLabel": __("Apply"), "saveBtnTooltip": __("Save and preview changes before publishing them."), "removeBtnLabel": __("Remove"), "removeBtnTooltip": __("Keep widget settings and move it to the inactive widgets"), "error": __("An error has occurred. Please reload the page and try again."), "widgetMovedUp": __("Widget moved up"), "widgetMovedDown": __("Widget moved down"), "navigatePreview": __("You can navigate to other pages on your site while using the Customizer to view and edit the widgets displayed on those pages."), "someAreasShown": some_non_rendered_areas_messages_, "noAreasShown": no_areas_shown_message_, "reorderModeOn": __("Reorder mode enabled"), "reorderModeOff": __("Reorder mode closed"), "reorderLabelOn": esc_attr__("Reorder widgets"), "widgetsFound": __("Number of widgets found: %d"), "noWidgetsFound": __("No widgets found.")})}, {"tpl": Array({"widgetReorderNav": widget_reorder_nav_tpl_, "moveWidgetArea": move_widget_area_tpl_})}, {"selectiveRefreshableWidgets": self.get_selective_refreshable_widgets()})
        for registered_widget_ in settings_["registeredWidgets"]:
            registered_widget_["callback"] = None
            pass
        # end for
        wp_scripts_.add_data("customize-widgets", "data", php_sprintf("var _wpCustomizeWidgetsSettings = %s;", wp_json_encode(settings_)))
    # end def enqueue_scripts
    #// 
    #// Renders the widget form control templates into the DOM.
    #// 
    #// @since 3.9.0
    #//
    def output_widget_control_templates(self):
        
        
        php_print("""       <div id=\"widgets-left\"><!-- compatibility with JS which looks for widget templates here -->
        <div id=\"available-widgets\">
        <div class=\"customize-section-title\">
        <button class=\"customize-section-back\" tabindex=\"-1\">
        <span class=\"screen-reader-text\">""")
        _e("Back")
        php_print("""</span>
        </button>
        <h3>
        <span class=\"customize-action\">
        """)
        #// translators: &#9656; is the unicode right-pointing triangle. %s: Section title in the Customizer.
        php_print(php_sprintf(__("Customizing &#9656; %s"), esc_html(self.manager.get_panel("widgets").title)))
        php_print("                 </span>\n                   ")
        _e("Add a Widget")
        php_print("""               </h3>
        </div>
        <div id=\"available-widgets-filter\">
        <label class=\"screen-reader-text\" for=\"widgets-search\">""")
        _e("Search Widgets")
        php_print("</label>\n               <input type=\"text\" id=\"widgets-search\" placeholder=\"")
        esc_attr_e("Search widgets&hellip;")
        php_print("\" aria-describedby=\"widgets-search-desc\" />\n             <div class=\"search-icon\" aria-hidden=\"true\"></div>\n                <button type=\"button\" class=\"clear-results\"><span class=\"screen-reader-text\">")
        _e("Clear Results")
        php_print("</span></button>\n               <p class=\"screen-reader-text\" id=\"widgets-search-desc\">")
        _e("The search results will be updated as you type.")
        php_print("""</p>
        </div>
        <div id=\"available-widgets-list\">
        """)
        for available_widget_ in self.get_available_widgets():
            php_print("             <div id=\"widget-tpl-")
            php_print(esc_attr(available_widget_["id"]))
            php_print("\" data-widget-id=\"")
            php_print(esc_attr(available_widget_["id"]))
            php_print("\" class=\"widget-tpl ")
            php_print(esc_attr(available_widget_["id"]))
            php_print("\" tabindex=\"0\">\n                 ")
            php_print(available_widget_["control_tpl"])
            php_print("             </div>\n            ")
        # end for
        php_print("         <p class=\"no-widgets-found-message\">")
        _e("No widgets found.")
        php_print("""</p>
        </div><!-- #available-widgets-list -->
        </div><!-- #available-widgets -->
        </div><!-- #widgets-left -->
        """)
    # end def output_widget_control_templates
    #// 
    #// Calls admin_print_footer_scripts and admin_print_scripts hooks to
    #// allow custom scripts from plugins.
    #// 
    #// @since 3.9.0
    #//
    def print_footer_scripts(self):
        
        
        #// This action is documented in wp-admin/admin-footer.php
        do_action("admin_print_footer_scripts-widgets.php")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        #// This action is documented in wp-admin/admin-footer.php
        do_action("admin_print_footer_scripts")
        #// This action is documented in wp-admin/admin-footer.php
        do_action("admin_footer-widgets.php")
        pass
    # end def print_footer_scripts
    #// 
    #// Retrieves common arguments to supply when constructing a Customizer setting.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $id        Widget setting ID.
    #// @param array  $overrides Array of setting overrides.
    #// @return array Possibly modified setting arguments.
    #//
    def get_setting_args(self, id_=None, overrides_=None):
        if overrides_ is None:
            overrides_ = Array()
        # end if
        
        args_ = Array({"type": "option", "capability": "edit_theme_options", "default": Array()})
        if php_preg_match(self.setting_id_patterns["sidebar_widgets"], id_, matches_):
            args_["sanitize_callback"] = Array(self, "sanitize_sidebar_widgets")
            args_["sanitize_js_callback"] = Array(self, "sanitize_sidebar_widgets_js_instance")
            args_["transport"] = "postMessage" if current_theme_supports("customize-selective-refresh-widgets") else "refresh"
        elif php_preg_match(self.setting_id_patterns["widget_instance"], id_, matches_):
            args_["sanitize_callback"] = Array(self, "sanitize_widget_instance")
            args_["sanitize_js_callback"] = Array(self, "sanitize_widget_js_instance")
            args_["transport"] = "postMessage" if self.is_widget_selective_refreshable(matches_["id_base"]) else "refresh"
        # end if
        args_ = php_array_merge(args_, overrides_)
        #// 
        #// Filters the common arguments supplied when constructing a Customizer setting.
        #// 
        #// @since 3.9.0
        #// 
        #// @see WP_Customize_Setting
        #// 
        #// @param array  $args Array of Customizer setting arguments.
        #// @param string $id   Widget setting ID.
        #//
        return apply_filters("widget_customizer_setting_args", args_, id_)
    # end def get_setting_args
    #// 
    #// Ensures sidebar widget arrays only ever contain widget IDS.
    #// 
    #// Used as the 'sanitize_callback' for each $sidebars_widgets setting.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string[] $widget_ids Array of widget IDs.
    #// @return string[] Array of sanitized widget IDs.
    #//
    def sanitize_sidebar_widgets(self, widget_ids_=None):
        
        
        widget_ids_ = php_array_map("strval", widget_ids_)
        sanitized_widget_ids_ = Array()
        for widget_id_ in widget_ids_:
            sanitized_widget_ids_[-1] = php_preg_replace("/[^a-z0-9_\\-]/", "", widget_id_)
        # end for
        return sanitized_widget_ids_
    # end def sanitize_sidebar_widgets
    #// 
    #// Builds up an index of all available widgets for use in Backbone models.
    #// 
    #// @since 3.9.0
    #// 
    #// @global array $wp_registered_widgets
    #// @global array $wp_registered_widget_controls
    #// @staticvar array $available_widgets
    #// 
    #// @see wp_list_widgets()
    #// 
    #// @return array List of available widgets.
    #//
    def get_available_widgets(self):
        
        
        available_widgets_ = Array()
        if (not php_empty(lambda : available_widgets_)):
            return available_widgets_
        # end if
        global wp_registered_widgets_
        global wp_registered_widget_controls_
        php_check_if_defined("wp_registered_widgets_","wp_registered_widget_controls_")
        php_include_file(ABSPATH + "wp-admin/includes/widgets.php", once=True)
        #// For next_widget_id_number().
        sort_ = wp_registered_widgets_
        usort(sort_, Array(self, "_sort_name_callback"))
        done_ = Array()
        for widget_ in sort_:
            if php_in_array(widget_["callback"], done_, True):
                continue
            # end if
            sidebar_ = is_active_widget(widget_["callback"], widget_["id"], False, False)
            done_[-1] = widget_["callback"]
            if (not (php_isset(lambda : widget_["params"][0]))):
                widget_["params"][0] = Array()
            # end if
            available_widget_ = widget_
            available_widget_["callback"] = None
            #// Not serializable to JSON.
            args_ = Array({"widget_id": widget_["id"], "widget_name": widget_["name"], "_display": "template"})
            is_disabled_ = False
            is_multi_widget_ = (php_isset(lambda : wp_registered_widget_controls_[widget_["id"]]["id_base"])) and (php_isset(lambda : widget_["params"][0]["number"]))
            if is_multi_widget_:
                id_base_ = wp_registered_widget_controls_[widget_["id"]]["id_base"]
                args_["_temp_id"] = str(id_base_) + str("-__i__")
                args_["_multi_num"] = next_widget_id_number(id_base_)
                args_["_add"] = "multi"
            else:
                args_["_add"] = "single"
                if sidebar_ and "wp_inactive_widgets" != sidebar_:
                    is_disabled_ = True
                # end if
                id_base_ = widget_["id"]
            # end if
            list_widget_controls_args_ = wp_list_widget_controls_dynamic_sidebar(Array({0: args_, 1: widget_["params"][0]}))
            control_tpl_ = self.get_widget_control(list_widget_controls_args_)
            #// The properties here are mapped to the Backbone Widget model.
            available_widget_ = php_array_merge(available_widget_, Array({"temp_id": args_["_temp_id"] if (php_isset(lambda : args_["_temp_id"])) else None, "is_multi": is_multi_widget_, "control_tpl": control_tpl_, "multi_number": args_["_multi_num"] if "multi" == args_["_add"] else False, "is_disabled": is_disabled_, "id_base": id_base_, "transport": "postMessage" if self.is_widget_selective_refreshable(id_base_) else "refresh", "width": wp_registered_widget_controls_[widget_["id"]]["width"], "height": wp_registered_widget_controls_[widget_["id"]]["height"], "is_wide": self.is_wide_widget(widget_["id"])}))
            available_widgets_[-1] = available_widget_
        # end for
        return available_widgets_
    # end def get_available_widgets
    #// 
    #// Naturally orders available widgets by name.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array $widget_a The first widget to compare.
    #// @param array $widget_b The second widget to compare.
    #// @return int Reorder position for the current widget comparison.
    #//
    def _sort_name_callback(self, widget_a_=None, widget_b_=None):
        
        
        return strnatcasecmp(widget_a_["name"], widget_b_["name"])
    # end def _sort_name_callback
    #// 
    #// Retrieves the widget control markup.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array $args Widget control arguments.
    #// @return string Widget control form HTML markup.
    #//
    def get_widget_control(self, args_=None):
        
        
        args_[0]["before_form"] = "<div class=\"form\">"
        args_[0]["after_form"] = "</div><!-- .form -->"
        args_[0]["before_widget_content"] = "<div class=\"widget-content\">"
        args_[0]["after_widget_content"] = "</div><!-- .widget-content -->"
        ob_start()
        wp_widget_control(args_)
        control_tpl_ = ob_get_clean()
        return control_tpl_
    # end def get_widget_control
    #// 
    #// Retrieves the widget control markup parts.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $args Widget control arguments.
    #// @return array {
    #// @type string $control Markup for widget control wrapping form.
    #// @type string $content The contents of the widget form itself.
    #// }
    #//
    def get_widget_control_parts(self, args_=None):
        
        
        args_[0]["before_widget_content"] = "<div class=\"widget-content\">"
        args_[0]["after_widget_content"] = "</div><!-- .widget-content -->"
        control_markup_ = self.get_widget_control(args_)
        content_start_pos_ = php_strpos(control_markup_, args_[0]["before_widget_content"])
        content_end_pos_ = php_strrpos(control_markup_, args_[0]["after_widget_content"])
        control_ = php_substr(control_markup_, 0, content_start_pos_ + php_strlen(args_[0]["before_widget_content"]))
        control_ += php_substr(control_markup_, content_end_pos_)
        content_ = php_trim(php_substr(control_markup_, content_start_pos_ + php_strlen(args_[0]["before_widget_content"]), content_end_pos_ - content_start_pos_ - php_strlen(args_[0]["before_widget_content"])))
        return php_compact("control", "content")
    # end def get_widget_control_parts
    #// 
    #// Adds hooks for the Customizer preview.
    #// 
    #// @since 3.9.0
    #//
    def customize_preview_init(self):
        
        
        add_action("wp_enqueue_scripts", Array(self, "customize_preview_enqueue"))
        add_action("wp_print_styles", Array(self, "print_preview_css"), 1)
        add_action("wp_footer", Array(self, "export_preview_data"), 20)
    # end def customize_preview_init
    #// 
    #// Refreshes the nonce for widget updates.
    #// 
    #// @since 4.2.0
    #// 
    #// @param  array $nonces Array of nonces.
    #// @return array Array of nonces.
    #//
    def refresh_nonces(self, nonces_=None):
        
        
        nonces_["update-widget"] = wp_create_nonce("update-widget")
        return nonces_
    # end def refresh_nonces
    #// 
    #// When previewing, ensures the proper previewing widgets are used.
    #// 
    #// Because wp_get_sidebars_widgets() gets called early at {@see 'init' } (via
    #// wp_convert_widget_settings()) and can set global variable `$_wp_sidebars_widgets`
    #// to the value of `get_option( 'sidebars_widgets' )` before the Customizer preview
    #// filter is added, it has to be reset after the filter has been added.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array $sidebars_widgets List of widgets for the current sidebar.
    #// @return array
    #//
    def preview_sidebars_widgets(self, sidebars_widgets_=None):
        
        
        sidebars_widgets_ = get_option("sidebars_widgets", Array())
        sidebars_widgets_["array_version"] = None
        return sidebars_widgets_
    # end def preview_sidebars_widgets
    #// 
    #// Enqueues scripts for the Customizer preview.
    #// 
    #// @since 3.9.0
    #//
    def customize_preview_enqueue(self):
        
        
        wp_enqueue_script("customize-preview-widgets")
    # end def customize_preview_enqueue
    #// 
    #// Inserts default style for highlighted widget at early point so theme
    #// stylesheet can override.
    #// 
    #// @since 3.9.0
    #//
    def print_preview_css(self):
        
        
        php_print("""       <style>
        .widget-customizer-highlighted-widget {
        outline: none;
        -webkit-box-shadow: 0 0 2px rgba(30, 140, 190, 0.8);
        box-shadow: 0 0 2px rgba(30, 140, 190, 0.8);
        position: relative;
        z-index: 1;
        }
        </style>
        """)
    # end def print_preview_css
    #// 
    #// Communicates the sidebars that appeared on the page at the very end of the page,
    #// and at the very end of the wp_footer,
    #// 
    #// @since 3.9.0
    #// 
    #// @global array $wp_registered_sidebars
    #// @global array $wp_registered_widgets
    #//
    def export_preview_data(self):
        
        
        global wp_registered_sidebars_
        global wp_registered_widgets_
        php_check_if_defined("wp_registered_sidebars_","wp_registered_widgets_")
        switched_locale_ = switch_to_locale(get_user_locale())
        l10n_ = Array({"widgetTooltip": __("Shift-click to edit this widget.")})
        if switched_locale_:
            restore_previous_locale()
        # end if
        #// Prepare Customizer settings to pass to JavaScript.
        settings_ = Array({"renderedSidebars": php_array_fill_keys(array_unique(self.rendered_sidebars), True), "renderedWidgets": php_array_fill_keys(php_array_keys(self.rendered_widgets), True), "registeredSidebars": php_array_values(wp_registered_sidebars_), "registeredWidgets": wp_registered_widgets_, "l10n": l10n_, "selectiveRefreshableWidgets": self.get_selective_refreshable_widgets()})
        for registered_widget_ in settings_["registeredWidgets"]:
            registered_widget_["callback"] = None
            pass
        # end for
        php_print("     <script type=\"text/javascript\">\n         var _wpWidgetCustomizerPreviewSettings = ")
        php_print(wp_json_encode(settings_))
        php_print(";\n      </script>\n     ")
    # end def export_preview_data
    #// 
    #// Tracks the widgets that were rendered.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array $widget Rendered widget to tally.
    #//
    def tally_rendered_widgets(self, widget_=None):
        
        
        self.rendered_widgets[widget_["id"]] = True
    # end def tally_rendered_widgets
    #// 
    #// Determine if a widget is rendered on the page.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $widget_id Widget ID to check.
    #// @return bool Whether the widget is rendered.
    #//
    def is_widget_rendered(self, widget_id_=None):
        
        
        return php_in_array(widget_id_, self.rendered_widgets)
    # end def is_widget_rendered
    #// 
    #// Determines if a sidebar is rendered on the page.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $sidebar_id Sidebar ID to check.
    #// @return bool Whether the sidebar is rendered.
    #//
    def is_sidebar_rendered(self, sidebar_id_=None):
        
        
        return php_in_array(sidebar_id_, self.rendered_sidebars)
    # end def is_sidebar_rendered
    #// 
    #// Tallies the sidebars rendered via is_active_sidebar().
    #// 
    #// Keep track of the times that is_active_sidebar() is called in the template,
    #// and assume that this means that the sidebar would be rendered on the template
    #// if there were widgets populating it.
    #// 
    #// @since 3.9.0
    #// 
    #// @param bool   $is_active  Whether the sidebar is active.
    #// @param string $sidebar_id Sidebar ID.
    #// @return bool Whether the sidebar is active.
    #//
    def tally_sidebars_via_is_active_sidebar_calls(self, is_active_=None, sidebar_id_=None):
        
        
        if is_registered_sidebar(sidebar_id_):
            self.rendered_sidebars[-1] = sidebar_id_
        # end if
        #// 
        #// We may need to force this to true, and also force-true the value
        #// for 'dynamic_sidebar_has_widgets' if we want to ensure that there
        #// is an area to drop widgets into, if the sidebar is empty.
        #//
        return is_active_
    # end def tally_sidebars_via_is_active_sidebar_calls
    #// 
    #// Tallies the sidebars rendered via dynamic_sidebar().
    #// 
    #// Keep track of the times that dynamic_sidebar() is called in the template,
    #// and assume this means the sidebar would be rendered on the template if
    #// there were widgets populating it.
    #// 
    #// @since 3.9.0
    #// 
    #// @param bool   $has_widgets Whether the current sidebar has widgets.
    #// @param string $sidebar_id  Sidebar ID.
    #// @return bool Whether the current sidebar has widgets.
    #//
    def tally_sidebars_via_dynamic_sidebar_calls(self, has_widgets_=None, sidebar_id_=None):
        
        
        if is_registered_sidebar(sidebar_id_):
            self.rendered_sidebars[-1] = sidebar_id_
        # end if
        #// 
        #// We may need to force this to true, and also force-true the value
        #// for 'is_active_sidebar' if we want to ensure there is an area to
        #// drop widgets into, if the sidebar is empty.
        #//
        return has_widgets_
    # end def tally_sidebars_via_dynamic_sidebar_calls
    #// 
    #// Retrieves MAC for a serialized widget instance string.
    #// 
    #// Allows values posted back from JS to be rejected if any tampering of the
    #// data has occurred.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $serialized_instance Widget instance.
    #// @return string MAC for serialized widget instance.
    #//
    def get_instance_hash_key(self, serialized_instance_=None):
        
        
        return wp_hash(serialized_instance_)
    # end def get_instance_hash_key
    #// 
    #// Sanitizes a widget instance.
    #// 
    #// Unserialize the JS-instance for storing in the options. It's important that this filter
    #// only get applied to an instance *once*.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array $value Widget instance to sanitize.
    #// @return array|void Sanitized widget instance.
    #//
    def sanitize_widget_instance(self, value_=None):
        
        
        if Array() == value_:
            return value_
        # end if
        if php_empty(lambda : value_["is_widget_customizer_js_value"]) or php_empty(lambda : value_["instance_hash_key"]) or php_empty(lambda : value_["encoded_serialized_instance"]):
            return
        # end if
        decoded_ = php_base64_decode(value_["encoded_serialized_instance"], True)
        if False == decoded_:
            return
        # end if
        if (not hash_equals(self.get_instance_hash_key(decoded_), value_["instance_hash_key"])):
            return
        # end if
        instance_ = unserialize(decoded_)
        if False == instance_:
            return
        # end if
        return instance_
    # end def sanitize_widget_instance
    #// 
    #// Converts a widget instance into JSON-representable format.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array $value Widget instance to convert to JSON.
    #// @return array JSON-converted widget instance.
    #//
    def sanitize_widget_js_instance(self, value_=None):
        
        
        if php_empty(lambda : value_["is_widget_customizer_js_value"]):
            serialized_ = serialize(value_)
            value_ = Array({"encoded_serialized_instance": php_base64_encode(serialized_), "title": "" if php_empty(lambda : value_["title"]) else value_["title"], "is_widget_customizer_js_value": True, "instance_hash_key": self.get_instance_hash_key(serialized_)})
        # end if
        return value_
    # end def sanitize_widget_js_instance
    #// 
    #// Strips out widget IDs for widgets which are no longer registered.
    #// 
    #// One example where this might happen is when a plugin orphans a widget
    #// in a sidebar upon deactivation.
    #// 
    #// @since 3.9.0
    #// 
    #// @global array $wp_registered_widgets
    #// 
    #// @param array $widget_ids List of widget IDs.
    #// @return array Parsed list of widget IDs.
    #//
    def sanitize_sidebar_widgets_js_instance(self, widget_ids_=None):
        
        
        global wp_registered_widgets_
        php_check_if_defined("wp_registered_widgets_")
        widget_ids_ = php_array_values(php_array_intersect(widget_ids_, php_array_keys(wp_registered_widgets_)))
        return widget_ids_
    # end def sanitize_sidebar_widgets_js_instance
    #// 
    #// Finds and invokes the widget update and control callbacks.
    #// 
    #// Requires that `$_POST` be populated with the instance data.
    #// 
    #// @since 3.9.0
    #// 
    #// @global array $wp_registered_widget_updates
    #// @global array $wp_registered_widget_controls
    #// 
    #// @param  string $widget_id Widget ID.
    #// @return array|WP_Error Array containing the updated widget information.
    #// A WP_Error object, otherwise.
    #//
    def call_widget_update(self, widget_id_=None):
        
        global PHP_REQUEST, PHP_POST
        global wp_registered_widget_updates_
        global wp_registered_widget_controls_
        php_check_if_defined("wp_registered_widget_updates_","wp_registered_widget_controls_")
        setting_id_ = self.get_setting_id(widget_id_)
        #// 
        #// Make sure that other setting changes have previewed since this widget
        #// may depend on them (e.g. Menus being present for Navigation Menu widget).
        #//
        if (not did_action("customize_preview_init")):
            for setting_ in self.manager.settings():
                if setting_.id != setting_id_:
                    setting_.preview()
                # end if
            # end for
        # end if
        self.start_capturing_option_updates()
        parsed_id_ = self.parse_widget_id(widget_id_)
        option_name_ = "widget_" + parsed_id_["id_base"]
        #// 
        #// If a previously-sanitized instance is provided, populate the input vars
        #// with its values so that the widget update callback will read this instance
        #//
        added_input_vars_ = Array()
        if (not php_empty(lambda : PHP_POST["sanitized_widget_setting"])):
            sanitized_widget_setting_ = php_json_decode(self.get_post_value("sanitized_widget_setting"), True)
            if False == sanitized_widget_setting_:
                self.stop_capturing_option_updates()
                return php_new_class("WP_Error", lambda : WP_Error("widget_setting_malformed"))
            # end if
            instance_ = self.sanitize_widget_instance(sanitized_widget_setting_)
            if is_null(instance_):
                self.stop_capturing_option_updates()
                return php_new_class("WP_Error", lambda : WP_Error("widget_setting_unsanitized"))
            # end if
            if (not is_null(parsed_id_["number"])):
                value_ = Array()
                value_[parsed_id_["number"]] = instance_
                key_ = "widget-" + parsed_id_["id_base"]
                PHP_REQUEST[key_] = wp_slash(value_)
                PHP_POST[key_] = PHP_REQUEST[key_]
                added_input_vars_[-1] = key_
            else:
                for key_,value_ in instance_:
                    PHP_REQUEST[key_] = wp_slash(value_)
                    PHP_POST[key_] = PHP_REQUEST[key_]
                    added_input_vars_[-1] = key_
                # end for
            # end if
        # end if
        #// Invoke the widget update callback.
        for name_,control_ in wp_registered_widget_updates_:
            if name_ == parsed_id_["id_base"] and php_is_callable(control_["callback"]):
                ob_start()
                call_user_func_array(control_["callback"], control_["params"])
                ob_end_clean()
                break
            # end if
        # end for
        #// Clean up any input vars that were manually added.
        for key_ in added_input_vars_:
            PHP_POST[key_] = None
            PHP_REQUEST[key_] = None
        # end for
        #// Make sure the expected option was updated.
        if 0 != self.count_captured_options():
            if self.count_captured_options() > 1:
                self.stop_capturing_option_updates()
                return php_new_class("WP_Error", lambda : WP_Error("widget_setting_too_many_options"))
            # end if
            updated_option_name_ = key(self.get_captured_options())
            if updated_option_name_ != option_name_:
                self.stop_capturing_option_updates()
                return php_new_class("WP_Error", lambda : WP_Error("widget_setting_unexpected_option"))
            # end if
        # end if
        #// Obtain the widget instance.
        option_ = self.get_captured_option(option_name_)
        if None != parsed_id_["number"]:
            instance_ = option_[parsed_id_["number"]]
        else:
            instance_ = option_
        # end if
        #// 
        #// Override the incoming $_POST['customized'] for a newly-created widget's
        #// setting with the new $instance so that the preview filter currently
        #// in place from WP_Customize_Setting::preview() will use this value
        #// instead of the default widget instance value (an empty array).
        #//
        self.manager.set_post_value(setting_id_, self.sanitize_widget_js_instance(instance_))
        #// Obtain the widget control with the updated instance in place.
        ob_start()
        form_ = wp_registered_widget_controls_[widget_id_]
        if form_:
            call_user_func_array(form_["callback"], form_["params"])
        # end if
        form_ = ob_get_clean()
        self.stop_capturing_option_updates()
        return php_compact("instance", "form")
    # end def call_widget_update
    #// 
    #// Updates widget settings asynchronously.
    #// 
    #// Allows the Customizer to update a widget using its form, but return the new
    #// instance info via Ajax instead of saving it to the options table.
    #// 
    #// Most code here copied from wp_ajax_save_widget().
    #// 
    #// @since 3.9.0
    #// 
    #// @see wp_ajax_save_widget()
    #//
    def wp_ajax_update_widget(self):
        
        
        if (not is_user_logged_in()):
            wp_die(0)
        # end if
        check_ajax_referer("update-widget", "nonce")
        if (not current_user_can("edit_theme_options")):
            wp_die(-1)
        # end if
        if php_empty(lambda : PHP_POST["widget-id"]):
            wp_send_json_error("missing_widget-id")
        # end if
        #// This action is documented in wp-admin/includes/ajax-actions.php
        do_action("load-widgets.php")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        #// This action is documented in wp-admin/includes/ajax-actions.php
        do_action("widgets.php")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        #// This action is documented in wp-admin/widgets.php
        do_action("sidebar_admin_setup")
        widget_id_ = self.get_post_value("widget-id")
        parsed_id_ = self.parse_widget_id(widget_id_)
        id_base_ = parsed_id_["id_base"]
        is_updating_widget_template_ = (php_isset(lambda : PHP_POST["widget-" + id_base_])) and php_is_array(PHP_POST["widget-" + id_base_]) and php_preg_match("/__i__|%i%/", key(PHP_POST["widget-" + id_base_]))
        if is_updating_widget_template_:
            wp_send_json_error("template_widget_not_updatable")
        # end if
        updated_widget_ = self.call_widget_update(widget_id_)
        #// => {instance,form}
        if is_wp_error(updated_widget_):
            wp_send_json_error(updated_widget_.get_error_code())
        # end if
        form_ = updated_widget_["form"]
        instance_ = self.sanitize_widget_js_instance(updated_widget_["instance"])
        wp_send_json_success(php_compact("form", "instance"))
    # end def wp_ajax_update_widget
    #// 
    #// Selective Refresh Methods
    #// 
    #// 
    #// Filters arguments for dynamic widget partials.
    #// 
    #// @since 4.5.0
    #// 
    #// @param array|false $partial_args Partial arguments.
    #// @param string      $partial_id   Partial ID.
    #// @return array (Maybe) modified partial arguments.
    #//
    def customize_dynamic_partial_args(self, partial_args_=None, partial_id_=None):
        
        
        if (not current_theme_supports("customize-selective-refresh-widgets")):
            return partial_args_
        # end if
        if php_preg_match("/^widget\\[(?P<widget_id>.+)\\]$/", partial_id_, matches_):
            if False == partial_args_:
                partial_args_ = Array()
            # end if
            partial_args_ = php_array_merge(partial_args_, Array({"type": "widget", "render_callback": Array(self, "render_widget_partial"), "container_inclusive": True, "settings": Array(self.get_setting_id(matches_["widget_id"])), "capability": "edit_theme_options"}))
        # end if
        return partial_args_
    # end def customize_dynamic_partial_args
    #// 
    #// Adds hooks for selective refresh.
    #// 
    #// @since 4.5.0
    #//
    def selective_refresh_init(self):
        
        
        if (not current_theme_supports("customize-selective-refresh-widgets")):
            return
        # end if
        add_filter("dynamic_sidebar_params", Array(self, "filter_dynamic_sidebar_params"))
        add_filter("wp_kses_allowed_html", Array(self, "filter_wp_kses_allowed_data_attributes"))
        add_action("dynamic_sidebar_before", Array(self, "start_dynamic_sidebar"))
        add_action("dynamic_sidebar_after", Array(self, "end_dynamic_sidebar"))
    # end def selective_refresh_init
    #// 
    #// Inject selective refresh data attributes into widget container elements.
    #// 
    #// @since 4.5.0
    #// 
    #// @param array $params {
    #// Dynamic sidebar params.
    #// 
    #// @type array $args        Sidebar args.
    #// @type array $widget_args Widget args.
    #// }
    #// @see WP_Customize_Nav_Menus::filter_wp_nav_menu_args()
    #// 
    #// @return array Params.
    #//
    def filter_dynamic_sidebar_params(self, params_=None):
        
        
        sidebar_args_ = php_array_merge(Array({"before_widget": "", "after_widget": ""}), params_[0])
        #// Skip widgets not in a registered sidebar or ones which lack a proper wrapper element to attach the data-* attributes to.
        matches_ = Array()
        is_valid_ = (php_isset(lambda : sidebar_args_["id"])) and is_registered_sidebar(sidebar_args_["id"]) and (php_isset(lambda : self.current_dynamic_sidebar_id_stack[0])) and self.current_dynamic_sidebar_id_stack[0] == sidebar_args_["id"] and php_preg_match("#^<(?P<tag_name>\\w+)#", sidebar_args_["before_widget"], matches_)
        if (not is_valid_):
            return params_
        # end if
        self.before_widget_tags_seen[matches_["tag_name"]] = True
        context_ = Array({"sidebar_id": sidebar_args_["id"]})
        if (php_isset(lambda : self.context_sidebar_instance_number)):
            context_["sidebar_instance_number"] = self.context_sidebar_instance_number
        elif (php_isset(lambda : sidebar_args_["id"])) and (php_isset(lambda : self.sidebar_instance_count[sidebar_args_["id"]])):
            context_["sidebar_instance_number"] = self.sidebar_instance_count[sidebar_args_["id"]]
        # end if
        attributes_ = php_sprintf(" data-customize-partial-id=\"%s\"", esc_attr("widget[" + sidebar_args_["widget_id"] + "]"))
        attributes_ += " data-customize-partial-type=\"widget\""
        attributes_ += php_sprintf(" data-customize-partial-placement-context=\"%s\"", esc_attr(wp_json_encode(context_)))
        attributes_ += php_sprintf(" data-customize-widget-id=\"%s\"", esc_attr(sidebar_args_["widget_id"]))
        sidebar_args_["before_widget"] = php_preg_replace("#^(<\\w+)#", "$1 " + attributes_, sidebar_args_["before_widget"])
        params_[0] = sidebar_args_
        return params_
    # end def filter_dynamic_sidebar_params
    #// 
    #// List of the tag names seen for before_widget strings.
    #// 
    #// This is used in the {@see 'filter_wp_kses_allowed_html'} filter to ensure that the
    #// data-* attributes can be whitelisted.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    before_widget_tags_seen = Array()
    #// 
    #// Ensures the HTML data-* attributes for selective refresh are allowed by kses.
    #// 
    #// This is needed in case the `$before_widget` is run through wp_kses() when printed.
    #// 
    #// @since 4.5.0
    #// 
    #// @param array $allowed_html Allowed HTML.
    #// @return array (Maybe) modified allowed HTML.
    #//
    def filter_wp_kses_allowed_data_attributes(self, allowed_html_=None):
        
        
        for tag_name_ in php_array_keys(self.before_widget_tags_seen):
            if (not (php_isset(lambda : allowed_html_[tag_name_]))):
                allowed_html_[tag_name_] = Array()
            # end if
            allowed_html_[tag_name_] = php_array_merge(allowed_html_[tag_name_], php_array_fill_keys(Array("data-customize-partial-id", "data-customize-partial-type", "data-customize-partial-placement-context", "data-customize-partial-widget-id", "data-customize-partial-options"), True))
        # end for
        return allowed_html_
    # end def filter_wp_kses_allowed_data_attributes
    #// 
    #// Keep track of the number of times that dynamic_sidebar() was called for a given sidebar index.
    #// 
    #// This helps facilitate the uncommon scenario where a single sidebar is rendered multiple times on a template.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    sidebar_instance_count = Array()
    #// 
    #// The current request's sidebar_instance_number context.
    #// 
    #// @since 4.5.0
    #// @var int|null
    #//
    context_sidebar_instance_number = Array()
    #// 
    #// Current sidebar ID being rendered.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    current_dynamic_sidebar_id_stack = Array()
    #// 
    #// Begins keeping track of the current sidebar being rendered.
    #// 
    #// Insert marker before widgets are rendered in a dynamic sidebar.
    #// 
    #// @since 4.5.0
    #// 
    #// @param int|string $index Index, name, or ID of the dynamic sidebar.
    #//
    def start_dynamic_sidebar(self, index_=None):
        
        
        array_unshift(self.current_dynamic_sidebar_id_stack, index_)
        if (not (php_isset(lambda : self.sidebar_instance_count[index_]))):
            self.sidebar_instance_count[index_] = 0
        # end if
        self.sidebar_instance_count[index_] += 1
        if (not self.manager.selective_refresh.is_render_partials_request()):
            printf("\n<!--dynamic_sidebar_before:%s:%d-->\n", esc_html(index_), php_intval(self.sidebar_instance_count[index_]))
        # end if
    # end def start_dynamic_sidebar
    #// 
    #// Finishes keeping track of the current sidebar being rendered.
    #// 
    #// Inserts a marker after widgets are rendered in a dynamic sidebar.
    #// 
    #// @since 4.5.0
    #// 
    #// @param int|string $index Index, name, or ID of the dynamic sidebar.
    #//
    def end_dynamic_sidebar(self, index_=None):
        
        
        php_array_shift(self.current_dynamic_sidebar_id_stack)
        if (not self.manager.selective_refresh.is_render_partials_request()):
            printf("\n<!--dynamic_sidebar_after:%s:%d-->\n", esc_html(index_), php_intval(self.sidebar_instance_count[index_]))
        # end if
    # end def end_dynamic_sidebar
    #// 
    #// Current sidebar being rendered.
    #// 
    #// @since 4.5.0
    #// @var string|null
    #//
    rendering_widget_id = Array()
    #// 
    #// Current widget being rendered.
    #// 
    #// @since 4.5.0
    #// @var string|null
    #//
    rendering_sidebar_id = Array()
    #// 
    #// Filters sidebars_widgets to ensure the currently-rendered widget is the only widget in the current sidebar.
    #// 
    #// @since 4.5.0
    #// 
    #// @param array $sidebars_widgets Sidebars widgets.
    #// @return array Filtered sidebars widgets.
    #//
    def filter_sidebars_widgets_for_rendering_widget(self, sidebars_widgets_=None):
        
        
        sidebars_widgets_[self.rendering_sidebar_id] = Array(self.rendering_widget_id)
        return sidebars_widgets_
    # end def filter_sidebars_widgets_for_rendering_widget
    #// 
    #// Renders a specific widget using the supplied sidebar arguments.
    #// 
    #// @since 4.5.0
    #// 
    #// @see dynamic_sidebar()
    #// 
    #// @param WP_Customize_Partial $partial Partial.
    #// @param array                $context {
    #// Sidebar args supplied as container context.
    #// 
    #// @type string $sidebar_id              ID for sidebar for widget to render into.
    #// @type int    $sidebar_instance_number Disambiguating instance number.
    #// }
    #// @return string|false
    #//
    def render_widget_partial(self, partial_=None, context_=None):
        
        
        id_data_ = partial_.id_data()
        widget_id_ = php_array_shift(id_data_["keys"])
        if (not php_is_array(context_)) or php_empty(lambda : context_["sidebar_id"]) or (not is_registered_sidebar(context_["sidebar_id"])):
            return False
        # end if
        self.rendering_sidebar_id = context_["sidebar_id"]
        if (php_isset(lambda : context_["sidebar_instance_number"])):
            self.context_sidebar_instance_number = php_intval(context_["sidebar_instance_number"])
        # end if
        #// Filter sidebars_widgets so that only the queried widget is in the sidebar.
        self.rendering_widget_id = widget_id_
        filter_callback_ = Array(self, "filter_sidebars_widgets_for_rendering_widget")
        add_filter("sidebars_widgets", filter_callback_, 1000)
        #// Render the widget.
        ob_start()
        self.rendering_sidebar_id = context_["sidebar_id"]
        dynamic_sidebar(self.rendering_sidebar_id)
        container_ = ob_get_clean()
        #// Reset variables for next partial render.
        remove_filter("sidebars_widgets", filter_callback_, 1000)
        self.context_sidebar_instance_number = None
        self.rendering_sidebar_id = None
        self.rendering_widget_id = None
        return container_
    # end def render_widget_partial
    #// 
    #// Option Update Capturing.
    #// 
    #// 
    #// List of captured widget option updates.
    #// 
    #// @since 3.9.0
    #// @var array $_captured_options Values updated while option capture is happening.
    #//
    _captured_options = Array()
    #// 
    #// Whether option capture is currently happening.
    #// 
    #// @since 3.9.0
    #// @var bool $_is_current Whether option capture is currently happening or not.
    #//
    _is_capturing_option_updates = False
    #// 
    #// Determines whether the captured option update should be ignored.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $option_name Option name.
    #// @return bool Whether the option capture is ignored.
    #//
    def is_option_capture_ignored(self, option_name_=None):
        
        
        return 0 == php_strpos(option_name_, "_transient_")
    # end def is_option_capture_ignored
    #// 
    #// Retrieves captured widget option updates.
    #// 
    #// @since 3.9.0
    #// 
    #// @return array Array of captured options.
    #//
    def get_captured_options(self):
        
        
        return self._captured_options
    # end def get_captured_options
    #// 
    #// Retrieves the option that was captured from being saved.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $option_name Option name.
    #// @param mixed  $default     Optional. Default value to return if the option does not exist. Default false.
    #// @return mixed Value set for the option.
    #//
    def get_captured_option(self, option_name_=None, default_=None):
        if default_ is None:
            default_ = False
        # end if
        
        if php_array_key_exists(option_name_, self._captured_options):
            value_ = self._captured_options[option_name_]
        else:
            value_ = default_
        # end if
        return value_
    # end def get_captured_option
    #// 
    #// Retrieves the number of captured widget option updates.
    #// 
    #// @since 3.9.0
    #// 
    #// @return int Number of updated options.
    #//
    def count_captured_options(self):
        
        
        return php_count(self._captured_options)
    # end def count_captured_options
    #// 
    #// Begins keeping track of changes to widget options, caching new values.
    #// 
    #// @since 3.9.0
    #//
    def start_capturing_option_updates(self):
        
        
        if self._is_capturing_option_updates:
            return
        # end if
        self._is_capturing_option_updates = True
        add_filter("pre_update_option", Array(self, "capture_filter_pre_update_option"), 10, 3)
    # end def start_capturing_option_updates
    #// 
    #// Pre-filters captured option values before updating.
    #// 
    #// @since 3.9.0
    #// 
    #// @param mixed  $new_value   The new option value.
    #// @param string $option_name Name of the option.
    #// @param mixed  $old_value   The old option value.
    #// @return mixed Filtered option value.
    #//
    def capture_filter_pre_update_option(self, new_value_=None, option_name_=None, old_value_=None):
        
        
        if self.is_option_capture_ignored(option_name_):
            return new_value_
        # end if
        if (not (php_isset(lambda : self._captured_options[option_name_]))):
            add_filter(str("pre_option_") + str(option_name_), Array(self, "capture_filter_pre_get_option"))
        # end if
        self._captured_options[option_name_] = new_value_
        return old_value_
    # end def capture_filter_pre_update_option
    #// 
    #// Pre-filters captured option values before retrieving.
    #// 
    #// @since 3.9.0
    #// 
    #// @param mixed $value Value to return instead of the option value.
    #// @return mixed Filtered option value.
    #//
    def capture_filter_pre_get_option(self, value_=None):
        
        
        option_name_ = php_preg_replace("/^pre_option_/", "", current_filter())
        if (php_isset(lambda : self._captured_options[option_name_])):
            value_ = self._captured_options[option_name_]
            #// This filter is documented in wp-includes/option.php
            value_ = apply_filters("option_" + option_name_, value_, option_name_)
        # end if
        return value_
    # end def capture_filter_pre_get_option
    #// 
    #// Undoes any changes to the options since options capture began.
    #// 
    #// @since 3.9.0
    #//
    def stop_capturing_option_updates(self):
        
        
        if (not self._is_capturing_option_updates):
            return
        # end if
        remove_filter("pre_update_option", Array(self, "capture_filter_pre_update_option"), 10)
        for option_name_ in php_array_keys(self._captured_options):
            remove_filter(str("pre_option_") + str(option_name_), Array(self, "capture_filter_pre_get_option"))
        # end for
        self._captured_options = Array()
        self._is_capturing_option_updates = False
    # end def stop_capturing_option_updates
    #// 
    #// {@internal Missing Summary}
    #// 
    #// See the {@see 'customize_dynamic_setting_args'} filter.
    #// 
    #// @since 3.9.0
    #// @deprecated 4.2.0 Deprecated in favor of the {@see 'customize_dynamic_setting_args'} filter.
    #//
    def setup_widget_addition_previews(self):
        
        
        _deprecated_function(__METHOD__, "4.2.0", "customize_dynamic_setting_args")
    # end def setup_widget_addition_previews
    #// 
    #// {@internal Missing Summary}
    #// 
    #// See the {@see 'customize_dynamic_setting_args'} filter.
    #// 
    #// @since 3.9.0
    #// @deprecated 4.2.0 Deprecated in favor of the {@see 'customize_dynamic_setting_args'} filter.
    #//
    def prepreview_added_sidebars_widgets(self):
        
        
        _deprecated_function(__METHOD__, "4.2.0", "customize_dynamic_setting_args")
    # end def prepreview_added_sidebars_widgets
    #// 
    #// {@internal Missing Summary}
    #// 
    #// See the {@see 'customize_dynamic_setting_args'} filter.
    #// 
    #// @since 3.9.0
    #// @deprecated 4.2.0 Deprecated in favor of the {@see 'customize_dynamic_setting_args'} filter.
    #//
    def prepreview_added_widget_instance(self):
        
        
        _deprecated_function(__METHOD__, "4.2.0", "customize_dynamic_setting_args")
    # end def prepreview_added_widget_instance
    #// 
    #// {@internal Missing Summary}
    #// 
    #// See the {@see 'customize_dynamic_setting_args'} filter.
    #// 
    #// @since 3.9.0
    #// @deprecated 4.2.0 Deprecated in favor of the {@see 'customize_dynamic_setting_args'} filter.
    #//
    def remove_prepreview_filters(self):
        
        
        _deprecated_function(__METHOD__, "4.2.0", "customize_dynamic_setting_args")
    # end def remove_prepreview_filters
# end class WP_Customize_Widgets
