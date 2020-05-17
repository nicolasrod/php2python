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
    #// 
    #// Registered block types, as `$name => $instance` pairs.
    #// 
    #// @since 5.0.0
    #// @var WP_Block_Type[]
    #//
    registered_block_types = Array()
    #// 
    #// Container for the main instance of the class.
    #// 
    #// @since 5.0.0
    #// @var WP_Block_Type_Registry|null
    #//
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
    def register(self, name_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        block_type_ = None
        if type(name_).__name__ == "WP_Block_Type":
            block_type_ = name_
            name_ = block_type_.name
        # end if
        if (not php_is_string(name_)):
            message_ = __("Block type names must be strings.")
            _doing_it_wrong(__METHOD__, message_, "5.0.0")
            return False
        # end if
        if php_preg_match("/[A-Z]+/", name_):
            message_ = __("Block type names must not contain uppercase characters.")
            _doing_it_wrong(__METHOD__, message_, "5.0.0")
            return False
        # end if
        name_matcher_ = "/^[a-z0-9-]+\\/[a-z0-9-]+$/"
        if (not php_preg_match(name_matcher_, name_)):
            message_ = __("Block type names must contain a namespace prefix. Example: my-plugin/my-custom-block-type")
            _doing_it_wrong(__METHOD__, message_, "5.0.0")
            return False
        # end if
        if self.is_registered(name_):
            #// translators: %s: Block name.
            message_ = php_sprintf(__("Block type \"%s\" is already registered."), name_)
            _doing_it_wrong(__METHOD__, message_, "5.0.0")
            return False
        # end if
        if (not block_type_):
            block_type_ = php_new_class("WP_Block_Type", lambda : WP_Block_Type(name_, args_))
        # end if
        self.registered_block_types[name_] = block_type_
        return block_type_
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
    def unregister(self, name_=None):
        
        
        if type(name_).__name__ == "WP_Block_Type":
            name_ = name_.name
        # end if
        if (not self.is_registered(name_)):
            #// translators: %s: Block name.
            message_ = php_sprintf(__("Block type \"%s\" is not registered."), name_)
            _doing_it_wrong(__METHOD__, message_, "5.0.0")
            return False
        # end if
        unregistered_block_type_ = self.registered_block_types[name_]
        self.registered_block_types[name_] = None
        return unregistered_block_type_
    # end def unregister
    #// 
    #// Retrieves a registered block type.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $name Block type name including namespace.
    #// @return WP_Block_Type|null The registered block type, or null if it is not registered.
    #//
    def get_registered(self, name_=None):
        
        
        if (not self.is_registered(name_)):
            return None
        # end if
        return self.registered_block_types[name_]
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
    def is_registered(self, name_=None):
        
        
        return (php_isset(lambda : self.registered_block_types[name_]))
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
