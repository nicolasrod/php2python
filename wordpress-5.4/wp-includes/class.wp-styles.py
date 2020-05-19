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
#// Dependencies API: WP_Styles class
#// 
#// @since 2.6.0
#// 
#// @package WordPress
#// @subpackage Dependencies
#// 
#// 
#// Core class used to register styles.
#// 
#// @since 2.6.0
#// 
#// @see WP_Dependencies
#//
class WP_Styles(WP_Dependencies):
    #// 
    #// Base URL for styles.
    #// 
    #// Full URL with trailing slash.
    #// 
    #// @since 2.6.0
    #// @var string
    #//
    base_url = Array()
    #// 
    #// URL of the content directory.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    content_url = Array()
    #// 
    #// Default version string for stylesheets.
    #// 
    #// @since 2.6.0
    #// @var string
    #//
    default_version = Array()
    #// 
    #// The current text direction.
    #// 
    #// @since 2.6.0
    #// @var string
    #//
    text_direction = "ltr"
    #// 
    #// Holds a list of style handles which will be concatenated.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    concat = ""
    #// 
    #// Holds a string which contains style handles and their version.
    #// 
    #// @since 2.8.0
    #// @deprecated 3.4.0
    #// @var string
    #//
    concat_version = ""
    #// 
    #// Whether to perform concatenation.
    #// 
    #// @since 2.8.0
    #// @var bool
    #//
    do_concat = False
    #// 
    #// Holds HTML markup of styles and additional data if concatenation
    #// is enabled.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    print_html = ""
    #// 
    #// Holds inline styles if concatenation is enabled.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    print_code = ""
    #// 
    #// List of default directories.
    #// 
    #// @since 2.8.0
    #// @var array
    #//
    default_dirs = Array()
    #// 
    #// Holds a string which contains the type attribute for style tag.
    #// 
    #// If the current theme does not declare HTML5 support for 'style',
    #// then it initializes as `type='text/css'`.
    #// 
    #// @since 5.3.0
    #// @var string
    #//
    type_attr = ""
    #// 
    #// Constructor.
    #// 
    #// @since 2.6.0
    #//
    def __init__(self):
        
        
        if php_function_exists("is_admin") and (not is_admin()) and php_function_exists("current_theme_supports") and (not current_theme_supports("html5", "style")):
            self.type_attr = " type='text/css'"
        # end if
        #// 
        #// Fires when the WP_Styles instance is initialized.
        #// 
        #// @since 2.6.0
        #// 
        #// @param WP_Styles $this WP_Styles instance (passed by reference).
        #//
        do_action_ref_array("wp_default_styles", Array(self))
    # end def __init__
    #// 
    #// Processes a style dependency.
    #// 
    #// @since 2.6.0
    #// 
    #// @see WP_Dependencies::do_item()
    #// 
    #// @param string $handle The style's registered handle.
    #// @return bool True on success, false on failure.
    #//
    def do_item(self, handle_=None):
        
        
        if (not super().do_item(handle_)):
            return False
        # end if
        obj_ = self.registered[handle_]
        if None == obj_.ver:
            ver_ = ""
        else:
            ver_ = obj_.ver if obj_.ver else self.default_version
        # end if
        if (php_isset(lambda : self.args[handle_])):
            ver_ = ver_ + "&amp;" + self.args[handle_] if ver_ else self.args[handle_]
        # end if
        src_ = obj_.src
        cond_before_ = ""
        cond_after_ = ""
        conditional_ = obj_.extra["conditional"] if (php_isset(lambda : obj_.extra["conditional"])) else ""
        if conditional_:
            cond_before_ = str("<!--[if ") + str(conditional_) + str("]>\n")
            cond_after_ = "<![endif]-->\n"
        # end if
        inline_style_ = self.print_inline_style(handle_, False)
        if inline_style_:
            inline_style_tag_ = php_sprintf("""<style id='%s-inline-css'%s>
            %s
            </style>
            """, esc_attr(handle_), self.type_attr, inline_style_)
        else:
            inline_style_tag_ = ""
        # end if
        if self.do_concat:
            if self.in_default_dir(src_) and (not conditional_) and (not (php_isset(lambda : obj_.extra["alt"]))):
                self.concat += str(handle_) + str(",")
                self.concat_version += str(handle_) + str(ver_)
                self.print_code += inline_style_
                return True
            # end if
        # end if
        if (php_isset(lambda : obj_.args)):
            media_ = esc_attr(obj_.args)
        else:
            media_ = "all"
        # end if
        #// A single item may alias a set of items, by having dependencies, but no source.
        if (not src_):
            if inline_style_tag_:
                if self.do_concat:
                    self.print_html += inline_style_tag_
                else:
                    php_print(inline_style_tag_)
                # end if
            # end if
            return True
        # end if
        href_ = self._css_href(src_, ver_, handle_)
        if (not href_):
            return True
        # end if
        rel_ = "alternate stylesheet" if (php_isset(lambda : obj_.extra["alt"])) and obj_.extra["alt"] else "stylesheet"
        title_ = php_sprintf("title='%s'", esc_attr(obj_.extra["title"])) if (php_isset(lambda : obj_.extra["title"])) else ""
        tag_ = php_sprintf("<link rel='%s' id='%s-css' %s href='%s'%s media='%s' />\n", rel_, handle_, title_, href_, self.type_attr, media_)
        #// 
        #// Filters the HTML link tag of an enqueued style.
        #// 
        #// @since 2.6.0
        #// @since 4.3.0 Introduced the `$href` parameter.
        #// @since 4.5.0 Introduced the `$media` parameter.
        #// 
        #// @param string $html   The link tag for the enqueued style.
        #// @param string $handle The style's registered handle.
        #// @param string $href   The stylesheet's source URL.
        #// @param string $media  The stylesheet's media attribute.
        #//
        tag_ = apply_filters("style_loader_tag", tag_, handle_, href_, media_)
        if "rtl" == self.text_direction and (php_isset(lambda : obj_.extra["rtl"])) and obj_.extra["rtl"]:
            if php_is_bool(obj_.extra["rtl"]) or "replace" == obj_.extra["rtl"]:
                suffix_ = obj_.extra["suffix"] if (php_isset(lambda : obj_.extra["suffix"])) else ""
                rtl_href_ = php_str_replace(str(suffix_) + str(".css"), str("-rtl") + str(suffix_) + str(".css"), self._css_href(src_, ver_, str(handle_) + str("-rtl")))
            else:
                rtl_href_ = self._css_href(obj_.extra["rtl"], ver_, str(handle_) + str("-rtl"))
            # end if
            rtl_tag_ = php_sprintf("<link rel='%s' id='%s-rtl-css' %s href='%s'%s media='%s' />\n", rel_, handle_, title_, rtl_href_, self.type_attr, media_)
            #// This filter is documented in wp-includes/class.wp-styles.php
            rtl_tag_ = apply_filters("style_loader_tag", rtl_tag_, handle_, rtl_href_, media_)
            if "replace" == obj_.extra["rtl"]:
                tag_ = rtl_tag_
            else:
                tag_ += rtl_tag_
            # end if
        # end if
        if self.do_concat:
            self.print_html += cond_before_
            self.print_html += tag_
            if inline_style_tag_:
                self.print_html += inline_style_tag_
            # end if
            self.print_html += cond_after_
        else:
            php_print(cond_before_)
            php_print(tag_)
            self.print_inline_style(handle_)
            php_print(cond_after_)
        # end if
        return True
    # end def do_item
    #// 
    #// Adds extra CSS styles to a registered stylesheet.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $handle The style's registered handle.
    #// @param string $code   String containing the CSS styles to be added.
    #// @return bool True on success, false on failure.
    #//
    def add_inline_style(self, handle_=None, code_=None):
        
        
        if (not code_):
            return False
        # end if
        after_ = self.get_data(handle_, "after")
        if (not after_):
            after_ = Array()
        # end if
        after_[-1] = code_
        return self.add_data(handle_, "after", after_)
    # end def add_inline_style
    #// 
    #// Prints extra CSS styles of a registered stylesheet.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $handle The style's registered handle.
    #// @param bool   $echo   Optional. Whether to echo the inline style
    #// instead of just returning it. Default true.
    #// @return string|bool False if no data exists, inline styles if `$echo` is true,
    #// true otherwise.
    #//
    def print_inline_style(self, handle_=None, echo_=None):
        if echo_ is None:
            echo_ = True
        # end if
        
        output_ = self.get_data(handle_, "after")
        if php_empty(lambda : output_):
            return False
        # end if
        output_ = php_implode("\n", output_)
        if (not echo_):
            return output_
        # end if
        php_printf("""<style id='%s-inline-css'%s>
        %s
        </style>
        """, esc_attr(handle_), self.type_attr, output_)
        return True
    # end def print_inline_style
    #// 
    #// Determines style dependencies.
    #// 
    #// @since 2.6.0
    #// 
    #// @see WP_Dependencies::all_deps()
    #// 
    #// @param string|string[] $handles   Item handle (string) or item handles (array of strings).
    #// @param bool            $recursion Optional. Internal flag that function is calling itself.
    #// Default false.
    #// @param int|false       $group     Optional. Group level: level (int), no groups (false).
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def all_deps(self, handles_=None, recursion_=None, group_=None):
        if recursion_ is None:
            recursion_ = False
        # end if
        if group_ is None:
            group_ = False
        # end if
        
        r_ = super().all_deps(handles_, recursion_, group_)
        if (not recursion_):
            #// 
            #// Filters the array of enqueued styles before processing for output.
            #// 
            #// @since 2.6.0
            #// 
            #// @param string[] $to_do The list of enqueued style handles about to be processed.
            #//
            self.to_do = apply_filters("print_styles_array", self.to_do)
        # end if
        return r_
    # end def all_deps
    #// 
    #// Generates an enqueued style's fully-qualified URL.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $src    The source of the enqueued style.
    #// @param string $ver    The version of the enqueued style.
    #// @param string $handle The style's registered handle.
    #// @return string Style's fully-qualified URL.
    #//
    def _css_href(self, src_=None, ver_=None, handle_=None):
        
        
        if (not php_is_bool(src_)) and (not php_preg_match("|^(https?:)?//|", src_)) and (not self.content_url and 0 == php_strpos(src_, self.content_url)):
            src_ = self.base_url + src_
        # end if
        if (not php_empty(lambda : ver_)):
            src_ = add_query_arg("ver", ver_, src_)
        # end if
        #// 
        #// Filters an enqueued style's fully-qualified URL.
        #// 
        #// @since 2.6.0
        #// 
        #// @param string $src    The source URL of the enqueued style.
        #// @param string $handle The style's registered handle.
        #//
        src_ = apply_filters("style_loader_src", src_, handle_)
        return esc_url(src_)
    # end def _css_href
    #// 
    #// Whether a handle's source is in a default directory.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $src The source of the enqueued style.
    #// @return bool True if found, false if not.
    #//
    def in_default_dir(self, src_=None):
        
        
        if (not self.default_dirs):
            return True
        # end if
        for test_ in self.default_dirs:
            if 0 == php_strpos(src_, test_):
                return True
            # end if
        # end for
        return False
    # end def in_default_dir
    #// 
    #// Processes items and dependencies for the footer group.
    #// 
    #// HTML 5 allows styles in the body, grab late enqueued items and output them in the footer.
    #// 
    #// @since 3.3.0
    #// 
    #// @see WP_Dependencies::do_items()
    #// 
    #// @return string[] Handles of items that have been processed.
    #//
    def do_footer_items(self):
        
        
        self.do_items(False, 1)
        return self.done
    # end def do_footer_items
    #// 
    #// Resets class properties.
    #// 
    #// @since 3.3.0
    #//
    def reset(self):
        
        
        self.do_concat = False
        self.concat = ""
        self.concat_version = ""
        self.print_html = ""
    # end def reset
# end class WP_Styles
