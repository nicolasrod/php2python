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
#// Dependencies API: WP_Scripts class
#// 
#// @since 2.6.0
#// 
#// @package WordPress
#// @subpackage Dependencies
#// 
#// 
#// Core class used to register scripts.
#// 
#// @since 2.1.0
#// 
#// @see WP_Dependencies
#//
class WP_Scripts(WP_Dependencies):
    base_url = Array()
    content_url = Array()
    default_version = Array()
    in_footer = Array()
    concat = ""
    concat_version = ""
    do_concat = False
    print_html = ""
    print_code = ""
    ext_handles = ""
    ext_version = ""
    default_dirs = Array()
    type_attr = ""
    #// 
    #// Constructor.
    #// 
    #// @since 2.6.0
    #//
    def __init__(self):
        
        self.init()
        add_action("init", Array(self, "init"), 0)
    # end def __init__
    #// 
    #// Initialize the class.
    #// 
    #// @since 3.4.0
    #//
    def init(self):
        
        if php_function_exists("is_admin") and (not is_admin()) and php_function_exists("current_theme_supports") and (not current_theme_supports("html5", "script")):
            self.type_attr = " type='text/javascript'"
        # end if
        #// 
        #// Fires when the WP_Scripts instance is initialized.
        #// 
        #// @since 2.6.0
        #// 
        #// @param WP_Scripts $this WP_Scripts instance (passed by reference).
        #//
        do_action_ref_array("wp_default_scripts", Array(self))
    # end def init
    #// 
    #// Prints scripts.
    #// 
    #// Prints the scripts passed to it or the print queue. Also prints all necessary dependencies.
    #// 
    #// @since 2.1.0
    #// @since 2.8.0 Added the `$group` parameter.
    #// 
    #// @param string|string[]|false $handles Optional. Scripts to be printed: queue (false),
    #// single script (string), or multiple scripts (array of strings).
    #// Default false.
    #// @param int|false             $group   Optional. Group level: level (int), no groups (false).
    #// Default false.
    #// @return string[] Handles of scripts that have been printed.
    #//
    def print_scripts(self, handles=False, group=False):
        
        return self.do_items(handles, group)
    # end def print_scripts
    #// 
    #// Prints extra scripts of a registered script.
    #// 
    #// @since 2.1.0
    #// @since 2.8.0 Added the `$echo` parameter.
    #// @deprecated 3.3.0
    #// 
    #// @see print_extra_script()
    #// 
    #// @param string $handle The script's registered handle.
    #// @param bool   $echo   Optional. Whether to echo the extra script
    #// instead of just returning it. Default true.
    #// @return bool|string|void Void if no data exists, extra scripts if `$echo` is true,
    #// true otherwise.
    #//
    def print_scripts_l10n(self, handle=None, echo=True):
        
        _deprecated_function(__FUNCTION__, "3.3.0", "WP_Scripts::print_extra_script()")
        return self.print_extra_script(handle, echo)
    # end def print_scripts_l10n
    #// 
    #// Prints extra scripts of a registered script.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $handle The script's registered handle.
    #// @param bool   $echo   Optional. Whether to echo the extra script
    #// instead of just returning it. Default true.
    #// @return bool|string|void Void if no data exists, extra scripts if `$echo` is true,
    #// true otherwise.
    #//
    def print_extra_script(self, handle=None, echo=True):
        
        output = self.get_data(handle, "data")
        if (not output):
            return
        # end if
        if (not echo):
            return output
        # end if
        php_print(str("<script") + str(self.type_attr) + str(">\n"))
        #// CDATA is not needed for HTML 5.
        if self.type_attr:
            php_print("/* <![CDATA[ */\n")
        # end if
        php_print(str(output) + str("\n"))
        if self.type_attr:
            php_print("/* ]]> */\n")
        # end if
        php_print("</script>\n")
        return True
    # end def print_extra_script
    #// 
    #// Processes a script dependency.
    #// 
    #// @since 2.6.0
    #// @since 2.8.0 Added the `$group` parameter.
    #// 
    #// @see WP_Dependencies::do_item()
    #// 
    #// @param string    $handle The script's registered handle.
    #// @param int|false $group  Optional. Group level: level (int), no groups (false).
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def do_item(self, handle=None, group=False):
        
        if (not super().do_item(handle)):
            return False
        # end if
        if 0 == group and self.groups[handle] > 0:
            self.in_footer[-1] = handle
            return False
        # end if
        if False == group and php_in_array(handle, self.in_footer, True):
            self.in_footer = php_array_diff(self.in_footer, handle)
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
        before_handle = self.print_inline_script(handle, "before", False)
        after_handle = self.print_inline_script(handle, "after", False)
        if before_handle:
            before_handle = php_sprintf("""<script%s>
            %s
            </script>
            """, self.type_attr, before_handle)
        # end if
        if after_handle:
            after_handle = php_sprintf("""<script%s>
            %s
            </script>
            """, self.type_attr, after_handle)
        # end if
        if before_handle or after_handle:
            inline_script_tag = cond_before + before_handle + after_handle + cond_after
        else:
            inline_script_tag = ""
        # end if
        if self.do_concat:
            #// 
            #// Filters the script loader source.
            #// 
            #// @since 2.2.0
            #// 
            #// @param string $src    Script loader source path.
            #// @param string $handle Script handle.
            #//
            srce = apply_filters("script_loader_src", src, handle)
            if self.in_default_dir(srce) and before_handle or after_handle:
                self.do_concat = False
                #// Have to print the so-far concatenated scripts right away to maintain the right order.
                _print_scripts()
                self.reset()
            elif self.in_default_dir(srce) and (not conditional):
                self.print_code += self.print_extra_script(handle, False)
                self.concat += str(handle) + str(",")
                self.concat_version += str(handle) + str(ver)
                return True
            else:
                self.ext_handles += str(handle) + str(",")
                self.ext_version += str(handle) + str(ver)
            # end if
        # end if
        has_conditional_data = conditional and self.get_data(handle, "data")
        if has_conditional_data:
            php_print(cond_before)
        # end if
        self.print_extra_script(handle)
        if has_conditional_data:
            php_print(cond_after)
        # end if
        #// A single item may alias a set of items, by having dependencies, but no source.
        if (not src):
            if inline_script_tag:
                if self.do_concat:
                    self.print_html += inline_script_tag
                else:
                    php_print(inline_script_tag)
                # end if
            # end if
            return True
        # end if
        translations = self.print_translations(handle, False)
        if translations:
            translations = php_sprintf("""<script%s>
            %s
            </script>
            """, self.type_attr, translations)
        # end if
        if (not php_preg_match("|^(https?:)?//|", src)) and (not self.content_url and 0 == php_strpos(src, self.content_url)):
            src = self.base_url + src
        # end if
        if (not php_empty(lambda : ver)):
            src = add_query_arg("ver", ver, src)
        # end if
        #// This filter is documented in wp-includes/class.wp-scripts.php
        src = esc_url(apply_filters("script_loader_src", src, handle))
        if (not src):
            return True
        # end if
        tag = translations + cond_before + before_handle
        tag += php_sprintf("<script%s src='%s'></script>\n", self.type_attr, src)
        tag += after_handle + cond_after
        #// 
        #// Filters the HTML script tag of an enqueued script.
        #// 
        #// @since 4.1.0
        #// 
        #// @param string $tag    The `<script>` tag for the enqueued script.
        #// @param string $handle The script's registered handle.
        #// @param string $src    The script's source URL.
        #//
        tag = apply_filters("script_loader_tag", tag, handle, src)
        if self.do_concat:
            self.print_html += tag
        else:
            php_print(tag)
        # end if
        return True
    # end def do_item
    #// 
    #// Adds extra code to a registered script.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $handle   Name of the script to add the inline script to.
    #// Must be lowercase.
    #// @param string $data     String containing the javascript to be added.
    #// @param string $position Optional. Whether to add the inline script
    #// before the handle or after. Default 'after'.
    #// @return bool True on success, false on failure.
    #//
    def add_inline_script(self, handle=None, data=None, position="after"):
        
        if (not data):
            return False
        # end if
        if "after" != position:
            position = "before"
        # end if
        script = self.get_data(handle, position)
        script[-1] = data
        return self.add_data(handle, position, script)
    # end def add_inline_script
    #// 
    #// Prints inline scripts registered for a specific handle.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $handle   Name of the script to add the inline script to.
    #// Must be lowercase.
    #// @param string $position Optional. Whether to add the inline script
    #// before the handle or after. Default 'after'.
    #// @param bool   $echo     Optional. Whether to echo the script
    #// instead of just returning it. Default true.
    #// @return string|false Script on success, false otherwise.
    #//
    def print_inline_script(self, handle=None, position="after", echo=True):
        
        output = self.get_data(handle, position)
        if php_empty(lambda : output):
            return False
        # end if
        output = php_trim(php_implode("\n", output), "\n")
        if echo:
            printf("""<script%s>
            %s
            </script>
            """, self.type_attr, output)
        # end if
        return output
    # end def print_inline_script
    #// 
    #// Localizes a script, only if the script has already been added.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $handle      Name of the script to attach data to.
    #// @param string $object_name Name of the variable that will contain the data.
    #// @param array  $l10n        Array of data to localize.
    #// @return bool True on success, false on failure.
    #//
    def localize(self, handle=None, object_name=None, l10n=None):
        
        if "jquery" == handle:
            handle = "jquery-core"
        # end if
        if php_is_array(l10n) and (php_isset(lambda : l10n["l10n_print_after"])):
            #// back compat, preserve the code in 'l10n_print_after' if present.
            after = l10n["l10n_print_after"]
            l10n["l10n_print_after"] = None
        # end if
        for key,value in l10n:
            if (not is_scalar(value)):
                continue
            # end if
            l10n[key] = html_entity_decode(php_str(value), ENT_QUOTES, "UTF-8")
        # end for
        script = str("var ") + str(object_name) + str(" = ") + wp_json_encode(l10n) + ";"
        if (not php_empty(lambda : after)):
            script += str("\n") + str(after) + str(";")
        # end if
        data = self.get_data(handle, "data")
        if (not php_empty(lambda : data)):
            script = str(data) + str("\n") + str(script)
        # end if
        return self.add_data(handle, "data", script)
    # end def localize
    #// 
    #// Sets handle group.
    #// 
    #// @since 2.8.0
    #// 
    #// @see WP_Dependencies::set_group()
    #// 
    #// @param string    $handle    Name of the item. Should be unique.
    #// @param bool      $recursion Internal flag that calling function was called recursively.
    #// @param int|false $group     Optional. Group level: level (int), no groups (false).
    #// Default false.
    #// @return bool Not already in the group or a lower group.
    #//
    def set_group(self, handle=None, recursion=None, group=False):
        
        if (php_isset(lambda : self.registered[handle].args)) and 1 == self.registered[handle].args:
            grp = 1
        else:
            grp = php_int(self.get_data(handle, "group"))
        # end if
        if False != group and grp > group:
            grp = group
        # end if
        return super().set_group(handle, recursion, grp)
    # end def set_group
    #// 
    #// Sets a translation textdomain.
    #// 
    #// @since 5.0.0
    #// @since 5.1.0 The `$domain` parameter was made optional.
    #// 
    #// @param string $handle Name of the script to register a translation domain to.
    #// @param string $domain Optional. Text domain. Default 'default'.
    #// @param string $path   Optional. The full file path to the directory containing translation files.
    #// @return bool True if the text domain was registered, false if not.
    #//
    def set_translations(self, handle=None, domain="default", path=None):
        
        if (not (php_isset(lambda : self.registered[handle]))):
            return False
        # end if
        #// @var \_WP_Dependency $obj
        obj = self.registered[handle]
        if (not php_in_array("wp-i18n", obj.deps, True)):
            obj.deps[-1] = "wp-i18n"
        # end if
        return obj.set_translations(domain, path)
    # end def set_translations
    #// 
    #// Prints translations set for a specific handle.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $handle Name of the script to add the inline script to.
    #// Must be lowercase.
    #// @param bool   $echo   Optional. Whether to echo the script
    #// instead of just returning it. Default true.
    #// @return string|false Script on success, false otherwise.
    #//
    def print_translations(self, handle=None, echo=True):
        
        if (not (php_isset(lambda : self.registered[handle]))) or php_empty(lambda : self.registered[handle].textdomain):
            return False
        # end if
        domain = self.registered[handle].textdomain
        path = self.registered[handle].translations_path
        json_translations = load_script_textdomain(handle, domain, path)
        if (not json_translations):
            #// Register empty locale data object to ensure the domain still exists.
            json_translations = "{ \"locale_data\": { \"messages\": { \"\": {} } } }"
        # end if
        output = str("""( function( domain, translations ) {\n  var localeData = translations.locale_data[ domain ] || translations.locale_data.messages;\n localeData[\"\"].domain = domain;\n wp.i18n.setLocaleData( localeData, domain );\n} )( \"""") + str(domain) + str("\", ") + str(json_translations) + str(" );")
        if echo:
            printf("""<script%s>
            %s
            </script>
            """, self.type_attr, output)
        # end if
        return output
    # end def print_translations
    #// 
    #// Determines script dependencies.
    #// 
    #// @since 2.1.0
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
            #// Filters the list of script dependencies left to print.
            #// 
            #// @since 2.3.0
            #// 
            #// @param string[] $to_do An array of script dependency handles.
            #//
            self.to_do = apply_filters("print_scripts_array", self.to_do)
        # end if
        return r
    # end def all_deps
    #// 
    #// Processes items and dependencies for the head group.
    #// 
    #// @since 2.8.0
    #// 
    #// @see WP_Dependencies::do_items()
    #// 
    #// @return string[] Handles of items that have been processed.
    #//
    def do_head_items(self):
        
        self.do_items(False, 0)
        return self.done
    # end def do_head_items
    #// 
    #// Processes items and dependencies for the footer group.
    #// 
    #// @since 2.8.0
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
    #// Whether a handle's source is in a default directory.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $src The source of the enqueued script.
    #// @return bool True if found, false if not.
    #//
    def in_default_dir(self, src=None):
        
        if (not self.default_dirs):
            return True
        # end if
        if 0 == php_strpos(src, "/" + WPINC + "/js/l10n"):
            return False
        # end if
        for test in self.default_dirs:
            if 0 == php_strpos(src, test):
                return True
            # end if
        # end for
        return False
    # end def in_default_dir
    #// 
    #// Resets class properties.
    #// 
    #// @since 2.8.0
    #//
    def reset(self):
        
        self.do_concat = False
        self.print_code = ""
        self.concat = ""
        self.concat_version = ""
        self.print_html = ""
        self.ext_version = ""
        self.ext_handles = ""
    # end def reset
# end class WP_Scripts
