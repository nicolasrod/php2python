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
#// Facilitates adding of the WordPress editor as used on the Write and Edit screens.
#// 
#// @package WordPress
#// @since 3.3.0
#// 
#// Private, not included by default. See wp_editor() in wp-includes/general-template.php.
#//
class _WP_Editors():
    mce_locale = Array()
    mce_settings = Array()
    qt_settings = Array()
    plugins = Array()
    qt_buttons = Array()
    ext_plugins = Array()
    baseurl = Array()
    first_init = Array()
    this_tinymce = False
    this_quicktags = False
    has_tinymce = False
    has_quicktags = False
    has_medialib = False
    editor_buttons_css = True
    drag_drop_upload = False
    translation = Array()
    tinymce_scripts_printed = False
    link_dialog_printed = False
    def __init__(self):
        
        pass
    # end def __init__
    #// 
    #// Parse default arguments for the editor instance.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $editor_id HTML ID for the textarea and TinyMCE and Quicktags instances.
    #// Should not contain square brackets.
    #// @param array  $settings {
    #// Array of editor arguments.
    #// 
    #// @type bool       $wpautop           Whether to use wpautop(). Default true.
    #// @type bool       $media_buttons     Whether to show the Add Media/other media buttons.
    #// @type string     $default_editor    When both TinyMCE and Quicktags are used, set which
    #// editor is shown on page load. Default empty.
    #// @type bool       $drag_drop_upload  Whether to enable drag & drop on the editor uploading. Default false.
    #// Requires the media modal.
    #// @type string     $textarea_name     Give the textarea a unique name here. Square brackets
    #// can be used here. Default $editor_id.
    #// @type int        $textarea_rows     Number rows in the editor textarea. Default 20.
    #// @type string|int $tabindex          Tabindex value to use. Default empty.
    #// @type string     $tabfocus_elements The previous and next element ID to move the focus to
    #// when pressing the Tab key in TinyMCE. Default ':prev,:next'.
    #// @type string     $editor_css        Intended for extra styles for both Visual and Text editors.
    #// Should include `<style>` tags, and can use "scoped". Default empty.
    #// @type string     $editor_class      Extra classes to add to the editor textarea element. Default empty.
    #// @type bool       $teeny             Whether to output the minimal editor config. Examples include
    #// Press This and the Comment editor. Default false.
    #// @type bool       $dfw               Deprecated in 4.1. Unused.
    #// @type bool|array $tinymce           Whether to load TinyMCE. Can be used to pass settings directly to
    #// TinyMCE using an array. Default true.
    #// @type bool|array $quicktags         Whether to load Quicktags. Can be used to pass settings directly to
    #// Quicktags using an array. Default true.
    #// }
    #// @return array Parsed arguments array.
    #//
    @classmethod
    def parse_settings(self, editor_id=None, settings=None):
        
        #// 
        #// Filters the wp_editor() settings.
        #// 
        #// @since 4.0.0
        #// 
        #// @see _WP_Editors::parse_settings()
        #// 
        #// @param array  $settings  Array of editor arguments.
        #// @param string $editor_id Unique editor identifier, e.g. 'content'. Accepts 'classic-block'
        #// when called from block editor's Classic block.
        #//
        settings = apply_filters("wp_editor_settings", settings, editor_id)
        set = wp_parse_args(settings, Array({"wpautop": (not has_blocks()), "media_buttons": True, "default_editor": "", "drag_drop_upload": False, "textarea_name": editor_id, "textarea_rows": 20, "tabindex": "", "tabfocus_elements": ":prev,:next", "editor_css": "", "editor_class": "", "teeny": False, "_content_editor_dfw": False, "tinymce": True, "quicktags": True}))
        self.this_tinymce = set["tinymce"] and user_can_richedit()
        if self.this_tinymce:
            if False != php_strpos(editor_id, "["):
                self.this_tinymce = False
                _deprecated_argument("wp_editor()", "3.9.0", "TinyMCE editor IDs cannot have brackets.")
            # end if
        # end if
        self.this_quicktags = bool(set["quicktags"])
        if self.this_tinymce:
            self.has_tinymce = True
        # end if
        if self.this_quicktags:
            self.has_quicktags = True
        # end if
        if php_empty(lambda : set["editor_height"]):
            return set
        # end if
        if "content" == editor_id and php_empty(lambda : set["tinymce"]["wp_autoresize_on"]):
            #// A cookie (set when a user resizes the editor) overrides the height.
            cookie = int(get_user_setting("ed_size"))
            if cookie:
                set["editor_height"] = cookie
            # end if
        # end if
        if set["editor_height"] < 50:
            set["editor_height"] = 50
        elif set["editor_height"] > 5000:
            set["editor_height"] = 5000
        # end if
        return set
    # end def parse_settings
    #// 
    #// Outputs the HTML for a single instance of the editor.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $content   Initial content for the editor.
    #// @param string $editor_id HTML ID for the textarea and TinyMCE and Quicktags instances.
    #// Should not contain square brackets.
    #// @param array  $settings  See _WP_Editors::parse_settings() for description.
    #//
    @classmethod
    def editor(self, content=None, editor_id=None, settings=Array()):
        
        set = self.parse_settings(editor_id, settings)
        editor_class = " class=\"" + php_trim(esc_attr(set["editor_class"]) + " wp-editor-area") + "\""
        tabindex = " tabindex=\"" + int(set["tabindex"]) + "\"" if set["tabindex"] else ""
        default_editor = "html"
        buttons = ""
        autocomplete = ""
        editor_id_attr = esc_attr(editor_id)
        if set["drag_drop_upload"]:
            self.drag_drop_upload = True
        # end if
        if (not php_empty(lambda : set["editor_height"])):
            height = " style=\"height: " + int(set["editor_height"]) + "px\""
        else:
            height = " rows=\"" + int(set["textarea_rows"]) + "\""
        # end if
        if (not current_user_can("upload_files")):
            set["media_buttons"] = False
        # end if
        if self.this_tinymce:
            autocomplete = " autocomplete=\"off\""
            if self.this_quicktags:
                default_editor = set["default_editor"] if set["default_editor"] else wp_default_editor()
                #// 'html' is used for the "Text" editor tab.
                if "html" != default_editor:
                    default_editor = "tinymce"
                # end if
                buttons += "<button type=\"button\" id=\"" + editor_id_attr + "-tmce\" class=\"wp-switch-editor switch-tmce\"" + " data-wp-editor-id=\"" + editor_id_attr + "\">" + _x("Visual", "Name for the Visual editor tab") + "</button>\n"
                buttons += "<button type=\"button\" id=\"" + editor_id_attr + "-html\" class=\"wp-switch-editor switch-html\"" + " data-wp-editor-id=\"" + editor_id_attr + "\">" + _x("Text", "Name for the Text editor tab (formerly HTML)") + "</button>\n"
            else:
                default_editor = "tinymce"
            # end if
        # end if
        switch_class = "html-active" if "html" == default_editor else "tmce-active"
        wrap_class = "wp-core-ui wp-editor-wrap " + switch_class
        if set["_content_editor_dfw"]:
            wrap_class += " has-dfw"
        # end if
        php_print("<div id=\"wp-" + editor_id_attr + "-wrap\" class=\"" + wrap_class + "\">")
        if self.editor_buttons_css:
            wp_print_styles("editor-buttons")
            self.editor_buttons_css = False
        # end if
        if (not php_empty(lambda : set["editor_css"])):
            php_print(set["editor_css"] + "\n")
        # end if
        if (not php_empty(lambda : buttons)) or set["media_buttons"]:
            php_print("<div id=\"wp-" + editor_id_attr + "-editor-tools\" class=\"wp-editor-tools hide-if-no-js\">")
            if set["media_buttons"]:
                self.has_medialib = True
                if (not php_function_exists("media_buttons")):
                    php_include_file(ABSPATH + "wp-admin/includes/media.php", once=False)
                # end if
                php_print("<div id=\"wp-" + editor_id_attr + "-media-buttons\" class=\"wp-media-buttons\">")
                #// 
                #// Fires after the default media button(s) are displayed.
                #// 
                #// @since 2.5.0
                #// 
                #// @param string $editor_id Unique editor identifier, e.g. 'content'.
                #//
                do_action("media_buttons", editor_id)
                php_print("</div>\n")
            # end if
            php_print("<div class=\"wp-editor-tabs\">" + buttons + "</div>\n")
            php_print("</div>\n")
        # end if
        quicktags_toolbar = ""
        if self.this_quicktags:
            if "content" == editor_id and (not php_empty(lambda : PHP_GLOBALS["current_screen"])) and "post" == PHP_GLOBALS["current_screen"].base:
                toolbar_id = "ed_toolbar"
            else:
                toolbar_id = "qt_" + editor_id_attr + "_toolbar"
            # end if
            quicktags_toolbar = "<div id=\"" + toolbar_id + "\" class=\"quicktags-toolbar\"></div>"
        # end if
        #// 
        #// Filters the HTML markup output that displays the editor.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $output Editor's HTML markup.
        #//
        the_editor = apply_filters("the_editor", "<div id=\"wp-" + editor_id_attr + "-editor-container\" class=\"wp-editor-container\">" + quicktags_toolbar + "<textarea" + editor_class + height + tabindex + autocomplete + " cols=\"40\" name=\"" + esc_attr(set["textarea_name"]) + "\" " + "id=\"" + editor_id_attr + "\">%s</textarea></div>")
        #// Prepare the content for the Visual or Text editor, only when TinyMCE is used (back-compat).
        if self.this_tinymce:
            add_filter("the_editor_content", "format_for_editor", 10, 2)
        # end if
        #// 
        #// Filters the default editor content.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $content        Default editor content.
        #// @param string $default_editor The default editor for the current user.
        #// Either 'html' or 'tinymce'.
        #//
        content = apply_filters("the_editor_content", content, default_editor)
        #// Remove the filter as the next editor on the same page may not need it.
        if self.this_tinymce:
            remove_filter("the_editor_content", "format_for_editor")
        # end if
        #// Back-compat for the `htmledit_pre` and `richedit_pre` filters.
        if "html" == default_editor and has_filter("htmledit_pre"):
            #// This filter is documented in wp-includes/deprecated.php
            content = apply_filters_deprecated("htmledit_pre", Array(content), "4.3.0", "format_for_editor")
        elif "tinymce" == default_editor and has_filter("richedit_pre"):
            #// This filter is documented in wp-includes/deprecated.php
            content = apply_filters_deprecated("richedit_pre", Array(content), "4.3.0", "format_for_editor")
        # end if
        if False != php_stripos(content, "textarea"):
            content = php_preg_replace("%</textarea%i", "&lt;/textarea", content)
        # end if
        printf(the_editor, content)
        php_print("""
        </div>
        """)
        self.editor_settings(editor_id, set)
    # end def editor
    #// 
    #// @since 3.3.0
    #// 
    #// @global string $tinymce_version
    #// 
    #// @param string $editor_id Unique editor identifier, e.g. 'content'.
    #// @param array  $set       Array of editor arguments.
    #//
    @classmethod
    def editor_settings(self, editor_id=None, set=None):
        
        global tinymce_version
        php_check_if_defined("tinymce_version")
        if php_empty(lambda : self.first_init):
            if is_admin():
                add_action("admin_print_footer_scripts", Array(__CLASS__, "editor_js"), 50)
                add_action("admin_print_footer_scripts", Array(__CLASS__, "force_uncompressed_tinymce"), 1)
                add_action("admin_print_footer_scripts", Array(__CLASS__, "enqueue_scripts"), 1)
            else:
                add_action("wp_print_footer_scripts", Array(__CLASS__, "editor_js"), 50)
                add_action("wp_print_footer_scripts", Array(__CLASS__, "force_uncompressed_tinymce"), 1)
                add_action("wp_print_footer_scripts", Array(__CLASS__, "enqueue_scripts"), 1)
            # end if
        # end if
        if self.this_quicktags:
            qtInit = Array({"id": editor_id, "buttons": ""})
            if php_is_array(set["quicktags"]):
                qtInit = php_array_merge(qtInit, set["quicktags"])
            # end if
            if php_empty(lambda : qtInit["buttons"]):
                qtInit["buttons"] = "strong,em,link,block,del,ins,img,ul,ol,li,code,more,close"
            # end if
            if set["_content_editor_dfw"]:
                qtInit["buttons"] += ",dfw"
            # end if
            #// 
            #// Filters the Quicktags settings.
            #// 
            #// @since 3.3.0
            #// 
            #// @param array  $qtInit    Quicktags settings.
            #// @param string $editor_id Unique editor identifier, e.g. 'content'.
            #//
            qtInit = apply_filters("quicktags_settings", qtInit, editor_id)
            self.qt_settings[editor_id] = qtInit
            self.qt_buttons = php_array_merge(self.qt_buttons, php_explode(",", qtInit["buttons"]))
        # end if
        if self.this_tinymce:
            if php_empty(lambda : self.first_init):
                baseurl = self.get_baseurl()
                mce_locale = self.get_mce_locale()
                ext_plugins = ""
                if set["teeny"]:
                    #// 
                    #// Filters the list of teenyMCE plugins.
                    #// 
                    #// @since 2.7.0
                    #// @since 3.3.0 The `$editor_id` parameter was added.
                    #// 
                    #// @param array  $plugins   An array of teenyMCE plugins.
                    #// @param string $editor_id Unique editor identifier, e.g. 'content'.
                    #//
                    plugins = apply_filters("teeny_mce_plugins", Array("colorpicker", "lists", "fullscreen", "image", "wordpress", "wpeditimage", "wplink"), editor_id)
                else:
                    #// 
                    #// Filters the list of TinyMCE external plugins.
                    #// 
                    #// The filter takes an associative array of external plugins for
                    #// TinyMCE in the form 'plugin_name' => 'url'.
                    #// 
                    #// The url should be absolute, and should include the js filename
                    #// to be loaded. For example:
                    #// 'myplugin' => 'http://mysite.com/wp-content/plugins/myfolder/mce_plugin.js'.
                    #// 
                    #// If the external plugin adds a button, it should be added with
                    #// one of the 'mce_buttons' filters.
                    #// 
                    #// @since 2.5.0
                    #// @since 5.3.0 The `$editor_id` parameter was added.
                    #// 
                    #// @param array  $external_plugins An array of external TinyMCE plugins.
                    #// @param string $editor_id        Unique editor identifier, e.g. 'content'. Accepts 'classic-block'
                    #// when called from block editor's Classic block.
                    #//
                    mce_external_plugins = apply_filters("mce_external_plugins", Array(), editor_id)
                    plugins = Array("charmap", "colorpicker", "hr", "lists", "media", "paste", "tabfocus", "textcolor", "fullscreen", "wordpress", "wpautoresize", "wpeditimage", "wpemoji", "wpgallery", "wplink", "wpdialogs", "wptextpattern", "wpview")
                    if (not self.has_medialib):
                        plugins[-1] = "image"
                    # end if
                    #// 
                    #// Filters the list of default TinyMCE plugins.
                    #// 
                    #// The filter specifies which of the default plugins included
                    #// in WordPress should be added to the TinyMCE instance.
                    #// 
                    #// @since 3.3.0
                    #// @since 5.3.0 The `$editor_id` parameter was added.
                    #// 
                    #// @param array  $plugins   An array of default TinyMCE plugins.
                    #// @param string $editor_id Unique editor identifier, e.g. 'content'. Accepts 'classic-block'
                    #// when called from block editor's Classic block.
                    #//
                    plugins = array_unique(apply_filters("tiny_mce_plugins", plugins, editor_id))
                    key = php_array_search("spellchecker", plugins)
                    if False != key:
                        plugins[key] = None
                    # end if
                    if (not php_empty(lambda : mce_external_plugins)):
                        #// 
                        #// Filters the translations loaded for external TinyMCE 3.x plugins.
                        #// 
                        #// The filter takes an associative array ('plugin_name' => 'path')
                        #// where 'path' is the include path to the file.
                        #// 
                        #// The language file should follow the same format as wp_mce_translation(),
                        #// and should define a variable ($strings) that holds all translated strings.
                        #// 
                        #// @since 2.5.0
                        #// @since 5.3.0 The `$editor_id` parameter was added.
                        #// 
                        #// @param array  $translations Translations for external TinyMCE plugins.
                        #// @param string $editor_id    Unique editor identifier, e.g. 'content'.
                        #//
                        mce_external_languages = apply_filters("mce_external_languages", Array(), editor_id)
                        loaded_langs = Array()
                        strings = ""
                        if (not php_empty(lambda : mce_external_languages)):
                            for name,path in mce_external_languages:
                                if php_no_error(lambda: php_is_file(path)) and php_no_error(lambda: php_is_readable(path)):
                                    php_include_file(path, once=False)
                                    ext_plugins += strings + "\n"
                                    loaded_langs[-1] = name
                                # end if
                            # end for
                        # end if
                        for name,url in mce_external_plugins:
                            if php_in_array(name, plugins, True):
                                mce_external_plugins[name] = None
                                continue
                            # end if
                            url = set_url_scheme(url)
                            mce_external_plugins[name] = url
                            plugurl = php_dirname(url)
                            strings = ""
                            #// Try to load langs/[locale].js and langs/[locale]_dlg.js.
                            if (not php_in_array(name, loaded_langs, True)):
                                path = php_str_replace(content_url(), "", plugurl)
                                path = WP_CONTENT_DIR + path + "/langs/"
                                path = trailingslashit(php_realpath(path))
                                if php_no_error(lambda: php_is_file(path + mce_locale + ".js")):
                                    strings += php_no_error(lambda: php_file_get_contents(path + mce_locale + ".js")) + "\n"
                                # end if
                                if php_no_error(lambda: php_is_file(path + mce_locale + "_dlg.js")):
                                    strings += php_no_error(lambda: php_file_get_contents(path + mce_locale + "_dlg.js")) + "\n"
                                # end if
                                if "en" != mce_locale and php_empty(lambda : strings):
                                    if php_no_error(lambda: php_is_file(path + "en.js")):
                                        str1 = php_no_error(lambda: php_file_get_contents(path + "en.js"))
                                        strings += php_preg_replace("/(['\"])en\\./", "$1" + mce_locale + ".", str1, 1) + "\n"
                                    # end if
                                    if php_no_error(lambda: php_is_file(path + "en_dlg.js")):
                                        str2 = php_no_error(lambda: php_file_get_contents(path + "en_dlg.js"))
                                        strings += php_preg_replace("/(['\"])en\\./", "$1" + mce_locale + ".", str2, 1) + "\n"
                                    # end if
                                # end if
                                if (not php_empty(lambda : strings)):
                                    ext_plugins += "\n" + strings + "\n"
                                # end if
                            # end if
                            ext_plugins += "tinyMCEPreInit.load_ext(\"" + plugurl + "\", \"" + mce_locale + "\");" + "\n"
                        # end for
                    # end if
                # end if
                self.plugins = plugins
                self.ext_plugins = ext_plugins
                settings = self.default_settings()
                settings["plugins"] = php_implode(",", plugins)
                if (not php_empty(lambda : mce_external_plugins)):
                    settings["external_plugins"] = wp_json_encode(mce_external_plugins)
                # end if
                #// This filter is documented in wp-admin/includes/media.php
                if apply_filters("disable_captions", ""):
                    settings["wpeditimage_disable_captions"] = True
                # end if
                mce_css = settings["content_css"]
                #// 
                #// The `editor-style.css` added by the theme is generally intended for the editor instance on the Edit Post screen.
                #// Plugins that use wp_editor() on the front-end can decide whether to add the theme stylesheet
                #// by using `get_editor_stylesheets()` and the `mce_css` or `tiny_mce_before_init` filters, see below.
                #//
                if is_admin():
                    editor_styles = get_editor_stylesheets()
                    if (not php_empty(lambda : editor_styles)):
                        #// Force urlencoding of commas.
                        for key,url in editor_styles:
                            if php_strpos(url, ",") != False:
                                editor_styles[key] = php_str_replace(",", "%2C", url)
                            # end if
                        # end for
                        mce_css += "," + php_implode(",", editor_styles)
                    # end if
                # end if
                #// 
                #// Filters the comma-delimited list of stylesheets to load in TinyMCE.
                #// 
                #// @since 2.1.0
                #// 
                #// @param string $stylesheets Comma-delimited list of stylesheets.
                #//
                mce_css = php_trim(apply_filters("mce_css", mce_css), " ,")
                if (not php_empty(lambda : mce_css)):
                    settings["content_css"] = mce_css
                else:
                    settings["content_css"] = None
                # end if
                self.first_init = settings
            # end if
            if set["teeny"]:
                mce_buttons = Array("bold", "italic", "underline", "blockquote", "strikethrough", "bullist", "numlist", "alignleft", "aligncenter", "alignright", "undo", "redo", "link", "fullscreen")
                #// 
                #// Filters the list of teenyMCE buttons (Text tab).
                #// 
                #// @since 2.7.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mce_buttons An array of teenyMCE buttons.
                #// @param string $editor_id   Unique editor identifier, e.g. 'content'.
                #//
                mce_buttons = apply_filters("teeny_mce_buttons", mce_buttons, editor_id)
                mce_buttons_2 = Array()
                mce_buttons_3 = Array()
                mce_buttons_4 = Array()
            else:
                mce_buttons = Array("formatselect", "bold", "italic", "bullist", "numlist", "blockquote", "alignleft", "aligncenter", "alignright", "link", "wp_more", "spellchecker")
                if (not wp_is_mobile()):
                    if set["_content_editor_dfw"]:
                        mce_buttons[-1] = "wp_adv"
                        mce_buttons[-1] = "dfw"
                    else:
                        mce_buttons[-1] = "fullscreen"
                        mce_buttons[-1] = "wp_adv"
                    # end if
                else:
                    mce_buttons[-1] = "wp_adv"
                # end if
                #// 
                #// Filters the first-row list of TinyMCE buttons (Visual tab).
                #// 
                #// @since 2.0.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mce_buttons First-row list of buttons.
                #// @param string $editor_id   Unique editor identifier, e.g. 'content'. Accepts 'classic-block'
                #// when called from block editor's Classic block.
                #//
                mce_buttons = apply_filters("mce_buttons", mce_buttons, editor_id)
                mce_buttons_2 = Array("strikethrough", "hr", "forecolor", "pastetext", "removeformat", "charmap", "outdent", "indent", "undo", "redo")
                if (not wp_is_mobile()):
                    mce_buttons_2[-1] = "wp_help"
                # end if
                #// 
                #// Filters the second-row list of TinyMCE buttons (Visual tab).
                #// 
                #// @since 2.0.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mce_buttons_2 Second-row list of buttons.
                #// @param string $editor_id     Unique editor identifier, e.g. 'content'. Accepts 'classic-block'
                #// when called from block editor's Classic block.
                #//
                mce_buttons_2 = apply_filters("mce_buttons_2", mce_buttons_2, editor_id)
                #// 
                #// Filters the third-row list of TinyMCE buttons (Visual tab).
                #// 
                #// @since 2.0.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mce_buttons_3 Third-row list of buttons.
                #// @param string $editor_id     Unique editor identifier, e.g. 'content'. Accepts 'classic-block'
                #// when called from block editor's Classic block.
                #//
                mce_buttons_3 = apply_filters("mce_buttons_3", Array(), editor_id)
                #// 
                #// Filters the fourth-row list of TinyMCE buttons (Visual tab).
                #// 
                #// @since 2.5.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mce_buttons_4 Fourth-row list of buttons.
                #// @param string $editor_id     Unique editor identifier, e.g. 'content'. Accepts 'classic-block'
                #// when called from block editor's Classic block.
                #//
                mce_buttons_4 = apply_filters("mce_buttons_4", Array(), editor_id)
            # end if
            body_class = editor_id
            post = get_post()
            if post:
                body_class += " post-type-" + sanitize_html_class(post.post_type) + " post-status-" + sanitize_html_class(post.post_status)
                if post_type_supports(post.post_type, "post-formats"):
                    post_format = get_post_format(post)
                    if post_format and (not is_wp_error(post_format)):
                        body_class += " post-format-" + sanitize_html_class(post_format)
                    else:
                        body_class += " post-format-standard"
                    # end if
                # end if
                page_template = get_page_template_slug(post)
                if False != page_template:
                    page_template = "default" if php_empty(lambda : page_template) else php_str_replace(".", "-", php_basename(page_template, ".php"))
                    body_class += " page-template-" + sanitize_html_class(page_template)
                # end if
            # end if
            body_class += " locale-" + sanitize_html_class(php_strtolower(php_str_replace("_", "-", get_user_locale())))
            if (not php_empty(lambda : set["tinymce"]["body_class"])):
                body_class += " " + set["tinymce"]["body_class"]
                set["tinymce"]["body_class"] = None
            # end if
            mceInit = Array({"selector": str("#") + str(editor_id), "wpautop": bool(set["wpautop"]), "indent": (not set["wpautop"]), "toolbar1": php_implode(",", mce_buttons), "toolbar2": php_implode(",", mce_buttons_2), "toolbar3": php_implode(",", mce_buttons_3), "toolbar4": php_implode(",", mce_buttons_4), "tabfocus_elements": set["tabfocus_elements"], "body_class": body_class})
            #// Merge with the first part of the init array.
            mceInit = php_array_merge(self.first_init, mceInit)
            if php_is_array(set["tinymce"]):
                mceInit = php_array_merge(mceInit, set["tinymce"])
            # end if
            #// 
            #// For people who really REALLY know what they're doing with TinyMCE
            #// You can modify $mceInit to add, remove, change elements of the config
            #// before tinyMCE.init. Setting "valid_elements", "invalid_elements"
            #// and "extended_valid_elements" can be done through this filter. Best
            #// is to use the default cleanup by not specifying valid_elements,
            #// as TinyMCE checks against the full set of HTML 5.0 elements and attributes.
            #//
            if set["teeny"]:
                #// 
                #// Filters the teenyMCE config before init.
                #// 
                #// @since 2.7.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mceInit   An array with teenyMCE config.
                #// @param string $editor_id Unique editor identifier, e.g. 'content'.
                #//
                mceInit = apply_filters("teeny_mce_before_init", mceInit, editor_id)
            else:
                #// 
                #// Filters the TinyMCE config before init.
                #// 
                #// @since 2.5.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mceInit   An array with TinyMCE config.
                #// @param string $editor_id Unique editor identifier, e.g. 'content'. Accepts 'classic-block'
                #// when called from block editor's Classic block.
                #//
                mceInit = apply_filters("tiny_mce_before_init", mceInit, editor_id)
            # end if
            if php_empty(lambda : mceInit["toolbar3"]) and (not php_empty(lambda : mceInit["toolbar4"])):
                mceInit["toolbar3"] = mceInit["toolbar4"]
                mceInit["toolbar4"] = ""
            # end if
            self.mce_settings[editor_id] = mceInit
        # end if
        pass
    # end def editor_settings
    #// 
    #// @since 3.3.0
    #// 
    #// @param array $init
    #// @return string
    #//
    def _parse_init(self, init=None):
        
        options = ""
        for key,value in init:
            if php_is_bool(value):
                val = "true" if value else "false"
                options += key + ":" + val + ","
                continue
            elif (not php_empty(lambda : value)) and php_is_string(value) and "{" == value[0] and "}" == value[php_strlen(value) - 1] or "[" == value[0] and "]" == value[php_strlen(value) - 1] or php_preg_match("/^\\(?function ?\\(/", value):
                options += key + ":" + value + ","
                continue
            # end if
            options += key + ":\"" + value + "\","
        # end for
        return "{" + php_trim(options, " ,") + "}"
    # end def _parse_init
    #// 
    #// @since 3.3.0
    #// 
    #// @param bool $default_scripts Optional. Whether default scripts should be enqueued. Default false.
    #//
    @classmethod
    def enqueue_scripts(self, default_scripts=False):
        
        if default_scripts or self.has_tinymce:
            wp_enqueue_script("editor")
        # end if
        if default_scripts or self.has_quicktags:
            wp_enqueue_script("quicktags")
            wp_enqueue_style("buttons")
        # end if
        if default_scripts or php_in_array("wplink", self.plugins, True) or php_in_array("link", self.qt_buttons, True):
            wp_enqueue_script("wplink")
            wp_enqueue_script("jquery-ui-autocomplete")
        # end if
        if self.has_medialib:
            add_thickbox()
            wp_enqueue_script("media-upload")
            wp_enqueue_script("wp-embed")
        elif default_scripts:
            wp_enqueue_script("media-upload")
        # end if
        #// 
        #// Fires when scripts and styles are enqueued for the editor.
        #// 
        #// @since 3.9.0
        #// 
        #// @param array $to_load An array containing boolean values whether TinyMCE
        #// and Quicktags are being loaded.
        #//
        do_action("wp_enqueue_editor", Array({"tinymce": default_scripts or self.has_tinymce, "quicktags": default_scripts or self.has_quicktags}))
    # end def enqueue_scripts
    #// 
    #// Enqueue all editor scripts.
    #// For use when the editor is going to be initialized after page load.
    #// 
    #// @since 4.8.0
    #//
    @classmethod
    def enqueue_default_editor(self):
        
        #// We are past the point where scripts can be enqueued properly.
        if did_action("wp_enqueue_editor"):
            return
        # end if
        self.enqueue_scripts(True)
        #// Also add wp-includes/css/editor.css.
        wp_enqueue_style("editor-buttons")
        if is_admin():
            add_action("admin_print_footer_scripts", Array(__CLASS__, "force_uncompressed_tinymce"), 1)
            add_action("admin_print_footer_scripts", Array(__CLASS__, "print_default_editor_scripts"), 45)
        else:
            add_action("wp_print_footer_scripts", Array(__CLASS__, "force_uncompressed_tinymce"), 1)
            add_action("wp_print_footer_scripts", Array(__CLASS__, "print_default_editor_scripts"), 45)
        # end if
    # end def enqueue_default_editor
    #// 
    #// Print (output) all editor scripts and default settings.
    #// For use when the editor is going to be initialized after page load.
    #// 
    #// @since 4.8.0
    #//
    @classmethod
    def print_default_editor_scripts(self):
        
        user_can_richedit = user_can_richedit()
        if user_can_richedit:
            settings = self.default_settings()
            settings["toolbar1"] = "bold,italic,bullist,numlist,link"
            settings["wpautop"] = False
            settings["indent"] = True
            settings["elementpath"] = False
            if is_rtl():
                settings["directionality"] = "rtl"
            # end if
            #// 
            #// In production all plugins are loaded (they are in wp-editor.js.gz).
            #// The 'wpview', 'wpdialogs', and 'media' TinyMCE plugins are not initialized by default.
            #// Can be added from js by using the 'wp-before-tinymce-init' event.
            #//
            settings["plugins"] = php_implode(",", Array("charmap", "colorpicker", "hr", "lists", "paste", "tabfocus", "textcolor", "fullscreen", "wordpress", "wpautoresize", "wpeditimage", "wpemoji", "wpgallery", "wplink", "wptextpattern"))
            settings = self._parse_init(settings)
        else:
            settings = "{}"
        # end if
        php_print("""       <script type=\"text/javascript\">
        window.wp = window.wp || {};
        window.wp.editor = window.wp.editor || {};
        window.wp.editor.getDefaultSettings = function() {
        return {
        tinymce: """)
        php_print(settings)
        php_print(""",
        quicktags: {
        buttons: 'strong,em,link,ul,ol,li,code'
        }
        };
        };
        """)
        if user_can_richedit:
            suffix = "" if SCRIPT_DEBUG else ".min"
            baseurl = self.get_baseurl()
            php_print("         var tinyMCEPreInit = {\n                baseURL: \"")
            php_print(baseurl)
            php_print("\",\n                suffix: \"")
            php_print(suffix)
            php_print("""\",
            mceInit: {},
            qtInit: {},
            load_ext: function(url,lang){var sl=tinymce.ScriptLoader;sl.markDone(url+'/langs/'+lang+'.js');sl.markDone(url+'/langs/'+lang+'_dlg.js');}
            };
            """)
        # end if
        php_print("     </script>\n     ")
        if user_can_richedit:
            self.print_tinymce_scripts()
        # end if
        #// 
        #// Fires when the editor scripts are loaded for later initialization,
        #// after all scripts and settings are printed.
        #// 
        #// @since 4.8.0
        #//
        do_action("print_default_editor_scripts")
        self.wp_link_dialog()
    # end def print_default_editor_scripts
    #// 
    #// Returns the TinyMCE locale.
    #// 
    #// @since 4.8.0
    #// 
    #// @return string
    #//
    @classmethod
    def get_mce_locale(self):
        
        if php_empty(lambda : self.mce_locale):
            mce_locale = get_user_locale()
            self.mce_locale = "en" if php_empty(lambda : mce_locale) else php_strtolower(php_substr(mce_locale, 0, 2))
            pass
        # end if
        return self.mce_locale
    # end def get_mce_locale
    #// 
    #// Returns the TinyMCE base URL.
    #// 
    #// @since 4.8.0
    #// 
    #// @return string
    #//
    @classmethod
    def get_baseurl(self):
        
        if php_empty(lambda : self.baseurl):
            self.baseurl = includes_url("js/tinymce")
        # end if
        return self.baseurl
    # end def get_baseurl
    #// 
    #// Returns the default TinyMCE settings.
    #// Doesn't include plugins, buttons, editor selector.
    #// 
    #// @since 4.8.0
    #// 
    #// @global string $tinymce_version
    #// 
    #// @return array
    #//
    def default_settings(self):
        
        global tinymce_version
        php_check_if_defined("tinymce_version")
        shortcut_labels = Array()
        for name,value in self.get_translation():
            if php_is_array(value):
                shortcut_labels[name] = value[1]
            # end if
        # end for
        settings = Array({"theme": "modern", "skin": "lightgray", "language": self.get_mce_locale(), "formats": "{" + "alignleft: [" + "{selector: \"p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li\", styles: {textAlign:\"left\"}}," + "{selector: \"img,table,dl.wp-caption\", classes: \"alignleft\"}" + "]," + "aligncenter: [" + "{selector: \"p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li\", styles: {textAlign:\"center\"}}," + "{selector: \"img,table,dl.wp-caption\", classes: \"aligncenter\"}" + "]," + "alignright: [" + "{selector: \"p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li\", styles: {textAlign:\"right\"}}," + "{selector: \"img,table,dl.wp-caption\", classes: \"alignright\"}" + "]," + "strikethrough: {inline: \"del\"}" + "}"}, {"relative_urls": False, "remove_script_host": False, "convert_urls": False, "browser_spellcheck": True, "fix_list_elements": True, "entities": "38,amp,60,lt,62,gt", "entity_encoding": "raw", "keep_styles": False, "cache_suffix": "wp-mce-" + tinymce_version, "resize": "vertical", "menubar": False, "branding": False, "preview_styles": "font-family font-size font-weight font-style text-decoration text-transform", "end_container_on_empty_block": True, "wpeditimage_html5_captions": True, "wp_lang_attr": get_bloginfo("language"), "wp_keep_scroll_position": False, "wp_shortcut_labels": wp_json_encode(shortcut_labels)})
        suffix = "" if SCRIPT_DEBUG else ".min"
        version = "ver=" + get_bloginfo("version")
        #// Default stylesheets.
        settings["content_css"] = includes_url(str("css/dashicons") + str(suffix) + str(".css?") + str(version)) + "," + includes_url(str("js/tinymce/skins/wordpress/wp-content.css?") + str(version))
        return settings
    # end def default_settings
    #// 
    #// @since 4.7.0
    #// 
    #// @return array
    #//
    def get_translation(self):
        
        if php_empty(lambda : self.translation):
            self.translation = Array({"New document": __("New document"), "Formats": _x("Formats", "TinyMCE"), "Headings": _x("Headings", "TinyMCE"), "Heading 1": Array(__("Heading 1"), "access1"), "Heading 2": Array(__("Heading 2"), "access2"), "Heading 3": Array(__("Heading 3"), "access3"), "Heading 4": Array(__("Heading 4"), "access4"), "Heading 5": Array(__("Heading 5"), "access5"), "Heading 6": Array(__("Heading 6"), "access6"), "Blocks": _x("Blocks", "TinyMCE"), "Paragraph": Array(__("Paragraph"), "access7"), "Blockquote": Array(__("Blockquote"), "accessQ"), "Div": _x("Div", "HTML tag"), "Pre": _x("Pre", "HTML tag"), "Preformatted": _x("Preformatted", "HTML tag"), "Address": _x("Address", "HTML tag"), "Inline": _x("Inline", "HTML elements"), "Underline": Array(__("Underline"), "metaU"), "Strikethrough": Array(__("Strikethrough"), "accessD"), "Subscript": __("Subscript"), "Superscript": __("Superscript"), "Clear formatting": __("Clear formatting"), "Bold": Array(__("Bold"), "metaB"), "Italic": Array(__("Italic"), "metaI"), "Code": Array(__("Code"), "accessX"), "Source code": __("Source code"), "Font Family": __("Font Family"), "Font Sizes": __("Font Sizes"), "Align center": Array(__("Align center"), "accessC"), "Align right": Array(__("Align right"), "accessR"), "Align left": Array(__("Align left"), "accessL"), "Justify": Array(__("Justify"), "accessJ"), "Increase indent": __("Increase indent"), "Decrease indent": __("Decrease indent"), "Cut": Array(__("Cut"), "metaX"), "Copy": Array(__("Copy"), "metaC"), "Paste": Array(__("Paste"), "metaV"), "Select all": Array(__("Select all"), "metaA"), "Undo": Array(__("Undo"), "metaZ"), "Redo": Array(__("Redo"), "metaY"), "Ok": __("OK"), "Cancel": __("Cancel"), "Close": __("Close"), "Visual aids": __("Visual aids"), "Bullet list": Array(__("Bulleted list"), "accessU"), "Numbered list": Array(__("Numbered list"), "accessO"), "Square": _x("Square", "list style"), "Default": _x("Default", "list style"), "Circle": _x("Circle", "list style"), "Disc": _x("Disc", "list style"), "Lower Greek": _x("Lower Greek", "list style"), "Lower Alpha": _x("Lower Alpha", "list style"), "Upper Alpha": _x("Upper Alpha", "list style"), "Upper Roman": _x("Upper Roman", "list style"), "Lower Roman": _x("Lower Roman", "list style"), "Name": _x("Name", "Name of link anchor (TinyMCE)"), "Anchor": _x("Anchor", "Link anchor (TinyMCE)"), "Anchors": _x("Anchors", "Link anchors (TinyMCE)"), "Id should start with a letter, followed only by letters, numbers, dashes, dots, colons or underscores.": __("Id should start with a letter, followed only by letters, numbers, dashes, dots, colons or underscores."), "Id": _x("Id", "Id for link anchor (TinyMCE)"), "Document properties": __("Document properties"), "Robots": __("Robots"), "Title": __("Title"), "Keywords": __("Keywords"), "Encoding": __("Encoding"), "Description": __("Description"), "Author": __("Author"), "Image": __("Image"), "Insert/edit image": Array(__("Insert/edit image"), "accessM"), "General": __("General"), "Advanced": __("Advanced"), "Source": __("Source"), "Border": __("Border"), "Constrain proportions": __("Constrain proportions"), "Vertical space": __("Vertical space"), "Image description": __("Image description"), "Style": __("Style"), "Dimensions": __("Dimensions"), "Insert image": __("Insert image"), "Date/time": __("Date/time"), "Insert date/time": __("Insert date/time"), "Table of Contents": __("Table of Contents"), "Insert/Edit code sample": __("Insert/edit code sample"), "Language": __("Language"), "Media": __("Media"), "Insert/edit media": __("Insert/edit media"), "Poster": __("Poster"), "Alternative source": __("Alternative source"), "Paste your embed code below:": __("Paste your embed code below:"), "Insert video": __("Insert video"), "Embed": __("Embed"), "Special character": __("Special character"), "Right to left": _x("Right to left", "editor button"), "Left to right": _x("Left to right", "editor button"), "Emoticons": __("Emoticons"), "Nonbreaking space": __("Nonbreaking space"), "Page break": __("Page break"), "Paste as text": __("Paste as text"), "Preview": __("Preview"), "Print": __("Print"), "Save": __("Save"), "Fullscreen": __("Fullscreen"), "Horizontal line": __("Horizontal line"), "Horizontal space": __("Horizontal space"), "Restore last draft": __("Restore last draft"), "Insert/edit link": Array(__("Insert/edit link"), "metaK"), "Remove link": Array(__("Remove link"), "accessS"), "Link": __("Link"), "Insert link": __("Insert link"), "Target": __("Target"), "New window": __("New window"), "Text to display": __("Text to display"), "Url": __("URL"), "The URL you entered seems to be an email address. Do you want to add the required mailto: prefix?": __("The URL you entered seems to be an email address. Do you want to add the required mailto: prefix?"), "The URL you entered seems to be an external link. Do you want to add the required http:// prefix?": __("The URL you entered seems to be an external link. Do you want to add the required http:// prefix?"), "Color": __("Color"), "Custom color": __("Custom color"), "Custom...": _x("Custom...", "label for custom color"), "No color": __("No color"), "R": _x("R", "Short for red in RGB"), "G": _x("G", "Short for green in RGB"), "B": _x("B", "Short for blue in RGB"), "Could not find the specified string.": __("Could not find the specified string."), "Replace": _x("Replace", "find/replace"), "Next": _x("Next", "find/replace"), "Prev": _x("Prev", "find/replace"), "Whole words": _x("Whole words", "find/replace"), "Find and replace": __("Find and replace"), "Replace with": _x("Replace with", "find/replace"), "Find": _x("Find", "find/replace"), "Replace all": _x("Replace all", "find/replace"), "Match case": __("Match case"), "Spellcheck": __("Check Spelling"), "Finish": _x("Finish", "spellcheck"), "Ignore all": _x("Ignore all", "spellcheck"), "Ignore": _x("Ignore", "spellcheck"), "Add to Dictionary": __("Add to Dictionary"), "Insert table": __("Insert table"), "Delete table": __("Delete table"), "Table properties": __("Table properties"), "Row properties": __("Table row properties"), "Cell properties": __("Table cell properties"), "Border color": __("Border color"), "Row": __("Row"), "Rows": __("Rows"), "Column": _x("Column", "table column"), "Cols": _x("Cols", "table columns"), "Cell": _x("Cell", "table cell"), "Header cell": __("Header cell"), "Header": _x("Header", "table header"), "Body": _x("Body", "table body"), "Footer": _x("Footer", "table footer"), "Insert row before": __("Insert row before"), "Insert row after": __("Insert row after"), "Insert column before": __("Insert column before"), "Insert column after": __("Insert column after"), "Paste row before": __("Paste table row before"), "Paste row after": __("Paste table row after"), "Delete row": __("Delete row"), "Delete column": __("Delete column"), "Cut row": __("Cut table row"), "Copy row": __("Copy table row"), "Merge cells": __("Merge table cells"), "Split cell": __("Split table cell"), "Height": __("Height"), "Width": __("Width"), "Caption": __("Caption"), "Alignment": __("Alignment"), "H Align": _x("H Align", "horizontal table cell alignment"), "Left": __("Left"), "Center": __("Center"), "Right": __("Right"), "None": _x("None", "table cell alignment attribute"), "V Align": _x("V Align", "vertical table cell alignment"), "Top": __("Top"), "Middle": __("Middle"), "Bottom": __("Bottom"), "Row group": __("Row group"), "Column group": __("Column group"), "Row type": __("Row type"), "Cell type": __("Cell type"), "Cell padding": __("Cell padding"), "Cell spacing": __("Cell spacing"), "Scope": _x("Scope", "table cell scope attribute"), "Insert template": _x("Insert template", "TinyMCE"), "Templates": _x("Templates", "TinyMCE"), "Background color": __("Background color"), "Text color": __("Text color"), "Show blocks": _x("Show blocks", "editor button"), "Show invisible characters": __("Show invisible characters"), "Words: {0}": php_sprintf(__("Words: %s"), "{0}")}, {"Paste is now in plain text mode. Contents will now be pasted as plain text until you toggle this option off.": __("Paste is now in plain text mode. Contents will now be pasted as plain text until you toggle this option off.") + "\n\n" + __("If you&#8217;re looking to paste rich content from Microsoft Word, try turning this option off. The editor will clean up text pasted from Word automatically."), "Rich Text Area. Press ALT-F9 for menu. Press ALT-F10 for toolbar. Press ALT-0 for help": __("Rich Text Area. Press Alt-Shift-H for help."), "Rich Text Area. Press Control-Option-H for help.": __("Rich Text Area. Press Control-Option-H for help."), "You have unsaved changes are you sure you want to navigate away?": __("The changes you made will be lost if you navigate away from this page."), "Your browser doesn't support direct access to the clipboard. Please use the Ctrl+X/C/V keyboard shortcuts instead.": __("Your browser does not support direct access to the clipboard. Please use keyboard shortcuts or your browser&#8217;s edit menu instead."), "Insert": _x("Insert", "TinyMCE menu"), "File": _x("File", "TinyMCE menu"), "Edit": _x("Edit", "TinyMCE menu"), "Tools": _x("Tools", "TinyMCE menu"), "View": _x("View", "TinyMCE menu"), "Table": _x("Table", "TinyMCE menu"), "Format": _x("Format", "TinyMCE menu"), "Toolbar Toggle": Array(__("Toolbar Toggle"), "accessZ"), "Insert Read More tag": Array(__("Insert Read More tag"), "accessT"), "Insert Page Break tag": Array(__("Insert Page Break tag"), "accessP"), "Read more...": __("Read more..."), "Distraction-free writing mode": Array(__("Distraction-free writing mode"), "accessW"), "No alignment": __("No alignment"), "Remove": __("Remove"), "Edit|button": __("Edit"), "Paste URL or type to search": __("Paste URL or type to search"), "Apply": __("Apply"), "Link options": __("Link options"), "Visual": _x("Visual", "Name for the Visual editor tab"), "Text": _x("Text", "Name for the Text editor tab (formerly HTML)"), "Add Media": Array(__("Add Media"), "accessM"), "Keyboard Shortcuts": Array(__("Keyboard Shortcuts"), "accessH"), "Classic Block Keyboard Shortcuts": __("Classic Block Keyboard Shortcuts"), "Default shortcuts,": __("Default shortcuts,"), "Additional shortcuts,": __("Additional shortcuts,"), "Focus shortcuts:": __("Focus shortcuts:"), "Inline toolbar (when an image, link or preview is selected)": __("Inline toolbar (when an image, link or preview is selected)"), "Editor menu (when enabled)": __("Editor menu (when enabled)"), "Editor toolbar": __("Editor toolbar"), "Elements path": __("Elements path"), "Ctrl + Alt + letter:": __("Ctrl + Alt + letter:"), "Shift + Alt + letter:": __("Shift + Alt + letter:"), "Cmd + letter:": __("Cmd + letter:"), "Ctrl + letter:": __("Ctrl + letter:"), "Letter": __("Letter"), "Action": __("Action"), "Warning: the link has been inserted but may have errors. Please test it.": __("Warning: the link has been inserted but may have errors. Please test it."), "To move focus to other buttons use Tab or the arrow keys. To return focus to the editor press Escape or use one of the buttons.": __("To move focus to other buttons use Tab or the arrow keys. To return focus to the editor press Escape or use one of the buttons."), "When starting a new paragraph with one of these formatting shortcuts followed by a space, the formatting will be applied automatically. Press Backspace or Escape to undo.": __("When starting a new paragraph with one of these formatting shortcuts followed by a space, the formatting will be applied automatically. Press Backspace or Escape to undo."), "The following formatting shortcuts are replaced when pressing Enter. Press Escape or the Undo button to undo.": __("The following formatting shortcuts are replaced when pressing Enter. Press Escape or the Undo button to undo."), "The next group of formatting shortcuts are applied as you type or when you insert them around plain text in the same paragraph. Press Escape or the Undo button to undo.": __("The next group of formatting shortcuts are applied as you type or when you insert them around plain text in the same paragraph. Press Escape or the Undo button to undo.")})
        # end if
        #// 
        #// Imagetools plugin (not included):
        #// 'Edit image' => __( 'Edit image' ),
        #// 'Image options' => __( 'Image options' ),
        #// 'Back' => __( 'Back' ),
        #// 'Invert' => __( 'Invert' ),
        #// 'Flip horizontally' => __( 'Flip horizontal' ),
        #// 'Flip vertically' => __( 'Flip vertical' ),
        #// 'Crop' => __( 'Crop' ),
        #// 'Orientation' => __( 'Orientation' ),
        #// 'Resize' => __( 'Resize' ),
        #// 'Rotate clockwise' => __( 'Rotate right' ),
        #// 'Rotate counterclockwise' => __( 'Rotate left' ),
        #// 'Sharpen' => __( 'Sharpen' ),
        #// 'Brightness' => __( 'Brightness' ),
        #// 'Color levels' => __( 'Color levels' ),
        #// 'Contrast' => __( 'Contrast' ),
        #// 'Gamma' => __( 'Gamma' ),
        #// 'Zoom in' => __( 'Zoom in' ),
        #// 'Zoom out' => __( 'Zoom out' ),
        #//
        return self.translation
    # end def get_translation
    #// 
    #// Translates the default TinyMCE strings and returns them as JSON encoded object ready to be loaded with tinymce.addI18n(),
    #// or as JS snippet that should run after tinymce.js is loaded.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $mce_locale The locale used for the editor.
    #// @param bool $json_only optional Whether to include the JavaScript calls to tinymce.addI18n() and tinymce.ScriptLoader.markDone().
    #// @return string Translation object, JSON encoded.
    #//
    @classmethod
    def wp_mce_translation(self, mce_locale="", json_only=False):
        
        if (not mce_locale):
            mce_locale = self.get_mce_locale()
        # end if
        mce_translation = self.get_translation()
        for name,value in mce_translation:
            if php_is_array(value):
                mce_translation[name] = value[0]
            # end if
        # end for
        #// 
        #// Filters translated strings prepared for TinyMCE.
        #// 
        #// @since 3.9.0
        #// 
        #// @param array  $mce_translation Key/value pairs of strings.
        #// @param string $mce_locale      Locale.
        #//
        mce_translation = apply_filters("wp_mce_translation", mce_translation, mce_locale)
        for key,value in mce_translation:
            #// Remove strings that are not translated.
            if key == value:
                mce_translation[key] = None
                continue
            # end if
            if False != php_strpos(value, "&"):
                mce_translation[key] = html_entity_decode(value, ENT_QUOTES, "UTF-8")
            # end if
        # end for
        #// Set direction.
        if is_rtl():
            mce_translation["_dir"] = "rtl"
        # end if
        if json_only:
            return wp_json_encode(mce_translation)
        # end if
        baseurl = self.get_baseurl()
        return str("tinymce.addI18n( '") + str(mce_locale) + str("', ") + wp_json_encode(mce_translation) + ");\n" + str("tinymce.ScriptLoader.markDone( '") + str(baseurl) + str("/langs/") + str(mce_locale) + str(".js' );\n")
    # end def wp_mce_translation
    #// 
    #// Force uncompressed TinyMCE when a custom theme has been defined.
    #// 
    #// The compressed TinyMCE file cannot deal with custom themes, so this makes
    #// sure that we use the uncompressed TinyMCE file if a theme is defined.
    #// Even if we are on a production environment.
    #// 
    #// @since 5.0.0
    #//
    @classmethod
    def force_uncompressed_tinymce(self):
        
        has_custom_theme = False
        for init in self.mce_settings:
            if (not php_empty(lambda : init["theme_url"])):
                has_custom_theme = True
                break
            # end if
        # end for
        if (not has_custom_theme):
            return
        # end if
        wp_scripts = wp_scripts()
        wp_scripts.remove("wp-tinymce")
        wp_register_tinymce_scripts(wp_scripts, True)
    # end def force_uncompressed_tinymce
    #// 
    #// Print (output) the main TinyMCE scripts.
    #// 
    #// @since 4.8.0
    #// 
    #// @global string $tinymce_version
    #// @global bool   $concatenate_scripts
    #// @global bool   $compress_scripts
    #//
    @classmethod
    def print_tinymce_scripts(self):
        
        global concatenate_scripts
        php_check_if_defined("concatenate_scripts")
        if self.tinymce_scripts_printed:
            return
        # end if
        self.tinymce_scripts_printed = True
        if (not (php_isset(lambda : concatenate_scripts))):
            script_concat_settings()
        # end if
        wp_print_scripts(Array("wp-tinymce"))
        php_print("<script type='text/javascript'>\n" + self.wp_mce_translation() + "</script>\n")
    # end def print_tinymce_scripts
    #// 
    #// Print (output) the TinyMCE configuration and initialization scripts.
    #// 
    #// @since 3.3.0
    #// 
    #// @global string $tinymce_version
    #//
    @classmethod
    def editor_js(self):
        
        global tinymce_version
        php_check_if_defined("tinymce_version")
        tmce_on = (not php_empty(lambda : self.mce_settings))
        mceInit = ""
        qtInit = ""
        if tmce_on:
            for editor_id,init in self.mce_settings:
                options = self._parse_init(init)
                mceInit += str("'") + str(editor_id) + str("':") + str(options) + str(",")
            # end for
            mceInit = "{" + php_trim(mceInit, ",") + "}"
        else:
            mceInit = "{}"
        # end if
        if (not php_empty(lambda : self.qt_settings)):
            for editor_id,init in self.qt_settings:
                options = self._parse_init(init)
                qtInit += str("'") + str(editor_id) + str("':") + str(options) + str(",")
            # end for
            qtInit = "{" + php_trim(qtInit, ",") + "}"
        else:
            qtInit = "{}"
        # end if
        ref = Array({"plugins": php_implode(",", self.plugins), "theme": "modern", "language": self.mce_locale})
        suffix = "" if SCRIPT_DEBUG else ".min"
        baseurl = self.get_baseurl()
        version = "ver=" + tinymce_version
        #// 
        #// Fires immediately before the TinyMCE settings are printed.
        #// 
        #// @since 3.2.0
        #// 
        #// @param array $mce_settings TinyMCE settings array.
        #//
        do_action("before_wp_tiny_mce", self.mce_settings)
        php_print("""
        <script type=\"text/javascript\">
        tinyMCEPreInit = {
        baseURL: \"""")
        php_print(baseurl)
        php_print("\",\n            suffix: \"")
        php_print(suffix)
        php_print("\",\n            ")
        if self.drag_drop_upload:
            php_print("dragDropUpload: true,")
        # end if
        php_print("         mceInit: ")
        php_print(mceInit)
        php_print(",\n          qtInit: ")
        php_print(qtInit)
        php_print(",\n          ref: ")
        php_print(self._parse_init(ref))
        php_print(""",
        load_ext: function(url,lang){var sl=tinymce.ScriptLoader;sl.markDone(url+'/langs/'+lang+'.js');sl.markDone(url+'/langs/'+lang+'_dlg.js');}
        };
        </script>
        """)
        if tmce_on:
            self.print_tinymce_scripts()
            if self.ext_plugins:
                #// Load the old-format English strings to prevent unsightly labels in old style popups.
                php_print(str("<script type='text/javascript' src='") + str(baseurl) + str("/langs/wp-langs-en.js?") + str(version) + str("'></script>\n"))
            # end if
        # end if
        #// 
        #// Fires after tinymce.js is loaded, but before any TinyMCE editor
        #// instances are created.
        #// 
        #// @since 3.9.0
        #// 
        #// @param array $mce_settings TinyMCE settings array.
        #//
        do_action("wp_tiny_mce_init", self.mce_settings)
        php_print("     <script type=\"text/javascript\">\n     ")
        if self.ext_plugins:
            php_print(self.ext_plugins + "\n")
        # end if
        if (not is_admin()):
            php_print("var ajaxurl = \"" + admin_url("admin-ajax.php", "relative") + "\";")
        # end if
        php_print("""
        ( function() {
        var init, id, $wrap;
    if ( typeof tinymce !== 'undefined' ) {
    if ( tinymce.Env.ie && tinymce.Env.ie < 11 ) {
        tinymce.$( '.wp-editor-wrap ' ).removeClass( 'tmce-active' ).addClass( 'html-active' );
        return;
        }
    for ( id in tinyMCEPreInit.mceInit ) {
        init = tinyMCEPreInit.mceInit[id];
        $wrap = tinymce.$( '#wp-' + id + '-wrap' );
    if ( ( $wrap.hasClass( 'tmce-active' ) || ! tinyMCEPreInit.qtInit.hasOwnProperty( id ) ) && ! init.wp_skip_init ) {
        tinymce.init( init );
    if ( ! window.wpActiveEditor ) {
        window.wpActiveEditor = id;
        }
        }
        }
        }
    if ( typeof quicktags !== 'undefined' ) {
    for ( id in tinyMCEPreInit.qtInit ) {
        quicktags( tinyMCEPreInit.qtInit[id] );
    if ( ! window.wpActiveEditor ) {
        window.wpActiveEditor = id;
        }
        }
        }
        }());
        </script>
        """)
        if php_in_array("wplink", self.plugins, True) or php_in_array("link", self.qt_buttons, True):
            self.wp_link_dialog()
        # end if
        #// 
        #// Fires after any core TinyMCE editor instances are created.
        #// 
        #// @since 3.2.0
        #// 
        #// @param array $mce_settings TinyMCE settings array.
        #//
        do_action("after_wp_tiny_mce", self.mce_settings)
    # end def editor_js
    #// 
    #// Outputs the HTML for distraction-free writing mode.
    #// 
    #// @since 3.2.0
    #// @deprecated 4.3.0
    #//
    @classmethod
    def wp_fullscreen_html(self):
        
        _deprecated_function(__FUNCTION__, "4.3.0")
    # end def wp_fullscreen_html
    #// 
    #// Performs post queries for internal linking.
    #// 
    #// @since 3.1.0
    #// 
    #// @param array $args Optional. Accepts 'pagenum' and 's' (search) arguments.
    #// @return array|false Results.
    #//
    @classmethod
    def wp_link_query(self, args=Array()):
        
        pts = get_post_types(Array({"public": True}), "objects")
        pt_names = php_array_keys(pts)
        query = Array({"post_type": pt_names, "suppress_filters": True, "update_post_term_cache": False, "update_post_meta_cache": False, "post_status": "publish", "posts_per_page": 20})
        args["pagenum"] = absint(args["pagenum"]) if (php_isset(lambda : args["pagenum"])) else 1
        if (php_isset(lambda : args["s"])):
            query["s"] = args["s"]
        # end if
        query["offset"] = query["posts_per_page"] * args["pagenum"] - 1 if args["pagenum"] > 1 else 0
        #// 
        #// Filters the link query arguments.
        #// 
        #// Allows modification of the link query arguments before querying.
        #// 
        #// @see WP_Query for a full list of arguments
        #// 
        #// @since 3.7.0
        #// 
        #// @param array $query An array of WP_Query arguments.
        #//
        query = apply_filters("wp_link_query_args", query)
        #// Do main query.
        get_posts = php_new_class("WP_Query", lambda : WP_Query())
        posts = get_posts.query(query)
        #// Build results.
        results = Array()
        for post in posts:
            if "post" == post.post_type:
                info = mysql2date(__("Y/m/d"), post.post_date)
            else:
                info = pts[post.post_type].labels.singular_name
            # end if
            results[-1] = Array({"ID": post.ID, "title": php_trim(esc_html(strip_tags(get_the_title(post)))), "permalink": get_permalink(post.ID), "info": info})
        # end for
        #// 
        #// Filters the link query results.
        #// 
        #// Allows modification of the returned link query results.
        #// 
        #// @since 3.7.0
        #// 
        #// @see 'wp_link_query_args' filter
        #// 
        #// @param array $results {
        #// An associative array of query results.
        #// 
        #// @type array {
        #// @type int    $ID        Post ID.
        #// @type string $title     The trimmed, escaped post title.
        #// @type string $permalink Post permalink.
        #// @type string $info      A 'Y/m/d'-formatted date for 'post' post type,
        #// the 'singular_name' post type label otherwise.
        #// }
        #// }
        #// @param array $query  An array of WP_Query arguments.
        #//
        results = apply_filters("wp_link_query", results, query)
        return results if (not php_empty(lambda : results)) else False
    # end def wp_link_query
    #// 
    #// Dialog for internal linking.
    #// 
    #// @since 3.1.0
    #//
    @classmethod
    def wp_link_dialog(self):
        
        #// Run once.
        if self.link_dialog_printed:
            return
        # end if
        self.link_dialog_printed = True
        pass
        php_print("""       <div id=\"wp-link-backdrop\" style=\"display: none\"></div>
        <div id=\"wp-link-wrap\" class=\"wp-core-ui\" style=\"display: none\" role=\"dialog\" aria-labelledby=\"link-modal-title\">
        <form id=\"wp-link\" tabindex=\"-1\">
        """)
        wp_nonce_field("internal-linking", "_ajax_linking_nonce", False)
        php_print("     <h1 id=\"link-modal-title\">")
        _e("Insert/edit link")
        php_print("</h1>\n      <button type=\"button\" id=\"wp-link-close\"><span class=\"screen-reader-text\">")
        _e("Close")
        php_print("""</span></button>
        <div id=\"link-selector\">
        <div id=\"link-options\">
        <p class=\"howto\" id=\"wplink-enter-url\">""")
        _e("Enter the destination URL")
        php_print("</p>\n               <div>\n                 <label><span>")
        _e("URL")
        php_print("""</span>
        <input id=\"wp-link-url\" type=\"text\" aria-describedby=\"wplink-enter-url\" /></label>
        </div>
        <div class=\"wp-link-text-field\">
        <label><span>""")
        _e("Link Text")
        php_print("""</span>
        <input id=\"wp-link-text\" type=\"text\" /></label>
        </div>
        <div class=\"link-target\">
        <label><span></span>
        <input type=\"checkbox\" id=\"wp-link-target\" /> """)
        _e("Open link in a new tab")
        php_print("""</label>
        </div>
        </div>
        <p class=\"howto\" id=\"wplink-link-existing-content\">""")
        _e("Or link to existing content")
        php_print("""</p>
        <div id=\"search-panel\">
        <div class=\"link-search-wrapper\">
        <label>
        <span class=\"search-label\">""")
        _e("Search")
        php_print("""</span>
        <input type=\"search\" id=\"wp-link-search\" class=\"link-search-field\" autocomplete=\"off\" aria-describedby=\"wplink-link-existing-content\" />
        <span class=\"spinner\"></span>
        </label>
        </div>
        <div id=\"search-results\" class=\"query-results\" tabindex=\"0\">
        <ul></ul>
        <div class=\"river-waiting\">
        <span class=\"spinner\"></span>
        </div>
        </div>
        <div id=\"most-recent-results\" class=\"query-results\" tabindex=\"0\">
        <div class=\"query-notice\" id=\"query-notice-message\">
        <em class=\"query-notice-default\">""")
        _e("No search term specified. Showing recent items.")
        php_print("</em>\n                      <em class=\"query-notice-hint screen-reader-text\">")
        _e("Search or use up and down arrow keys to select an item.")
        php_print("""</em>
        </div>
        <ul></ul>
        <div class=\"river-waiting\">
        <span class=\"spinner\"></span>
        </div>
        </div>
        </div>
        </div>
        <div class=\"submitbox\">
        <div id=\"wp-link-cancel\">
        <button type=\"button\" class=\"button\">""")
        _e("Cancel")
        php_print("""</button>
        </div>
        <div id=\"wp-link-update\">
        <input type=\"submit\" value=\"""")
        esc_attr_e("Add Link")
        php_print("""\" class=\"button button-primary\" id=\"wp-link-submit\" name=\"wp-link-submit\">
        </div>
        </div>
        </form>
        </div>
        """)
    # end def wp_link_dialog
# end class _WP_Editors
