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
shortcode_tags_ = Array()
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
def add_shortcode(tag_=None, callback_=None, *_args_):
    
    
    global shortcode_tags_
    php_check_if_defined("shortcode_tags_")
    if "" == php_trim(tag_):
        message_ = __("Invalid shortcode name: Empty name given.")
        _doing_it_wrong(__FUNCTION__, message_, "4.4.0")
        return
    # end if
    if 0 != php_preg_match("@[<>&/\\[\\]\\x00-\\x20=]@", tag_):
        #// translators: 1: Shortcode name, 2: Space-separated list of reserved characters.
        message_ = php_sprintf(__("Invalid shortcode name: %1$s. Do not use spaces or reserved characters: %2$s"), tag_, "& / < > [ ] =")
        _doing_it_wrong(__FUNCTION__, message_, "4.4.0")
        return
    # end if
    shortcode_tags_[tag_] = callback_
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
def remove_shortcode(tag_=None, *_args_):
    
    
    global shortcode_tags_
    php_check_if_defined("shortcode_tags_")
    shortcode_tags_[tag_] = None
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
def remove_all_shortcodes(*_args_):
    
    
    global shortcode_tags_
    php_check_if_defined("shortcode_tags_")
    shortcode_tags_ = Array()
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
def shortcode_exists(tag_=None, *_args_):
    
    
    global shortcode_tags_
    php_check_if_defined("shortcode_tags_")
    return php_array_key_exists(tag_, shortcode_tags_)
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
def has_shortcode(content_=None, tag_=None, *_args_):
    
    
    if False == php_strpos(content_, "["):
        return False
    # end if
    if shortcode_exists(tag_):
        preg_match_all("/" + get_shortcode_regex() + "/", content_, matches_, PREG_SET_ORDER)
        if php_empty(lambda : matches_):
            return False
        # end if
        for shortcode_ in matches_:
            if tag_ == shortcode_[2]:
                return True
            elif (not php_empty(lambda : shortcode_[5])) and has_shortcode(shortcode_[5], tag_):
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
def apply_shortcodes(content_=None, ignore_html_=None, *_args_):
    if ignore_html_ is None:
        ignore_html_ = False
    # end if
    
    return do_shortcode(content_, ignore_html_)
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
def do_shortcode(content_=None, ignore_html_=None, *_args_):
    if ignore_html_ is None:
        ignore_html_ = False
    # end if
    
    global shortcode_tags_
    php_check_if_defined("shortcode_tags_")
    if False == php_strpos(content_, "["):
        return content_
    # end if
    if php_empty(lambda : shortcode_tags_) or (not php_is_array(shortcode_tags_)):
        return content_
    # end if
    #// Find all registered tag names in $content.
    preg_match_all("@\\[([^<>&/\\[\\]\\x00-\\x20=]++)@", content_, matches_)
    tagnames_ = php_array_intersect(php_array_keys(shortcode_tags_), matches_[1])
    if php_empty(lambda : tagnames_):
        return content_
    # end if
    content_ = do_shortcodes_in_html_tags(content_, ignore_html_, tagnames_)
    pattern_ = get_shortcode_regex(tagnames_)
    content_ = preg_replace_callback(str("/") + str(pattern_) + str("/"), "do_shortcode_tag", content_)
    #// Always restore square braces so we don't break things like <!--[if IE ]>.
    content_ = unescape_invalid_shortcodes(content_)
    return content_
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
def get_shortcode_regex(tagnames_=None, *_args_):
    if tagnames_ is None:
        tagnames_ = None
    # end if
    
    global shortcode_tags_
    php_check_if_defined("shortcode_tags_")
    if php_empty(lambda : tagnames_):
        tagnames_ = php_array_keys(shortcode_tags_)
    # end if
    tagregexp_ = join("|", php_array_map("preg_quote", tagnames_))
    #// WARNING! Do not change this regex without changing do_shortcode_tag() and strip_shortcode_tag().
    #// Also, see shortcode_unautop() and shortcode.js.
    #// phpcs:disable Squiz.Strings.ConcatenationSpacing.PaddingFound -- don't remove regex indentation
    return "\\[" + "(\\[?)" + str("(") + str(tagregexp_) + str(")") + "(?![\\w-])" + "(" + "[^\\]\\/]*" + "(?:" + "\\/(?!\\])" + "[^\\]\\/]*" + ")*?" + ")" + "(?:" + "(\\/)" + "\\]" + "|" + "\\]" + "(?:" + "(" + "[^\\[]*+" + "(?:" + "\\[(?!\\/\\2\\])" + "[^\\[]*+" + ")*+" + ")" + "\\[\\/\\2\\]" + ")?" + ")" + "(\\]?)"
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
def do_shortcode_tag(m_=None, *_args_):
    
    
    global shortcode_tags_
    php_check_if_defined("shortcode_tags_")
    #// Allow [[foo]] syntax for escaping a tag.
    if "[" == m_[1] and "]" == m_[6]:
        return php_substr(m_[0], 1, -1)
    # end if
    tag_ = m_[2]
    attr_ = shortcode_parse_atts(m_[3])
    if (not php_is_callable(shortcode_tags_[tag_])):
        #// translators: %s: Shortcode tag.
        message_ = php_sprintf(__("Attempting to parse a shortcode without a valid callback: %s"), tag_)
        _doing_it_wrong(__FUNCTION__, message_, "4.3.0")
        return m_[0]
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
    return_ = apply_filters("pre_do_shortcode_tag", False, tag_, attr_, m_)
    if False != return_:
        return return_
    # end if
    content_ = m_[5] if (php_isset(lambda : m_[5])) else None
    output_ = m_[1] + php_call_user_func(shortcode_tags_[tag_], attr_, content_, tag_) + m_[6]
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
    return apply_filters("do_shortcode_tag", output_, tag_, attr_, m_)
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
def do_shortcodes_in_html_tags(content_=None, ignore_html_=None, tagnames_=None, *_args_):
    
    
    #// Normalize entities in unfiltered HTML before adding placeholders.
    trans_ = Array({"&#91;": "&#091;", "&#93;": "&#093;"})
    content_ = php_strtr(content_, trans_)
    trans_ = Array({"[": "&#91;", "]": "&#93;"})
    pattern_ = get_shortcode_regex(tagnames_)
    textarr_ = wp_html_split(content_)
    for element_ in textarr_:
        if "" == element_ or "<" != element_[0]:
            continue
        # end if
        noopen_ = False == php_strpos(element_, "[")
        noclose_ = False == php_strpos(element_, "]")
        if noopen_ or noclose_:
            #// This element does not contain shortcodes.
            if bool(noopen_) != bool(noclose_):
                #// Need to encode stray '[' or ']' chars.
                element_ = php_strtr(element_, trans_)
            # end if
            continue
        # end if
        if ignore_html_ or "<!--" == php_substr(element_, 0, 4) or "<![CDATA[" == php_substr(element_, 0, 9):
            #// Encode all '[' and ']' chars.
            element_ = php_strtr(element_, trans_)
            continue
        # end if
        attributes_ = wp_kses_attr_parse(element_)
        if False == attributes_:
            #// Some plugins are doing things like [name] <[email]>.
            if 1 == php_preg_match("%^<\\s*\\[\\[?[^\\[\\]]+\\]%", element_):
                element_ = preg_replace_callback(str("/") + str(pattern_) + str("/"), "do_shortcode_tag", element_)
            # end if
            #// Looks like we found some crazy unfiltered HTML. Skipping it for sanity.
            element_ = php_strtr(element_, trans_)
            continue
        # end if
        #// Get element name.
        front_ = php_array_shift(attributes_)
        back_ = php_array_pop(attributes_)
        matches_ = Array()
        php_preg_match("%[a-zA-Z0-9]+%", front_, matches_)
        elname_ = matches_[0]
        #// Look for shortcodes in each attribute separately.
        for attr_ in attributes_:
            open_ = php_strpos(attr_, "[")
            close_ = php_strpos(attr_, "]")
            if False == open_ or False == close_:
                continue
                pass
            # end if
            double_ = php_strpos(attr_, "\"")
            single_ = php_strpos(attr_, "'")
            if False == single_ or open_ < single_ and False == double_ or open_ < double_:
                #// 
                #// $attr like '[shortcode]' or 'name = [shortcode]' implies unfiltered_html.
                #// In this specific situation we assume KSES did not run because the input
                #// was written by an administrator, so we should avoid changing the output
                #// and we do not need to run KSES here.
                #//
                attr_ = preg_replace_callback(str("/") + str(pattern_) + str("/"), "do_shortcode_tag", attr_)
            else:
                #// $attr like 'name = "[shortcode]"' or "name = '[shortcode]'".
                #// We do not know if $content was unfiltered. Assume KSES ran before shortcodes.
                count_ = 0
                new_attr_ = preg_replace_callback(str("/") + str(pattern_) + str("/"), "do_shortcode_tag", attr_, -1, count_)
                if count_ > 0:
                    #// Sanitize the shortcode output using KSES.
                    new_attr_ = wp_kses_one_attr(new_attr_, elname_)
                    if "" != php_trim(new_attr_):
                        #// The shortcode is safe to use now.
                        attr_ = new_attr_
                    # end if
                # end if
            # end if
        # end for
        element_ = front_ + php_implode("", attributes_) + back_
        #// Now encode any remaining '[' or ']' chars.
        element_ = php_strtr(element_, trans_)
    # end for
    content_ = php_implode("", textarr_)
    return content_
# end def do_shortcodes_in_html_tags
#// 
#// Remove placeholders added by do_shortcodes_in_html_tags().
#// 
#// @since 4.2.3
#// 
#// @param string $content Content to search for placeholders.
#// @return string Content with placeholders removed.
#//
def unescape_invalid_shortcodes(content_=None, *_args_):
    
    
    #// Clean up entire string, avoids re-parsing HTML.
    trans_ = Array({"&#91;": "[", "&#93;": "]"})
    content_ = php_strtr(content_, trans_)
    return content_
# end def unescape_invalid_shortcodes
#// 
#// Retrieve the shortcode attributes regex.
#// 
#// @since 4.4.0
#// 
#// @return string The shortcode attribute regular expression
#//
def get_shortcode_atts_regex(*_args_):
    
    
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
def shortcode_parse_atts(text_=None, *_args_):
    
    
    atts_ = Array()
    pattern_ = get_shortcode_atts_regex()
    text_ = php_preg_replace("/[\\x{00a0}\\x{200b}]+/u", " ", text_)
    if preg_match_all(pattern_, text_, match_, PREG_SET_ORDER):
        for m_ in match_:
            if (not php_empty(lambda : m_[1])):
                atts_[php_strtolower(m_[1])] = stripcslashes(m_[2])
            elif (not php_empty(lambda : m_[3])):
                atts_[php_strtolower(m_[3])] = stripcslashes(m_[4])
            elif (not php_empty(lambda : m_[5])):
                atts_[php_strtolower(m_[5])] = stripcslashes(m_[6])
            elif (php_isset(lambda : m_[7])) and php_strlen(m_[7]):
                atts_[-1] = stripcslashes(m_[7])
            elif (php_isset(lambda : m_[8])) and php_strlen(m_[8]):
                atts_[-1] = stripcslashes(m_[8])
            elif (php_isset(lambda : m_[9])):
                atts_[-1] = stripcslashes(m_[9])
            # end if
        # end for
        #// Reject any unclosed HTML elements.
        for value_ in atts_:
            if False != php_strpos(value_, "<"):
                if 1 != php_preg_match("/^[^<]*+(?:<[^>]*+>[^<]*+)*+$/", value_):
                    value_ = ""
                # end if
            # end if
        # end for
    else:
        atts_ = php_ltrim(text_)
    # end if
    return atts_
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
def shortcode_atts(pairs_=None, atts_=None, shortcode_="", *_args_):
    
    
    atts_ = atts_
    out_ = Array()
    for name_,default_ in pairs_.items():
        if php_array_key_exists(name_, atts_):
            out_[name_] = atts_[name_]
        else:
            out_[name_] = default_
        # end if
    # end for
    if shortcode_:
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
        out_ = apply_filters(str("shortcode_atts_") + str(shortcode_), out_, pairs_, atts_, shortcode_)
    # end if
    return out_
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
def strip_shortcodes(content_=None, *_args_):
    
    
    global shortcode_tags_
    php_check_if_defined("shortcode_tags_")
    if False == php_strpos(content_, "["):
        return content_
    # end if
    if php_empty(lambda : shortcode_tags_) or (not php_is_array(shortcode_tags_)):
        return content_
    # end if
    #// Find all registered tag names in $content.
    preg_match_all("@\\[([^<>&/\\[\\]\\x00-\\x20=]++)@", content_, matches_)
    tags_to_remove_ = php_array_keys(shortcode_tags_)
    #// 
    #// Filters the list of shortcode tags to remove from the content.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array  $tags_to_remove Array of shortcode tags to remove.
    #// @param string $content        Content shortcodes are being removed from.
    #//
    tags_to_remove_ = apply_filters("strip_shortcodes_tagnames", tags_to_remove_, content_)
    tagnames_ = php_array_intersect(tags_to_remove_, matches_[1])
    if php_empty(lambda : tagnames_):
        return content_
    # end if
    content_ = do_shortcodes_in_html_tags(content_, True, tagnames_)
    pattern_ = get_shortcode_regex(tagnames_)
    content_ = preg_replace_callback(str("/") + str(pattern_) + str("/"), "strip_shortcode_tag", content_)
    #// Always restore square braces so we don't break things like <!--[if IE ]>.
    content_ = unescape_invalid_shortcodes(content_)
    return content_
# end def strip_shortcodes
#// 
#// Strips a shortcode tag based on RegEx matches against post content.
#// 
#// @since 3.3.0
#// 
#// @param array $m RegEx matches against post content.
#// @return string|false The content stripped of the tag, otherwise false.
#//
def strip_shortcode_tag(m_=None, *_args_):
    
    
    #// Allow [[foo]] syntax for escaping a tag.
    if "[" == m_[1] and "]" == m_[6]:
        return php_substr(m_[0], 1, -1)
    # end if
    return m_[1] + m_[6]
# end def strip_shortcode_tag
