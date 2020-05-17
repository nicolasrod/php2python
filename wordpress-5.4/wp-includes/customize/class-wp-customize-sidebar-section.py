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
#// Customize API: WP_Customize_Sidebar_Section class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customizer section representing widget area (sidebar).
#// 
#// @since 4.1.0
#// 
#// @see WP_Customize_Section
#//
class WP_Customize_Sidebar_Section(WP_Customize_Section):
    #// 
    #// Type of this section.
    #// 
    #// @since 4.1.0
    #// @var string
    #//
    type = "sidebar"
    #// 
    #// Unique identifier.
    #// 
    #// @since 4.1.0
    #// @var string
    #//
    sidebar_id = Array()
    #// 
    #// Gather the parameters passed to client JavaScript via JSON.
    #// 
    #// @since 4.1.0
    #// 
    #// @return array The array to be exported to the client as JSON.
    #//
    def json(self):
        
        
        json_ = super().json()
        json_["sidebarId"] = self.sidebar_id
        return json_
    # end def json
    #// 
    #// Whether the current sidebar is rendered on the page.
    #// 
    #// @since 4.1.0
    #// 
    #// @return bool Whether sidebar is rendered.
    #//
    def active_callback(self):
        
        
        return self.manager.widgets.is_sidebar_rendered(self.sidebar_id)
    # end def active_callback
# end class WP_Customize_Sidebar_Section
