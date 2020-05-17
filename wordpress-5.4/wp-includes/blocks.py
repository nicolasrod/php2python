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
def register_block_type(name_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    return WP_Block_Type_Registry.get_instance().register(name_, args_)
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
def unregister_block_type(name_=None, *_args_):
    
    
    return WP_Block_Type_Registry.get_instance().unregister(name_)
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
def has_blocks(post_=None, *_args_):
    
    
    if (not php_is_string(post_)):
        wp_post_ = get_post(post_)
        if type(wp_post_).__name__ == "WP_Post":
            post_ = wp_post_.post_content
        # end if
    # end if
    return False != php_strpos(php_str(post_), "<!-- wp:")
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
def has_block(block_name_=None, post_=None, *_args_):
    
    
    if (not has_blocks(post_)):
        return False
    # end if
    if (not php_is_string(post_)):
        wp_post_ = get_post(post_)
        if type(wp_post_).__name__ == "WP_Post":
            post_ = wp_post_.post_content
        # end if
    # end if
    #// 
    #// Normalize block name to include namespace, if provided as non-namespaced.
    #// This matches behavior for WordPress 5.0.0 - 5.3.0 in matching blocks by
    #// their serialized names.
    #//
    if False == php_strpos(block_name_, "/"):
        block_name_ = "core/" + block_name_
    # end if
    #// Test for existence of block by its fully qualified name.
    has_block_ = False != php_strpos(post_, "<!-- wp:" + block_name_ + " ")
    if (not has_block_):
        #// 
        #// If the given block name would serialize to a different name, test for
        #// existence by the serialized form.
        #//
        serialized_block_name_ = strip_core_block_namespace(block_name_)
        if serialized_block_name_ != block_name_:
            has_block_ = False != php_strpos(post_, "<!-- wp:" + serialized_block_name_ + " ")
        # end if
    # end if
    return has_block_
# end def has_block
#// 
#// Returns an array of the names of all registered dynamic block types.
#// 
#// @since 5.0.0
#// 
#// @return string[] Array of dynamic block names.
#//
def get_dynamic_block_names(*_args_):
    
    
    dynamic_block_names_ = Array()
    block_types_ = WP_Block_Type_Registry.get_instance().get_all_registered()
    for block_type_ in block_types_:
        if block_type_.is_dynamic():
            dynamic_block_names_[-1] = block_type_.name
        # end if
    # end for
    return dynamic_block_names_
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
def serialize_block_attributes(block_attributes_=None, *_args_):
    
    
    encoded_attributes_ = php_json_encode(block_attributes_)
    encoded_attributes_ = php_preg_replace("/--/", "\\u002d\\u002d", encoded_attributes_)
    encoded_attributes_ = php_preg_replace("/</", "\\u003c", encoded_attributes_)
    encoded_attributes_ = php_preg_replace("/>/", "\\u003e", encoded_attributes_)
    encoded_attributes_ = php_preg_replace("/&/", "\\u0026", encoded_attributes_)
    #// Regex: /\\"
    encoded_attributes_ = php_preg_replace("/\\\\\"/", "\\u0022", encoded_attributes_)
    return encoded_attributes_
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
def strip_core_block_namespace(block_name_=None, *_args_):
    
    
    if php_is_string(block_name_) and 0 == php_strpos(block_name_, "core/"):
        return php_substr(block_name_, 5)
    # end if
    return block_name_
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
def get_comment_delimited_block_content(block_name_=None, block_attributes_=None, block_content_=None, *_args_):
    
    
    if is_null(block_name_):
        return block_content_
    # end if
    serialized_block_name_ = strip_core_block_namespace(block_name_)
    serialized_attributes_ = "" if php_empty(lambda : block_attributes_) else serialize_block_attributes(block_attributes_) + " "
    if php_empty(lambda : block_content_):
        return php_sprintf("<!-- wp:%s %s/-->", serialized_block_name_, serialized_attributes_)
    # end if
    return php_sprintf("<!-- wp:%s %s-->%s<!-- /wp:%s -->", serialized_block_name_, serialized_attributes_, block_content_, serialized_block_name_)
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
def serialize_block(block_=None, *_args_):
    
    
    block_content_ = ""
    index_ = 0
    for chunk_ in block_["innerContent"]:
        block_content_ += chunk_ if php_is_string(chunk_) else index_
        index_ += 1
        index_ += 1
    # end for
    if (not php_is_array(block_["attrs"])):
        block_["attrs"] = Array()
    # end if
    return get_comment_delimited_block_content(block_["blockName"], block_["attrs"], block_content_)
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
def serialize_blocks(blocks_=None, *_args_):
    
    
    return php_implode("", php_array_map("serialize_block", blocks_))
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
def filter_block_content(text_=None, allowed_html_="post", allowed_protocols_=None, *_args_):
    if allowed_protocols_ is None:
        allowed_protocols_ = Array()
    # end if
    
    result_ = ""
    blocks_ = parse_blocks(text_)
    for block_ in blocks_:
        block_ = filter_block_kses(block_, allowed_html_, allowed_protocols_)
        result_ += serialize_block(block_)
    # end for
    return result_
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
def filter_block_kses(block_=None, allowed_html_=None, allowed_protocols_=None, *_args_):
    if allowed_protocols_ is None:
        allowed_protocols_ = Array()
    # end if
    
    block_["attrs"] = filter_block_kses_value(block_["attrs"], allowed_html_, allowed_protocols_)
    if php_is_array(block_["innerBlocks"]):
        for i_,inner_block_ in block_["innerBlocks"]:
            block_["innerBlocks"][i_] = filter_block_kses(inner_block_, allowed_html_, allowed_protocols_)
        # end for
    # end if
    return block_
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
def filter_block_kses_value(value_=None, allowed_html_=None, allowed_protocols_=None, *_args_):
    if allowed_protocols_ is None:
        allowed_protocols_ = Array()
    # end if
    
    if php_is_array(value_):
        for key_,inner_value_ in value_:
            filtered_key_ = filter_block_kses_value(key_, allowed_html_, allowed_protocols_)
            filtered_value_ = filter_block_kses_value(inner_value_, allowed_html_, allowed_protocols_)
            if filtered_key_ != key_:
                value_[key_] = None
            # end if
            value_[filtered_key_] = filtered_value_
        # end for
    elif php_is_string(value_):
        return wp_kses(value_, allowed_html_, allowed_protocols_)
    # end if
    return value_
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
def excerpt_remove_blocks(content_=None, *_args_):
    
    
    allowed_inner_blocks_ = Array(None, "core/freeform", "core/heading", "core/html", "core/list", "core/media-text", "core/paragraph", "core/preformatted", "core/pullquote", "core/quote", "core/table", "core/verse")
    allowed_blocks_ = php_array_merge(allowed_inner_blocks_, Array("core/columns"))
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
    allowed_blocks_ = apply_filters("excerpt_allowed_blocks", allowed_blocks_)
    blocks_ = parse_blocks(content_)
    output_ = ""
    for block_ in blocks_:
        if php_in_array(block_["blockName"], allowed_blocks_, True):
            if (not php_empty(lambda : block_["innerBlocks"])):
                if "core/columns" == block_["blockName"]:
                    output_ += _excerpt_render_inner_columns_blocks(block_, allowed_inner_blocks_)
                    continue
                # end if
                #// Skip the block if it has disallowed or nested inner blocks.
                for inner_block_ in block_["innerBlocks"]:
                    if (not php_in_array(inner_block_["blockName"], allowed_inner_blocks_, True)) or (not php_empty(lambda : inner_block_["innerBlocks"])):
                        continue
                    # end if
                # end for
            # end if
            output_ += render_block(block_)
        # end if
    # end for
    return output_
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
def _excerpt_render_inner_columns_blocks(columns_=None, allowed_blocks_=None, *_args_):
    
    
    output_ = ""
    for column_ in columns_["innerBlocks"]:
        for inner_block_ in column_["innerBlocks"]:
            if php_in_array(inner_block_["blockName"], allowed_blocks_, True) and php_empty(lambda : inner_block_["innerBlocks"]):
                output_ += render_block(inner_block_)
            # end if
        # end for
    # end for
    return output_
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
def render_block(block_=None, *_args_):
    
    
    global post_
    php_check_if_defined("post_")
    #// 
    #// Allows render_block() to be shortcircuited, by returning a non-null value.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string|null $pre_render The pre-rendered content. Default null.
    #// @param array       $block      The block being rendered.
    #//
    pre_render_ = apply_filters("pre_render_block", None, block_)
    if (not is_null(pre_render_)):
        return pre_render_
    # end if
    source_block_ = block_
    #// 
    #// Filters the block being rendered in render_block(), before it's processed.
    #// 
    #// @since 5.1.0
    #// 
    #// @param array $block        The block being rendered.
    #// @param array $source_block An un-modified copy of $block, as it appeared in the source content.
    #//
    block_ = apply_filters("render_block_data", block_, source_block_)
    block_type_ = WP_Block_Type_Registry.get_instance().get_registered(block_["blockName"])
    is_dynamic_ = block_["blockName"] and None != block_type_ and block_type_.is_dynamic()
    block_content_ = ""
    index_ = 0
    for chunk_ in block_["innerContent"]:
        block_content_ += chunk_ if php_is_string(chunk_) else index_
        index_ += 1
        index_ += 1
    # end for
    if (not php_is_array(block_["attrs"])):
        block_["attrs"] = Array()
    # end if
    if is_dynamic_:
        global_post_ = post_
        block_content_ = block_type_.render(block_["attrs"], block_content_)
        post_ = global_post_
    # end if
    #// 
    #// Filters the content of a single block.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $block_content The block content about to be appended.
    #// @param array  $block         The full block, including name and attributes.
    #//
    return apply_filters("render_block", block_content_, block_)
# end def render_block
#// 
#// Parses blocks out of a content string.
#// 
#// @since 5.0.0
#// 
#// @param string $content Post content.
#// @return array[] Array of parsed block objects.
#//
def parse_blocks(content_=None, *_args_):
    
    
    #// 
    #// Filter to allow plugins to replace the server-side block parser
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $parser_class Name of block parser class.
    #//
    parser_class_ = apply_filters("block_parser_class", "WP_Block_Parser")
    parser_ = php_new_class(parser_class_, lambda : {**locals(), **globals()}[parser_class_]())
    return parser_.parse(content_)
# end def parse_blocks
#// 
#// Parses dynamic blocks out of `post_content` and re-renders them.
#// 
#// @since 5.0.0
#// 
#// @param string $content Post content.
#// @return string Updated post content.
#//
def do_blocks(content_=None, *_args_):
    
    
    blocks_ = parse_blocks(content_)
    output_ = ""
    for block_ in blocks_:
        output_ += render_block(block_)
    # end for
    #// If there are blocks in this content, we shouldn't run wpautop() on it later.
    priority_ = has_filter("the_content", "wpautop")
    if False != priority_ and doing_filter("the_content") and has_blocks(content_):
        remove_filter("the_content", "wpautop", priority_)
        add_filter("the_content", "_restore_wpautop_hook", priority_ + 1)
    # end if
    return output_
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
def _restore_wpautop_hook(content_=None, *_args_):
    
    
    current_priority_ = has_filter("the_content", "_restore_wpautop_hook")
    add_filter("the_content", "wpautop", current_priority_ - 1)
    remove_filter("the_content", "_restore_wpautop_hook", current_priority_)
    return content_
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
def block_version(content_=None, *_args_):
    
    
    return 1 if has_blocks(content_) else 0
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
def register_block_style(block_name_=None, style_properties_=None, *_args_):
    
    
    return WP_Block_Styles_Registry.get_instance().register(block_name_, style_properties_)
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
def unregister_block_style(block_name_=None, block_style_name_=None, *_args_):
    
    
    return WP_Block_Styles_Registry.get_instance().unregister(block_name_, block_style_name_)
# end def unregister_block_style
