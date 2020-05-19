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
#// Customize API: WP_Customize_Theme_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Theme Control class.
#// 
#// @since 4.2.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Theme_Control(WP_Customize_Control):
    #// 
    #// Customize control type.
    #// 
    #// @since 4.2.0
    #// @var string
    #//
    type = "theme"
    #// 
    #// Theme object.
    #// 
    #// @since 4.2.0
    #// @var WP_Theme
    #//
    theme = Array()
    #// 
    #// Refresh the parameters passed to the JavaScript via JSON.
    #// 
    #// @since 4.2.0
    #// 
    #// @see WP_Customize_Control::to_json()
    #//
    def to_json(self):
        
        
        super().to_json()
        self.json["theme"] = self.theme
    # end def to_json
    #// 
    #// Don't render the control content from PHP, as it's rendered via JS on load.
    #// 
    #// @since 4.2.0
    #//
    def render_content(self):
        
        
        pass
    # end def render_content
    #// 
    #// Render a JS template for theme display.
    #// 
    #// @since 4.2.0
    #//
    def content_template(self):
        
        
        #// translators: %s: Theme name.
        details_label_ = php_sprintf(__("Details for theme: %s"), "{{ data.theme.name }}")
        #// translators: %s: Theme name.
        customize_label_ = php_sprintf(__("Customize theme: %s"), "{{ data.theme.name }}")
        #// translators: %s: Theme name.
        preview_label_ = php_sprintf(__("Live preview theme: %s"), "{{ data.theme.name }}")
        #// translators: %s: Theme name.
        install_label_ = php_sprintf(__("Install and preview theme: %s"), "{{ data.theme.name }}")
        php_print("""       <# if ( data.theme.active ) { #>
        <div class=\"theme active\" tabindex=\"0\" aria-describedby=\"{{ data.section }}-{{ data.theme.id }}-action\">
        <# } else { #>
        <div class=\"theme\" tabindex=\"0\" aria-describedby=\"{{ data.section }}-{{ data.theme.id }}-action\">
        <# } #>
        <# if ( data.theme.screenshot && data.theme.screenshot[0] ) { #>
        <div class=\"theme-screenshot\">
        <img data-src=\"{{ data.theme.screenshot[0] }}\" alt=\"\" />
        </div>
        <# } else { #>
        <div class=\"theme-screenshot blank\"></div>
        <# } #>
        <span class=\"more-details theme-details\" id=\"{{ data.section }}-{{ data.theme.id }}-action\" aria-label=\"""")
        php_print(esc_attr(details_label_))
        php_print("\">")
        _e("Theme Details")
        php_print("""</span>
        <div class=\"theme-author\">
        """)
        #// translators: Theme author name.
        php_printf(_x("By %s", "theme author"), "{{ data.theme.author }}")
        php_print("""           </div>
        <# if ( 'installed' === data.theme.type && data.theme.hasUpdate ) { #>
        <div class=\"update-message notice inline notice-warning notice-alt\" data-slug=\"{{ data.theme.id }}\">
        <p>
        """)
        if is_multisite():
            _e("New version available.")
        else:
            php_printf(__("New version available. %s"), "<button class=\"button-link update-theme\" type=\"button\">" + __("Update now") + "</button>")
        # end if
        php_print("""                   </p>
        </div>
        <# } #>
        <# if ( data.theme.active ) { #>
        <div class=\"theme-id-container\">
        <h3 class=\"theme-name\" id=\"{{ data.section }}-{{ data.theme.id }}-name\">
        <span>""")
        _ex("Previewing:", "theme")
        php_print("""</span> {{ data.theme.name }}
        </h3>
        <div class=\"theme-actions\">
        <button type=\"button\" class=\"button button-primary customize-theme\" aria-label=\"""")
        php_print(esc_attr(customize_label_))
        php_print("\">")
        _e("Customize")
        php_print("""</button>
        </div>
        </div>
        <div class=\"notice notice-success notice-alt\"><p>""")
        _ex("Installed", "theme")
        php_print("""</p></div>
        <# } else if ( 'installed' === data.theme.type ) { #>
        <div class=\"theme-id-container\">
        <h3 class=\"theme-name\" id=\"{{ data.section }}-{{ data.theme.id }}-name\">{{ data.theme.name }}</h3>
        <div class=\"theme-actions\">
        <button type=\"button\" class=\"button button-primary preview-theme\" aria-label=\"""")
        php_print(esc_attr(preview_label_))
        php_print("\" data-slug=\"{{ data.theme.id }}\">")
        _e("Live Preview")
        php_print("""</button>
        </div>
        </div>
        <div class=\"notice notice-success notice-alt\"><p>""")
        _ex("Installed", "theme")
        php_print("""</p></div>
        <# } else { #>
        <div class=\"theme-id-container\">
        <h3 class=\"theme-name\" id=\"{{ data.section }}-{{ data.theme.id }}-name\">{{ data.theme.name }}</h3>
        <div class=\"theme-actions\">
        <button type=\"button\" class=\"button button-primary theme-install preview\" aria-label=\"""")
        php_print(esc_attr(install_label_))
        php_print("\" data-slug=\"{{ data.theme.id }}\" data-name=\"{{ data.theme.name }}\">")
        _e("Install &amp; Preview")
        php_print("""</button>
        </div>
        </div>
        <# } #>
        </div>
        """)
    # end def content_template
# end class WP_Customize_Theme_Control
