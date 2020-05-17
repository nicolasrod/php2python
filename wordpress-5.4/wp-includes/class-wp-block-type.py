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
#// Blocks API: WP_Block_Type class
#// 
#// @package WordPress
#// @subpackage Blocks
#// @since 5.0.0
#// 
#// 
#// Core class representing a block type.
#// 
#// @since 5.0.0
#// 
#// @see register_block_type()
#//
class WP_Block_Type():
    #// 
    #// Block type key.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
    name = Array()
    #// 
    #// Block type render callback.
    #// 
    #// @since 5.0.0
    #// @var callable
    #//
    render_callback = Array()
    #// 
    #// Block type attributes property schemas.
    #// 
    #// @since 5.0.0
    #// @var array
    #//
    attributes = Array()
    #// 
    #// Block type editor script handle.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
    editor_script = Array()
    #// 
    #// Block type front end script handle.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
    script = Array()
    #// 
    #// Block type editor style handle.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
    editor_style = Array()
    #// 
    #// Block type front end style handle.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
    style = Array()
    #// 
    #// Constructor.
    #// 
    #// Will populate object properties from the provided arguments.
    #// 
    #// @since 5.0.0
    #// 
    #// @see register_block_type()
    #// 
    #// @param string       $block_type Block type name including namespace.
    #// @param array|string $args       Optional. Array or string of arguments for registering a block type.
    #// Default empty array.
    #//
    def __init__(self, block_type_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        self.name = block_type_
        self.set_props(args_)
    # end def __init__
    #// 
    #// Renders the block type output for given attributes.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array  $attributes Optional. Block attributes. Default empty array.
    #// @param string $content    Optional. Block content. Default empty string.
    #// @return string Rendered block type output.
    #//
    def render(self, attributes_=None, content_=""):
        if attributes_ is None:
            attributes_ = Array()
        # end if
        
        if (not self.is_dynamic()):
            return ""
        # end if
        attributes_ = self.prepare_attributes_for_render(attributes_)
        return php_str(php_call_user_func(self.render_callback, attributes_, content_))
    # end def render
    #// 
    #// Returns true if the block type is dynamic, or false otherwise. A dynamic
    #// block is one which defers its rendering to occur on-demand at runtime.
    #// 
    #// @since 5.0.0
    #// 
    #// @return boolean Whether block type is dynamic.
    #//
    def is_dynamic(self):
        
        
        return php_is_callable(self.render_callback)
    # end def is_dynamic
    #// 
    #// Validates attributes against the current block schema, populating
    #// defaulted and missing values.
    #// 
    #// @since 5.0.0
    #// 
    #// @param  array $attributes Original block attributes.
    #// @return array             Prepared block attributes.
    #//
    def prepare_attributes_for_render(self, attributes_=None):
        
        
        #// If there are no attribute definitions for the block type, skip
        #// processing and return vebatim.
        if (not (php_isset(lambda : self.attributes))):
            return attributes_
        # end if
        for attribute_name_,value_ in attributes_:
            #// If the attribute is not defined by the block type, it cannot be
            #// validated.
            if (not (php_isset(lambda : self.attributes[attribute_name_]))):
                continue
            # end if
            schema_ = self.attributes[attribute_name_]
            #// Validate value by JSON schema. An invalid value should revert to
            #// its default, if one exists. This occurs by virtue of the missing
            #// attributes loop immediately following. If there is not a default
            #// assigned, the attribute value should remain unset.
            is_valid_ = rest_validate_value_from_schema(value_, schema_)
            if is_wp_error(is_valid_):
                attributes_[attribute_name_] = None
            # end if
        # end for
        #// Populate values of any missing attributes for which the block type
        #// defines a default.
        missing_schema_attributes_ = php_array_diff_key(self.attributes, attributes_)
        for attribute_name_,schema_ in missing_schema_attributes_:
            if (php_isset(lambda : schema_["default"])):
                attributes_[attribute_name_] = schema_["default"]
            # end if
        # end for
        return attributes_
    # end def prepare_attributes_for_render
    #// 
    #// Sets block type properties.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array|string $args Array or string of arguments for registering a block type.
    #//
    def set_props(self, args_=None):
        
        
        args_ = wp_parse_args(args_, Array({"render_callback": None}))
        args_["name"] = self.name
        for property_name_,property_value_ in args_:
            self.property_name_ = property_value_
        # end for
    # end def set_props
    #// 
    #// Get all available block attributes including possible layout attribute from Columns block.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Array of attributes.
    #//
    def get_attributes(self):
        
        
        return php_array_merge(self.attributes, Array({"layout": Array({"type": "string"})})) if php_is_array(self.attributes) else Array({"layout": Array({"type": "string"})})
    # end def get_attributes
# end class WP_Block_Type
