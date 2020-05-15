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
    base_url = Array()
    content_url = Array()
    default_version = Array()
    text_direction = "ltr"
    concat = ""
    concat_version = ""
    do_concat = False
    print_html = ""
    print_code = ""
    default_dirs = Array()
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
    def do_item(self, handle=None):
        
        if (not super().do_item(handle)):
            return False
        # end if
        obj = self.registered[handle]
        if None == obj.ver:
            ver = ""
        else:
            ver = obj.ver if obj.ver else self.default_version
        # end if
        if (php_isset(lambda : self.args[handle])):
            ver = ver + "&amp;" + self.args[handle] if ver else self.args[handle]
        # end if
        src = obj.src
        cond_before = ""
        cond_after = ""
        conditional = obj.extra["conditional"] if (php_isset(lambda : obj.extra["conditional"])) else ""
        if conditional:
            cond_before = str("<!--[if ") + str(conditional) + str("]>\n")
            cond_after = "<![endif]-->\n"
        # end if
        inline_style = self.print_inline_style(handle, False)
        if inline_style:
            inline_style_tag = php_sprintf("""<style id='%s-inline-css'%s>
            %s
            </style>
            """, esc_attr(handle), self.type_attr, inline_style)
        else:
            inline_style_tag = ""
        # end if
        if self.do_concat:
            if self.in_default_dir(src) and (not conditional) and (not (php_isset(lambda : obj.extra["alt"]))):
                self.concat += str(handle) + str(",")
                self.concat_version += str(handle) + str(ver)
                self.print_code += inline_style
                return True
            # end if
        # end if
        if (php_isset(lambda : obj.args)):
            media = esc_attr(obj.args)
        else:
            media = "all"
        # end if
        #// A single item may alias a set of items, by having dependencies, but no source.
        if (not src):
            if inline_style_tag:
                if self.do_concat:
                    self.print_html += inline_style_tag
                else:
                    php_print(inline_style_tag)
                # end if
            # end if
            return True
        # end if
        href = self._css_href(src, ver, handle)
        if (not href):
            return True
        # end if
        rel = "alternate stylesheet" if (php_isset(lambda : obj.extra["alt"])) and obj.extra["alt"] else "stylesheet"
        title = php_sprintf("title='%s'", esc_attr(obj.extra["title"])) if (php_isset(lambda : obj.extra["title"])) else ""
        tag = php_sprintf("<link rel='%s' id='%s-css' %s href='%s'%s media='%s' />\n", rel, handle, title, href, self.type_attr, media)
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
        tag = apply_filters("style_loader_tag", tag, handle, href, media)
        if "rtl" == self.text_direction and (php_isset(lambda : obj.extra["rtl"])) and obj.extra["rtl"]:
            if php_is_bool(obj.extra["rtl"]) or "replace" == obj.extra["rtl"]:
                suffix = obj.extra["suffix"] if (php_isset(lambda : obj.extra["suffix"])) else ""
                rtl_href = php_str_replace(str(suffix) + str(".css"), str("-rtl") + str(suffix) + str(".css"), self._css_href(src, ver, str(handle) + str("-rtl")))
            else:
                rtl_href = self._css_href(obj.extra["rtl"], ver, str(handle) + str("-rtl"))
            # end if
            rtl_tag = php_sprintf("<link rel='%s' id='%s-rtl-css' %s href='%s'%s media='%s' />\n", rel, handle, title, rtl_href, self.type_attr, media)
            #// This filter is documented in wp-includes/class.wp-styles.php
            rtl_tag = apply_filters("style_loader_tag", rtl_tag, handle, rtl_href, media)
            if "replace" == obj.extra["rtl"]:
                tag = rtl_tag
            else:
                tag += rtl_tag
            # end if
        # end if
        if self.do_concat:
            self.print_html += cond_before
            self.print_html += tag
            if inline_style_tag:
                self.print_html += inline_style_tag
            # end if
            self.print_html += cond_after
        else:
            php_print(cond_before)
            php_print(tag)
            self.print_inline_style(handle)
            php_print(cond_after)
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
    def add_inline_style(self, handle=None, code=None):
        
        if (not code):
            return False
        # end if
        after = self.get_data(handle, "after")
        if (not after):
            after = Array()
        # end if
        after[-1] = code
        return self.add_data(handle, "after", after)
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
    def print_inline_style(self, handle=None, echo=True):
        
        output = self.get_data(handle, "after")
        if php_empty(lambda : output):
            return False
        # end if
        output = php_implode("\n", output)
        if (not echo):
            return output
        # end if
        printf("""<style id='%s-inline-css'%s>
        %s
        </style>
        """, esc_attr(handle), self.type_attr, output)
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
    def all_deps(self, handles=None, recursion=False, group=False):
        
        r = super().all_deps(handles, recursion, group)
        if (not recursion):
            #// 
            #// Filters the array of enqueued styles before processing for output.
            #// 
            #// @since 2.6.0
            #// 
            #// @param string[] $to_do The list of enqueued style handles about to be processed.
            #//
            self.to_do = apply_filters("print_styles_array", self.to_do)
        # end if
        return r
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
    def _css_href(self, src=None, ver=None, handle=None):
        
        if (not php_is_bool(src)) and (not php_preg_match("|^(https?:)?//|", src)) and (not self.content_url and 0 == php_strpos(src, self.content_url)):
            src = self.base_url + src
        # end if
        if (not php_empty(lambda : ver)):
            src = add_query_arg("ver", ver, src)
        # end if
        #// 
        #// Filters an enqueued style's fully-qualified URL.
        #// 
        #// @since 2.6.0
        #// 
        #// @param string $src    The source URL of the enqueued style.
        #// @param string $handle The style's registered handle.
        #//
        src = apply_filters("style_loader_src", src, handle)
        return esc_url(src)
    # end def _css_href
    #// 
    #// Whether a handle's source is in a default directory.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $src The source of the enqueued style.
    #// @return bool True if found, false if not.
    #//
    def in_default_dir(self, src=None):
        
        if (not self.default_dirs):
            return True
        # end if
        for test in self.default_dirs:
            if 0 == php_strpos(src, test):
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
