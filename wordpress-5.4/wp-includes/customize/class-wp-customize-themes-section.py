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
#// Customize API: WP_Customize_Themes_Section class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Themes Section class.
#// 
#// A UI container for theme controls, which are displayed within sections.
#// 
#// @since 4.2.0
#// 
#// @see WP_Customize_Section
#//
class WP_Customize_Themes_Section(WP_Customize_Section):
    #// 
    #// Section type.
    #// 
    #// @since 4.2.0
    #// @var string
    #//
    type = "themes"
    #// 
    #// Theme section action.
    #// 
    #// Defines the type of themes to load (installed, wporg, etc.).
    #// 
    #// @since 4.9.0
    #// @var string
    #//
    action = ""
    #// 
    #// Theme section filter type.
    #// 
    #// Determines whether filters are applied to loaded (local) themes or by initiating a new remote query (remote).
    #// When filtering is local, the initial themes query is not paginated by default.
    #// 
    #// @since 4.9.0
    #// @var string
    #//
    filter_type = "local"
    #// 
    #// Get section parameters for JS.
    #// 
    #// @since 4.9.0
    #// @return array Exported parameters.
    #//
    def json(self):
        
        
        exported_ = super().json()
        exported_["action"] = self.action
        exported_["filter_type"] = self.filter_type
        return exported_
    # end def json
    #// 
    #// Render a themes section as a JS template.
    #// 
    #// The template is only rendered by PHP once, so all actions are prepared at once on the server side.
    #// 
    #// @since 4.9.0
    #//
    def render_template(self):
        
        
        php_print("     <li id=\"accordion-section-{{ data.id }}\" class=\"theme-section\">\n           <button type=\"button\" class=\"customize-themes-section-title themes-section-{{ data.id }}\">{{ data.title }}</button>\n           ")
        if current_user_can("install_themes") or is_multisite():
            pass
            php_print("         ")
        # end if
        php_print("         <div class=\"customize-themes-section themes-section-{{ data.id }} control-section-content themes-php\">\n              <div class=\"theme-overlay\" tabindex=\"0\" role=\"dialog\" aria-label=\"")
        esc_attr_e("Theme Details")
        php_print("""\"></div>
        <div class=\"theme-browser rendered\">
        <div class=\"customize-preview-header themes-filter-bar\">
        """)
        self.filter_bar_content_template()
        php_print("                 </div>\n                    ")
        self.filter_drawer_content_template()
        php_print("                 <div class=\"error unexpected-error\" style=\"display: none; \">\n                      <p>\n                           ")
        printf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/"))
        php_print("""                       </p>
        </div>
        <ul class=\"themes\">
        </ul>
        <p class=\"no-themes\">""")
        _e("No themes found. Try a different search.")
        php_print("</p>\n                   <p class=\"no-themes-local\">\n                     ")
        printf(__("No themes found. Try a different search, or %s."), php_sprintf("<button type=\"button\" class=\"button-link search-dotorg-themes\">%s</button>", __("Search WordPress.org themes")))
        php_print("""                   </p>
        <p class=\"spinner\"></p>
        </div>
        </div>
        </li>
        """)
    # end def render_template
    #// 
    #// Render the filter bar portion of a themes section as a JS template.
    #// 
    #// The template is only rendered by PHP once, so all actions are prepared at once on the server side.
    #// The filter bar container is rendered by @see `render_template()`.
    #// 
    #// @since 4.9.0
    #//
    def filter_bar_content_template(self):
        
        
        php_print("     <button type=\"button\" class=\"button button-primary customize-section-back customize-themes-mobile-back\">")
        _e("Back to theme sources")
        php_print("""</button>
        <# if ( 'wporg' === data.action ) { #>
        <div class=\"search-form\">
        <label for=\"wp-filter-search-input-{{ data.id }}\" class=\"screen-reader-text\">""")
        _e("Search themes&hellip;")
        php_print("</label>\n               <input type=\"search\" id=\"wp-filter-search-input-{{ data.id }}\" placeholder=\"")
        esc_attr_e("Search themes&hellip;")
        php_print("\" aria-describedby=\"{{ data.id }}-live-search-desc\" class=\"wp-filter-search\">\n             <div class=\"search-icon\" aria-hidden=\"true\"></div>\n                <span id=\"{{ data.id }}-live-search-desc\" class=\"screen-reader-text\">")
        _e("The search results will be updated as you type.")
        php_print("""</span>
        </div>
        <button type=\"button\" class=\"button feature-filter-toggle\">
        <span class=\"filter-count-0\">""")
        _e("Filter themes")
        php_print("</span><span class=\"filter-count-filters\">\n               ")
        #// translators: %s: Number of filters selected.
        printf(__("Filter themes (%s)"), "<span class=\"theme-filter-count\">0</span>")
        php_print("""               </span>
        </button>
        <# } else { #>
        <div class=\"themes-filter-container\">
        <label for=\"{{ data.id }}-themes-filter\" class=\"screen-reader-text\">""")
        _e("Search themes&hellip;")
        php_print("</label>\n               <input type=\"search\" id=\"{{ data.id }}-themes-filter\" placeholder=\"")
        esc_attr_e("Search themes&hellip;")
        php_print("\" aria-describedby=\"{{ data.id }}-live-search-desc\" class=\"wp-filter-search wp-filter-search-themes\" />\n               <div class=\"search-icon\" aria-hidden=\"true\"></div>\n                <span id=\"{{ data.id }}-live-search-desc\" class=\"screen-reader-text\">")
        _e("The search results will be updated as you type.")
        php_print("""</span>
        </div>
        <# } #>
        <div class=\"filter-themes-count\">
        <span class=\"themes-displayed\">
        """)
        #// translators: %s: Number of themes displayed.
        php_print(php_sprintf(__("%s themes"), "<span class=\"theme-count\">0</span>"))
        php_print("         </span>\n       </div>\n        ")
    # end def filter_bar_content_template
    #// 
    #// Render the filter drawer portion of a themes section as a JS template.
    #// 
    #// The filter bar container is rendered by @see `render_template()`.
    #// 
    #// @since 4.9.0
    #//
    def filter_drawer_content_template(self):
        
        
        feature_list_ = get_theme_feature_list(False)
        pass
        php_print("     <# if ( 'wporg' === data.action ) { #>\n            <div class=\"filter-drawer filter-details\">\n              ")
        for feature_name_,features_ in feature_list_.items():
            php_print("                 <fieldset class=\"filter-group\">\n                     <legend>")
            php_print(esc_html(feature_name_))
            php_print("</legend>\n                      <div class=\"filter-group-feature\">\n                          ")
            for feature_,feature_name_ in features_.items():
                php_print("                             <input type=\"checkbox\" id=\"filter-id-")
                php_print(esc_attr(feature_))
                php_print("\" value=\"")
                php_print(esc_attr(feature_))
                php_print("\" />\n                              <label for=\"filter-id-")
                php_print(esc_attr(feature_))
                php_print("\">")
                php_print(esc_html(feature_name_))
                php_print("</label>\n                           ")
            # end for
            php_print("                     </div>\n                    </fieldset>\n               ")
        # end for
        php_print("         </div>\n        <# } #>\n       ")
    # end def filter_drawer_content_template
# end class WP_Customize_Themes_Section
