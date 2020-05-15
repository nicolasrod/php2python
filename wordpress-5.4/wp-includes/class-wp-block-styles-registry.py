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
#// Blocks API: WP_Block_Styles_Registry class
#// 
#// @package WordPress
#// @subpackage Blocks
#// @since 5.3.0
#// 
#// 
#// Class used for interacting with block styles.
#// 
#// @since 5.3.0
#//
class WP_Block_Styles_Registry():
    registered_block_styles = Array()
    instance = None
    #// 
    #// Registers a block style.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $block_name       Block type name including namespace.
    #// @param array  $style_properties Array containing the properties of the style name, label,
    #// style (name of the stylesheet to be enqueued),
    #// inline_style (string containing the CSS to be added).
    #// @return boolean True if the block style was registered with success and false otherwise.
    #//
    def register(self, block_name=None, style_properties=None):
        
        if (not (php_isset(lambda : block_name))) or (not php_is_string(block_name)):
            message = __("Block name must be a string.")
            _doing_it_wrong(__METHOD__, message, "5.3.0")
            return False
        # end if
        if (not (php_isset(lambda : style_properties["name"]))) or (not php_is_string(style_properties["name"])):
            message = __("Block style name must be a string.")
            _doing_it_wrong(__METHOD__, message, "5.3.0")
            return False
        # end if
        block_style_name = style_properties["name"]
        if (not (php_isset(lambda : self.registered_block_styles[block_name]))):
            self.registered_block_styles[block_name] = Array()
        # end if
        self.registered_block_styles[block_name][block_style_name] = style_properties
        return True
    # end def register
    #// 
    #// Unregisters a block style.
    #// 
    #// @param string $block_name       Block type name including namespace.
    #// @param string $block_style_name Block style name.
    #// @return boolean True if the block style was unregistered with success and false otherwise.
    #//
    def unregister(self, block_name=None, block_style_name=None):
        
        if (not self.is_registered(block_name, block_style_name)):
            #// translators: 1: Block name, 2: Block style name.
            message = php_sprintf(__("Block \"%1$s\" does not contain a style named \"%2$s\"."), block_name, block_style_name)
            _doing_it_wrong(__METHOD__, message, "5.3.0")
            return False
        # end if
        self.registered_block_styles[block_name][block_style_name] = None
        return True
    # end def unregister
    #// 
    #// Retrieves an array containing the properties of a registered block style.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $block_name       Block type name including namespace.
    #// @param string $block_style_name Block style name.
    #// @return array Registered block style properties.
    #//
    def get_registered(self, block_name=None, block_style_name=None):
        
        if (not self.is_registered(block_name, block_style_name)):
            return None
        # end if
        return self.registered_block_styles[block_name][block_style_name]
    # end def get_registered
    #// 
    #// Retrieves all registered block styles.
    #// 
    #// @since 5.3.0
    #// 
    #// @return array Array of arrays containing the registered block styles properties grouped per block,
    #// and per style.
    #//
    def get_all_registered(self):
        
        return self.registered_block_styles
    # end def get_all_registered
    #// 
    #// Retrieves registered block styles for a specific block.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $block_name Block type name including namespace.
    #// @return array Array whose keys are block style names and whose value are block style properties.
    #//
    def get_registered_styles_for_block(self, block_name=None):
        
        if (php_isset(lambda : self.registered_block_styles[block_name])):
            return self.registered_block_styles[block_name]
        # end if
        return Array()
    # end def get_registered_styles_for_block
    #// 
    #// Checks if a block style is registered.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $block_name       Block type name including namespace.
    #// @param string $block_style_name Block style name.
    #// @return bool True if the block style is registered, false otherwise.
    #//
    def is_registered(self, block_name=None, block_style_name=None):
        
        return (php_isset(lambda : self.registered_block_styles[block_name][block_style_name]))
    # end def is_registered
    #// 
    #// Utility method to retrieve the main instance of the class.
    #// 
    #// The instance will be created if it does not exist yet.
    #// 
    #// @since 5.3.0
    #// 
    #// @return WP_Block_Styles_Registry The main instance.
    #//
    @classmethod
    def get_instance(self):
        
        if None == self.instance:
            self.instance = php_new_class("self", lambda : self())
        # end if
        return self.instance
    # end def get_instance
# end class WP_Block_Styles_Registry
