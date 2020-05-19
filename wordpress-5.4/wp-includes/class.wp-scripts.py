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
    #// 
    #// Base URL for scripts.
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
    #// Default version string for scripts.
    #// 
    #// @since 2.6.0
    #// @var string
    #//
    default_version = Array()
    #// 
    #// Holds handles of scripts which are enqueued in footer.
    #// 
    #// @since 2.8.0
    #// @var array
    #//
    in_footer = Array()
    #// 
    #// Holds a list of script handles which will be concatenated.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    concat = ""
    #// 
    #// Holds a string which contains script handles and their version.
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
    #// Holds HTML markup of scripts and additional data if concatenation
    #// is enabled.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    print_html = ""
    #// 
    #// Holds inline code if concatenation is enabled.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    print_code = ""
    #// 
    #// Holds a list of script handles which are not in the default directory
    #// if concatenation is enabled.
    #// 
    #// Unused in core.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    ext_handles = ""
    #// 
    #// Holds a string which contains handles and versions of scripts which
    #// are not in the default directory if concatenation is enabled.
    #// 
    #// Unused in core.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    ext_version = ""
    #// 
    #// List of default directories.
    #// 
    #// @since 2.8.0
    #// @var array
    #//
    default_dirs = Array()
    #// 
    #// Holds a string which contains the type attribute for script tag.
    #// 
    #// If the current theme does not declare HTML5 support for 'script',
    #// then it initializes as `type='text/javascript'`.
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
    def print_scripts(self, handles_=None, group_=None):
        if handles_ is None:
            handles_ = False
        # end if
        if group_ is None:
            group_ = False
        # end if
        
        return self.do_items(handles_, group_)
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
    def print_scripts_l10n(self, handle_=None, echo_=None):
        if echo_ is None:
            echo_ = True
        # end if
        
        _deprecated_function(__FUNCTION__, "3.3.0", "WP_Scripts::print_extra_script()")
        return self.print_extra_script(handle_, echo_)
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
    def print_extra_script(self, handle_=None, echo_=None):
        if echo_ is None:
            echo_ = True
        # end if
        
        output_ = self.get_data(handle_, "data")
        if (not output_):
            return
        # end if
        if (not echo_):
            return output_
        # end if
        php_print(str("<script") + str(self.type_attr) + str(">\n"))
        #// CDATA is not needed for HTML 5.
        if self.type_attr:
            php_print("/* <![CDATA[ */\n")
        # end if
        php_print(str(output_) + str("\n"))
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
    def do_item(self, handle_=None, group_=None):
        if group_ is None:
            group_ = False
        # end if
        
        if (not super().do_item(handle_)):
            return False
        # end if
        if 0 == group_ and self.groups[handle_] > 0:
            self.in_footer[-1] = handle_
            return False
        # end if
        if False == group_ and php_in_array(handle_, self.in_footer, True):
            self.in_footer = php_array_diff(self.in_footer, handle_)
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
        before_handle_ = self.print_inline_script(handle_, "before", False)
        after_handle_ = self.print_inline_script(handle_, "after", False)
        if before_handle_:
            before_handle_ = php_sprintf("""<script%s>
            %s
            </script>
            """, self.type_attr, before_handle_)
        # end if
        if after_handle_:
            after_handle_ = php_sprintf("""<script%s>
            %s
            </script>
            """, self.type_attr, after_handle_)
        # end if
        if before_handle_ or after_handle_:
            inline_script_tag_ = cond_before_ + before_handle_ + after_handle_ + cond_after_
        else:
            inline_script_tag_ = ""
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
            srce_ = apply_filters("script_loader_src", src_, handle_)
            if self.in_default_dir(srce_) and before_handle_ or after_handle_:
                self.do_concat = False
                #// Have to print the so-far concatenated scripts right away to maintain the right order.
                _print_scripts()
                self.reset()
            elif self.in_default_dir(srce_) and (not conditional_):
                self.print_code += self.print_extra_script(handle_, False)
                self.concat += str(handle_) + str(",")
                self.concat_version += str(handle_) + str(ver_)
                return True
            else:
                self.ext_handles += str(handle_) + str(",")
                self.ext_version += str(handle_) + str(ver_)
            # end if
        # end if
        has_conditional_data_ = conditional_ and self.get_data(handle_, "data")
        if has_conditional_data_:
            php_print(cond_before_)
        # end if
        self.print_extra_script(handle_)
        if has_conditional_data_:
            php_print(cond_after_)
        # end if
        #// A single item may alias a set of items, by having dependencies, but no source.
        if (not src_):
            if inline_script_tag_:
                if self.do_concat:
                    self.print_html += inline_script_tag_
                else:
                    php_print(inline_script_tag_)
                # end if
            # end if
            return True
        # end if
        translations_ = self.print_translations(handle_, False)
        if translations_:
            translations_ = php_sprintf("""<script%s>
            %s
            </script>
            """, self.type_attr, translations_)
        # end if
        if (not php_preg_match("|^(https?:)?//|", src_)) and (not self.content_url and 0 == php_strpos(src_, self.content_url)):
            src_ = self.base_url + src_
        # end if
        if (not php_empty(lambda : ver_)):
            src_ = add_query_arg("ver", ver_, src_)
        # end if
        #// This filter is documented in wp-includes/class.wp-scripts.php
        src_ = esc_url(apply_filters("script_loader_src", src_, handle_))
        if (not src_):
            return True
        # end if
        tag_ = translations_ + cond_before_ + before_handle_
        tag_ += php_sprintf("<script%s src='%s'></script>\n", self.type_attr, src_)
        tag_ += after_handle_ + cond_after_
        #// 
        #// Filters the HTML script tag of an enqueued script.
        #// 
        #// @since 4.1.0
        #// 
        #// @param string $tag    The `<script>` tag for the enqueued script.
        #// @param string $handle The script's registered handle.
        #// @param string $src    The script's source URL.
        #//
        tag_ = apply_filters("script_loader_tag", tag_, handle_, src_)
        if self.do_concat:
            self.print_html += tag_
        else:
            php_print(tag_)
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
    def add_inline_script(self, handle_=None, data_=None, position_="after"):
        
        
        if (not data_):
            return False
        # end if
        if "after" != position_:
            position_ = "before"
        # end if
        script_ = self.get_data(handle_, position_)
        script_[-1] = data_
        return self.add_data(handle_, position_, script_)
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
    def print_inline_script(self, handle_=None, position_="after", echo_=None):
        if echo_ is None:
            echo_ = True
        # end if
        
        output_ = self.get_data(handle_, position_)
        if php_empty(lambda : output_):
            return False
        # end if
        output_ = php_trim(php_implode("\n", output_), "\n")
        if echo_:
            printf("""<script%s>
            %s
            </script>
            """, self.type_attr, output_)
        # end if
        return output_
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
    def localize(self, handle_=None, object_name_=None, l10n_=None):
        
        
        if "jquery" == handle_:
            handle_ = "jquery-core"
        # end if
        if php_is_array(l10n_) and (php_isset(lambda : l10n_["l10n_print_after"])):
            #// back compat, preserve the code in 'l10n_print_after' if present.
            after_ = l10n_["l10n_print_after"]
            l10n_["l10n_print_after"] = None
        # end if
        for key_,value_ in l10n_.items():
            if (not php_is_scalar(value_)):
                continue
            # end if
            l10n_[key_] = html_entity_decode(php_str(value_), ENT_QUOTES, "UTF-8")
        # end for
        script_ = str("var ") + str(object_name_) + str(" = ") + wp_json_encode(l10n_) + ";"
        if (not php_empty(lambda : after_)):
            script_ += str("\n") + str(after_) + str(";")
        # end if
        data_ = self.get_data(handle_, "data")
        if (not php_empty(lambda : data_)):
            script_ = str(data_) + str("\n") + str(script_)
        # end if
        return self.add_data(handle_, "data", script_)
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
    def set_group(self, handle_=None, recursion_=None, group_=None):
        if group_ is None:
            group_ = False
        # end if
        
        if (php_isset(lambda : self.registered[handle_].args)) and 1 == self.registered[handle_].args:
            grp_ = 1
        else:
            grp_ = php_int(self.get_data(handle_, "group"))
        # end if
        if False != group_ and grp_ > group_:
            grp_ = group_
        # end if
        return super().set_group(handle_, recursion_, grp_)
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
    def set_translations(self, handle_=None, domain_="default", path_=None):
        if path_ is None:
            path_ = None
        # end if
        
        if (not (php_isset(lambda : self.registered[handle_]))):
            return False
        # end if
        #// @var \_WP_Dependency $obj
        obj_ = self.registered[handle_]
        if (not php_in_array("wp-i18n", obj_.deps, True)):
            obj_.deps[-1] = "wp-i18n"
        # end if
        return obj_.set_translations(domain_, path_)
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
    def print_translations(self, handle_=None, echo_=None):
        if echo_ is None:
            echo_ = True
        # end if
        
        if (not (php_isset(lambda : self.registered[handle_]))) or php_empty(lambda : self.registered[handle_].textdomain):
            return False
        # end if
        domain_ = self.registered[handle_].textdomain
        path_ = self.registered[handle_].translations_path
        json_translations_ = load_script_textdomain(handle_, domain_, path_)
        if (not json_translations_):
            #// Register empty locale data object to ensure the domain still exists.
            json_translations_ = "{ \"locale_data\": { \"messages\": { \"\": {} } } }"
        # end if
        output_ = str("""( function( domain, translations ) {\n var localeData = translations.locale_data[ domain ] || translations.locale_data.messages;\n localeData[\"\"].domain = domain;\n wp.i18n.setLocaleData( localeData, domain );\n} )( \"""") + str(domain_) + str("\", ") + str(json_translations_) + str(" );")
        if echo_:
            printf("""<script%s>
            %s
            </script>
            """, self.type_attr, output_)
        # end if
        return output_
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
            #// Filters the list of script dependencies left to print.
            #// 
            #// @since 2.3.0
            #// 
            #// @param string[] $to_do An array of script dependency handles.
            #//
            self.to_do = apply_filters("print_scripts_array", self.to_do)
        # end if
        return r_
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
    def in_default_dir(self, src_=None):
        
        
        if (not self.default_dirs):
            return True
        # end if
        if 0 == php_strpos(src_, "/" + WPINC + "/js/l10n"):
            return False
        # end if
        for test_ in self.default_dirs:
            if 0 == php_strpos(src_, test_):
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
