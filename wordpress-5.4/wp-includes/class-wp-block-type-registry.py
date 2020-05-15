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
#// Blocks API: WP_Block_Type_Registry class
#// 
#// @package WordPress
#// @subpackage Blocks
#// @since 5.0.0
#// 
#// 
#// Core class used for interacting with block types.
#// 
#// @since 5.0.0
#//
class WP_Block_Type_Registry():
    registered_block_types = Array()
    instance = None
    #// 
    #// Registers a block type.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string|WP_Block_Type $name Block type name including namespace, or alternatively a
    #// complete WP_Block_Type instance. In case a WP_Block_Type
    #// is provided, the $args parameter will be ignored.
    #// @param array                $args {
    #// Optional. Array of block type arguments. Any arguments may be defined, however the
    #// ones described below are supported by default. Default empty array.
    #// 
    #// @type callable $render_callback Callback used to render blocks of this block type.
    #// @type array    $attributes      Block attributes mapping, property name to schema.
    #// }
    #// @return WP_Block_Type|false The registered block type on success, or false on failure.
    #//
    def register(self, name=None, args=Array()):
        
        block_type = None
        if type(name).__name__ == "WP_Block_Type":
            block_type = name
            name = block_type.name
        # end if
        if (not php_is_string(name)):
            message = __("Block type names must be strings.")
            _doing_it_wrong(__METHOD__, message, "5.0.0")
            return False
        # end if
        if php_preg_match("/[A-Z]+/", name):
            message = __("Block type names must not contain uppercase characters.")
            _doing_it_wrong(__METHOD__, message, "5.0.0")
            return False
        # end if
        name_matcher = "/^[a-z0-9-]+\\/[a-z0-9-]+$/"
        if (not php_preg_match(name_matcher, name)):
            message = __("Block type names must contain a namespace prefix. Example: my-plugin/my-custom-block-type")
            _doing_it_wrong(__METHOD__, message, "5.0.0")
            return False
        # end if
        if self.is_registered(name):
            #// translators: %s: Block name.
            message = php_sprintf(__("Block type \"%s\" is already registered."), name)
            _doing_it_wrong(__METHOD__, message, "5.0.0")
            return False
        # end if
        if (not block_type):
            block_type = php_new_class("WP_Block_Type", lambda : WP_Block_Type(name, args))
        # end if
        self.registered_block_types[name] = block_type
        return block_type
    # end def register
    #// 
    #// Unregisters a block type.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string|WP_Block_Type $name Block type name including namespace, or alternatively a
    #// complete WP_Block_Type instance.
    #// @return WP_Block_Type|false The unregistered block type on success, or false on failure.
    #//
    def unregister(self, name=None):
        
        if type(name).__name__ == "WP_Block_Type":
            name = name.name
        # end if
        if (not self.is_registered(name)):
            #// translators: %s: Block name.
            message = php_sprintf(__("Block type \"%s\" is not registered."), name)
            _doing_it_wrong(__METHOD__, message, "5.0.0")
            return False
        # end if
        unregistered_block_type = self.registered_block_types[name]
        self.registered_block_types[name] = None
        return unregistered_block_type
    # end def unregister
    #// 
    #// Retrieves a registered block type.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $name Block type name including namespace.
    #// @return WP_Block_Type|null The registered block type, or null if it is not registered.
    #//
    def get_registered(self, name=None):
        
        if (not self.is_registered(name)):
            return None
        # end if
        return self.registered_block_types[name]
    # end def get_registered
    #// 
    #// Retrieves all registered block types.
    #// 
    #// @since 5.0.0
    #// 
    #// @return WP_Block_Type[] Associative array of `$block_type_name => $block_type` pairs.
    #//
    def get_all_registered(self):
        
        return self.registered_block_types
    # end def get_all_registered
    #// 
    #// Checks if a block type is registered.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $name Block type name including namespace.
    #// @return bool True if the block type is registered, false otherwise.
    #//
    def is_registered(self, name=None):
        
        return (php_isset(lambda : self.registered_block_types[name]))
    # end def is_registered
    #// 
    #// Utility method to retrieve the main instance of the class.
    #// 
    #// The instance will be created if it does not exist yet.
    #// 
    #// @since 5.0.0
    #// 
    #// @return WP_Block_Type_Registry The main instance.
    #//
    @classmethod
    def get_instance(self):
        
        if None == self.instance:
            self.instance = php_new_class("self", lambda : self())
        # end if
        return self.instance
    # end def get_instance
# end class WP_Block_Type_Registry
