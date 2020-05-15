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
#// Functions related to registering and parsing blocks.
#// 
#// @package WordPress
#// @subpackage Blocks
#// @since 5.0.0
#// 
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
#// }
#// @return WP_Block_Type|false The registered block type on success, or false on failure.
#//
def register_block_type(name=None, args=Array(), *args_):
    
    return WP_Block_Type_Registry.get_instance().register(name, args)
# end def register_block_type
#// 
#// Unregisters a block type.
#// 
#// @since 5.0.0
#// 
#// @param string|WP_Block_Type $name Block type name including namespace, or alternatively a
#// complete WP_Block_Type instance.
#// @return WP_Block_Type|false The unregistered block type on success, or false on failure.
#//
def unregister_block_type(name=None, *args_):
    
    return WP_Block_Type_Registry.get_instance().unregister(name)
# end def unregister_block_type
#// 
#// Determine whether a post or content string has blocks.
#// 
#// This test optimizes for performance rather than strict accuracy, detecting
#// the pattern of a block but not validating its structure. For strict accuracy,
#// you should use the block parser on post content.
#// 
#// @since 5.0.0
#// @see parse_blocks()
#// 
#// @param int|string|WP_Post|null $post Optional. Post content, post ID, or post object. Defaults to global $post.
#// @return bool Whether the post has blocks.
#//
def has_blocks(post=None, *args_):
    
    if (not php_is_string(post)):
        wp_post = get_post(post)
        if type(wp_post).__name__ == "WP_Post":
            post = wp_post.post_content
        # end if
    # end if
    return False != php_strpos(str(post), "<!-- wp:")
# end def has_blocks
#// 
#// Determine whether a $post or a string contains a specific block type.
#// 
#// This test optimizes for performance rather than strict accuracy, detecting
#// the block type exists but not validating its structure. For strict accuracy,
#// you should use the block parser on post content.
#// 
#// @since 5.0.0
#// @see parse_blocks()
#// 
#// @param string                  $block_name Full Block type to look for.
#// @param int|string|WP_Post|null $post Optional. Post content, post ID, or post object. Defaults to global $post.
#// @return bool Whether the post content contains the specified block.
#//
def has_block(block_name=None, post=None, *args_):
    
    if (not has_blocks(post)):
        return False
    # end if
    if (not php_is_string(post)):
        wp_post = get_post(post)
        if type(wp_post).__name__ == "WP_Post":
            post = wp_post.post_content
        # end if
    # end if
    #// 
    #// Normalize block name to include namespace, if provided as non-namespaced.
    #// This matches behavior for WordPress 5.0.0 - 5.3.0 in matching blocks by
    #// their serialized names.
    #//
    if False == php_strpos(block_name, "/"):
        block_name = "core/" + block_name
    # end if
    #// Test for existence of block by its fully qualified name.
    has_block = False != php_strpos(post, "<!-- wp:" + block_name + " ")
    if (not has_block):
        #// 
        #// If the given block name would serialize to a different name, test for
        #// existence by the serialized form.
        #//
        serialized_block_name = strip_core_block_namespace(block_name)
        if serialized_block_name != block_name:
            has_block = False != php_strpos(post, "<!-- wp:" + serialized_block_name + " ")
        # end if
    # end if
    return has_block
# end def has_block
#// 
#// Returns an array of the names of all registered dynamic block types.
#// 
#// @since 5.0.0
#// 
#// @return string[] Array of dynamic block names.
#//
def get_dynamic_block_names(*args_):
    
    dynamic_block_names = Array()
    block_types = WP_Block_Type_Registry.get_instance().get_all_registered()
    for block_type in block_types:
        if block_type.is_dynamic():
            dynamic_block_names[-1] = block_type.name
        # end if
    # end for
    return dynamic_block_names
# end def get_dynamic_block_names
#// 
#// Given an array of attributes, returns a string in the serialized attributes
#// format prepared for post content.
#// 
#// The serialized result is a JSON-encoded string, with unicode escape sequence
#// substitution for characters which might otherwise interfere with embedding
#// the result in an HTML comment.
#// 
#// @since 5.3.1
#// 
#// @param array $attributes Attributes object.
#// @return string Serialized attributes.
#//
def serialize_block_attributes(block_attributes=None, *args_):
    
    encoded_attributes = php_json_encode(block_attributes)
    encoded_attributes = php_preg_replace("/--/", "\\u002d\\u002d", encoded_attributes)
    encoded_attributes = php_preg_replace("/</", "\\u003c", encoded_attributes)
    encoded_attributes = php_preg_replace("/>/", "\\u003e", encoded_attributes)
    encoded_attributes = php_preg_replace("/&/", "\\u0026", encoded_attributes)
    #// Regex: /\\"
    encoded_attributes = php_preg_replace("/\\\\\"/", "\\u0022", encoded_attributes)
    return encoded_attributes
# end def serialize_block_attributes
#// 
#// Returns the block name to use for serialization. This will remove the default
#// "core/" namespace from a block name.
#// 
#// @since 5.3.1
#// 
#// @param string $block_name Original block name.
#// @return string Block name to use for serialization.
#//
def strip_core_block_namespace(block_name=None, *args_):
    
    if php_is_string(block_name) and 0 == php_strpos(block_name, "core/"):
        return php_substr(block_name, 5)
    # end if
    return block_name
# end def strip_core_block_namespace
#// 
#// Returns the content of a block, including comment delimiters.
#// 
#// @since 5.3.1
#// 
#// @param string $block_name Block name.
#// @param array  $attributes Block attributes.
#// @param string $content    Block save content.
#// @return string Comment-delimited block content.
#//
def get_comment_delimited_block_content(block_name=None, block_attributes=None, block_content=None, *args_):
    
    if php_is_null(block_name):
        return block_content
    # end if
    serialized_block_name = strip_core_block_namespace(block_name)
    serialized_attributes = "" if php_empty(lambda : block_attributes) else serialize_block_attributes(block_attributes) + " "
    if php_empty(lambda : block_content):
        return php_sprintf("<!-- wp:%s %s/-->", serialized_block_name, serialized_attributes)
    # end if
    return php_sprintf("<!-- wp:%s %s-->%s<!-- /wp:%s -->", serialized_block_name, serialized_attributes, block_content, serialized_block_name)
# end def get_comment_delimited_block_content
#// 
#// Returns the content of a block, including comment delimiters, serializing all
#// attributes from the given parsed block.
#// 
#// This should be used when preparing a block to be saved to post content.
#// Prefer `render_block` when preparing a block for display. Unlike
#// `render_block`, this does not evaluate a block's `render_callback`, and will
#// instead preserve the markup as parsed.
#// 
#// @since 5.3.1
#// 
#// @param WP_Block_Parser_Block $block A single parsed block object.
#// @return string String of rendered HTML.
#//
def serialize_block(block=None, *args_):
    
    block_content = ""
    index = 0
    for chunk in block["innerContent"]:
        block_content += chunk if php_is_string(chunk) else serialize_block(block["innerBlocks"][index])
        index += 1
    # end for
    if (not php_is_array(block["attrs"])):
        block["attrs"] = Array()
    # end if
    return get_comment_delimited_block_content(block["blockName"], block["attrs"], block_content)
# end def serialize_block
#// 
#// Returns a joined string of the aggregate serialization of the given parsed
#// blocks.
#// 
#// @since 5.3.1
#// 
#// @param WP_Block_Parser_Block[] $blocks Parsed block objects.
#// @return string String of rendered HTML.
#//
def serialize_blocks(blocks=None, *args_):
    
    return php_implode("", php_array_map("serialize_block", blocks))
# end def serialize_blocks
#// 
#// Filters and sanitizes block content to remove non-allowable HTML from
#// parsed block attribute values.
#// 
#// @since 5.3.1
#// 
#// @param string         $text              Text that may contain block content.
#// @param array[]|string $allowed_html      An array of allowed HTML elements
#// and attributes, or a context name
#// such as 'post'.
#// @param string[]       $allowed_protocols Array of allowed URL protocols.
#// @return string The filtered and sanitized content result.
#//
def filter_block_content(text=None, allowed_html="post", allowed_protocols=Array(), *args_):
    
    result = ""
    blocks = parse_blocks(text)
    for block in blocks:
        block = filter_block_kses(block, allowed_html, allowed_protocols)
        result += serialize_block(block)
    # end for
    return result
# end def filter_block_content
#// 
#// Filters and sanitizes a parsed block to remove non-allowable HTML from block
#// attribute values.
#// 
#// @since 5.3.1
#// 
#// @param WP_Block_Parser_Block $block             The parsed block object.
#// @param array[]|string        $allowed_html      An array of allowed HTML
#// elements and attributes, or a
#// context name such as 'post'.
#// @param string[]              $allowed_protocols Allowed URL protocols.
#// @return array The filtered and sanitized block object result.
#//
def filter_block_kses(block=None, allowed_html=None, allowed_protocols=Array(), *args_):
    
    block["attrs"] = filter_block_kses_value(block["attrs"], allowed_html, allowed_protocols)
    if php_is_array(block["innerBlocks"]):
        for i,inner_block in block["innerBlocks"]:
            block["innerBlocks"][i] = filter_block_kses(inner_block, allowed_html, allowed_protocols)
        # end for
    # end if
    return block
# end def filter_block_kses
#// 
#// Filters and sanitizes a parsed block attribute value to remove non-allowable
#// HTML.
#// 
#// @since 5.3.1
#// 
#// @param string[]|string $value             The attribute value to filter.
#// @param array[]|string  $allowed_html      An array of allowed HTML elements
#// and attributes, or a context name
#// such as 'post'.
#// @param string[]        $allowed_protocols Array of allowed URL protocols.
#// @return string[]|string The filtered and sanitized result.
#//
def filter_block_kses_value(value=None, allowed_html=None, allowed_protocols=Array(), *args_):
    
    if php_is_array(value):
        for key,inner_value in value:
            filtered_key = filter_block_kses_value(key, allowed_html, allowed_protocols)
            filtered_value = filter_block_kses_value(inner_value, allowed_html, allowed_protocols)
            if filtered_key != key:
                value[key] = None
            # end if
            value[filtered_key] = filtered_value
        # end for
    elif php_is_string(value):
        return wp_kses(value, allowed_html, allowed_protocols)
    # end if
    return value
# end def filter_block_kses_value
#// 
#// Parses blocks out of a content string, and renders those appropriate for the excerpt.
#// 
#// As the excerpt should be a small string of text relevant to the full post content,
#// this function renders the blocks that are most likely to contain such text.
#// 
#// @since 5.0.0
#// 
#// @param string $content The content to parse.
#// @return string The parsed and filtered content.
#//
def excerpt_remove_blocks(content=None, *args_):
    
    allowed_inner_blocks = Array(None, "core/freeform", "core/heading", "core/html", "core/list", "core/media-text", "core/paragraph", "core/preformatted", "core/pullquote", "core/quote", "core/table", "core/verse")
    allowed_blocks = php_array_merge(allowed_inner_blocks, Array("core/columns"))
    #// 
    #// Filters the list of blocks that can contribute to the excerpt.
    #// 
    #// If a dynamic block is added to this list, it must not generate another
    #// excerpt, as this will cause an infinite loop to occur.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array $allowed_blocks The list of allowed blocks.
    #//
    allowed_blocks = apply_filters("excerpt_allowed_blocks", allowed_blocks)
    blocks = parse_blocks(content)
    output = ""
    for block in blocks:
        if php_in_array(block["blockName"], allowed_blocks, True):
            if (not php_empty(lambda : block["innerBlocks"])):
                if "core/columns" == block["blockName"]:
                    output += _excerpt_render_inner_columns_blocks(block, allowed_inner_blocks)
                    continue
                # end if
                #// Skip the block if it has disallowed or nested inner blocks.
                for inner_block in block["innerBlocks"]:
                    if (not php_in_array(inner_block["blockName"], allowed_inner_blocks, True)) or (not php_empty(lambda : inner_block["innerBlocks"])):
                        continue
                    # end if
                # end for
            # end if
            output += render_block(block)
        # end if
    # end for
    return output
# end def excerpt_remove_blocks
#// 
#// Render inner blocks from the `core/columns` block for generating an excerpt.
#// 
#// @since 5.2.0
#// @access private
#// 
#// @param array $columns        The parsed columns block.
#// @param array $allowed_blocks The list of allowed inner blocks.
#// @return string The rendered inner blocks.
#//
def _excerpt_render_inner_columns_blocks(columns=None, allowed_blocks=None, *args_):
    
    output = ""
    for column in columns["innerBlocks"]:
        for inner_block in column["innerBlocks"]:
            if php_in_array(inner_block["blockName"], allowed_blocks, True) and php_empty(lambda : inner_block["innerBlocks"]):
                output += render_block(inner_block)
            # end if
        # end for
    # end for
    return output
# end def _excerpt_render_inner_columns_blocks
#// 
#// Renders a single block into a HTML string.
#// 
#// @since 5.0.0
#// 
#// @global WP_Post $post The post to edit.
#// 
#// @param array $block A single parsed block object.
#// @return string String of rendered HTML.
#//
def render_block(block=None, *args_):
    
    global post
    php_check_if_defined("post")
    #// 
    #// Allows render_block() to be shortcircuited, by returning a non-null value.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string|null $pre_render The pre-rendered content. Default null.
    #// @param array       $block      The block being rendered.
    #//
    pre_render = apply_filters("pre_render_block", None, block)
    if (not php_is_null(pre_render)):
        return pre_render
    # end if
    source_block = block
    #// 
    #// Filters the block being rendered in render_block(), before it's processed.
    #// 
    #// @since 5.1.0
    #// 
    #// @param array $block        The block being rendered.
    #// @param array $source_block An un-modified copy of $block, as it appeared in the source content.
    #//
    block = apply_filters("render_block_data", block, source_block)
    block_type = WP_Block_Type_Registry.get_instance().get_registered(block["blockName"])
    is_dynamic = block["blockName"] and None != block_type and block_type.is_dynamic()
    block_content = ""
    index = 0
    for chunk in block["innerContent"]:
        block_content += chunk if php_is_string(chunk) else render_block(block["innerBlocks"][index])
        index += 1
    # end for
    if (not php_is_array(block["attrs"])):
        block["attrs"] = Array()
    # end if
    if is_dynamic:
        global_post = post
        block_content = block_type.render(block["attrs"], block_content)
        post = global_post
    # end if
    #// 
    #// Filters the content of a single block.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $block_content The block content about to be appended.
    #// @param array  $block         The full block, including name and attributes.
    #//
    return apply_filters("render_block", block_content, block)
# end def render_block
#// 
#// Parses blocks out of a content string.
#// 
#// @since 5.0.0
#// 
#// @param string $content Post content.
#// @return array[] Array of parsed block objects.
#//
def parse_blocks(content=None, *args_):
    
    #// 
    #// Filter to allow plugins to replace the server-side block parser
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $parser_class Name of block parser class.
    #//
    parser_class = apply_filters("block_parser_class", "WP_Block_Parser")
    parser = php_new_class(parser_class, lambda : {**locals(), **globals()}[parser_class]())
    return parser.parse(content)
# end def parse_blocks
#// 
#// Parses dynamic blocks out of `post_content` and re-renders them.
#// 
#// @since 5.0.0
#// 
#// @param string $content Post content.
#// @return string Updated post content.
#//
def do_blocks(content=None, *args_):
    
    blocks = parse_blocks(content)
    output = ""
    for block in blocks:
        output += render_block(block)
    # end for
    #// If there are blocks in this content, we shouldn't run wpautop() on it later.
    priority = has_filter("the_content", "wpautop")
    if False != priority and doing_filter("the_content") and has_blocks(content):
        remove_filter("the_content", "wpautop", priority)
        add_filter("the_content", "_restore_wpautop_hook", priority + 1)
    # end if
    return output
# end def do_blocks
#// 
#// If do_blocks() needs to remove wpautop() from the `the_content` filter, this re-adds it afterwards,
#// for subsequent `the_content` usage.
#// 
#// @access private
#// 
#// @since 5.0.0
#// 
#// @param string $content The post content running through this filter.
#// @return string The unmodified content.
#//
def _restore_wpautop_hook(content=None, *args_):
    
    current_priority = has_filter("the_content", "_restore_wpautop_hook")
    add_filter("the_content", "wpautop", current_priority - 1)
    remove_filter("the_content", "_restore_wpautop_hook", current_priority)
    return content
# end def _restore_wpautop_hook
#// 
#// Returns the current version of the block format that the content string is using.
#// 
#// If the string doesn't contain blocks, it returns 0.
#// 
#// @since 5.0.0
#// 
#// @param string $content Content to test.
#// @return int The block format version is 1 if the content contains one or more blocks, 0 otherwise.
#//
def block_version(content=None, *args_):
    
    return 1 if has_blocks(content) else 0
# end def block_version
#// 
#// Registers a new block style.
#// 
#// @since 5.3.0
#// 
#// @param string $block_name       Block type name including namespace.
#// @param array  $style_properties Array containing the properties of the style name, label, style (name of the stylesheet to be enqueued), inline_style (string containing the CSS to be added).
#// 
#// @return boolean True if the block style was registered with success and false otherwise.
#//
def register_block_style(block_name=None, style_properties=None, *args_):
    
    return WP_Block_Styles_Registry.get_instance().register(block_name, style_properties)
# end def register_block_style
#// 
#// Unregisters a block style.
#// 
#// @since 5.3.0
#// 
#// @param string $block_name       Block type name including namespace.
#// @param array  $block_style_name Block style name.
#// 
#// @return boolean True if the block style was unregistered with success and false otherwise.
#//
def unregister_block_style(block_name=None, block_style_name=None, *args_):
    
    return WP_Block_Styles_Registry.get_instance().unregister(block_name, block_style_name)
# end def unregister_block_style
