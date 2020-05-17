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
#// WordPress Customize Panel classes
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.0.0
#// 
#// 
#// Customize Panel class.
#// 
#// A UI container for sections, managed by the WP_Customize_Manager.
#// 
#// @since 4.0.0
#// 
#// @see WP_Customize_Manager
#//
class WP_Customize_Panel():
    #// 
    #// Incremented with each new class instantiation, then stored in $instance_number.
    #// 
    #// Used when sorting two instances whose priorities are equal.
    #// 
    #// @since 4.1.0
    #// @var int
    #//
    instance_count = 0
    #// 
    #// Order in which this instance was created in relation to other instances.
    #// 
    #// @since 4.1.0
    #// @var int
    #//
    instance_number = Array()
    #// 
    #// WP_Customize_Manager instance.
    #// 
    #// @since 4.0.0
    #// @var WP_Customize_Manager
    #//
    manager = Array()
    #// 
    #// Unique identifier.
    #// 
    #// @since 4.0.0
    #// @var string
    #//
    id = Array()
    #// 
    #// Priority of the panel, defining the display order of panels and sections.
    #// 
    #// @since 4.0.0
    #// @var integer
    #//
    priority = 160
    #// 
    #// Capability required for the panel.
    #// 
    #// @since 4.0.0
    #// @var string
    #//
    capability = "edit_theme_options"
    #// 
    #// Theme features required to support the panel.
    #// 
    #// @since 4.0.0
    #// @var string|string[]
    #//
    theme_supports = ""
    #// 
    #// Title of the panel to show in UI.
    #// 
    #// @since 4.0.0
    #// @var string
    #//
    title = ""
    #// 
    #// Description to show in the UI.
    #// 
    #// @since 4.0.0
    #// @var string
    #//
    description = ""
    #// 
    #// Auto-expand a section in a panel when the panel is expanded when the panel only has the one section.
    #// 
    #// @since 4.7.4
    #// @var bool
    #//
    auto_expand_sole_section = False
    #// 
    #// Customizer sections for this panel.
    #// 
    #// @since 4.0.0
    #// @var array
    #//
    sections = Array()
    #// 
    #// Type of this panel.
    #// 
    #// @since 4.1.0
    #// @var string
    #//
    type = "default"
    #// 
    #// Active callback.
    #// 
    #// @since 4.1.0
    #// 
    #// @see WP_Customize_Section::active()
    #// 
    #// @var callable Callback is called with one argument, the instance of
    #// WP_Customize_Section, and returns bool to indicate whether
    #// the section is active (such as it relates to the URL currently
    #// being previewed).
    #//
    active_callback = ""
    #// 
    #// Constructor.
    #// 
    #// Any supplied $args override class property defaults.
    #// 
    #// @since 4.0.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      A specific ID for the panel.
    #// @param array                $args    {
    #// Optional. Array of properties for the new Panel object. Default empty array.
    #// 
    #// @type int             $priority        Priority of the panel, defining the display order
    #// of panels and sections. Default 160.
    #// @type string          $capability      Capability required for the panel.
    #// Default `edit_theme_options`.
    #// @type string|string[] $theme_supports  Theme features required to support the panel.
    #// @type string          $title           Title of the panel to show in UI.
    #// @type string          $description     Description to show in the UI.
    #// @type string          $type            Type of the panel.
    #// @type callable        $active_callback Active callback.
    #// }
    #//
    def __init__(self, manager_=None, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        keys_ = php_array_keys(get_object_vars(self))
        for key_ in keys_:
            if (php_isset(lambda : args_[key_])):
                self.key_ = args_[key_]
            # end if
        # end for
        self.manager = manager_
        self.id = id_
        if php_empty(lambda : self.active_callback):
            self.active_callback = Array(self, "active_callback")
        # end if
        self.instance_count += 1
        self.instance_number = self.instance_count
        self.sections = Array()
        pass
    # end def __init__
    #// 
    #// Check whether panel is active to current Customizer preview.
    #// 
    #// @since 4.1.0
    #// 
    #// @return bool Whether the panel is active to the current preview.
    #//
    def active(self):
        
        
        panel_ = self
        active_ = php_call_user_func(self.active_callback, self)
        #// 
        #// Filters response of WP_Customize_Panel::active().
        #// 
        #// @since 4.1.0
        #// 
        #// @param bool               $active Whether the Customizer panel is active.
        #// @param WP_Customize_Panel $panel  WP_Customize_Panel instance.
        #//
        active_ = apply_filters("customize_panel_active", active_, panel_)
        return active_
    # end def active
    #// 
    #// Default callback used when invoking WP_Customize_Panel::active().
    #// 
    #// Subclasses can override this with their specific logic, or they may
    #// provide an 'active_callback' argument to the constructor.
    #// 
    #// @since 4.1.0
    #// 
    #// @return bool Always true.
    #//
    def active_callback(self):
        
        
        return True
    # end def active_callback
    #// 
    #// Gather the parameters passed to client JavaScript via JSON.
    #// 
    #// @since 4.1.0
    #// 
    #// @return array The array to be exported to the client as JSON.
    #//
    def json(self):
        
        
        array_ = wp_array_slice_assoc(self, Array("id", "description", "priority", "type"))
        array_["title"] = html_entity_decode(self.title, ENT_QUOTES, get_bloginfo("charset"))
        array_["content"] = self.get_content()
        array_["active"] = self.active()
        array_["instanceNumber"] = self.instance_number
        array_["autoExpandSoleSection"] = self.auto_expand_sole_section
        return array_
    # end def json
    #// 
    #// Checks required user capabilities and whether the theme has the
    #// feature support required by the panel.
    #// 
    #// @since 4.0.0
    #// 
    #// @return bool False if theme doesn't support the panel or the user doesn't have the capability.
    #//
    def check_capabilities(self):
        
        
        if self.capability and (not current_user_can(self.capability)):
            return False
        # end if
        if self.theme_supports and (not current_theme_supports(self.theme_supports)):
            return False
        # end if
        return True
    # end def check_capabilities
    #// 
    #// Get the panel's content template for insertion into the Customizer pane.
    #// 
    #// @since 4.1.0
    #// 
    #// @return string Content for the panel.
    #//
    def get_content(self):
        
        
        ob_start()
        self.maybe_render()
        return php_trim(ob_get_clean())
    # end def get_content
    #// 
    #// Check capabilities and render the panel.
    #// 
    #// @since 4.0.0
    #//
    def maybe_render(self):
        
        
        if (not self.check_capabilities()):
            return
        # end if
        #// 
        #// Fires before rendering a Customizer panel.
        #// 
        #// @since 4.0.0
        #// 
        #// @param WP_Customize_Panel $this WP_Customize_Panel instance.
        #//
        do_action("customize_render_panel", self)
        #// 
        #// Fires before rendering a specific Customizer panel.
        #// 
        #// The dynamic portion of the hook name, `$this->id`, refers to
        #// the ID of the specific Customizer panel to be rendered.
        #// 
        #// @since 4.0.0
        #//
        do_action(str("customize_render_panel_") + str(self.id))
        self.render()
    # end def maybe_render
    #// 
    #// Render the panel container, and then its contents (via `this->render_content()`) in a subclass.
    #// 
    #// Panel containers are now rendered in JS by default, see WP_Customize_Panel::print_template().
    #// 
    #// @since 4.0.0
    #//
    def render(self):
        
        
        pass
    # end def render
    #// 
    #// Render the panel UI in a subclass.
    #// 
    #// Panel contents are now rendered in JS by default, see WP_Customize_Panel::print_template().
    #// 
    #// @since 4.1.0
    #//
    def render_content(self):
        
        
        pass
    # end def render_content
    #// 
    #// Render the panel's JS templates.
    #// 
    #// This function is only run for panel types that have been registered with
    #// WP_Customize_Manager::register_panel_type().
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Manager::register_panel_type()
    #//
    def print_template(self):
        
        
        php_print("     <script type=\"text/html\" id=\"tmpl-customize-panel-")
        php_print(esc_attr(self.type))
        php_print("-content\">\n            ")
        self.content_template()
        php_print("     </script>\n     <script type=\"text/html\" id=\"tmpl-customize-panel-")
        php_print(esc_attr(self.type))
        php_print("\">\n            ")
        self.render_template()
        php_print("     </script>\n     ")
    # end def print_template
    #// 
    #// An Underscore (JS) template for rendering this panel's container.
    #// 
    #// Class variables for this panel class are available in the `data` JS object;
    #// export custom variables by overriding WP_Customize_Panel::json().
    #// 
    #// @see WP_Customize_Panel::print_template()
    #// 
    #// @since 4.3.0
    #//
    def render_template(self):
        
        
        php_print("""       <li id=\"accordion-panel-{{ data.id }}\" class=\"accordion-section control-section control-panel control-panel-{{ data.type }}\">
        <h3 class=\"accordion-section-title\" tabindex=\"0\">
        {{ data.title }}
        <span class=\"screen-reader-text\">""")
        _e("Press return or enter to open this panel")
        php_print("""</span>
        </h3>
        <ul class=\"accordion-sub-container control-panel-content\"></ul>
        </li>
        """)
    # end def render_template
    #// 
    #// An Underscore (JS) template for this panel's content (but not its container).
    #// 
    #// Class variables for this panel class are available in the `data` JS object;
    #// export custom variables by overriding WP_Customize_Panel::json().
    #// 
    #// @see WP_Customize_Panel::print_template()
    #// 
    #// @since 4.3.0
    #//
    def content_template(self):
        
        
        php_print("     <li class=\"panel-meta customize-info accordion-section <# if ( ! data.description ) { #> cannot-expand<# } #>\">\n         <button class=\"customize-panel-back\" tabindex=\"-1\"><span class=\"screen-reader-text\">")
        _e("Back")
        php_print("""</span></button>
        <div class=\"accordion-section-title\">
        <span class=\"preview-notice\">
        """)
        #// translators: %s: The site/panel title in the Customizer.
        php_print(php_sprintf(__("You are customizing %s"), "<strong class=\"panel-title\">{{ data.title }}</strong>"))
        php_print("             </span>\n               <# if ( data.description ) { #>\n                   <button type=\"button\" class=\"customize-help-toggle dashicons dashicons-editor-help\" aria-expanded=\"false\"><span class=\"screen-reader-text\">")
        _e("Help")
        php_print("""</span></button>
        <# } #>
        </div>
        <# if ( data.description ) { #>
        <div class=\"description customize-panel-description\">
        {{{ data.description }}}
        </div>
        <# } #>
        <div class=\"customize-control-notifications-container\"></div>
        </li>
        """)
    # end def content_template
# end class WP_Customize_Panel
#// WP_Customize_Nav_Menus_Panel class
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menus-panel.php", once=True)
