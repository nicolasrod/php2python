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
#// Customize API: WP_Customize_Image_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Image Control class.
#// 
#// @since 3.4.0
#// 
#// @see WP_Customize_Upload_Control
#//
class WP_Customize_Image_Control(WP_Customize_Upload_Control):
    type = "image"
    mime_type = "image"
    #// 
    #// @since 3.4.2
    #// @deprecated 4.1.0
    #//
    def prepare_control(self):
        
        
        pass
    # end def prepare_control
    #// 
    #// @since 3.4.0
    #// @deprecated 4.1.0
    #// 
    #// @param string $id
    #// @param string $label
    #// @param mixed $callback
    #//
    def add_tab(self, id_=None, label_=None, callback_=None):
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.1.0")
    # end def add_tab
    #// 
    #// @since 3.4.0
    #// @deprecated 4.1.0
    #// 
    #// @param string $id
    #//
    def remove_tab(self, id_=None):
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.1.0")
    # end def remove_tab
    #// 
    #// @since 3.4.0
    #// @deprecated 4.1.0
    #// 
    #// @param string $url
    #// @param string $thumbnail_url
    #//
    def print_tab_image(self, url_=None, thumbnail_url_=None):
        if thumbnail_url_ is None:
            thumbnail_url_ = None
        # end if
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.1.0")
    # end def print_tab_image
# end class WP_Customize_Image_Control
