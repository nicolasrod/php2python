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
#// WordPress Customize Section classes
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 3.4.0
#// 
#// 
#// Customize Section class.
#// 
#// A UI container for controls, managed by the WP_Customize_Manager class.
#// 
#// @since 3.4.0
#// 
#// @see WP_Customize_Manager
#//
class WP_Customize_Section():
    instance_count = 0
    instance_number = Array()
    manager = Array()
    id = Array()
    priority = 160
    panel = ""
    capability = "edit_theme_options"
    theme_supports = ""
    title = ""
    description = ""
    controls = Array()
    type = "default"
    active_callback = ""
    description_hidden = False
    #// 
    #// Constructor.
    #// 
    #// Any supplied $args override class property defaults.
    #// 
    #// @since 3.4.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      A specific ID of the section.
    #// @param array                $args    {
    #// Optional. Array of properties for the new Section object. Default empty array.
    #// 
    #// @type int             $priority           Priority of the section, defining the display order
    #// of panels and sections. Default 160.
    #// @type string          $panel              The panel this section belongs to (if any).
    #// Default empty.
    #// @type string          $capability         Capability required for the section.
    #// Default 'edit_theme_options'
    #// @type string|string[] $theme_supports     Theme features required to support the section.
    #// @type string          $title              Title of the section to show in UI.
    #// @type string          $description        Description to show in the UI.
    #// @type string          $type               Type of the section.
    #// @type callable        $active_callback    Active callback.
    #// @type bool            $description_hidden Hide the description behind a help icon,
    #// instead of inline above the first control.
    #// Default false.
    #// }
    #//
    def __init__(self, manager=None, id=None, args=Array()):
        
        keys = php_array_keys(get_object_vars(self))
        for key in keys:
            if (php_isset(lambda : args[key])):
                self.key = args[key]
            # end if
        # end for
        self.manager = manager
        self.id = id
        if php_empty(lambda : self.active_callback):
            self.active_callback = Array(self, "active_callback")
        # end if
        self.instance_count += 1
        self.instance_number = self.instance_count
        self.controls = Array()
        pass
    # end def __init__
    #// 
    #// Check whether section is active to current Customizer preview.
    #// 
    #// @since 4.1.0
    #// 
    #// @return bool Whether the section is active to the current preview.
    #//
    def active(self):
        
        section = self
        active = php_call_user_func(self.active_callback, self)
        #// 
        #// Filters response of WP_Customize_Section::active().
        #// 
        #// @since 4.1.0
        #// 
        #// @param bool                 $active  Whether the Customizer section is active.
        #// @param WP_Customize_Section $section WP_Customize_Section instance.
        #//
        active = apply_filters("customize_section_active", active, section)
        return active
    # end def active
    #// 
    #// Default callback used when invoking WP_Customize_Section::active().
    #// 
    #// Subclasses can override this with their specific logic, or they may provide
    #// an 'active_callback' argument to the constructor.
    #// 
    #// @since 4.1.0
    #// 
    #// @return true Always true.
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
        
        array = wp_array_slice_assoc(self, Array("id", "description", "priority", "panel", "type", "description_hidden"))
        array["title"] = html_entity_decode(self.title, ENT_QUOTES, get_bloginfo("charset"))
        array["content"] = self.get_content()
        array["active"] = self.active()
        array["instanceNumber"] = self.instance_number
        if self.panel:
            #// translators: &#9656; is the unicode right-pointing triangle. %s: Section title in the Customizer.
            array["customizeAction"] = php_sprintf(__("Customizing &#9656; %s"), esc_html(self.manager.get_panel(self.panel).title))
        else:
            array["customizeAction"] = __("Customizing")
        # end if
        return array
    # end def json
    #// 
    #// Checks required user capabilities and whether the theme has the
    #// feature support required by the section.
    #// 
    #// @since 3.4.0
    #// 
    #// @return bool False if theme doesn't support the section or user doesn't have the capability.
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
    #// Get the section's content for insertion into the Customizer pane.
    #// 
    #// @since 4.1.0
    #// 
    #// @return string Contents of the section.
    #//
    def get_content(self):
        
        ob_start()
        self.maybe_render()
        return php_trim(ob_get_clean())
    # end def get_content
    #// 
    #// Check capabilities and render the section.
    #// 
    #// @since 3.4.0
    #//
    def maybe_render(self):
        
        if (not self.check_capabilities()):
            return
        # end if
        #// 
        #// Fires before rendering a Customizer section.
        #// 
        #// @since 3.4.0
        #// 
        #// @param WP_Customize_Section $this WP_Customize_Section instance.
        #//
        do_action("customize_render_section", self)
        #// 
        #// Fires before rendering a specific Customizer section.
        #// 
        #// The dynamic portion of the hook name, `$this->id`, refers to the ID
        #// of the specific Customizer section to be rendered.
        #// 
        #// @since 3.4.0
        #//
        do_action(str("customize_render_section_") + str(self.id))
        self.render()
    # end def maybe_render
    #// 
    #// Render the section UI in a subclass.
    #// 
    #// Sections are now rendered in JS by default, see WP_Customize_Section::print_template().
    #// 
    #// @since 3.4.0
    #//
    def render(self):
        
        pass
    # end def render
    #// 
    #// Render the section's JS template.
    #// 
    #// This function is only run for section types that have been registered with
    #// WP_Customize_Manager::register_section_type().
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Manager::render_template()
    #//
    def print_template(self):
        
        php_print("     <script type=\"text/html\" id=\"tmpl-customize-section-")
        php_print(self.type)
        php_print("\">\n            ")
        self.render_template()
        php_print("     </script>\n     ")
    # end def print_template
    #// 
    #// An Underscore (JS) template for rendering this section.
    #// 
    #// Class variables for this section class are available in the `data` JS object;
    #// export custom variables by overriding WP_Customize_Section::json().
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Section::print_template()
    #//
    def render_template(self):
        
        php_print("""       <li id=\"accordion-section-{{ data.id }}\" class=\"accordion-section control-section control-section-{{ data.type }}\">
        <h3 class=\"accordion-section-title\" tabindex=\"0\">
        {{ data.title }}
        <span class=\"screen-reader-text\">""")
        _e("Press return or enter to open this section")
        php_print("""</span>
        </h3>
        <ul class=\"accordion-section-content\">
        <li class=\"customize-section-description-container section-meta <# if ( data.description_hidden ) { #>customize-info<# } #>\">
        <div class=\"customize-section-title\">
        <button class=\"customize-section-back\" tabindex=\"-1\">
        <span class=\"screen-reader-text\">""")
        _e("Back")
        php_print("""</span>
        </button>
        <h3>
        <span class=\"customize-action\">
        {{{ data.customizeAction }}}
        </span>
        {{ data.title }}
        </h3>
        <# if ( data.description && data.description_hidden ) { #>
        <button type=\"button\" class=\"customize-help-toggle dashicons dashicons-editor-help\" aria-expanded=\"false\"><span class=\"screen-reader-text\">""")
        _e("Help")
        php_print("""</span></button>
        <div class=\"description customize-section-description\">
        {{{ data.description }}}
        </div>
        <# } #>
        <div class=\"customize-control-notifications-container\"></div>
        </div>
        <# if ( data.description && ! data.description_hidden ) { #>
        <div class=\"description customize-section-description\">
        {{{ data.description }}}
        </div>
        <# } #>
        </li>
        </ul>
        </li>
        """)
    # end def render_template
# end class WP_Customize_Section
#// WP_Customize_Themes_Section class
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-themes-section.php", once=True)
#// WP_Customize_Sidebar_Section class
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-sidebar-section.php", once=True)
#// WP_Customize_Nav_Menu_Section class
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-section.php", once=True)
