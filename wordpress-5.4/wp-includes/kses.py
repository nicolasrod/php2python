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
#// kses 0.2.2 - HTML/XHTML filter that only allows some elements and attributes
#// Copyright (C) 2002, 2003, 2005  Ulf Harnhammar
#// 
#// This program is free software and open source software; you can redistribute
#// it and/or modify it under the terms of the GNU General Public License as
#// published by the Free Software Foundation; either version 2 of the License,
#// or (at your option) any later version.
#// 
#// This program is distributed in the hope that it will be useful, but WITHOUT
#// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#// FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
#// more details.
#// 
#// You should have received a copy of the GNU General Public License along
#// with this program; if not, write to the Free Software Foundation, Inc.,
#// 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#// http://www.gnu.org/licenses/gpl.html
#// 
#// [kses strips evil scripts!]
#// 
#// Added wp_ prefix to avoid conflicts with existing kses users
#// 
#// @version 0.2.2
#// @copyright (C) 2002, 2003, 2005
#// @author Ulf Harnhammar <http://advogato.org/person/metaur/>
#// 
#// @package External
#// @subpackage KSES
#// 
#// 
#// Specifies the default allowable HTML tags.
#// 
#// Using `CUSTOM_TAGS` is not recommended and should be considered deprecated. The
#// {@see 'wp_kses_allowed_html'} filter is more powerful and supplies context.
#// 
#// @see wp_kses_allowed_html()
#// @since 1.2.0
#// 
#// @var array[]|bool Array of default allowable HTML tags, or false to use the defaults.
#//
if (not php_defined("CUSTOM_TAGS")):
    php_define("CUSTOM_TAGS", False)
# end if
#// Ensure that these variables are added to the global namespace
#// (e.g. if using namespaces / autoload in the current PHP environment).
global allowedposttags_
global allowedtags_
global allowedentitynames_
php_check_if_defined("allowedposttags_","allowedtags_","allowedentitynames_")
if (not CUSTOM_TAGS):
    #// 
    #// KSES global for default allowable HTML tags.
    #// 
    #// Can be overridden with the `CUSTOM_TAGS` constant.
    #// 
    #// @var array[] $allowedposttags Array of default allowable HTML tags.
    #// @since 2.0.0
    #//
    allowedposttags_ = Array({"address": Array(), "a": Array({"href": True, "rel": True, "rev": True, "name": True, "target": True, "download": Array({"valueless": "y"})})}, {"abbr": Array(), "acronym": Array(), "area": Array({"alt": True, "coords": True, "href": True, "nohref": True, "shape": True, "target": True})}, {"article": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"aside": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"audio": Array({"autoplay": True, "controls": True, "loop": True, "muted": True, "preload": True, "src": True})}, {"b": Array(), "bdo": Array({"dir": True})}, {"big": Array(), "blockquote": Array({"cite": True, "lang": True, "xml:lang": True})}, {"br": Array(), "button": Array({"disabled": True, "name": True, "type": True, "value": True})}, {"caption": Array({"align": True})}, {"cite": Array({"dir": True, "lang": True})}, {"code": Array(), "col": Array({"align": True, "char": True, "charoff": True, "span": True, "dir": True, "valign": True, "width": True})}, {"colgroup": Array({"align": True, "char": True, "charoff": True, "span": True, "valign": True, "width": True})}, {"del": Array({"datetime": True})}, {"dd": Array(), "dfn": Array(), "details": Array({"align": True, "dir": True, "lang": True, "open": True, "xml:lang": True})}, {"div": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"dl": Array(), "dt": Array(), "em": Array(), "fieldset": Array(), "figure": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"figcaption": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"font": Array({"color": True, "face": True, "size": True})}, {"footer": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"h1": Array({"align": True})}, {"h2": Array({"align": True})}, {"h3": Array({"align": True})}, {"h4": Array({"align": True})}, {"h5": Array({"align": True})}, {"h6": Array({"align": True})}, {"header": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"hgroup": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"hr": Array({"align": True, "noshade": True, "size": True, "width": True})}, {"i": Array(), "img": Array({"alt": True, "align": True, "border": True, "height": True, "hspace": True, "longdesc": True, "vspace": True, "src": True, "usemap": True, "width": True})}, {"ins": Array({"datetime": True, "cite": True})}, {"kbd": Array(), "label": Array({"for": True})}, {"legend": Array({"align": True})}, {"li": Array({"align": True, "value": True})}, {"map": Array({"name": True})}, {"mark": Array(), "menu": Array({"type": True})}, {"nav": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"p": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"pre": Array({"width": True})}, {"q": Array({"cite": True})}, {"s": Array(), "samp": Array(), "span": Array({"dir": True, "align": True, "lang": True, "xml:lang": True})}, {"section": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"small": Array(), "strike": Array(), "strong": Array(), "sub": Array(), "summary": Array({"align": True, "dir": True, "lang": True, "xml:lang": True})}, {"sup": Array(), "table": Array({"align": True, "bgcolor": True, "border": True, "cellpadding": True, "cellspacing": True, "dir": True, "rules": True, "summary": True, "width": True})}, {"tbody": Array({"align": True, "char": True, "charoff": True, "valign": True})}, {"td": Array({"abbr": True, "align": True, "axis": True, "bgcolor": True, "char": True, "charoff": True, "colspan": True, "dir": True, "headers": True, "height": True, "nowrap": True, "rowspan": True, "scope": True, "valign": True, "width": True})}, {"textarea": Array({"cols": True, "rows": True, "disabled": True, "name": True, "readonly": True})}, {"tfoot": Array({"align": True, "char": True, "charoff": True, "valign": True})}, {"th": Array({"abbr": True, "align": True, "axis": True, "bgcolor": True, "char": True, "charoff": True, "colspan": True, "headers": True, "height": True, "nowrap": True, "rowspan": True, "scope": True, "valign": True, "width": True})}, {"thead": Array({"align": True, "char": True, "charoff": True, "valign": True})}, {"title": Array(), "tr": Array({"align": True, "bgcolor": True, "char": True, "charoff": True, "valign": True})}, {"track": Array({"default": True, "kind": True, "label": True, "src": True, "srclang": True})}, {"tt": Array(), "u": Array(), "ul": Array({"type": True})}, {"ol": Array({"start": True, "type": True, "reversed": True})}, {"var": Array(), "video": Array({"autoplay": True, "controls": True, "height": True, "loop": True, "muted": True, "poster": True, "preload": True, "src": True, "width": True})})
    #// 
    #// @var array[] $allowedtags Array of KSES allowed HTML elements.
    #// @since 1.0.0
    #//
    allowedtags_ = Array({"a": Array({"href": True, "title": True})}, {"abbr": Array({"title": True})}, {"acronym": Array({"title": True})}, {"b": Array(), "blockquote": Array({"cite": True})}, {"cite": Array(), "code": Array(), "del": Array({"datetime": True})}, {"em": Array(), "i": Array(), "q": Array({"cite": True})}, {"s": Array(), "strike": Array(), "strong": Array()})
    #// 
    #// @var string[] $allowedentitynames Array of KSES allowed HTML entitity names.
    #// @since 1.0.0
    #//
    allowedentitynames_ = Array("nbsp", "iexcl", "cent", "pound", "curren", "yen", "brvbar", "sect", "uml", "copy", "ordf", "laquo", "not", "shy", "reg", "macr", "deg", "plusmn", "acute", "micro", "para", "middot", "cedil", "ordm", "raquo", "iquest", "Agrave", "Aacute", "Acirc", "Atilde", "Auml", "Aring", "AElig", "Ccedil", "Egrave", "Eacute", "Ecirc", "Euml", "Igrave", "Iacute", "Icirc", "Iuml", "ETH", "Ntilde", "Ograve", "Oacute", "Ocirc", "Otilde", "Ouml", "times", "Oslash", "Ugrave", "Uacute", "Ucirc", "Uuml", "Yacute", "THORN", "szlig", "agrave", "aacute", "acirc", "atilde", "auml", "aring", "aelig", "ccedil", "egrave", "eacute", "ecirc", "euml", "igrave", "iacute", "icirc", "iuml", "eth", "ntilde", "ograve", "oacute", "ocirc", "otilde", "ouml", "divide", "oslash", "ugrave", "uacute", "ucirc", "uuml", "yacute", "thorn", "yuml", "quot", "amp", "lt", "gt", "apos", "OElig", "oelig", "Scaron", "scaron", "Yuml", "circ", "tilde", "ensp", "emsp", "thinsp", "zwnj", "zwj", "lrm", "rlm", "ndash", "mdash", "lsquo", "rsquo", "sbquo", "ldquo", "rdquo", "bdquo", "dagger", "Dagger", "permil", "lsaquo", "rsaquo", "euro", "fnof", "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega", "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigmaf", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega", "thetasym", "upsih", "piv", "bull", "hellip", "prime", "Prime", "oline", "frasl", "weierp", "image", "real", "trade", "alefsym", "larr", "uarr", "rarr", "darr", "harr", "crarr", "lArr", "uArr", "rArr", "dArr", "hArr", "forall", "part", "exist", "empty", "nabla", "isin", "notin", "ni", "prod", "sum", "minus", "lowast", "radic", "prop", "infin", "ang", "and", "or", "cap", "cup", "int", "sim", "cong", "asymp", "ne", "equiv", "le", "ge", "sub", "sup", "nsub", "sube", "supe", "oplus", "otimes", "perp", "sdot", "lceil", "rceil", "lfloor", "rfloor", "lang", "rang", "loz", "spades", "clubs", "hearts", "diams", "sup1", "sup2", "sup3", "frac14", "frac12", "frac34", "there4")
    allowedposttags_ = php_array_map("_wp_add_global_attributes", allowedposttags_)
else:
    allowedtags_ = wp_kses_array_lc(allowedtags_)
    allowedposttags_ = wp_kses_array_lc(allowedposttags_)
# end if
#// 
#// Filters text content and strips out disallowed HTML.
#// 
#// This function makes sure that only the allowed HTML element names, attribute
#// names, attribute values, and HTML entities will occur in the given text string.
#// 
#// This function expects unslashed data.
#// 
#// @see wp_kses_post() for specifically filtering post content and fields.
#// @see wp_allowed_protocols() for the default allowed protocols in link URLs.
#// 
#// @since 1.0.0
#// 
#// @param string         $string            Text content to filter.
#// @param array[]|string $allowed_html      An array of allowed HTML elements and attributes, or a
#// context name such as 'post'.
#// @param string[]       $allowed_protocols Array of allowed URL protocols.
#// @return string Filtered content containing only the allowed HTML.
#//
def wp_kses(string_=None, allowed_html_=None, allowed_protocols_=None, *_args_):
    if allowed_protocols_ is None:
        allowed_protocols_ = Array()
    # end if
    
    if php_empty(lambda : allowed_protocols_):
        allowed_protocols_ = wp_allowed_protocols()
    # end if
    string_ = wp_kses_no_null(string_, Array({"slash_zero": "keep"}))
    string_ = wp_kses_normalize_entities(string_)
    string_ = wp_kses_hook(string_, allowed_html_, allowed_protocols_)
    return wp_kses_split(string_, allowed_html_, allowed_protocols_)
# end def wp_kses
#// 
#// Filters one HTML attribute and ensures its value is allowed.
#// 
#// This function can escape data in some situations where `wp_kses()` must strip the whole attribute.
#// 
#// @since 4.2.3
#// 
#// @param string $string  The 'whole' attribute, including name and value.
#// @param string $element The HTML element name to which the attribute belongs.
#// @return string Filtered attribute.
#//
def wp_kses_one_attr(string_=None, element_=None, *_args_):
    
    
    uris_ = wp_kses_uri_attributes()
    allowed_html_ = wp_kses_allowed_html("post")
    allowed_protocols_ = wp_allowed_protocols()
    string_ = wp_kses_no_null(string_, Array({"slash_zero": "keep"}))
    #// Preserve leading and trailing whitespace.
    matches_ = Array()
    php_preg_match("/^\\s*/", string_, matches_)
    lead_ = matches_[0]
    php_preg_match("/\\s*$/", string_, matches_)
    trail_ = matches_[0]
    if php_empty(lambda : trail_):
        string_ = php_substr(string_, php_strlen(lead_))
    else:
        string_ = php_substr(string_, php_strlen(lead_), -php_strlen(trail_))
    # end if
    #// Parse attribute name and value from input.
    split_ = php_preg_split("/\\s*=\\s*/", string_, 2)
    name_ = split_[0]
    if php_count(split_) == 2:
        value_ = split_[1]
        #// Remove quotes surrounding $value.
        #// Also guarantee correct quoting in $string for this one attribute.
        if "" == value_:
            quote_ = ""
        else:
            quote_ = value_[0]
        # end if
        if "\"" == quote_ or "'" == quote_:
            if php_substr(value_, -1) != quote_:
                return ""
            # end if
            value_ = php_substr(value_, 1, -1)
        else:
            quote_ = "\""
        # end if
        #// Sanitize quotes, angle braces, and entities.
        value_ = esc_attr(value_)
        #// Sanitize URI values.
        if php_in_array(php_strtolower(name_), uris_):
            value_ = wp_kses_bad_protocol(value_, allowed_protocols_)
        # end if
        string_ = str(name_) + str("=") + str(quote_) + str(value_) + str(quote_)
        vless_ = "n"
    else:
        value_ = ""
        vless_ = "y"
    # end if
    #// Sanitize attribute by name.
    wp_kses_attr_check(name_, value_, string_, vless_, element_, allowed_html_)
    #// Restore whitespace.
    return lead_ + string_ + trail_
# end def wp_kses_one_attr
#// 
#// Returns an array of allowed HTML tags and attributes for a given context.
#// 
#// @since 3.5.0
#// @since 5.0.1 `form` removed as allowable HTML tag.
#// 
#// @global array $allowedposttags
#// @global array $allowedtags
#// @global array $allowedentitynames
#// 
#// @param string|array $context The context for which to retrieve tags. Allowed values are 'post',
#// 'strip', 'data', 'entities', or the name of a field filter such as
#// 'pre_user_description'.
#// @return array Array of allowed HTML tags and their allowed attributes.
#//
def wp_kses_allowed_html(context_="", *_args_):
    
    
    global allowedposttags_
    global allowedtags_
    global allowedentitynames_
    php_check_if_defined("allowedposttags_","allowedtags_","allowedentitynames_")
    if php_is_array(context_):
        #// 
        #// Filters the HTML that is allowed for a given context.
        #// 
        #// @since 3.5.0
        #// 
        #// @param array[]|string $context      Context to judge allowed tags by.
        #// @param string         $context_type Context name.
        #//
        return apply_filters("wp_kses_allowed_html", context_, "explicit")
    # end if
    for case in Switch(context_):
        if case("post"):
            #// This filter is documented in wp-includes/kses.php
            tags_ = apply_filters("wp_kses_allowed_html", allowedposttags_, context_)
            #// 5.0.1 removed the `<form>` tag, allow it if a filter is allowing it's sub-elements `<input>` or `<select>`.
            if (not CUSTOM_TAGS) and (not (php_isset(lambda : tags_["form"]))) and (php_isset(lambda : tags_["input"])) or (php_isset(lambda : tags_["select"])):
                tags_ = allowedposttags_
                tags_["form"] = Array({"action": True, "accept": True, "accept-charset": True, "enctype": True, "method": True, "name": True, "target": True})
                #// This filter is documented in wp-includes/kses.php
                tags_ = apply_filters("wp_kses_allowed_html", tags_, context_)
            # end if
            return tags_
        # end if
        if case("user_description"):
            pass
        # end if
        if case("pre_user_description"):
            tags_ = allowedtags_
            tags_["a"]["rel"] = True
            #// This filter is documented in wp-includes/kses.php
            return apply_filters("wp_kses_allowed_html", tags_, context_)
        # end if
        if case("strip"):
            #// This filter is documented in wp-includes/kses.php
            return apply_filters("wp_kses_allowed_html", Array(), context_)
        # end if
        if case("entities"):
            #// This filter is documented in wp-includes/kses.php
            return apply_filters("wp_kses_allowed_html", allowedentitynames_, context_)
        # end if
        if case("data"):
            pass
        # end if
        if case():
            #// This filter is documented in wp-includes/kses.php
            return apply_filters("wp_kses_allowed_html", allowedtags_, context_)
        # end if
    # end for
# end def wp_kses_allowed_html
#// 
#// You add any KSES hooks here.
#// 
#// There is currently only one KSES WordPress hook, {@see 'pre_kses'}, and it is called here.
#// All parameters are passed to the hooks and expected to receive a string.
#// 
#// @since 1.0.0
#// 
#// @param string          $string            Content to filter through KSES.
#// @param array[]|string  $allowed_html      List of allowed HTML elements.
#// @param string[]        $allowed_protocols Array of allowed URL protocols.
#// @return string Filtered content through {@see 'pre_kses'} hook.
#//
def wp_kses_hook(string_=None, allowed_html_=None, allowed_protocols_=None, *_args_):
    
    
    #// 
    #// Filters content to be run through kses.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string          $string            Content to run through KSES.
    #// @param array[]|string  $allowed_html      Allowed HTML elements.
    #// @param string[]        $allowed_protocols Array of allowed URL protocols.
    #//
    return apply_filters("pre_kses", string_, allowed_html_, allowed_protocols_)
# end def wp_kses_hook
#// 
#// Returns the version number of KSES.
#// 
#// @since 1.0.0
#// 
#// @return string KSES version number.
#//
def wp_kses_version(*_args_):
    
    
    return "0.2.2"
# end def wp_kses_version
#// 
#// Searches for HTML tags, no matter how malformed.
#// 
#// It also matches stray `>` characters.
#// 
#// @since 1.0.0
#// 
#// @global array $pass_allowed_html
#// @global array $pass_allowed_protocols
#// 
#// @param string   $string            Content to filter.
#// @param array    $allowed_html      Allowed HTML elements.
#// @param string[] $allowed_protocols Array of allowed URL protocols.
#// @return string Content with fixed HTML tags
#//
def wp_kses_split(string_=None, allowed_html_=None, allowed_protocols_=None, *_args_):
    
    
    global pass_allowed_html_
    global pass_allowed_protocols_
    php_check_if_defined("pass_allowed_html_","pass_allowed_protocols_")
    pass_allowed_html_ = allowed_html_
    pass_allowed_protocols_ = allowed_protocols_
    return preg_replace_callback("%(<!--.*?(-->|$))|(<[^>]*(>|$)|>)%", "_wp_kses_split_callback", string_)
# end def wp_kses_split
#// 
#// Returns an array of HTML attribute names whose value contains a URL.
#// 
#// This function returns a list of all HTML attributes that must contain
#// a URL according to the HTML specification.
#// 
#// This list includes URI attributes both allowed and disallowed by KSES.
#// 
#// @link https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes
#// 
#// @since 5.0.1
#// 
#// @return string[] HTML attribute names whose value contains a URL.
#//
def wp_kses_uri_attributes(*_args_):
    
    
    uri_attributes_ = Array("action", "archive", "background", "cite", "classid", "codebase", "data", "formaction", "href", "icon", "longdesc", "manifest", "poster", "profile", "src", "usemap", "xmlns")
    #// 
    #// Filters the list of attributes that are required to contain a URL.
    #// 
    #// Use this filter to add any `data-` attributes that are required to be
    #// validated as a URL.
    #// 
    #// @since 5.0.1
    #// 
    #// @param string[] $uri_attributes HTML attribute names whose value contains a URL.
    #//
    uri_attributes_ = apply_filters("wp_kses_uri_attributes", uri_attributes_)
    return uri_attributes_
# end def wp_kses_uri_attributes
#// 
#// Callback for `wp_kses_split()`.
#// 
#// @since 3.1.0
#// @access private
#// @ignore
#// 
#// @global array $pass_allowed_html
#// @global array $pass_allowed_protocols
#// 
#// @return string
#//
def _wp_kses_split_callback(match_=None, *_args_):
    
    
    global pass_allowed_html_
    global pass_allowed_protocols_
    php_check_if_defined("pass_allowed_html_","pass_allowed_protocols_")
    return wp_kses_split2(match_[0], pass_allowed_html_, pass_allowed_protocols_)
# end def _wp_kses_split_callback
#// 
#// Callback for `wp_kses_split()` for fixing malformed HTML tags.
#// 
#// This function does a lot of work. It rejects some very malformed things like
#// `<:::>`. It returns an empty string, if the element isn't allowed (look ma, no
#// `strip_tags()`!). Otherwise it splits the tag into an element and an attribute
#// list.
#// 
#// After the tag is split into an element and an attribute list, it is run
#// through another filter which will remove illegal attributes and once that is
#// completed, will be returned.
#// 
#// @access private
#// @ignore
#// @since 1.0.0
#// 
#// @param string   $string            Content to filter.
#// @param array    $allowed_html      Allowed HTML elements.
#// @param string[] $allowed_protocols Array of allowed URL protocols.
#// @return string Fixed HTML element
#//
def wp_kses_split2(string_=None, allowed_html_=None, allowed_protocols_=None, *_args_):
    
    
    string_ = wp_kses_stripslashes(string_)
    #// It matched a ">" character.
    if php_substr(string_, 0, 1) != "<":
        return "&gt;"
    # end if
    #// Allow HTML comments.
    if "<!--" == php_substr(string_, 0, 4):
        string_ = php_str_replace(Array("<!--", "-->"), "", string_)
        while True:
            newstring_ = wp_kses(string_, allowed_html_, allowed_protocols_)
            if not (newstring_ != string_):
                break
            # end if
            string_ = newstring_
        # end while
        if "" == string_:
            return ""
        # end if
        #// Prevent multiple dashes in comments.
        string_ = php_preg_replace("/--+/", "-", string_)
        #// Prevent three dashes closing a comment.
        string_ = php_preg_replace("/-$/", "", string_)
        return str("<!--") + str(string_) + str("-->")
    # end if
    #// It's seriously malformed.
    if (not php_preg_match("%^<\\s*(/\\s*)?([a-zA-Z0-9-]+)([^>]*)>?$%", string_, matches_)):
        return ""
    # end if
    slash_ = php_trim(matches_[1])
    elem_ = matches_[2]
    attrlist_ = matches_[3]
    if (not php_is_array(allowed_html_)):
        allowed_html_ = wp_kses_allowed_html(allowed_html_)
    # end if
    #// They are using a not allowed HTML element.
    if (not (php_isset(lambda : allowed_html_[php_strtolower(elem_)]))):
        return ""
    # end if
    #// No attributes are allowed for closing elements.
    if "" != slash_:
        return str("</") + str(elem_) + str(">")
    # end if
    return wp_kses_attr(elem_, attrlist_, allowed_html_, allowed_protocols_)
# end def wp_kses_split2
#// 
#// Removes all attributes, if none are allowed for this element.
#// 
#// If some are allowed it calls `wp_kses_hair()` to split them further, and then
#// it builds up new HTML code from the data that `kses_hair()` returns. It also
#// removes `<` and `>` characters, if there are any left. One more thing it does
#// is to check if the tag has a closing XHTML slash, and if it does, it puts one
#// in the returned code as well.
#// 
#// @since 1.0.0
#// 
#// @param string   $element           HTML element/tag.
#// @param string   $attr              HTML attributes from HTML element to closing HTML element tag.
#// @param array    $allowed_html      Allowed HTML elements.
#// @param string[] $allowed_protocols Array of allowed URL protocols.
#// @return string Sanitized HTML element.
#//
def wp_kses_attr(element_=None, attr_=None, allowed_html_=None, allowed_protocols_=None, *_args_):
    
    
    if (not php_is_array(allowed_html_)):
        allowed_html_ = wp_kses_allowed_html(allowed_html_)
    # end if
    #// Is there a closing XHTML slash at the end of the attributes?
    xhtml_slash_ = ""
    if php_preg_match("%\\s*/\\s*$%", attr_):
        xhtml_slash_ = " /"
    # end if
    #// Are any attributes allowed at all for this element?
    element_low_ = php_strtolower(element_)
    if php_empty(lambda : allowed_html_[element_low_]) or True == allowed_html_[element_low_]:
        return str("<") + str(element_) + str(xhtml_slash_) + str(">")
    # end if
    #// Split it.
    attrarr_ = wp_kses_hair(attr_, allowed_protocols_)
    #// Go through $attrarr, and save the allowed attributes for this element
    #// in $attr2.
    attr2_ = ""
    for arreach_ in attrarr_:
        if wp_kses_attr_check(arreach_["name"], arreach_["value"], arreach_["whole"], arreach_["vless"], element_, allowed_html_):
            attr2_ += " " + arreach_["whole"]
        # end if
    # end for
    #// Remove any "<" or ">" characters.
    attr2_ = php_preg_replace("/[<>]/", "", attr2_)
    return str("<") + str(element_) + str(attr2_) + str(xhtml_slash_) + str(">")
# end def wp_kses_attr
#// 
#// Determines whether an attribute is allowed.
#// 
#// @since 4.2.3
#// @since 5.0.0 Add support for `data-*` wildcard attributes.
#// 
#// @param string $name         The attribute name. Passed by reference. Returns empty string when not allowed.
#// @param string $value        The attribute value. Passed by reference. Returns a filtered value.
#// @param string $whole        The `name=value` input. Passed by reference. Returns filtered input.
#// @param string $vless        Whether the attribute is valueless. Use 'y' or 'n'.
#// @param string $element      The name of the element to which this attribute belongs.
#// @param array  $allowed_html The full list of allowed elements and attributes.
#// @return bool Whether or not the attribute is allowed.
#//
def wp_kses_attr_check(name_=None, value_=None, whole_=None, vless_=None, element_=None, allowed_html_=None, *_args_):
    
    
    name_low_ = php_strtolower(name_)
    element_low_ = php_strtolower(element_)
    if (not (php_isset(lambda : allowed_html_[element_low_]))):
        name_ = ""
        value_ = ""
        whole_ = ""
        return False
    # end if
    allowed_attr_ = allowed_html_[element_low_]
    if (not (php_isset(lambda : allowed_attr_[name_low_]))) or "" == allowed_attr_[name_low_]:
        #// 
        #// Allow `data-*` attributes.
        #// 
        #// When specifying `$allowed_html`, the attribute name should be set as
        #// `data-*` (not to be mixed with the HTML 4.0 `data` attribute, see
        #// https://www.w3.org/TR/html40/struct/objects.html#adef-data).
        #// 
        #// Note: the attribute name should only contain `A-Za-z0-9_-` chars,
        #// double hyphens `--` are not accepted by WordPress.
        #//
        if php_strpos(name_low_, "data-") == 0 and (not php_empty(lambda : allowed_attr_["data-*"])) and php_preg_match("/^data(?:-[a-z0-9_]+)+$/", name_low_, match_):
            #// 
            #// Add the whole attribute name to the allowed attributes and set any restrictions
            #// for the `data-*` attribute values for the current element.
            #//
            allowed_attr_[match_[0]] = allowed_attr_["data-*"]
        else:
            name_ = ""
            value_ = ""
            whole_ = ""
            return False
        # end if
    # end if
    if "style" == name_low_:
        new_value_ = safecss_filter_attr(value_)
        if php_empty(lambda : new_value_):
            name_ = ""
            value_ = ""
            whole_ = ""
            return False
        # end if
        whole_ = php_str_replace(value_, new_value_, whole_)
        value_ = new_value_
    # end if
    if php_is_array(allowed_attr_[name_low_]):
        #// There are some checks.
        for currkey_,currval_ in allowed_attr_[name_low_].items():
            if (not wp_kses_check_attr_val(value_, vless_, currkey_, currval_)):
                name_ = ""
                value_ = ""
                whole_ = ""
                return False
            # end if
        # end for
    # end if
    return True
# end def wp_kses_attr_check
#// 
#// Builds an attribute list from string containing attributes.
#// 
#// This function does a lot of work. It parses an attribute list into an array
#// with attribute data, and tries to do the right thing even if it gets weird
#// input. It will add quotes around attribute values that don't have any quotes
#// or apostrophes around them, to make it easier to produce HTML code that will
#// conform to W3C's HTML specification. It will also remove bad URL protocols
#// from attribute values. It also reduces duplicate attributes by using the
#// attribute defined first (`foo='bar' foo='baz'` will result in `foo='bar'`).
#// 
#// @since 1.0.0
#// 
#// @param string   $attr              Attribute list from HTML element to closing HTML element tag.
#// @param string[] $allowed_protocols Array of allowed URL protocols.
#// @return array[] Array of attribute information after parsing.
#//
def wp_kses_hair(attr_=None, allowed_protocols_=None, *_args_):
    
    
    attrarr_ = Array()
    mode_ = 0
    attrname_ = ""
    uris_ = wp_kses_uri_attributes()
    #// Loop through the whole attribute list.
    while True:
        
        if not (php_strlen(attr_) != 0):
            break
        # end if
        working_ = 0
        #// Was the last operation successful?
        for case in Switch(mode_):
            if case(0):
                if php_preg_match("/^([-a-zA-Z:]+)/", attr_, match_):
                    attrname_ = match_[1]
                    working_ = 1
                    mode_ = 1
                    attr_ = php_preg_replace("/^[-a-zA-Z:]+/", "", attr_)
                # end if
                break
            # end if
            if case(1):
                if php_preg_match("/^\\s*=\\s*/", attr_):
                    #// Equals sign.
                    working_ = 1
                    mode_ = 2
                    attr_ = php_preg_replace("/^\\s*=\\s*/", "", attr_)
                    break
                # end if
                if php_preg_match("/^\\s+/", attr_):
                    #// Valueless.
                    working_ = 1
                    mode_ = 0
                    if False == php_array_key_exists(attrname_, attrarr_):
                        attrarr_[attrname_] = Array({"name": attrname_, "value": "", "whole": attrname_, "vless": "y"})
                    # end if
                    attr_ = php_preg_replace("/^\\s+/", "", attr_)
                # end if
                break
            # end if
            if case(2):
                if php_preg_match("%^\"([^\"]*)\"(\\s+|/?$)%", attr_, match_):
                    #// "value"
                    thisval_ = match_[1]
                    if php_in_array(php_strtolower(attrname_), uris_):
                        thisval_ = wp_kses_bad_protocol(thisval_, allowed_protocols_)
                    # end if
                    if False == php_array_key_exists(attrname_, attrarr_):
                        attrarr_[attrname_] = Array({"name": attrname_, "value": thisval_, "whole": str(attrname_) + str("=\"") + str(thisval_) + str("\""), "vless": "n"})
                    # end if
                    working_ = 1
                    mode_ = 0
                    attr_ = php_preg_replace("/^\"[^\"]*\"(\\s+|$)/", "", attr_)
                    break
                # end if
                if php_preg_match("%^'([^']*)'(\\s+|/?$)%", attr_, match_):
                    #// 'value'
                    thisval_ = match_[1]
                    if php_in_array(php_strtolower(attrname_), uris_):
                        thisval_ = wp_kses_bad_protocol(thisval_, allowed_protocols_)
                    # end if
                    if False == php_array_key_exists(attrname_, attrarr_):
                        attrarr_[attrname_] = Array({"name": attrname_, "value": thisval_, "whole": str(attrname_) + str("='") + str(thisval_) + str("'"), "vless": "n"})
                    # end if
                    working_ = 1
                    mode_ = 0
                    attr_ = php_preg_replace("/^'[^']*'(\\s+|$)/", "", attr_)
                    break
                # end if
                if php_preg_match("%^([^\\s\"']+)(\\s+|/?$)%", attr_, match_):
                    #// value
                    thisval_ = match_[1]
                    if php_in_array(php_strtolower(attrname_), uris_):
                        thisval_ = wp_kses_bad_protocol(thisval_, allowed_protocols_)
                    # end if
                    if False == php_array_key_exists(attrname_, attrarr_):
                        attrarr_[attrname_] = Array({"name": attrname_, "value": thisval_, "whole": str(attrname_) + str("=\"") + str(thisval_) + str("\""), "vless": "n"})
                    # end if
                    #// We add quotes to conform to W3C's HTML spec.
                    working_ = 1
                    mode_ = 0
                    attr_ = php_preg_replace("%^[^\\s\"']+(\\s+|$)%", "", attr_)
                # end if
                break
            # end if
        # end for
        #// End switch.
        if 0 == working_:
            #// Not well-formed, remove and try again.
            attr_ = wp_kses_html_error(attr_)
            mode_ = 0
        # end if
    # end while
    #// End while.
    if 1 == mode_ and False == php_array_key_exists(attrname_, attrarr_):
        #// Special case, for when the attribute list ends with a valueless
        #// attribute like "selected".
        attrarr_[attrname_] = Array({"name": attrname_, "value": "", "whole": attrname_, "vless": "y"})
    # end if
    return attrarr_
# end def wp_kses_hair
#// 
#// Finds all attributes of an HTML element.
#// 
#// Does not modify input.  May return "evil" output.
#// 
#// Based on `wp_kses_split2()` and `wp_kses_attr()`.
#// 
#// @since 4.2.3
#// 
#// @param string $element HTML element.
#// @return array|bool List of attributes found in the element. Returns false on failure.
#//
def wp_kses_attr_parse(element_=None, *_args_):
    
    
    valid_ = php_preg_match("%^(<\\s*)(/\\s*)?([a-zA-Z0-9]+\\s*)([^>]*)(>?)$%", element_, matches_)
    if 1 != valid_:
        return False
    # end if
    begin_ = matches_[1]
    slash_ = matches_[2]
    elname_ = matches_[3]
    attr_ = matches_[4]
    end_ = matches_[5]
    if "" != slash_:
        #// Closing elements do not get parsed.
        return False
    # end if
    #// Is there a closing XHTML slash at the end of the attributes?
    if 1 == php_preg_match("%\\s*/\\s*$%", attr_, matches_):
        xhtml_slash_ = matches_[0]
        attr_ = php_substr(attr_, 0, -php_strlen(xhtml_slash_))
    else:
        xhtml_slash_ = ""
    # end if
    #// Split it.
    attrarr_ = wp_kses_hair_parse(attr_)
    if False == attrarr_:
        return False
    # end if
    #// Make sure all input is returned by adding front and back matter.
    array_unshift(attrarr_, begin_ + slash_ + elname_)
    php_array_push(attrarr_, xhtml_slash_ + end_)
    return attrarr_
# end def wp_kses_attr_parse
#// 
#// Builds an attribute list from string containing attributes.
#// 
#// Does not modify input.  May return "evil" output.
#// In case of unexpected input, returns false instead of stripping things.
#// 
#// Based on `wp_kses_hair()` but does not return a multi-dimensional array.
#// 
#// @since 4.2.3
#// 
#// @param string $attr Attribute list from HTML element to closing HTML element tag.
#// @return array|bool List of attributes found in $attr. Returns false on failure.
#//
def wp_kses_hair_parse(attr_=None, *_args_):
    
    
    if "" == attr_:
        return Array()
    # end if
    #// phpcs:disable Squiz.Strings.ConcatenationSpacing.PaddingFound -- don't remove regex indentation
    regex_ = "(?:" + "[-a-zA-Z:]+" + "|" + "\\[\\[?[^\\[\\]]+\\]\\]?" + ")" + "(?:" + "\\s*=\\s*" + "(?:" + "\"[^\"]*\"" + "|" + "'[^']*'" + "|" + "[^\\s\"']+" + "(?:\\s|$)" + ")" + "|" + "(?:\\s|$)" + ")" + "\\s*"
    #// Trailing space is optional except as mentioned above.
    #// phpcs:enable
    #// Although it is possible to reduce this procedure to a single regexp,
    #// we must run that regexp twice to get exactly the expected result.
    validation_ = str("%^(") + str(regex_) + str(")+$%")
    extraction_ = str("%") + str(regex_) + str("%")
    if 1 == php_preg_match(validation_, attr_):
        preg_match_all(extraction_, attr_, attrarr_)
        return attrarr_[0]
    else:
        return False
    # end if
# end def wp_kses_hair_parse
#// 
#// Performs different checks for attribute values.
#// 
#// The currently implemented checks are "maxlen", "minlen", "maxval", "minval",
#// and "valueless".
#// 
#// @since 1.0.0
#// 
#// @param string $value      Attribute value.
#// @param string $vless      Whether the attribute is valueless. Use 'y' or 'n'.
#// @param string $checkname  What $checkvalue is checking for.
#// @param mixed  $checkvalue What constraint the value should pass.
#// @return bool Whether check passes.
#//
def wp_kses_check_attr_val(value_=None, vless_=None, checkname_=None, checkvalue_=None, *_args_):
    
    
    ok_ = True
    for case in Switch(php_strtolower(checkname_)):
        if case("maxlen"):
            #// 
            #// The maxlen check makes sure that the attribute value has a length not
            #// greater than the given value. This can be used to avoid Buffer Overflows
            #// in WWW clients and various Internet servers.
            #//
            if php_strlen(value_) > checkvalue_:
                ok_ = False
            # end if
            break
        # end if
        if case("minlen"):
            #// 
            #// The minlen check makes sure that the attribute value has a length not
            #// smaller than the given value.
            #//
            if php_strlen(value_) < checkvalue_:
                ok_ = False
            # end if
            break
        # end if
        if case("maxval"):
            #// 
            #// The maxval check does two things: it checks that the attribute value is
            #// an integer from 0 and up, without an excessive amount of zeroes or
            #// whitespace (to avoid Buffer Overflows). It also checks that the attribute
            #// value is not greater than the given value.
            #// This check can be used to avoid Denial of Service attacks.
            #//
            if (not php_preg_match("/^\\s{0,6}[0-9]{1,6}\\s{0,6}$/", value_)):
                ok_ = False
            # end if
            if value_ > checkvalue_:
                ok_ = False
            # end if
            break
        # end if
        if case("minval"):
            #// 
            #// The minval check makes sure that the attribute value is a positive integer,
            #// and that it is not smaller than the given value.
            #//
            if (not php_preg_match("/^\\s{0,6}[0-9]{1,6}\\s{0,6}$/", value_)):
                ok_ = False
            # end if
            if value_ < checkvalue_:
                ok_ = False
            # end if
            break
        # end if
        if case("valueless"):
            #// 
            #// The valueless check makes sure if the attribute has a value
            #// (like `<a href="blah">`) or not (`<option selected>`). If the given value
            #// is a "y" or a "Y", the attribute must not have a value.
            #// If the given value is an "n" or an "N", the attribute must have a value.
            #//
            if php_strtolower(checkvalue_) != vless_:
                ok_ = False
            # end if
            break
        # end if
    # end for
    #// End switch.
    return ok_
# end def wp_kses_check_attr_val
#// 
#// Sanitizes a string and removed disallowed URL protocols.
#// 
#// This function removes all non-allowed protocols from the beginning of the
#// string. It ignores whitespace and the case of the letters, and it does
#// understand HTML entities. It does its work recursively, so it won't be
#// fooled by a string like `javascript:javascript:alert(57)`.
#// 
#// @since 1.0.0
#// 
#// @param string   $string            Content to filter bad protocols from.
#// @param string[] $allowed_protocols Array of allowed URL protocols.
#// @return string Filtered content.
#//
def wp_kses_bad_protocol(string_=None, allowed_protocols_=None, *_args_):
    
    
    string_ = wp_kses_no_null(string_)
    iterations_ = 0
    iterations_ += 1
    while True:
        original_string_ = string_
        string_ = wp_kses_bad_protocol_once(string_, allowed_protocols_)
        iterations_ += 1
        if original_string_ != string_ and iterations_ < 6:
            break
        # end if
    # end while
    if original_string_ != string_:
        return ""
    # end if
    return string_
# end def wp_kses_bad_protocol
#// 
#// Removes any invalid control characters in a text string.
#// 
#// Also removes any instance of the `\0` string.
#// 
#// @since 1.0.0
#// 
#// @param string $string  Content to filter null characters from.
#// @param array  $options Set 'slash_zero' => 'keep' when '\0' is allowed. Default is 'remove'.
#// @return string Filtered content.
#//
def wp_kses_no_null(string_=None, options_=None, *_args_):
    if options_ is None:
        options_ = None
    # end if
    
    if (not (php_isset(lambda : options_["slash_zero"]))):
        options_ = Array({"slash_zero": "remove"})
    # end if
    string_ = php_preg_replace("/[\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F]/", "", string_)
    if "remove" == options_["slash_zero"]:
        string_ = php_preg_replace("/\\\\+0+/", "", string_)
    # end if
    return string_
# end def wp_kses_no_null
#// 
#// Strips slashes from in front of quotes.
#// 
#// This function changes the character sequence `\"` to just `"`. It leaves all other
#// slashes alone. The quoting from `preg_replace(//e)` requires this.
#// 
#// @since 1.0.0
#// 
#// @param string $string String to strip slashes from.
#// @return string Fixed string with quoted slashes.
#//
def wp_kses_stripslashes(string_=None, *_args_):
    
    
    return php_preg_replace("%\\\\\"%", "\"", string_)
# end def wp_kses_stripslashes
#// 
#// Converts the keys of an array to lowercase.
#// 
#// @since 1.0.0
#// 
#// @param array $inarray Unfiltered array.
#// @return array Fixed array with all lowercase keys.
#//
def wp_kses_array_lc(inarray_=None, *_args_):
    
    
    outarray_ = Array()
    for inkey_,inval_ in inarray_.items():
        outkey_ = php_strtolower(inkey_)
        outarray_[outkey_] = Array()
        for inkey2_,inval2_ in inval_.items():
            outkey2_ = php_strtolower(inkey2_)
            outarray_[outkey_][outkey2_] = inval2_
        # end for
    # end for
    return outarray_
# end def wp_kses_array_lc
#// 
#// Handles parsing errors in `wp_kses_hair()`.
#// 
#// The general plan is to remove everything to and including some whitespace,
#// but it deals with quotes and apostrophes as well.
#// 
#// @since 1.0.0
#// 
#// @param string $string
#// @return string
#//
def wp_kses_html_error(string_=None, *_args_):
    
    
    return php_preg_replace("/^(\"[^\"]*(\"|$)|'[^']*('|$)|\\S)*\\s*/", "", string_)
# end def wp_kses_html_error
#// 
#// Sanitizes content from bad protocols and other characters.
#// 
#// This function searches for URL protocols at the beginning of the string, while
#// handling whitespace and HTML entities.
#// 
#// @since 1.0.0
#// 
#// @param string   $string            Content to check for bad protocols.
#// @param string[] $allowed_protocols Array of allowed URL protocols.
#// @return string Sanitized content.
#//
def wp_kses_bad_protocol_once(string_=None, allowed_protocols_=None, count_=1, *_args_):
    
    
    string_ = php_preg_replace("/(&#0*58(?![;0-9])|&#x0*3a(?![;a-f0-9]))/i", "$1;", string_)
    string2_ = php_preg_split("/:|&#0*58;|&#x0*3a;|&colon;/i", string_, 2)
    if (php_isset(lambda : string2_[1])) and (not php_preg_match("%/\\?%", string2_[0])):
        string_ = php_trim(string2_[1])
        protocol_ = wp_kses_bad_protocol_once2(string2_[0], allowed_protocols_)
        if "feed:" == protocol_:
            if count_ > 2:
                return ""
            # end if
            count_ += 1
            count_ += 1
            string_ = wp_kses_bad_protocol_once(string_, allowed_protocols_, count_)
            if php_empty(lambda : string_):
                return string_
            # end if
        # end if
        string_ = protocol_ + string_
    # end if
    return string_
# end def wp_kses_bad_protocol_once
#// 
#// Callback for `wp_kses_bad_protocol_once()` regular expression.
#// 
#// This function processes URL protocols, checks to see if they're in the
#// whitelist or not, and returns different data depending on the answer.
#// 
#// @access private
#// @ignore
#// @since 1.0.0
#// 
#// @param string   $string            URI scheme to check against the whitelist.
#// @param string[] $allowed_protocols Array of allowed URL protocols.
#// @return string Sanitized content.
#//
def wp_kses_bad_protocol_once2(string_=None, allowed_protocols_=None, *_args_):
    
    
    string2_ = wp_kses_decode_entities(string_)
    string2_ = php_preg_replace("/\\s/", "", string2_)
    string2_ = wp_kses_no_null(string2_)
    string2_ = php_strtolower(string2_)
    allowed_ = False
    for one_protocol_ in allowed_protocols_:
        if php_strtolower(one_protocol_) == string2_:
            allowed_ = True
            break
        # end if
    # end for
    if allowed_:
        return str(string2_) + str(":")
    else:
        return ""
    # end if
# end def wp_kses_bad_protocol_once2
#// 
#// Converts and fixes HTML entities.
#// 
#// This function normalizes HTML entities. It will convert `AT&T` to the correct
#// `AT&amp;T`, `&#00058;` to `&#58;`, `&#XYZZY;` to `&amp;#XYZZY;` and so on.
#// 
#// @since 1.0.0
#// 
#// @param string $string Content to normalize entities.
#// @return string Content with normalized entities.
#//
def wp_kses_normalize_entities(string_=None, *_args_):
    
    
    #// Disarm all entities by converting & to &amp;
    string_ = php_str_replace("&", "&amp;", string_)
    #// Change back the allowed entities in our entity whitelist.
    string_ = preg_replace_callback("/&amp;([A-Za-z]{2,8}[0-9]{0,2});/", "wp_kses_named_entities", string_)
    string_ = preg_replace_callback("/&amp;#(0*[0-9]{1,7});/", "wp_kses_normalize_entities2", string_)
    string_ = preg_replace_callback("/&amp;#[Xx](0*[0-9A-Fa-f]{1,6});/", "wp_kses_normalize_entities3", string_)
    return string_
# end def wp_kses_normalize_entities
#// 
#// Callback for `wp_kses_normalize_entities()` regular expression.
#// 
#// This function only accepts valid named entity references, which are finite,
#// case-sensitive, and highly scrutinized by HTML and XML validators.
#// 
#// @since 3.0.0
#// 
#// @global array $allowedentitynames
#// 
#// @param array $matches preg_replace_callback() matches array.
#// @return string Correctly encoded entity.
#//
def wp_kses_named_entities(matches_=None, *_args_):
    
    
    global allowedentitynames_
    php_check_if_defined("allowedentitynames_")
    if php_empty(lambda : matches_[1]):
        return ""
    # end if
    i_ = matches_[1]
    return str("&amp;") + str(i_) + str(";") if (not php_in_array(i_, allowedentitynames_)) else str("&") + str(i_) + str(";")
# end def wp_kses_named_entities
#// 
#// Callback for `wp_kses_normalize_entities()` regular expression.
#// 
#// This function helps `wp_kses_normalize_entities()` to only accept 16-bit
#// values and nothing more for `&#number;` entities.
#// 
#// @access private
#// @ignore
#// @since 1.0.0
#// 
#// @param array $matches `preg_replace_callback()` matches array.
#// @return string Correctly encoded entity.
#//
def wp_kses_normalize_entities2(matches_=None, *_args_):
    
    
    if php_empty(lambda : matches_[1]):
        return ""
    # end if
    i_ = matches_[1]
    if valid_unicode(i_):
        i_ = php_str_pad(php_ltrim(i_, "0"), 3, "0", STR_PAD_LEFT)
        i_ = str("&#") + str(i_) + str(";")
    else:
        i_ = str("&amp;#") + str(i_) + str(";")
    # end if
    return i_
# end def wp_kses_normalize_entities2
#// 
#// Callback for `wp_kses_normalize_entities()` for regular expression.
#// 
#// This function helps `wp_kses_normalize_entities()` to only accept valid Unicode
#// numeric entities in hex form.
#// 
#// @since 2.7.0
#// @access private
#// @ignore
#// 
#// @param array $matches `preg_replace_callback()` matches array.
#// @return string Correctly encoded entity.
#//
def wp_kses_normalize_entities3(matches_=None, *_args_):
    
    
    if php_empty(lambda : matches_[1]):
        return ""
    # end if
    hexchars_ = matches_[1]
    return str("&amp;#x") + str(hexchars_) + str(";") if (not valid_unicode(hexdec(hexchars_))) else "&#x" + php_ltrim(hexchars_, "0") + ";"
# end def wp_kses_normalize_entities3
#// 
#// Determines if a Unicode codepoint is valid.
#// 
#// @since 2.7.0
#// 
#// @param int $i Unicode codepoint.
#// @return bool Whether or not the codepoint is a valid Unicode codepoint.
#//
def valid_unicode(i_=None, *_args_):
    
    
    return 9 == i_ or 10 == i_ or 13 == i_ or 32 <= i_ and i_ <= 55295 or 57344 <= i_ and i_ <= 65533 or 65536 <= i_ and i_ <= 1114111
# end def valid_unicode
#// 
#// Converts all numeric HTML entities to their named counterparts.
#// 
#// This function decodes numeric HTML entities (`&#65;` and `&#x41;`).
#// It doesn't do anything with named entities like `&auml;`, but we don't
#// need them in the URL protocol whitelisting system anyway.
#// 
#// @since 1.0.0
#// 
#// @param string $string Content to change entities.
#// @return string Content after decoded entities.
#//
def wp_kses_decode_entities(string_=None, *_args_):
    
    
    string_ = preg_replace_callback("/&#([0-9]+);/", "_wp_kses_decode_entities_chr", string_)
    string_ = preg_replace_callback("/&#[Xx]([0-9A-Fa-f]+);/", "_wp_kses_decode_entities_chr_hexdec", string_)
    return string_
# end def wp_kses_decode_entities
#// 
#// Regex callback for `wp_kses_decode_entities()`.
#// 
#// @since 2.9.0
#// @access private
#// @ignore
#// 
#// @param array $match preg match
#// @return string
#//
def _wp_kses_decode_entities_chr(match_=None, *_args_):
    
    
    return chr(match_[1])
# end def _wp_kses_decode_entities_chr
#// 
#// Regex callback for `wp_kses_decode_entities()`.
#// 
#// @since 2.9.0
#// @access private
#// @ignore
#// 
#// @param array $match preg match
#// @return string
#//
def _wp_kses_decode_entities_chr_hexdec(match_=None, *_args_):
    
    
    return chr(hexdec(match_[1]))
# end def _wp_kses_decode_entities_chr_hexdec
#// 
#// Sanitize content with allowed HTML KSES rules.
#// 
#// This function expects slashed data.
#// 
#// @since 1.0.0
#// 
#// @param string $data Content to filter, expected to be escaped with slashes.
#// @return string Filtered content.
#//
def wp_filter_kses(data_=None, *_args_):
    
    
    return addslashes(wp_kses(stripslashes(data_), current_filter()))
# end def wp_filter_kses
#// 
#// Sanitize content with allowed HTML KSES rules.
#// 
#// This function expects unslashed data.
#// 
#// @since 2.9.0
#// 
#// @param string $data Content to filter, expected to not be escaped.
#// @return string Filtered content.
#//
def wp_kses_data(data_=None, *_args_):
    
    
    return wp_kses(data_, current_filter())
# end def wp_kses_data
#// 
#// Sanitizes content for allowed HTML tags for post content.
#// 
#// Post content refers to the page contents of the 'post' type and not `$_POST`
#// data from forms.
#// 
#// This function expects slashed data.
#// 
#// @since 2.0.0
#// 
#// @param string $data Post content to filter, expected to be escaped with slashes.
#// @return string Filtered post content with allowed HTML tags and attributes intact.
#//
def wp_filter_post_kses(data_=None, *_args_):
    
    
    return addslashes(wp_kses(stripslashes(data_), "post"))
# end def wp_filter_post_kses
#// 
#// Sanitizes content for allowed HTML tags for post content.
#// 
#// Post content refers to the page contents of the 'post' type and not `$_POST`
#// data from forms.
#// 
#// This function expects unslashed data.
#// 
#// @since 2.9.0
#// 
#// @param string $data Post content to filter.
#// @return string Filtered post content with allowed HTML tags and attributes intact.
#//
def wp_kses_post(data_=None, *_args_):
    
    
    return wp_kses(data_, "post")
# end def wp_kses_post
#// 
#// Navigates through an array, object, or scalar, and sanitizes content for
#// allowed HTML tags for post content.
#// 
#// @since 4.4.2
#// 
#// @see map_deep()
#// 
#// @param mixed $data The array, object, or scalar value to inspect.
#// @return mixed The filtered content.
#//
def wp_kses_post_deep(data_=None, *_args_):
    
    
    return map_deep(data_, "wp_kses_post")
# end def wp_kses_post_deep
#// 
#// Strips all HTML from a text string.
#// 
#// This function expects slashed data.
#// 
#// @since 2.1.0
#// 
#// @param string $data Content to strip all HTML from.
#// @return string Filtered content without any HTML.
#//
def wp_filter_nohtml_kses(data_=None, *_args_):
    
    
    return addslashes(wp_kses(stripslashes(data_), "strip"))
# end def wp_filter_nohtml_kses
#// 
#// Adds all KSES input form content filters.
#// 
#// All hooks have default priority. The `wp_filter_kses()` function is added to
#// the 'pre_comment_content' and 'title_save_pre' hooks.
#// 
#// The `wp_filter_post_kses()` function is added to the 'content_save_pre',
#// 'excerpt_save_pre', and 'content_filtered_save_pre' hooks.
#// 
#// @since 2.0.0
#//
def kses_init_filters(*_args_):
    
    
    #// Normal filtering.
    add_filter("title_save_pre", "wp_filter_kses")
    #// Comment filtering.
    if current_user_can("unfiltered_html"):
        add_filter("pre_comment_content", "wp_filter_post_kses")
    else:
        add_filter("pre_comment_content", "wp_filter_kses")
    # end if
    #// Post filtering.
    add_filter("content_save_pre", "wp_filter_post_kses")
    add_filter("excerpt_save_pre", "wp_filter_post_kses")
    add_filter("content_filtered_save_pre", "wp_filter_post_kses")
# end def kses_init_filters
#// 
#// Removes all KSES input form content filters.
#// 
#// A quick procedural method to removing all of the filters that KSES uses for
#// content in WordPress Loop.
#// 
#// Does not remove the `kses_init()` function from {@see 'init'} hook (priority is
#// default). Also does not remove `kses_init()` function from {@see 'set_current_user'}
#// hook (priority is also default).
#// 
#// @since 2.0.6
#//
def kses_remove_filters(*_args_):
    
    
    #// Normal filtering.
    remove_filter("title_save_pre", "wp_filter_kses")
    #// Comment filtering.
    remove_filter("pre_comment_content", "wp_filter_post_kses")
    remove_filter("pre_comment_content", "wp_filter_kses")
    #// Post filtering.
    remove_filter("content_save_pre", "wp_filter_post_kses")
    remove_filter("excerpt_save_pre", "wp_filter_post_kses")
    remove_filter("content_filtered_save_pre", "wp_filter_post_kses")
# end def kses_remove_filters
#// 
#// Sets up most of the KSES filters for input form content.
#// 
#// First removes all of the KSES filters in case the current user does not need
#// to have KSES filter the content. If the user does not have `unfiltered_html`
#// capability, then KSES filters are added.
#// 
#// @since 2.0.0
#//
def kses_init(*_args_):
    
    
    kses_remove_filters()
    if (not current_user_can("unfiltered_html")):
        kses_init_filters()
    # end if
# end def kses_init
#// 
#// Filters an inline style attribute and removes disallowed rules.
#// 
#// @since 2.8.1
#// 
#// @param string $css        A string of CSS rules.
#// @param string $deprecated Not used.
#// @return string Filtered string of CSS rules.
#//
def safecss_filter_attr(css_=None, deprecated_="", *_args_):
    
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.8.1")
        pass
    # end if
    css_ = wp_kses_no_null(css_)
    css_ = php_str_replace(Array("\n", "\r", "  "), "", css_)
    allowed_protocols_ = wp_allowed_protocols()
    css_array_ = php_explode(";", php_trim(css_))
    #// 
    #// Filters list of allowed CSS attributes.
    #// 
    #// @since 2.8.1
    #// @since 4.4.0 Added support for `min-height`, `max-height`, `min-width`, and `max-width`.
    #// @since 4.6.0 Added support for `list-style-type`.
    #// @since 5.0.0 Added support for `background-image`.
    #// @since 5.1.0 Added support for `text-transform`.
    #// @since 5.2.0 Added support for `background-position` and `grid-template-columns`
    #// @since 5.3.0 Added support for `grid`, `flex` and `column` layout properties.
    #// Extend `background-*` support of individual properties.
    #// @since 5.3.1 Added support for gradient backgrounds.
    #// 
    #// @param string[] $attr Array of allowed CSS attributes.
    #//
    allowed_attr_ = apply_filters("safe_style_css", Array("background", "background-color", "background-image", "background-position", "background-size", "background-attachment", "background-blend-mode", "border", "border-radius", "border-width", "border-color", "border-style", "border-right", "border-right-color", "border-right-style", "border-right-width", "border-bottom", "border-bottom-color", "border-bottom-style", "border-bottom-width", "border-left", "border-left-color", "border-left-style", "border-left-width", "border-top", "border-top-color", "border-top-style", "border-top-width", "border-spacing", "border-collapse", "caption-side", "columns", "column-count", "column-fill", "column-gap", "column-rule", "column-span", "column-width", "color", "font", "font-family", "font-size", "font-style", "font-variant", "font-weight", "letter-spacing", "line-height", "text-align", "text-decoration", "text-indent", "text-transform", "height", "min-height", "max-height", "width", "min-width", "max-width", "margin", "margin-right", "margin-bottom", "margin-left", "margin-top", "padding", "padding-right", "padding-bottom", "padding-left", "padding-top", "flex", "flex-basis", "flex-direction", "flex-flow", "flex-grow", "flex-shrink", "grid-template-columns", "grid-auto-columns", "grid-column-start", "grid-column-end", "grid-column-gap", "grid-template-rows", "grid-auto-rows", "grid-row-start", "grid-row-end", "grid-row-gap", "grid-gap", "justify-content", "justify-items", "justify-self", "align-content", "align-items", "align-self", "clear", "cursor", "direction", "float", "overflow", "vertical-align", "list-style-type"))
    #// 
    #// CSS attributes that accept URL data types.
    #// 
    #// This is in accordance to the CSS spec and unrelated to
    #// the sub-set of supported attributes above.
    #// 
    #// See: https://developer.mozilla.org/en-US/docs/Web/CSS/url
    #//
    css_url_data_types_ = Array("background", "background-image", "cursor", "list-style", "list-style-image")
    #// 
    #// CSS attributes that accept gradient data types.
    #// 
    #//
    css_gradient_data_types_ = Array("background", "background-image")
    if php_empty(lambda : allowed_attr_):
        return css_
    # end if
    css_ = ""
    for css_item_ in css_array_:
        if "" == css_item_:
            continue
        # end if
        css_item_ = php_trim(css_item_)
        css_test_string_ = css_item_
        found_ = False
        url_attr_ = False
        gradient_attr_ = False
        if php_strpos(css_item_, ":") == False:
            found_ = True
        else:
            parts_ = php_explode(":", css_item_, 2)
            css_selector_ = php_trim(parts_[0])
            if php_in_array(css_selector_, allowed_attr_, True):
                found_ = True
                url_attr_ = php_in_array(css_selector_, css_url_data_types_, True)
                gradient_attr_ = php_in_array(css_selector_, css_gradient_data_types_, True)
            # end if
        # end if
        if found_ and url_attr_:
            #// Simplified: matches the sequence `url(*)`.
            preg_match_all("/url\\([^)]+\\)/", parts_[1], url_matches_)
            for url_match_ in url_matches_[0]:
                #// Clean up the URL from each of the matches above.
                php_preg_match("/^url\\(\\s*(['\\\"]?)(.*)(\\g1)\\s*\\)$/", url_match_, url_pieces_)
                if php_empty(lambda : url_pieces_[2]):
                    found_ = False
                    break
                # end if
                url_ = php_trim(url_pieces_[2])
                if php_empty(lambda : url_) or wp_kses_bad_protocol(url_, allowed_protocols_) != url_:
                    found_ = False
                    break
                else:
                    #// Remove the whole `url(*)` bit that was matched above from the CSS.
                    css_test_string_ = php_str_replace(url_match_, "", css_test_string_)
                # end if
            # end for
        # end if
        if found_ and gradient_attr_:
            css_value_ = php_trim(parts_[1])
            if php_preg_match("/^(repeating-)?(linear|radial|conic)-gradient\\(([^()]|rgb[a]?\\([^()]*\\))*\\)$/", css_value_):
                #// Remove the whole `gradient` bit that was matched above from the CSS.
                css_test_string_ = php_str_replace(css_value_, "", css_test_string_)
            # end if
        # end if
        #// Remove any CSS containing containing \ ( & } = or comments, except for url() useage checked above.
        if found_ and (not php_preg_match("%[\\\\(&=}]|/\\*%", css_test_string_)):
            if "" != css_:
                css_ += ";"
            # end if
            css_ += css_item_
        # end if
    # end for
    return css_
# end def safecss_filter_attr
#// 
#// Helper function to add global attributes to a tag in the allowed html list.
#// 
#// @since 3.5.0
#// @since 5.0.0 Add support for `data-*` wildcard attributes.
#// @access private
#// @ignore
#// 
#// @param array $value An array of attributes.
#// @return array The array of attributes with global attributes added.
#//
def _wp_add_global_attributes(value_=None, *_args_):
    
    
    global_attributes_ = Array({"aria-describedby": True, "aria-details": True, "aria-label": True, "aria-labelledby": True, "aria-hidden": True, "class": True, "id": True, "style": True, "title": True, "role": True, "data-*": True})
    if True == value_:
        value_ = Array()
    # end if
    if php_is_array(value_):
        return php_array_merge(value_, global_attributes_)
    # end if
    return value_
# end def _wp_add_global_attributes
