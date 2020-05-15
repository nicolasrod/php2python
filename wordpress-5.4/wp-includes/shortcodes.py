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
#// WordPress API for creating bbcode-like tags or what WordPress calls
#// "shortcodes". The tag and attribute parsing or regular expression code is
#// based on the Textpattern tag parser.
#// 
#// A few examples are below:
#// 
#// [shortcode /]
#// [shortcode foo="bar" baz="bing" /]
#// [shortcode foo="bar"]content[/shortcode]
#// 
#// Shortcode tags support attributes and enclosed content, but does not entirely
#// support inline shortcodes in other shortcodes. You will have to call the
#// shortcode parser in your function to account for that.
#// 
#// {@internal
#// Please be aware that the above note was made during the beta of WordPress 2.6
#// and in the future may not be accurate. Please update the note when it is no
#// longer the case.}}
#// 
#// To apply shortcode tags to content:
#// 
#// $out = do_shortcode( $content );
#// 
#// @link https://developer.wordpress.org/plugins/shortcodes
#// 
#// @package WordPress
#// @subpackage Shortcodes
#// @since 2.5.0
#// 
#// 
#// Container for storing shortcode tags and their hook to call for the shortcode
#// 
#// @since 2.5.0
#// 
#// @name $shortcode_tags
#// @var array
#// @global array $shortcode_tags
#//
shortcode_tags = Array()
#// 
#// Adds a new shortcode.
#// 
#// Care should be taken through prefixing or other means to ensure that the
#// shortcode tag being added is unique and will not conflict with other,
#// already-added shortcode tags. In the event of a duplicated tag, the tag
#// loaded last will take precedence.
#// 
#// @since 2.5.0
#// 
#// @global array $shortcode_tags
#// 
#// @param string   $tag      Shortcode tag to be searched in post content.
#// @param callable $callback The callback function to run when the shortcode is found.
#// Every shortcode callback is passed three parameters by default,
#// including an array of attributes (`$atts`), the shortcode content
#// or null if not set (`$content`), and finally the shortcode tag
#// itself (`$shortcode_tag`), in that order.
#//
def add_shortcode(tag=None, callback=None, *args_):
    
    global shortcode_tags
    php_check_if_defined("shortcode_tags")
    if "" == php_trim(tag):
        message = __("Invalid shortcode name: Empty name given.")
        _doing_it_wrong(__FUNCTION__, message, "4.4.0")
        return
    # end if
    if 0 != php_preg_match("@[<>&/\\[\\]\\x00-\\x20=]@", tag):
        #// translators: 1: Shortcode name, 2: Space-separated list of reserved characters.
        message = php_sprintf(__("Invalid shortcode name: %1$s. Do not use spaces or reserved characters: %2$s"), tag, "& / < > [ ] =")
        _doing_it_wrong(__FUNCTION__, message, "4.4.0")
        return
    # end if
    shortcode_tags[tag] = callback
# end def add_shortcode
#// 
#// Removes hook for shortcode.
#// 
#// @since 2.5.0
#// 
#// @global array $shortcode_tags
#// 
#// @param string $tag Shortcode tag to remove hook for.
#//
def remove_shortcode(tag=None, *args_):
    
    global shortcode_tags
    php_check_if_defined("shortcode_tags")
    shortcode_tags[tag] = None
# end def remove_shortcode
#// 
#// Clear all shortcodes.
#// 
#// This function is simple, it clears all of the shortcode tags by replacing the
#// shortcodes global by a empty array. This is actually a very efficient method
#// for removing all shortcodes.
#// 
#// @since 2.5.0
#// 
#// @global array $shortcode_tags
#//
def remove_all_shortcodes(*args_):
    
    global shortcode_tags
    php_check_if_defined("shortcode_tags")
    shortcode_tags = Array()
# end def remove_all_shortcodes
#// 
#// Whether a registered shortcode exists named $tag
#// 
#// @since 3.6.0
#// 
#// @global array $shortcode_tags List of shortcode tags and their callback hooks.
#// 
#// @param string $tag Shortcode tag to check.
#// @return bool Whether the given shortcode exists.
#//
def shortcode_exists(tag=None, *args_):
    
    global shortcode_tags
    php_check_if_defined("shortcode_tags")
    return php_array_key_exists(tag, shortcode_tags)
# end def shortcode_exists
#// 
#// Whether the passed content contains the specified shortcode
#// 
#// @since 3.6.0
#// 
#// @global array $shortcode_tags
#// 
#// @param string $content Content to search for shortcodes.
#// @param string $tag     Shortcode tag to check.
#// @return bool Whether the passed content contains the given shortcode.
#//
def has_shortcode(content=None, tag=None, *args_):
    
    if False == php_strpos(content, "["):
        return False
    # end if
    if shortcode_exists(tag):
        preg_match_all("/" + get_shortcode_regex() + "/", content, matches, PREG_SET_ORDER)
        if php_empty(lambda : matches):
            return False
        # end if
        for shortcode in matches:
            if tag == shortcode[2]:
                return True
            elif (not php_empty(lambda : shortcode[5])) and has_shortcode(shortcode[5], tag):
                return True
            # end if
        # end for
    # end if
    return False
# end def has_shortcode
#// 
#// Search content for shortcodes and filter shortcodes through their hooks.
#// 
#// This function is an alias for do_shortcode().
#// 
#// @since 5.4.0
#// 
#// @see do_shortcode()
#// 
#// @param string $content     Content to search for shortcodes.
#// @param bool   $ignore_html When true, shortcodes inside HTML elements will be skipped.
#// Default false.
#// @return string Content with shortcodes filtered out.
#//
def apply_shortcodes(content=None, ignore_html=False, *args_):
    
    return do_shortcode(content, ignore_html)
# end def apply_shortcodes
#// 
#// Search content for shortcodes and filter shortcodes through their hooks.
#// 
#// If there are no shortcode tags defined, then the content will be returned
#// without any filtering. This might cause issues when plugins are disabled but
#// the shortcode will still show up in the post or content.
#// 
#// @since 2.5.0
#// 
#// @global array $shortcode_tags List of shortcode tags and their callback hooks.
#// 
#// @param string $content     Content to search for shortcodes.
#// @param bool   $ignore_html When true, shortcodes inside HTML elements will be skipped.
#// Default false.
#// @return string Content with shortcodes filtered out.
#//
def do_shortcode(content=None, ignore_html=False, *args_):
    
    global shortcode_tags
    php_check_if_defined("shortcode_tags")
    if False == php_strpos(content, "["):
        return content
    # end if
    if php_empty(lambda : shortcode_tags) or (not php_is_array(shortcode_tags)):
        return content
    # end if
    #// Find all registered tag names in $content.
    preg_match_all("@\\[([^<>&/\\[\\]\\x00-\\x20=]++)@", content, matches)
    tagnames = php_array_intersect(php_array_keys(shortcode_tags), matches[1])
    if php_empty(lambda : tagnames):
        return content
    # end if
    content = do_shortcodes_in_html_tags(content, ignore_html, tagnames)
    pattern = get_shortcode_regex(tagnames)
    content = preg_replace_callback(str("/") + str(pattern) + str("/"), "do_shortcode_tag", content)
    #// Always restore square braces so we don't break things like <!--[if IE ]>.
    content = unescape_invalid_shortcodes(content)
    return content
# end def do_shortcode
#// 
#// Retrieve the shortcode regular expression for searching.
#// 
#// The regular expression combines the shortcode tags in the regular expression
#// in a regex class.
#// 
#// The regular expression contains 6 different sub matches to help with parsing.
#// 
#// 1 - An extra [ to allow for escaping shortcodes with double [[]]
#// 2 - The shortcode name
#// 3 - The shortcode argument list
#// 4 - The self closing
#// 5 - The content of a shortcode when it wraps some content.
#// 6 - An extra ] to allow for escaping shortcodes with double [[]]
#// 
#// @since 2.5.0
#// @since 4.4.0 Added the `$tagnames` parameter.
#// 
#// @global array $shortcode_tags
#// 
#// @param array $tagnames Optional. List of shortcodes to find. Defaults to all registered shortcodes.
#// @return string The shortcode search regular expression
#//
def get_shortcode_regex(tagnames=None, *args_):
    
    global shortcode_tags
    php_check_if_defined("shortcode_tags")
    if php_empty(lambda : tagnames):
        tagnames = php_array_keys(shortcode_tags)
    # end if
    tagregexp = join("|", php_array_map("preg_quote", tagnames))
    #// WARNING! Do not change this regex without changing do_shortcode_tag() and strip_shortcode_tag().
    #// Also, see shortcode_unautop() and shortcode.js.
    #// phpcs:disable Squiz.Strings.ConcatenationSpacing.PaddingFound -- don't remove regex indentation
    return "\\[" + "(\\[?)" + str("(") + str(tagregexp) + str(")") + "(?![\\w-])" + "(" + "[^\\]\\/]*" + "(?:" + "\\/(?!\\])" + "[^\\]\\/]*" + ")*?" + ")" + "(?:" + "(\\/)" + "\\]" + "|" + "\\]" + "(?:" + "(" + "[^\\[]*+" + "(?:" + "\\[(?!\\/\\2\\])" + "[^\\[]*+" + ")*+" + ")" + "\\[\\/\\2\\]" + ")?" + ")" + "(\\]?)"
    pass
# end def get_shortcode_regex
#// 
#// Regular Expression callable for do_shortcode() for calling shortcode hook.
#// 
#// @see get_shortcode_regex for details of the match array contents.
#// 
#// @since 2.5.0
#// @access private
#// 
#// @global array $shortcode_tags
#// 
#// @param array $m Regular expression match array
#// @return string|false False on failure.
#//
def do_shortcode_tag(m=None, *args_):
    
    global shortcode_tags
    php_check_if_defined("shortcode_tags")
    #// Allow [[foo]] syntax for escaping a tag.
    if "[" == m[1] and "]" == m[6]:
        return php_substr(m[0], 1, -1)
    # end if
    tag = m[2]
    attr = shortcode_parse_atts(m[3])
    if (not php_is_callable(shortcode_tags[tag])):
        #// translators: %s: Shortcode tag.
        message = php_sprintf(__("Attempting to parse a shortcode without a valid callback: %s"), tag)
        _doing_it_wrong(__FUNCTION__, message, "4.3.0")
        return m[0]
    # end if
    #// 
    #// Filters whether to call a shortcode callback.
    #// 
    #// Returning a non-false value from filter will short-circuit the
    #// shortcode generation process, returning that value instead.
    #// 
    #// @since 4.7.0
    #// 
    #// @param false|string $return      Short-circuit return value. Either false or the value to replace the shortcode with.
    #// @param string       $tag         Shortcode name.
    #// @param array|string $attr        Shortcode attributes array or empty string.
    #// @param array        $m           Regular expression match array.
    #//
    return_ = apply_filters("pre_do_shortcode_tag", False, tag, attr, m)
    if False != return_:
        return return_
    # end if
    content = m[5] if (php_isset(lambda : m[5])) else None
    output = m[1] + php_call_user_func(shortcode_tags[tag], attr, content, tag) + m[6]
    #// 
    #// Filters the output created by a shortcode callback.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string       $output Shortcode output.
    #// @param string       $tag    Shortcode name.
    #// @param array|string $attr   Shortcode attributes array or empty string.
    #// @param array        $m      Regular expression match array.
    #//
    return apply_filters("do_shortcode_tag", output, tag, attr, m)
# end def do_shortcode_tag
#// 
#// Search only inside HTML elements for shortcodes and process them.
#// 
#// Any [ or ] characters remaining inside elements will be HTML encoded
#// to prevent interference with shortcodes that are outside the elements.
#// Assumes $content processed by KSES already.  Users with unfiltered_html
#// capability may get unexpected output if angle braces are nested in tags.
#// 
#// @since 4.2.3
#// 
#// @param string $content Content to search for shortcodes
#// @param bool $ignore_html When true, all square braces inside elements will be encoded.
#// @param array $tagnames List of shortcodes to find.
#// @return string Content with shortcodes filtered out.
#//
def do_shortcodes_in_html_tags(content=None, ignore_html=None, tagnames=None, *args_):
    
    #// Normalize entities in unfiltered HTML before adding placeholders.
    trans = Array({"&#91;": "&#091;", "&#93;": "&#093;"})
    content = php_strtr(content, trans)
    trans = Array({"[": "&#91;", "]": "&#93;"})
    pattern = get_shortcode_regex(tagnames)
    textarr = wp_html_split(content)
    for element in textarr:
        if "" == element or "<" != element[0]:
            continue
        # end if
        noopen = False == php_strpos(element, "[")
        noclose = False == php_strpos(element, "]")
        if noopen or noclose:
            #// This element does not contain shortcodes.
            if bool(noopen) != bool(noclose):
                #// Need to encode stray '[' or ']' chars.
                element = php_strtr(element, trans)
            # end if
            continue
        # end if
        if ignore_html or "<!--" == php_substr(element, 0, 4) or "<![CDATA[" == php_substr(element, 0, 9):
            #// Encode all '[' and ']' chars.
            element = php_strtr(element, trans)
            continue
        # end if
        attributes = wp_kses_attr_parse(element)
        if False == attributes:
            #// Some plugins are doing things like [name] <[email]>.
            if 1 == php_preg_match("%^<\\s*\\[\\[?[^\\[\\]]+\\]%", element):
                element = preg_replace_callback(str("/") + str(pattern) + str("/"), "do_shortcode_tag", element)
            # end if
            #// Looks like we found some crazy unfiltered HTML. Skipping it for sanity.
            element = php_strtr(element, trans)
            continue
        # end if
        #// Get element name.
        front = php_array_shift(attributes)
        back = php_array_pop(attributes)
        matches = Array()
        php_preg_match("%[a-zA-Z0-9]+%", front, matches)
        elname = matches[0]
        #// Look for shortcodes in each attribute separately.
        for attr in attributes:
            open_ = php_strpos(attr, "[")
            close = php_strpos(attr, "]")
            if False == open_ or False == close:
                continue
                pass
            # end if
            double = php_strpos(attr, "\"")
            single = php_strpos(attr, "'")
            if False == single or open_ < single and False == double or open_ < double:
                #// 
                #// $attr like '[shortcode]' or 'name = [shortcode]' implies unfiltered_html.
                #// In this specific situation we assume KSES did not run because the input
                #// was written by an administrator, so we should avoid changing the output
                #// and we do not need to run KSES here.
                #//
                attr = preg_replace_callback(str("/") + str(pattern) + str("/"), "do_shortcode_tag", attr)
            else:
                #// $attr like 'name = "[shortcode]"' or "name = '[shortcode]'".
                #// We do not know if $content was unfiltered. Assume KSES ran before shortcodes.
                count = 0
                new_attr = preg_replace_callback(str("/") + str(pattern) + str("/"), "do_shortcode_tag", attr, -1, count)
                if count > 0:
                    #// Sanitize the shortcode output using KSES.
                    new_attr = wp_kses_one_attr(new_attr, elname)
                    if "" != php_trim(new_attr):
                        #// The shortcode is safe to use now.
                        attr = new_attr
                    # end if
                # end if
            # end if
        # end for
        element = front + php_implode("", attributes) + back
        #// Now encode any remaining '[' or ']' chars.
        element = php_strtr(element, trans)
    # end for
    content = php_implode("", textarr)
    return content
# end def do_shortcodes_in_html_tags
#// 
#// Remove placeholders added by do_shortcodes_in_html_tags().
#// 
#// @since 4.2.3
#// 
#// @param string $content Content to search for placeholders.
#// @return string Content with placeholders removed.
#//
def unescape_invalid_shortcodes(content=None, *args_):
    
    #// Clean up entire string, avoids re-parsing HTML.
    trans = Array({"&#91;": "[", "&#93;": "]"})
    content = php_strtr(content, trans)
    return content
# end def unescape_invalid_shortcodes
#// 
#// Retrieve the shortcode attributes regex.
#// 
#// @since 4.4.0
#// 
#// @return string The shortcode attribute regular expression
#//
def get_shortcode_atts_regex(*args_):
    
    return "/([\\w-]+)\\s*=\\s*\"([^\"]*)\"(?:\\s|$)|([\\w-]+)\\s*=\\s*'([^']*)'(?:\\s|$)|([\\w-]+)\\s*=\\s*([^\\s'\"]+)(?:\\s|$)|\"([^\"]*)\"(?:\\s|$)|'([^']*)'(?:\\s|$)|(\\S+)(?:\\s|$)/"
# end def get_shortcode_atts_regex
#// 
#// Retrieve all attributes from the shortcodes tag.
#// 
#// The attributes list has the attribute name as the key and the value of the
#// attribute as the value in the key/value pair. This allows for easier
#// retrieval of the attributes, since all attributes have to be known.
#// 
#// @since 2.5.0
#// 
#// @param string $text
#// @return array|string List of attribute values.
#// Returns empty array if trim( $text ) == '""'.
#// Returns empty string if trim( $text ) == ''.
#// All other matches are checked for not empty().
#//
def shortcode_parse_atts(text=None, *args_):
    
    atts = Array()
    pattern = get_shortcode_atts_regex()
    text = php_preg_replace("/[\\x{00a0}\\x{200b}]+/u", " ", text)
    if preg_match_all(pattern, text, match, PREG_SET_ORDER):
        for m in match:
            if (not php_empty(lambda : m[1])):
                atts[php_strtolower(m[1])] = stripcslashes(m[2])
            elif (not php_empty(lambda : m[3])):
                atts[php_strtolower(m[3])] = stripcslashes(m[4])
            elif (not php_empty(lambda : m[5])):
                atts[php_strtolower(m[5])] = stripcslashes(m[6])
            elif (php_isset(lambda : m[7])) and php_strlen(m[7]):
                atts[-1] = stripcslashes(m[7])
            elif (php_isset(lambda : m[8])) and php_strlen(m[8]):
                atts[-1] = stripcslashes(m[8])
            elif (php_isset(lambda : m[9])):
                atts[-1] = stripcslashes(m[9])
            # end if
        # end for
        #// Reject any unclosed HTML elements.
        for value in atts:
            if False != php_strpos(value, "<"):
                if 1 != php_preg_match("/^[^<]*+(?:<[^>]*+>[^<]*+)*+$/", value):
                    value = ""
                # end if
            # end if
        # end for
    else:
        atts = php_ltrim(text)
    # end if
    return atts
# end def shortcode_parse_atts
#// 
#// Combine user attributes with known attributes and fill in defaults when needed.
#// 
#// The pairs should be considered to be all of the attributes which are
#// supported by the caller and given as a list. The returned attributes will
#// only contain the attributes in the $pairs list.
#// 
#// If the $atts list has unsupported attributes, then they will be ignored and
#// removed from the final returned list.
#// 
#// @since 2.5.0
#// 
#// @param array  $pairs     Entire list of supported attributes and their defaults.
#// @param array  $atts      User defined attributes in shortcode tag.
#// @param string $shortcode Optional. The name of the shortcode, provided for context to enable filtering
#// @return array Combined and filtered attribute list.
#//
def shortcode_atts(pairs=None, atts=None, shortcode="", *args_):
    
    atts = atts
    out = Array()
    for name,default in pairs:
        if php_array_key_exists(name, atts):
            out[name] = atts[name]
        else:
            out[name] = default
        # end if
    # end for
    if shortcode:
        #// 
        #// Filters shortcode attributes.
        #// 
        #// If the third parameter of the shortcode_atts() function is present then this filter is available.
        #// The third parameter, $shortcode, is the name of the shortcode.
        #// 
        #// @since 3.6.0
        #// @since 4.4.0 Added the `$shortcode` parameter.
        #// 
        #// @param array  $out       The output array of shortcode attributes.
        #// @param array  $pairs     The supported attributes and their defaults.
        #// @param array  $atts      The user defined shortcode attributes.
        #// @param string $shortcode The shortcode name.
        #//
        out = apply_filters(str("shortcode_atts_") + str(shortcode), out, pairs, atts, shortcode)
    # end if
    return out
# end def shortcode_atts
#// 
#// Remove all shortcode tags from the given content.
#// 
#// @since 2.5.0
#// 
#// @global array $shortcode_tags
#// 
#// @param string $content Content to remove shortcode tags.
#// @return string Content without shortcode tags.
#//
def strip_shortcodes(content=None, *args_):
    
    global shortcode_tags
    php_check_if_defined("shortcode_tags")
    if False == php_strpos(content, "["):
        return content
    # end if
    if php_empty(lambda : shortcode_tags) or (not php_is_array(shortcode_tags)):
        return content
    # end if
    #// Find all registered tag names in $content.
    preg_match_all("@\\[([^<>&/\\[\\]\\x00-\\x20=]++)@", content, matches)
    tags_to_remove = php_array_keys(shortcode_tags)
    #// 
    #// Filters the list of shortcode tags to remove from the content.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array  $tags_to_remove Array of shortcode tags to remove.
    #// @param string $content        Content shortcodes are being removed from.
    #//
    tags_to_remove = apply_filters("strip_shortcodes_tagnames", tags_to_remove, content)
    tagnames = php_array_intersect(tags_to_remove, matches[1])
    if php_empty(lambda : tagnames):
        return content
    # end if
    content = do_shortcodes_in_html_tags(content, True, tagnames)
    pattern = get_shortcode_regex(tagnames)
    content = preg_replace_callback(str("/") + str(pattern) + str("/"), "strip_shortcode_tag", content)
    #// Always restore square braces so we don't break things like <!--[if IE ]>.
    content = unescape_invalid_shortcodes(content)
    return content
# end def strip_shortcodes
#// 
#// Strips a shortcode tag based on RegEx matches against post content.
#// 
#// @since 3.3.0
#// 
#// @param array $m RegEx matches against post content.
#// @return string|false The content stripped of the tag, otherwise false.
#//
def strip_shortcode_tag(m=None, *args_):
    
    #// Allow [[foo]] syntax for escaping a tag.
    if "[" == m[1] and "]" == m[6]:
        return php_substr(m[0], 1, -1)
    # end if
    return m[1] + m[6]
# end def strip_shortcode_tag
