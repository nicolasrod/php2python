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
#// WP_Theme Class
#// 
#// @package WordPress
#// @subpackage Theme
#// @since 3.4.0
#//
class WP_Theme(ArrayAccess):
    #// 
    #// Whether the theme has been marked as updateable.
    #// 
    #// @since 4.4.0
    #// @var bool
    #// 
    #// @see WP_MS_Themes_List_Table
    #//
    update = False
    #// 
    #// Headers for style.css files.
    #// 
    #// @since 3.4.0
    #// @since 5.4.0 Added `Requires at least` and `Requires PHP` headers.
    #// @var array
    #//
    file_headers = Array({"Name": "Theme Name", "ThemeURI": "Theme URI", "Description": "Description", "Author": "Author", "AuthorURI": "Author URI", "Version": "Version", "Template": "Template", "Status": "Status", "Tags": "Tags", "TextDomain": "Text Domain", "DomainPath": "Domain Path", "RequiresWP": "Requires at least", "RequiresPHP": "Requires PHP"})
    #// 
    #// Default themes.
    #// 
    #// @var array
    #//
    default_themes = Array({"classic": "WordPress Classic", "default": "WordPress Default", "twentyten": "Twenty Ten", "twentyeleven": "Twenty Eleven", "twentytwelve": "Twenty Twelve", "twentythirteen": "Twenty Thirteen", "twentyfourteen": "Twenty Fourteen", "twentyfifteen": "Twenty Fifteen", "twentysixteen": "Twenty Sixteen", "twentyseventeen": "Twenty Seventeen", "twentynineteen": "Twenty Nineteen", "twentytwenty": "Twenty Twenty"})
    #// 
    #// Renamed theme tags.
    #// 
    #// @var array
    #//
    tag_map = Array({"fixed-width": "fixed-layout", "flexible-width": "fluid-layout"})
    #// 
    #// Absolute path to the theme root, usually wp-content/themes
    #// 
    #// @var string
    #//
    theme_root = Array()
    #// 
    #// Header data from the theme's style.css file.
    #// 
    #// @var array
    #//
    headers = Array()
    #// 
    #// Header data from the theme's style.css file after being sanitized.
    #// 
    #// @var array
    #//
    headers_sanitized = Array()
    #// 
    #// Header name from the theme's style.css after being translated.
    #// 
    #// Cached due to sorting functions running over the translated name.
    #// 
    #// @var string
    #//
    name_translated = Array()
    #// 
    #// Errors encountered when initializing the theme.
    #// 
    #// @var WP_Error
    #//
    errors = Array()
    #// 
    #// The directory name of the theme's files, inside the theme root.
    #// 
    #// In the case of a child theme, this is directory name of the child theme.
    #// Otherwise, 'stylesheet' is the same as 'template'.
    #// 
    #// @var string
    #//
    stylesheet = Array()
    #// 
    #// The directory name of the theme's files, inside the theme root.
    #// 
    #// In the case of a child theme, this is the directory name of the parent theme.
    #// Otherwise, 'template' is the same as 'stylesheet'.
    #// 
    #// @var string
    #//
    template = Array()
    #// 
    #// A reference to the parent theme, in the case of a child theme.
    #// 
    #// @var WP_Theme
    #//
    parent = Array()
    #// 
    #// URL to the theme root, usually an absolute URL to wp-content/themes
    #// 
    #// @var string
    #//
    theme_root_uri = Array()
    #// 
    #// Flag for whether the theme's textdomain is loaded.
    #// 
    #// @var bool
    #//
    textdomain_loaded = Array()
    #// 
    #// Stores an md5 hash of the theme root, to function as the cache key.
    #// 
    #// @var string
    #//
    cache_hash = Array()
    #// 
    #// Flag for whether the themes cache bucket should be persistently cached.
    #// 
    #// Default is false. Can be set with the {@see 'wp_cache_themes_persistently'} filter.
    #// 
    #// @var bool
    #//
    persistently_cache = Array()
    #// 
    #// Expiration time for the themes cache bucket.
    #// 
    #// By default the bucket is not cached, so this value is useless.
    #// 
    #// @var bool
    #//
    cache_expiration = 1800
    #// 
    #// Constructor for WP_Theme.
    #// 
    #// @since 3.4.0
    #// 
    #// @global array $wp_theme_directories
    #// 
    #// @param string $theme_dir Directory of the theme within the theme_root.
    #// @param string $theme_root Theme root.
    #// @param WP_Theme|null $_child If this theme is a parent theme, the child may be passed for validation purposes.
    #//
    def __init__(self, theme_dir_=None, theme_root_=None, _child_=None):
        if _child_ is None:
            _child_ = None
        # end if
        
        global wp_theme_directories_
        php_check_if_defined("wp_theme_directories_")
        #// Initialize caching on first run.
        if (not (php_isset(lambda : self.persistently_cache))):
            #// This action is documented in wp-includes/theme.php
            self.persistently_cache = apply_filters("wp_cache_themes_persistently", False, "WP_Theme")
            if self.persistently_cache:
                wp_cache_add_global_groups("themes")
                if php_is_int(self.persistently_cache):
                    self.cache_expiration = self.persistently_cache
                # end if
            else:
                wp_cache_add_non_persistent_groups("themes")
            # end if
        # end if
        self.theme_root = theme_root_
        self.stylesheet = theme_dir_
        #// Correct a situation where the theme is 'some-directory/some-theme' but 'some-directory' was passed in as part of the theme root instead.
        if (not php_in_array(theme_root_, wp_theme_directories_)) and php_in_array(php_dirname(theme_root_), wp_theme_directories_):
            self.stylesheet = php_basename(self.theme_root) + "/" + self.stylesheet
            self.theme_root = php_dirname(theme_root_)
        # end if
        self.cache_hash = php_md5(self.theme_root + "/" + self.stylesheet)
        theme_file_ = self.stylesheet + "/style.css"
        cache_ = self.cache_get("theme")
        if php_is_array(cache_):
            for key_ in Array("errors", "headers", "template"):
                if (php_isset(lambda : cache_[key_])):
                    self.key_ = cache_[key_]
                # end if
            # end for
            if self.errors:
                return
            # end if
            if (php_isset(lambda : cache_["theme_root_template"])):
                theme_root_template_ = cache_["theme_root_template"]
            # end if
        elif (not php_file_exists(self.theme_root + "/" + theme_file_)):
            self.headers["Name"] = self.stylesheet
            if (not php_file_exists(self.theme_root + "/" + self.stylesheet)):
                self.errors = php_new_class("WP_Error", lambda : WP_Error("theme_not_found", php_sprintf(__("The theme directory \"%s\" does not exist."), esc_html(self.stylesheet))))
            else:
                self.errors = php_new_class("WP_Error", lambda : WP_Error("theme_no_stylesheet", __("Stylesheet is missing.")))
            # end if
            self.template = self.stylesheet
            self.cache_add("theme", Array({"headers": self.headers, "errors": self.errors, "stylesheet": self.stylesheet, "template": self.template}))
            if (not php_file_exists(self.theme_root)):
                #// Don't cache this one.
                self.errors.add("theme_root_missing", __("Error: The themes directory is either empty or doesn&#8217;t exist. Please check your installation."))
            # end if
            return
        elif (not php_is_readable(self.theme_root + "/" + theme_file_)):
            self.headers["Name"] = self.stylesheet
            self.errors = php_new_class("WP_Error", lambda : WP_Error("theme_stylesheet_not_readable", __("Stylesheet is not readable.")))
            self.template = self.stylesheet
            self.cache_add("theme", Array({"headers": self.headers, "errors": self.errors, "stylesheet": self.stylesheet, "template": self.template}))
            return
        else:
            self.headers = get_file_data(self.theme_root + "/" + theme_file_, self.file_headers, "theme")
            #// Default themes always trump their pretenders.
            #// Properly identify default themes that are inside a directory within wp-content/themes.
            default_theme_slug_ = php_array_search(self.headers["Name"], self.default_themes)
            if default_theme_slug_:
                if php_basename(self.stylesheet) != default_theme_slug_:
                    self.headers["Name"] += "/" + self.stylesheet
                # end if
            # end if
        # end if
        if (not self.template) and self.stylesheet == self.headers["Template"]:
            self.errors = php_new_class("WP_Error", lambda : WP_Error("theme_child_invalid", php_sprintf(__("The theme defines itself as its parent theme. Please check the %s header."), "<code>Template</code>")))
            self.cache_add("theme", Array({"headers": self.headers, "errors": self.errors, "stylesheet": self.stylesheet}))
            return
        # end if
        #// (If template is set from cache [and there are no errors], we know it's good.)
        if (not self.template):
            self.template = self.headers["Template"]
        # end if
        if (not self.template):
            self.template = self.stylesheet
            if (not php_file_exists(self.theme_root + "/" + self.stylesheet + "/index.php")):
                error_message_ = php_sprintf(__("Template is missing. Standalone themes need to have a %1$s template file. <a href=\"%2$s\">Child themes</a> need to have a Template header in the %3$s stylesheet."), "<code>index.php</code>", __("https://developer.wordpress.org/themes/advanced-topics/child-themes/"), "<code>style.css</code>")
                self.errors = php_new_class("WP_Error", lambda : WP_Error("theme_no_index", error_message_))
                self.cache_add("theme", Array({"headers": self.headers, "errors": self.errors, "stylesheet": self.stylesheet, "template": self.template}))
                return
            # end if
        # end if
        #// If we got our data from cache, we can assume that 'template' is pointing to the right place.
        if (not php_is_array(cache_)) and self.template != self.stylesheet and (not php_file_exists(self.theme_root + "/" + self.template + "/index.php")):
            #// If we're in a directory of themes inside /themes, look for the parent nearby.
            #// wp-content/themes/directory-of-themes
            parent_dir_ = php_dirname(self.stylesheet)
            directories_ = search_theme_directories()
            if "." != parent_dir_ and php_file_exists(self.theme_root + "/" + parent_dir_ + "/" + self.template + "/index.php"):
                self.template = parent_dir_ + "/" + self.template
            elif directories_ and (php_isset(lambda : directories_[self.template])):
                #// Look for the template in the search_theme_directories() results, in case it is in another theme root.
                #// We don't look into directories of themes, just the theme root.
                theme_root_template_ = directories_[self.template]["theme_root"]
            else:
                #// Parent theme is missing.
                self.errors = php_new_class("WP_Error", lambda : WP_Error("theme_no_parent", php_sprintf(__("The parent theme is missing. Please install the \"%s\" parent theme."), esc_html(self.template))))
                self.cache_add("theme", Array({"headers": self.headers, "errors": self.errors, "stylesheet": self.stylesheet, "template": self.template}))
                self.parent = php_new_class("WP_Theme", lambda : WP_Theme(self.template, self.theme_root, self))
                return
            # end if
        # end if
        #// Set the parent, if we're a child theme.
        if self.template != self.stylesheet:
            #// If we are a parent, then there is a problem. Only two generations allowed! Cancel things out.
            if type(_child_).__name__ == "WP_Theme" and _child_.template == self.stylesheet:
                _child_.parent = None
                _child_.errors = php_new_class("WP_Error", lambda : WP_Error("theme_parent_invalid", php_sprintf(__("The \"%s\" theme is not a valid parent theme."), esc_html(_child_.template))))
                _child_.cache_add("theme", Array({"headers": _child_.headers, "errors": _child_.errors, "stylesheet": _child_.stylesheet, "template": _child_.template}))
                #// The two themes actually reference each other with the Template header.
                if _child_.stylesheet == self.template:
                    self.errors = php_new_class("WP_Error", lambda : WP_Error("theme_parent_invalid", php_sprintf(__("The \"%s\" theme is not a valid parent theme."), esc_html(self.template))))
                    self.cache_add("theme", Array({"headers": self.headers, "errors": self.errors, "stylesheet": self.stylesheet, "template": self.template}))
                # end if
                return
            # end if
            #// Set the parent. Pass the current instance so we can do the crazy checks above and assess errors.
            self.parent = php_new_class("WP_Theme", lambda : WP_Theme(self.template, theme_root_template_ if (php_isset(lambda : theme_root_template_)) else self.theme_root, self))
        # end if
        if wp_paused_themes().get(self.stylesheet) and (not is_wp_error(self.errors)) or (not (php_isset(lambda : self.errors.errors["theme_paused"]))):
            self.errors = php_new_class("WP_Error", lambda : WP_Error("theme_paused", __("This theme failed to load properly and was paused within the admin backend.")))
        # end if
        #// We're good. If we didn't retrieve from cache, set it.
        if (not php_is_array(cache_)):
            cache_ = Array({"headers": self.headers, "errors": self.errors, "stylesheet": self.stylesheet, "template": self.template})
            #// If the parent theme is in another root, we'll want to cache this. Avoids an entire branch of filesystem calls above.
            if (php_isset(lambda : theme_root_template_)):
                cache_["theme_root_template"] = theme_root_template_
            # end if
            self.cache_add("theme", cache_)
        # end if
    # end def __init__
    #// 
    #// When converting the object to a string, the theme name is returned.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Theme name, ready for display (translated)
    #//
    def __tostring(self):
        
        
        return php_str(self.display("Name"))
    # end def __tostring
    #// 
    #// __isset() magic method for properties formerly returned by current_theme_info()
    #// 
    #// @staticvar array $properties
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $offset Property to check if set.
    #// @return bool Whether the given property is set.
    #//
    def __isset(self, offset_=None):
        
        
        properties_ = Array("name", "title", "version", "parent_theme", "template_dir", "stylesheet_dir", "template", "stylesheet", "screenshot", "description", "author", "tags", "theme_root", "theme_root_uri")
        return php_in_array(offset_, properties_)
    # end def __isset
    #// 
    #// __get() magic method for properties formerly returned by current_theme_info()
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $offset Property to get.
    #// @return mixed Property value.
    #//
    def __get(self, offset_=None):
        
        
        for case in Switch(offset_):
            if case("name"):
                pass
            # end if
            if case("title"):
                return self.get("Name")
            # end if
            if case("version"):
                return self.get("Version")
            # end if
            if case("parent_theme"):
                return self.parent().get("Name") if self.parent() else ""
            # end if
            if case("template_dir"):
                return self.get_template_directory()
            # end if
            if case("stylesheet_dir"):
                return self.get_stylesheet_directory()
            # end if
            if case("template"):
                return self.get_template()
            # end if
            if case("stylesheet"):
                return self.get_stylesheet()
            # end if
            if case("screenshot"):
                return self.get_screenshot("relative")
            # end if
            if case("description"):
                return self.display("Description")
            # end if
            if case("author"):
                return self.display("Author")
            # end if
            if case("tags"):
                return self.get("Tags")
            # end if
            if case("theme_root"):
                return self.get_theme_root()
            # end if
            if case("theme_root_uri"):
                return self.get_theme_root_uri()
            # end if
            if case():
                return self.offsetget(offset_)
            # end if
        # end for
    # end def __get
    #// 
    #// Method to implement ArrayAccess for keys formerly returned by get_themes()
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $offset
    #// @param mixed $value
    #//
    def offsetset(self, offset_=None, value_=None):
        
        
        pass
    # end def offsetset
    #// 
    #// Method to implement ArrayAccess for keys formerly returned by get_themes()
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $offset
    #//
    def offsetunset(self, offset_=None):
        
        
        pass
    # end def offsetunset
    #// 
    #// Method to implement ArrayAccess for keys formerly returned by get_themes()
    #// 
    #// @staticvar array $keys
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $offset
    #// @return bool
    #//
    def offsetexists(self, offset_=None):
        
        
        keys_ = Array("Name", "Version", "Status", "Title", "Author", "Author Name", "Author URI", "Description", "Template", "Stylesheet", "Template Files", "Stylesheet Files", "Template Dir", "Stylesheet Dir", "Screenshot", "Tags", "Theme Root", "Theme Root URI", "Parent Theme")
        return php_in_array(offset_, keys_)
    # end def offsetexists
    #// 
    #// Method to implement ArrayAccess for keys formerly returned by get_themes().
    #// 
    #// Author, Author Name, Author URI, and Description did not previously return
    #// translated data. We are doing so now as it is safe to do. However, as
    #// Name and Title could have been used as the key for get_themes(), both remain
    #// untranslated for back compatibility. This means that ['Name'] is not ideal,
    #// and care should be taken to use `$theme::display( 'Name' )` to get a properly
    #// translated header.
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $offset
    #// @return mixed
    #//
    def offsetget(self, offset_=None):
        
        
        for case in Switch(offset_):
            if case("Name"):
                pass
            # end if
            if case("Title"):
                #// 
                #// See note above about using translated data. get() is not ideal.
                #// It is only for backward compatibility. Use display().
                #//
                return self.get("Name")
            # end if
            if case("Author"):
                return self.display("Author")
            # end if
            if case("Author Name"):
                return self.display("Author", False)
            # end if
            if case("Author URI"):
                return self.display("AuthorURI")
            # end if
            if case("Description"):
                return self.display("Description")
            # end if
            if case("Version"):
                pass
            # end if
            if case("Status"):
                return self.get(offset_)
            # end if
            if case("Template"):
                return self.get_template()
            # end if
            if case("Stylesheet"):
                return self.get_stylesheet()
            # end if
            if case("Template Files"):
                return self.get_files("php", 1, True)
            # end if
            if case("Stylesheet Files"):
                return self.get_files("css", 0, False)
            # end if
            if case("Template Dir"):
                return self.get_template_directory()
            # end if
            if case("Stylesheet Dir"):
                return self.get_stylesheet_directory()
            # end if
            if case("Screenshot"):
                return self.get_screenshot("relative")
            # end if
            if case("Tags"):
                return self.get("Tags")
            # end if
            if case("Theme Root"):
                return self.get_theme_root()
            # end if
            if case("Theme Root URI"):
                return self.get_theme_root_uri()
            # end if
            if case("Parent Theme"):
                return self.parent().get("Name") if self.parent() else ""
            # end if
            if case():
                return None
            # end if
        # end for
    # end def offsetget
    #// 
    #// Returns errors property.
    #// 
    #// @since 3.4.0
    #// 
    #// @return WP_Error|false WP_Error if there are errors, or false.
    #//
    def errors(self):
        
        
        return self.errors if is_wp_error(self.errors) else False
    # end def errors
    #// 
    #// Whether the theme exists.
    #// 
    #// A theme with errors exists. A theme with the error of 'theme_not_found',
    #// meaning that the theme's directory was not found, does not exist.
    #// 
    #// @since 3.4.0
    #// 
    #// @return bool Whether the theme exists.
    #//
    def exists(self):
        
        
        return (not self.errors() and php_in_array("theme_not_found", self.errors().get_error_codes()))
    # end def exists
    #// 
    #// Returns reference to the parent theme.
    #// 
    #// @since 3.4.0
    #// 
    #// @return WP_Theme|false Parent theme, or false if the current theme is not a child theme.
    #//
    def parent(self):
        
        
        return self.parent if (php_isset(lambda : self.parent)) else False
    # end def parent
    #// 
    #// Adds theme data to cache.
    #// 
    #// Cache entries keyed by the theme and the type of data.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $key Type of data to store (theme, screenshot, headers, post_templates)
    #// @param array|string $data Data to store
    #// @return bool Return value from wp_cache_add()
    #//
    def cache_add(self, key_=None, data_=None):
        
        
        return wp_cache_add(key_ + "-" + self.cache_hash, data_, "themes", self.cache_expiration)
    # end def cache_add
    #// 
    #// Gets theme data from cache.
    #// 
    #// Cache entries are keyed by the theme and the type of data.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $key Type of data to retrieve (theme, screenshot, headers, post_templates)
    #// @return mixed Retrieved data
    #//
    def cache_get(self, key_=None):
        
        
        return wp_cache_get(key_ + "-" + self.cache_hash, "themes")
    # end def cache_get
    #// 
    #// Clears the cache for the theme.
    #// 
    #// @since 3.4.0
    #//
    def cache_delete(self):
        
        
        for key_ in Array("theme", "screenshot", "headers", "post_templates"):
            wp_cache_delete(key_ + "-" + self.cache_hash, "themes")
        # end for
        self.template = None
        self.textdomain_loaded = None
        self.theme_root_uri = None
        self.parent = None
        self.errors = None
        self.headers_sanitized = None
        self.name_translated = None
        self.headers = Array()
        self.__init__(self.stylesheet, self.theme_root)
    # end def cache_delete
    #// 
    #// Get a raw, unformatted theme header.
    #// 
    #// The header is sanitized, but is not translated, and is not marked up for display.
    #// To get a theme header for display, use the display() method.
    #// 
    #// Use the get_template() method, not the 'Template' header, for finding the template.
    #// The 'Template' header is only good for what was written in the style.css, while
    #// get_template() takes into account where WordPress actually located the theme and
    #// whether it is actually valid.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $header Theme header. Name, Description, Author, Version, ThemeURI, AuthorURI, Status, Tags.
    #// @return string|array|false String or array (for Tags header) on success, false on failure.
    #//
    def get(self, header_=None):
        
        
        if (not (php_isset(lambda : self.headers[header_]))):
            return False
        # end if
        if (not (php_isset(lambda : self.headers_sanitized))):
            self.headers_sanitized = self.cache_get("headers")
            if (not php_is_array(self.headers_sanitized)):
                self.headers_sanitized = Array()
            # end if
        # end if
        if (php_isset(lambda : self.headers_sanitized[header_])):
            return self.headers_sanitized[header_]
        # end if
        #// If themes are a persistent group, sanitize everything and cache it. One cache add is better than many cache sets.
        if self.persistently_cache:
            for _header_ in php_array_keys(self.headers):
                self.headers_sanitized[_header_] = self.sanitize_header(_header_, self.headers[_header_])
            # end for
            self.cache_add("headers", self.headers_sanitized)
        else:
            self.headers_sanitized[header_] = self.sanitize_header(header_, self.headers[header_])
        # end if
        return self.headers_sanitized[header_]
    # end def get
    #// 
    #// Gets a theme header, formatted and translated for display.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $header Theme header. Name, Description, Author, Version, ThemeURI, AuthorURI, Status, Tags.
    #// @param bool $markup Optional. Whether to mark up the header. Defaults to true.
    #// @param bool $translate Optional. Whether to translate the header. Defaults to true.
    #// @return string|array|false Processed header. An array for Tags if `$markup` is false, string otherwise.
    #// False on failure.
    #//
    def display(self, header_=None, markup_=None, translate_=None):
        if markup_ is None:
            markup_ = True
        # end if
        if translate_ is None:
            translate_ = True
        # end if
        
        value_ = self.get(header_)
        if False == value_:
            return False
        # end if
        if translate_ and php_empty(lambda : value_) or (not self.load_textdomain()):
            translate_ = False
        # end if
        if translate_:
            value_ = self.translate_header(header_, value_)
        # end if
        if markup_:
            value_ = self.markup_header(header_, value_, translate_)
        # end if
        return value_
    # end def display
    #// 
    #// Sanitize a theme header.
    #// 
    #// @since 3.4.0
    #// @since 5.4.0 Added support for `Requires at least` and `Requires PHP` headers.
    #// 
    #// @staticvar array $header_tags
    #// @staticvar array $header_tags_with_a
    #// 
    #// @param string $header Theme header. Accepts 'Name', 'Description', 'Author', 'Version',
    #// 'ThemeURI', 'AuthorURI', 'Status', 'Tags', 'RequiresWP', 'RequiresPHP'.
    #// @param string $value  Value to sanitize.
    #// @return string|array An array for Tags header, string otherwise.
    #//
    def sanitize_header(self, header_=None, value_=None):
        
        
        for case in Switch(header_):
            if case("Status"):
                if (not value_):
                    value_ = "publish"
                    break
                # end if
            # end if
            if case("Name"):
                header_tags_ = Array({"abbr": Array({"title": True})}, {"acronym": Array({"title": True})}, {"code": True, "em": True, "strong": True})
                value_ = wp_kses(value_, header_tags_)
                break
            # end if
            if case("Author"):
                pass
            # end if
            if case("Description"):
                header_tags_with_a_ = Array({"a": Array({"href": True, "title": True})}, {"abbr": Array({"title": True})}, {"acronym": Array({"title": True})}, {"code": True, "em": True, "strong": True})
                value_ = wp_kses(value_, header_tags_with_a_)
                break
            # end if
            if case("ThemeURI"):
                pass
            # end if
            if case("AuthorURI"):
                value_ = esc_url_raw(value_)
                break
            # end if
            if case("Tags"):
                value_ = php_array_filter(php_array_map("trim", php_explode(",", strip_tags(value_))))
                break
            # end if
            if case("Version"):
                pass
            # end if
            if case("RequiresWP"):
                pass
            # end if
            if case("RequiresPHP"):
                value_ = strip_tags(value_)
                break
            # end if
        # end for
        return value_
    # end def sanitize_header
    #// 
    #// Mark up a theme header.
    #// 
    #// @since 3.4.0
    #// 
    #// @staticvar string $comma
    #// 
    #// @param string       $header    Theme header. Name, Description, Author, Version, ThemeURI, AuthorURI, Status, Tags.
    #// @param string|array $value     Value to mark up. An array for Tags header, string otherwise.
    #// @param string       $translate Whether the header has been translated.
    #// @return string Value, marked up.
    #//
    def markup_header(self, header_=None, value_=None, translate_=None):
        
        
        for case in Switch(header_):
            if case("Name"):
                if php_empty(lambda : value_):
                    value_ = esc_html(self.get_stylesheet())
                # end if
                break
            # end if
            if case("Description"):
                value_ = wptexturize(value_)
                break
            # end if
            if case("Author"):
                if self.get("AuthorURI"):
                    value_ = php_sprintf("<a href=\"%1$s\">%2$s</a>", self.display("AuthorURI", True, translate_), value_)
                elif (not value_):
                    value_ = __("Anonymous")
                # end if
                break
            # end if
            if case("Tags"):
                comma_ = None
                if (not (php_isset(lambda : comma_))):
                    #// translators: Used between list items, there is a space after the comma.
                    comma_ = __(", ")
                # end if
                value_ = php_implode(comma_, value_)
                break
            # end if
            if case("ThemeURI"):
                pass
            # end if
            if case("AuthorURI"):
                value_ = esc_url(value_)
                break
            # end if
        # end for
        return value_
    # end def markup_header
    #// 
    #// Translate a theme header.
    #// 
    #// @since 3.4.0
    #// 
    #// @staticvar array $tags_list
    #// 
    #// @param string       $header Theme header. Name, Description, Author, Version, ThemeURI, AuthorURI, Status, Tags.
    #// @param string|array $value  Value to translate. An array for Tags header, string otherwise.
    #// @return string|array Translated value. An array for Tags header, string otherwise.
    #//
    def translate_header(self, header_=None, value_=None):
        
        
        for case in Switch(header_):
            if case("Name"):
                #// Cached for sorting reasons.
                if (php_isset(lambda : self.name_translated)):
                    return self.name_translated
                # end if
                #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText,WordPress.WP.I18n.NonSingularStringLiteralDomain
                self.name_translated = translate(value_, self.get("TextDomain"))
                return self.name_translated
            # end if
            if case("Tags"):
                if php_empty(lambda : value_) or (not php_function_exists("get_theme_feature_list")):
                    return value_
                # end if
                tags_list_ = None
                if (not (php_isset(lambda : tags_list_))):
                    tags_list_ = Array({"black": __("Black"), "blue": __("Blue"), "brown": __("Brown"), "gray": __("Gray"), "green": __("Green"), "orange": __("Orange"), "pink": __("Pink"), "purple": __("Purple"), "red": __("Red"), "silver": __("Silver"), "tan": __("Tan"), "white": __("White"), "yellow": __("Yellow"), "dark": __("Dark"), "light": __("Light"), "fixed-layout": __("Fixed Layout"), "fluid-layout": __("Fluid Layout"), "responsive-layout": __("Responsive Layout"), "blavatar": __("Blavatar"), "photoblogging": __("Photoblogging"), "seasonal": __("Seasonal")})
                    feature_list_ = get_theme_feature_list(False)
                    #// No API.
                    for tags_ in feature_list_:
                        tags_list_ += tags_
                    # end for
                # end if
                for tag_ in value_:
                    if (php_isset(lambda : tags_list_[tag_])):
                        tag_ = tags_list_[tag_]
                    elif (php_isset(lambda : self.tag_map[tag_])):
                        tag_ = tags_list_[self.tag_map[tag_]]
                    # end if
                # end for
                return value_
            # end if
            if case():
                #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText,WordPress.WP.I18n.NonSingularStringLiteralDomain
                value_ = translate(value_, self.get("TextDomain"))
            # end if
        # end for
        return value_
    # end def translate_header
    #// 
    #// The directory name of the theme's "stylesheet" files, inside the theme root.
    #// 
    #// In the case of a child theme, this is directory name of the child theme.
    #// Otherwise, get_stylesheet() is the same as get_template().
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Stylesheet
    #//
    def get_stylesheet(self):
        
        
        return self.stylesheet
    # end def get_stylesheet
    #// 
    #// The directory name of the theme's "template" files, inside the theme root.
    #// 
    #// In the case of a child theme, this is the directory name of the parent theme.
    #// Otherwise, the get_template() is the same as get_stylesheet().
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Template
    #//
    def get_template(self):
        
        
        return self.template
    # end def get_template
    #// 
    #// Returns the absolute path to the directory of a theme's "stylesheet" files.
    #// 
    #// In the case of a child theme, this is the absolute path to the directory
    #// of the child theme's files.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Absolute path of the stylesheet directory.
    #//
    def get_stylesheet_directory(self):
        
        
        if self.errors() and php_in_array("theme_root_missing", self.errors().get_error_codes()):
            return ""
        # end if
        return self.theme_root + "/" + self.stylesheet
    # end def get_stylesheet_directory
    #// 
    #// Returns the absolute path to the directory of a theme's "template" files.
    #// 
    #// In the case of a child theme, this is the absolute path to the directory
    #// of the parent theme's files.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Absolute path of the template directory.
    #//
    def get_template_directory(self):
        
        
        if self.parent():
            theme_root_ = self.parent().theme_root
        else:
            theme_root_ = self.theme_root
        # end if
        return theme_root_ + "/" + self.template
    # end def get_template_directory
    #// 
    #// Returns the URL to the directory of a theme's "stylesheet" files.
    #// 
    #// In the case of a child theme, this is the URL to the directory of the
    #// child theme's files.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string URL to the stylesheet directory.
    #//
    def get_stylesheet_directory_uri(self):
        
        
        return self.get_theme_root_uri() + "/" + php_str_replace("%2F", "/", rawurlencode(self.stylesheet))
    # end def get_stylesheet_directory_uri
    #// 
    #// Returns the URL to the directory of a theme's "template" files.
    #// 
    #// In the case of a child theme, this is the URL to the directory of the
    #// parent theme's files.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string URL to the template directory.
    #//
    def get_template_directory_uri(self):
        
        
        if self.parent():
            theme_root_uri_ = self.parent().get_theme_root_uri()
        else:
            theme_root_uri_ = self.get_theme_root_uri()
        # end if
        return theme_root_uri_ + "/" + php_str_replace("%2F", "/", rawurlencode(self.template))
    # end def get_template_directory_uri
    #// 
    #// The absolute path to the directory of the theme root.
    #// 
    #// This is typically the absolute path to wp-content/themes.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Theme root.
    #//
    def get_theme_root(self):
        
        
        return self.theme_root
    # end def get_theme_root
    #// 
    #// Returns the URL to the directory of the theme root.
    #// 
    #// This is typically the absolute URL to wp-content/themes. This forms the basis
    #// for all other URLs returned by WP_Theme, so we pass it to the public function
    #// get_theme_root_uri() and allow it to run the {@see 'theme_root_uri'} filter.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Theme root URI.
    #//
    def get_theme_root_uri(self):
        
        
        if (not (php_isset(lambda : self.theme_root_uri))):
            self.theme_root_uri = get_theme_root_uri(self.stylesheet, self.theme_root)
        # end if
        return self.theme_root_uri
    # end def get_theme_root_uri
    #// 
    #// Returns the main screenshot file for the theme.
    #// 
    #// The main screenshot is called screenshot.png. gif and jpg extensions are also allowed.
    #// 
    #// Screenshots for a theme must be in the stylesheet directory. (In the case of child
    #// themes, parent theme screenshots are not inherited.)
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $uri Type of URL to return, either 'relative' or an absolute URI. Defaults to absolute URI.
    #// @return string|false Screenshot file. False if the theme does not have a screenshot.
    #//
    def get_screenshot(self, uri_="uri"):
        
        
        screenshot_ = self.cache_get("screenshot")
        if screenshot_:
            if "relative" == uri_:
                return screenshot_
            # end if
            return self.get_stylesheet_directory_uri() + "/" + screenshot_
        elif 0 == screenshot_:
            return False
        # end if
        for ext_ in Array("png", "gif", "jpg", "jpeg"):
            if php_file_exists(self.get_stylesheet_directory() + str("/screenshot.") + str(ext_)):
                self.cache_add("screenshot", "screenshot." + ext_)
                if "relative" == uri_:
                    return "screenshot." + ext_
                # end if
                return self.get_stylesheet_directory_uri() + "/" + "screenshot." + ext_
            # end if
        # end for
        self.cache_add("screenshot", 0)
        return False
    # end def get_screenshot
    #// 
    #// Return files in the theme's directory.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string[]|string $type       Optional. Array of extensions to find, string of a single extension,
    #// or null for all extensions. Default null.
    #// @param int          $depth         Optional. How deep to search for files. Defaults to a flat scan (0 depth).
    #// -1 depth is infinite.
    #// @param bool         $search_parent Optional. Whether to return parent files. Default false.
    #// @return string[] Array of files, keyed by the path to the file relative to the theme's directory, with the values
    #// being absolute paths.
    #//
    def get_files(self, type_=None, depth_=0, search_parent_=None):
        if type_ is None:
            type_ = None
        # end if
        if search_parent_ is None:
            search_parent_ = False
        # end if
        
        files_ = self.scandir(self.get_stylesheet_directory(), type_, depth_)
        if search_parent_ and self.parent():
            files_ += self.scandir(self.get_template_directory(), type_, depth_)
        # end if
        return files_
    # end def get_files
    #// 
    #// Returns the theme's post templates.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string Array of page templates, keyed by filename and post type,
    #// with the value of the translated header name.
    #//
    def get_post_templates(self):
        
        
        #// If you screw up your current theme and we invalidate your parent, most things still work. Let it slide.
        if self.errors() and self.errors().get_error_codes() != Array("theme_parent_invalid"):
            return Array()
        # end if
        post_templates_ = self.cache_get("post_templates")
        if (not php_is_array(post_templates_)):
            post_templates_ = Array()
            files_ = self.get_files("php", 1, True)
            for file_,full_path_ in files_.items():
                if (not php_preg_match("|Template Name:(.*)$|mi", php_file_get_contents(full_path_), header_)):
                    continue
                # end if
                types_ = Array("page")
                if php_preg_match("|Template Post Type:(.*)$|mi", php_file_get_contents(full_path_), type_):
                    types_ = php_explode(",", _cleanup_header_comment(type_[1]))
                # end if
                for type_ in types_:
                    type_ = sanitize_key(type_)
                    if (not (php_isset(lambda : post_templates_[type_]))):
                        post_templates_[type_] = Array()
                    # end if
                    post_templates_[type_][file_] = _cleanup_header_comment(header_[1])
                # end for
            # end for
            self.cache_add("post_templates", post_templates_)
        # end if
        if self.load_textdomain():
            for post_type_ in post_templates_:
                for post_template_ in post_type_:
                    post_template_ = self.translate_header("Template Name", post_template_)
                # end for
            # end for
        # end if
        return post_templates_
    # end def get_post_templates
    #// 
    #// Returns the theme's post templates for a given post type.
    #// 
    #// @since 3.4.0
    #// @since 4.7.0 Added the `$post_type` parameter.
    #// 
    #// @param WP_Post|null $post      Optional. The post being edited, provided for context.
    #// @param string       $post_type Optional. Post type to get the templates for. Default 'page'.
    #// If a post is provided, its post type is used.
    #// @return string[] Array of template header names keyed by the template file name.
    #//
    def get_page_templates(self, post_=None, post_type_="page"):
        if post_ is None:
            post_ = None
        # end if
        
        if post_:
            post_type_ = get_post_type(post_)
        # end if
        post_templates_ = self.get_post_templates()
        post_templates_ = post_templates_[post_type_] if (php_isset(lambda : post_templates_[post_type_])) else Array()
        #// 
        #// Filters list of page templates for a theme.
        #// 
        #// @since 4.9.6
        #// 
        #// @param string[]     $post_templates Array of template header names keyed by the template file name.
        #// @param WP_Theme     $this           The theme object.
        #// @param WP_Post|null $post           The post being edited, provided for context, or null.
        #// @param string       $post_type      Post type to get the templates for.
        #//
        post_templates_ = apply_filters("theme_templates", post_templates_, self, post_, post_type_)
        #// 
        #// Filters list of page templates for a theme.
        #// 
        #// The dynamic portion of the hook name, `$post_type`, refers to the post type.
        #// 
        #// @since 3.9.0
        #// @since 4.4.0 Converted to allow complete control over the `$page_templates` array.
        #// @since 4.7.0 Added the `$post_type` parameter.
        #// 
        #// @param string[]     $post_templates Array of template header names keyed by the template file name.
        #// @param WP_Theme     $this           The theme object.
        #// @param WP_Post|null $post           The post being edited, provided for context, or null.
        #// @param string       $post_type      Post type to get the templates for.
        #//
        post_templates_ = apply_filters(str("theme_") + str(post_type_) + str("_templates"), post_templates_, self, post_, post_type_)
        return post_templates_
    # end def get_page_templates
    #// 
    #// Scans a directory for files of a certain extension.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string            $path          Absolute path to search.
    #// @param array|string|null $extensions    Optional. Array of extensions to find, string of a single extension,
    #// or null for all extensions. Default null.
    #// @param int               $depth         Optional. How many levels deep to search for files. Accepts 0, 1+, or
    #// -1 (infinite depth). Default 0.
    #// @param string            $relative_path Optional. The basename of the absolute path. Used to control the
    #// returned path for the found files, particularly when this function
    #// recurses to lower depths. Default empty.
    #// @return string[]|false Array of files, keyed by the path to the file relative to the `$path` directory prepended
    #// with `$relative_path`, with the values being absolute paths. False otherwise.
    #//
    def scandir(self, path_=None, extensions_=None, depth_=0, relative_path_=""):
        if extensions_ is None:
            extensions_ = None
        # end if
        
        if (not php_is_dir(path_)):
            return False
        # end if
        if extensions_:
            extensions_ = extensions_
            _extensions_ = php_implode("|", extensions_)
        # end if
        relative_path_ = trailingslashit(relative_path_)
        if "/" == relative_path_:
            relative_path_ = ""
        # end if
        results_ = scandir(path_)
        files_ = Array()
        #// 
        #// Filters the array of excluded directories and files while scanning theme folder.
        #// 
        #// @since 4.7.4
        #// 
        #// @param string[] $exclusions Array of excluded directories and files.
        #//
        exclusions_ = apply_filters("theme_scandir_exclusions", Array("CVS", "node_modules", "vendor", "bower_components"))
        for result_ in results_:
            if "." == result_[0] or php_in_array(result_, exclusions_, True):
                continue
            # end if
            if php_is_dir(path_ + "/" + result_):
                if (not depth_):
                    continue
                # end if
                found_ = self.scandir(path_ + "/" + result_, extensions_, depth_ - 1, relative_path_ + result_)
                files_ = php_array_merge_recursive(files_, found_)
            elif (not extensions_) or php_preg_match("~\\.(" + _extensions_ + ")$~", result_):
                files_[relative_path_ + result_] = path_ + "/" + result_
            # end if
        # end for
        return files_
    # end def scandir
    #// 
    #// Loads the theme's textdomain.
    #// 
    #// Translation files are not inherited from the parent theme. TODO: If this fails for the
    #// child theme, it should probably try to load the parent theme's translations.
    #// 
    #// @since 3.4.0
    #// 
    #// @return bool True if the textdomain was successfully loaded or has already been loaded.
    #// False if no textdomain was specified in the file headers, or if the domain could not be loaded.
    #//
    def load_textdomain(self):
        
        
        if (php_isset(lambda : self.textdomain_loaded)):
            return self.textdomain_loaded
        # end if
        textdomain_ = self.get("TextDomain")
        if (not textdomain_):
            self.textdomain_loaded = False
            return False
        # end if
        if is_textdomain_loaded(textdomain_):
            self.textdomain_loaded = True
            return True
        # end if
        path_ = self.get_stylesheet_directory()
        domainpath_ = self.get("DomainPath")
        if domainpath_:
            path_ += domainpath_
        else:
            path_ += "/languages"
        # end if
        self.textdomain_loaded = load_theme_textdomain(textdomain_, path_)
        return self.textdomain_loaded
    # end def load_textdomain
    #// 
    #// Whether the theme is allowed (multisite only).
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $check Optional. Whether to check only the 'network'-wide settings, the 'site'
    #// settings, or 'both'. Defaults to 'both'.
    #// @param int $blog_id Optional. Ignored if only network-wide settings are checked. Defaults to current site.
    #// @return bool Whether the theme is allowed for the network. Returns true in single-site.
    #//
    def is_allowed(self, check_="both", blog_id_=None):
        if blog_id_ is None:
            blog_id_ = None
        # end if
        
        if (not is_multisite()):
            return True
        # end if
        if "both" == check_ or "network" == check_:
            allowed_ = self.get_allowed_on_network()
            if (not php_empty(lambda : allowed_[self.get_stylesheet()])):
                return True
            # end if
        # end if
        if "both" == check_ or "site" == check_:
            allowed_ = self.get_allowed_on_site(blog_id_)
            if (not php_empty(lambda : allowed_[self.get_stylesheet()])):
                return True
            # end if
        # end if
        return False
    # end def is_allowed
    #// 
    #// Determines the latest WordPress default theme that is installed.
    #// 
    #// This hits the filesystem.
    #// 
    #// @since 4.4.0
    #// 
    #// @return WP_Theme|false Object, or false if no theme is installed, which would be bad.
    #//
    @classmethod
    def get_core_default_theme(self):
        
        
        for slug_,name_ in php_array_reverse(self.default_themes).items():
            theme_ = wp_get_theme(slug_)
            if theme_.exists():
                return theme_
            # end if
        # end for
        return False
    # end def get_core_default_theme
    #// 
    #// Returns array of stylesheet names of themes allowed on the site or network.
    #// 
    #// @since 3.4.0
    #// 
    #// @param int $blog_id Optional. ID of the site. Defaults to the current site.
    #// @return string[] Array of stylesheet names.
    #//
    @classmethod
    def get_allowed(self, blog_id_=None):
        if blog_id_ is None:
            blog_id_ = None
        # end if
        
        #// 
        #// Filters the array of themes allowed on the network.
        #// 
        #// Site is provided as context so that a list of network allowed themes can
        #// be filtered further.
        #// 
        #// @since 4.5.0
        #// 
        #// @param string[] $allowed_themes An array of theme stylesheet names.
        #// @param int      $blog_id        ID of the site.
        #//
        network_ = apply_filters("network_allowed_themes", self.get_allowed_on_network(), blog_id_)
        return network_ + self.get_allowed_on_site(blog_id_)
    # end def get_allowed
    #// 
    #// Returns array of stylesheet names of themes allowed on the network.
    #// 
    #// @since 3.4.0
    #// 
    #// @staticvar array $allowed_themes
    #// 
    #// @return string[] Array of stylesheet names.
    #//
    @classmethod
    def get_allowed_on_network(self):
        
        
        allowed_themes_ = None
        if (not (php_isset(lambda : allowed_themes_))):
            allowed_themes_ = get_site_option("allowedthemes")
        # end if
        #// 
        #// Filters the array of themes allowed on the network.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param string[] $allowed_themes An array of theme stylesheet names.
        #//
        allowed_themes_ = apply_filters("allowed_themes", allowed_themes_)
        return allowed_themes_
    # end def get_allowed_on_network
    #// 
    #// Returns array of stylesheet names of themes allowed on the site.
    #// 
    #// @since 3.4.0
    #// 
    #// @staticvar array $allowed_themes
    #// 
    #// @param int $blog_id Optional. ID of the site. Defaults to the current site.
    #// @return string[] Array of stylesheet names.
    #//
    @classmethod
    def get_allowed_on_site(self, blog_id_=None):
        if blog_id_ is None:
            blog_id_ = None
        # end if
        
        allowed_themes_ = Array()
        if (not blog_id_) or (not is_multisite()):
            blog_id_ = get_current_blog_id()
        # end if
        if (php_isset(lambda : allowed_themes_[blog_id_])):
            #// 
            #// Filters the array of themes allowed on the site.
            #// 
            #// @since 4.5.0
            #// 
            #// @param string[] $allowed_themes An array of theme stylesheet names.
            #// @param int      $blog_id        ID of the site. Defaults to current site.
            #//
            return apply_filters("site_allowed_themes", allowed_themes_[blog_id_], blog_id_)
        # end if
        current_ = get_current_blog_id() == blog_id_
        if current_:
            allowed_themes_[blog_id_] = get_option("allowedthemes")
        else:
            switch_to_blog(blog_id_)
            allowed_themes_[blog_id_] = get_option("allowedthemes")
            restore_current_blog()
        # end if
        #// This is all super old MU back compat joy.
        #// 'allowedthemes' keys things by stylesheet. 'allowed_themes' keyed things by name.
        if False == allowed_themes_[blog_id_]:
            if current_:
                allowed_themes_[blog_id_] = get_option("allowed_themes")
            else:
                switch_to_blog(blog_id_)
                allowed_themes_[blog_id_] = get_option("allowed_themes")
                restore_current_blog()
            # end if
            if (not php_is_array(allowed_themes_[blog_id_])) or php_empty(lambda : allowed_themes_[blog_id_]):
                allowed_themes_[blog_id_] = Array()
            else:
                converted_ = Array()
                themes_ = wp_get_themes()
                for stylesheet_,theme_data_ in themes_.items():
                    if (php_isset(lambda : allowed_themes_[blog_id_][theme_data_.get("Name")])):
                        converted_[stylesheet_] = True
                    # end if
                # end for
                allowed_themes_[blog_id_] = converted_
            # end if
            #// Set the option so we never have to go through this pain again.
            if is_admin() and allowed_themes_[blog_id_]:
                if current_:
                    update_option("allowedthemes", allowed_themes_[blog_id_])
                    delete_option("allowed_themes")
                else:
                    switch_to_blog(blog_id_)
                    update_option("allowedthemes", allowed_themes_[blog_id_])
                    delete_option("allowed_themes")
                    restore_current_blog()
                # end if
            # end if
        # end if
        #// This filter is documented in wp-includes/class-wp-theme.php
        return apply_filters("site_allowed_themes", allowed_themes_[blog_id_], blog_id_)
    # end def get_allowed_on_site
    #// 
    #// Enables a theme for all sites on the current network.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|string[] $stylesheets Stylesheet name or array of stylesheet names.
    #//
    @classmethod
    def network_enable_theme(self, stylesheets_=None):
        
        
        if (not is_multisite()):
            return
        # end if
        if (not php_is_array(stylesheets_)):
            stylesheets_ = Array(stylesheets_)
        # end if
        allowed_themes_ = get_site_option("allowedthemes")
        for stylesheet_ in stylesheets_:
            allowed_themes_[stylesheet_] = True
        # end for
        update_site_option("allowedthemes", allowed_themes_)
    # end def network_enable_theme
    #// 
    #// Disables a theme for all sites on the current network.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|string[] $stylesheets Stylesheet name or array of stylesheet names.
    #//
    @classmethod
    def network_disable_theme(self, stylesheets_=None):
        
        
        if (not is_multisite()):
            return
        # end if
        if (not php_is_array(stylesheets_)):
            stylesheets_ = Array(stylesheets_)
        # end if
        allowed_themes_ = get_site_option("allowedthemes")
        for stylesheet_ in stylesheets_:
            if (php_isset(lambda : allowed_themes_[stylesheet_])):
                allowed_themes_[stylesheet_] = None
            # end if
        # end for
        update_site_option("allowedthemes", allowed_themes_)
    # end def network_disable_theme
    #// 
    #// Sorts themes by name.
    #// 
    #// @since 3.4.0
    #// 
    #// @param WP_Theme[] $themes Array of theme objects to sort (passed by reference).
    #//
    @classmethod
    def sort_by_name(self, themes_=None):
        
        
        if 0 == php_strpos(get_user_locale(), "en_"):
            uasort(themes_, Array("WP_Theme", "_name_sort"))
        else:
            for key_,theme_ in themes_.items():
                theme_.translate_header("Name", theme_.headers["Name"])
            # end for
            uasort(themes_, Array("WP_Theme", "_name_sort_i18n"))
        # end if
    # end def sort_by_name
    #// 
    #// Callback function for usort() to naturally sort themes by name.
    #// 
    #// Accesses the Name header directly from the class for maximum speed.
    #// Would choke on HTML but we don't care enough to slow it down with strip_tags().
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $a First name.
    #// @param string $b Second name.
    #// @return int Negative if `$a` falls lower in the natural order than `$b`. Zero if they fall equally.
    #// Greater than 0 if `$a` falls higher in the natural order than `$b`. Used with usort().
    #//
    def _name_sort(self, a_=None, b_=None):
        
        
        return strnatcasecmp(a_.headers["Name"], b_.headers["Name"])
    # end def _name_sort
    #// 
    #// Callback function for usort() to naturally sort themes by translated name.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $a First name.
    #// @param string $b Second name.
    #// @return int Negative if `$a` falls lower in the natural order than `$b`. Zero if they fall equally.
    #// Greater than 0 if `$a` falls higher in the natural order than `$b`. Used with usort().
    #//
    def _name_sort_i18n(self, a_=None, b_=None):
        
        
        return strnatcasecmp(a_.name_translated, b_.name_translated)
    # end def _name_sort_i18n
# end class WP_Theme
