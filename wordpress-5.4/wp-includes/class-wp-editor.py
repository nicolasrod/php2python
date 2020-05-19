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
    def parse_settings(self, editor_id_=None, settings_=None):
        
        
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
        settings_ = apply_filters("wp_editor_settings", settings_, editor_id_)
        set_ = wp_parse_args(settings_, Array({"wpautop": (not has_blocks()), "media_buttons": True, "default_editor": "", "drag_drop_upload": False, "textarea_name": editor_id_, "textarea_rows": 20, "tabindex": "", "tabfocus_elements": ":prev,:next", "editor_css": "", "editor_class": "", "teeny": False, "_content_editor_dfw": False, "tinymce": True, "quicktags": True}))
        self.this_tinymce = set_["tinymce"] and user_can_richedit()
        if self.this_tinymce:
            if False != php_strpos(editor_id_, "["):
                self.this_tinymce = False
                _deprecated_argument("wp_editor()", "3.9.0", "TinyMCE editor IDs cannot have brackets.")
            # end if
        # end if
        self.this_quicktags = php_bool(set_["quicktags"])
        if self.this_tinymce:
            self.has_tinymce = True
        # end if
        if self.this_quicktags:
            self.has_quicktags = True
        # end if
        if php_empty(lambda : set_["editor_height"]):
            return set_
        # end if
        if "content" == editor_id_ and php_empty(lambda : set_["tinymce"]["wp_autoresize_on"]):
            #// A cookie (set when a user resizes the editor) overrides the height.
            cookie_ = php_int(get_user_setting("ed_size"))
            if cookie_:
                set_["editor_height"] = cookie_
            # end if
        # end if
        if set_["editor_height"] < 50:
            set_["editor_height"] = 50
        elif set_["editor_height"] > 5000:
            set_["editor_height"] = 5000
        # end if
        return set_
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
    def editor(self, content_=None, editor_id_=None, settings_=None):
        if settings_ is None:
            settings_ = Array()
        # end if
        
        set_ = self.parse_settings(editor_id_, settings_)
        editor_class_ = " class=\"" + php_trim(esc_attr(set_["editor_class"]) + " wp-editor-area") + "\""
        tabindex_ = " tabindex=\"" + php_int(set_["tabindex"]) + "\"" if set_["tabindex"] else ""
        default_editor_ = "html"
        buttons_ = ""
        autocomplete_ = ""
        editor_id_attr_ = esc_attr(editor_id_)
        if set_["drag_drop_upload"]:
            self.drag_drop_upload = True
        # end if
        if (not php_empty(lambda : set_["editor_height"])):
            height_ = " style=\"height: " + php_int(set_["editor_height"]) + "px\""
        else:
            height_ = " rows=\"" + php_int(set_["textarea_rows"]) + "\""
        # end if
        if (not current_user_can("upload_files")):
            set_["media_buttons"] = False
        # end if
        if self.this_tinymce:
            autocomplete_ = " autocomplete=\"off\""
            if self.this_quicktags:
                default_editor_ = set_["default_editor"] if set_["default_editor"] else wp_default_editor()
                #// 'html' is used for the "Text" editor tab.
                if "html" != default_editor_:
                    default_editor_ = "tinymce"
                # end if
                buttons_ += "<button type=\"button\" id=\"" + editor_id_attr_ + "-tmce\" class=\"wp-switch-editor switch-tmce\"" + " data-wp-editor-id=\"" + editor_id_attr_ + "\">" + _x("Visual", "Name for the Visual editor tab") + "</button>\n"
                buttons_ += "<button type=\"button\" id=\"" + editor_id_attr_ + "-html\" class=\"wp-switch-editor switch-html\"" + " data-wp-editor-id=\"" + editor_id_attr_ + "\">" + _x("Text", "Name for the Text editor tab (formerly HTML)") + "</button>\n"
            else:
                default_editor_ = "tinymce"
            # end if
        # end if
        switch_class_ = "html-active" if "html" == default_editor_ else "tmce-active"
        wrap_class_ = "wp-core-ui wp-editor-wrap " + switch_class_
        if set_["_content_editor_dfw"]:
            wrap_class_ += " has-dfw"
        # end if
        php_print("<div id=\"wp-" + editor_id_attr_ + "-wrap\" class=\"" + wrap_class_ + "\">")
        if self.editor_buttons_css:
            wp_print_styles("editor-buttons")
            self.editor_buttons_css = False
        # end if
        if (not php_empty(lambda : set_["editor_css"])):
            php_print(set_["editor_css"] + "\n")
        # end if
        if (not php_empty(lambda : buttons_)) or set_["media_buttons"]:
            php_print("<div id=\"wp-" + editor_id_attr_ + "-editor-tools\" class=\"wp-editor-tools hide-if-no-js\">")
            if set_["media_buttons"]:
                self.has_medialib = True
                if (not php_function_exists("media_buttons")):
                    php_include_file(ABSPATH + "wp-admin/includes/media.php", once=False)
                # end if
                php_print("<div id=\"wp-" + editor_id_attr_ + "-media-buttons\" class=\"wp-media-buttons\">")
                #// 
                #// Fires after the default media button(s) are displayed.
                #// 
                #// @since 2.5.0
                #// 
                #// @param string $editor_id Unique editor identifier, e.g. 'content'.
                #//
                do_action("media_buttons", editor_id_)
                php_print("</div>\n")
            # end if
            php_print("<div class=\"wp-editor-tabs\">" + buttons_ + "</div>\n")
            php_print("</div>\n")
        # end if
        quicktags_toolbar_ = ""
        if self.this_quicktags:
            if "content" == editor_id_ and (not php_empty(lambda : PHP_GLOBALS["current_screen"])) and "post" == PHP_GLOBALS["current_screen"].base:
                toolbar_id_ = "ed_toolbar"
            else:
                toolbar_id_ = "qt_" + editor_id_attr_ + "_toolbar"
            # end if
            quicktags_toolbar_ = "<div id=\"" + toolbar_id_ + "\" class=\"quicktags-toolbar\"></div>"
        # end if
        #// 
        #// Filters the HTML markup output that displays the editor.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $output Editor's HTML markup.
        #//
        the_editor_ = apply_filters("the_editor", "<div id=\"wp-" + editor_id_attr_ + "-editor-container\" class=\"wp-editor-container\">" + quicktags_toolbar_ + "<textarea" + editor_class_ + height_ + tabindex_ + autocomplete_ + " cols=\"40\" name=\"" + esc_attr(set_["textarea_name"]) + "\" " + "id=\"" + editor_id_attr_ + "\">%s</textarea></div>")
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
        content_ = apply_filters("the_editor_content", content_, default_editor_)
        #// Remove the filter as the next editor on the same page may not need it.
        if self.this_tinymce:
            remove_filter("the_editor_content", "format_for_editor")
        # end if
        #// Back-compat for the `htmledit_pre` and `richedit_pre` filters.
        if "html" == default_editor_ and has_filter("htmledit_pre"):
            #// This filter is documented in wp-includes/deprecated.php
            content_ = apply_filters_deprecated("htmledit_pre", Array(content_), "4.3.0", "format_for_editor")
        elif "tinymce" == default_editor_ and has_filter("richedit_pre"):
            #// This filter is documented in wp-includes/deprecated.php
            content_ = apply_filters_deprecated("richedit_pre", Array(content_), "4.3.0", "format_for_editor")
        # end if
        if False != php_stripos(content_, "textarea"):
            content_ = php_preg_replace("%</textarea%i", "&lt;/textarea", content_)
        # end if
        printf(the_editor_, content_)
        php_print("""
        </div>
        """)
        self.editor_settings(editor_id_, set_)
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
    def editor_settings(self, editor_id_=None, set_=None):
        
        
        global tinymce_version_
        php_check_if_defined("tinymce_version_")
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
            qtInit_ = Array({"id": editor_id_, "buttons": ""})
            if php_is_array(set_["quicktags"]):
                qtInit_ = php_array_merge(qtInit_, set_["quicktags"])
            # end if
            if php_empty(lambda : qtInit_["buttons"]):
                qtInit_["buttons"] = "strong,em,link,block,del,ins,img,ul,ol,li,code,more,close"
            # end if
            if set_["_content_editor_dfw"]:
                qtInit_["buttons"] += ",dfw"
            # end if
            #// 
            #// Filters the Quicktags settings.
            #// 
            #// @since 3.3.0
            #// 
            #// @param array  $qtInit    Quicktags settings.
            #// @param string $editor_id Unique editor identifier, e.g. 'content'.
            #//
            qtInit_ = apply_filters("quicktags_settings", qtInit_, editor_id_)
            self.qt_settings[editor_id_] = qtInit_
            self.qt_buttons = php_array_merge(self.qt_buttons, php_explode(",", qtInit_["buttons"]))
        # end if
        if self.this_tinymce:
            if php_empty(lambda : self.first_init):
                baseurl_ = self.get_baseurl()
                mce_locale_ = self.get_mce_locale()
                ext_plugins_ = ""
                if set_["teeny"]:
                    #// 
                    #// Filters the list of teenyMCE plugins.
                    #// 
                    #// @since 2.7.0
                    #// @since 3.3.0 The `$editor_id` parameter was added.
                    #// 
                    #// @param array  $plugins   An array of teenyMCE plugins.
                    #// @param string $editor_id Unique editor identifier, e.g. 'content'.
                    #//
                    plugins_ = apply_filters("teeny_mce_plugins", Array("colorpicker", "lists", "fullscreen", "image", "wordpress", "wpeditimage", "wplink"), editor_id_)
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
                    mce_external_plugins_ = apply_filters("mce_external_plugins", Array(), editor_id_)
                    plugins_ = Array("charmap", "colorpicker", "hr", "lists", "media", "paste", "tabfocus", "textcolor", "fullscreen", "wordpress", "wpautoresize", "wpeditimage", "wpemoji", "wpgallery", "wplink", "wpdialogs", "wptextpattern", "wpview")
                    if (not self.has_medialib):
                        plugins_[-1] = "image"
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
                    plugins_ = array_unique(apply_filters("tiny_mce_plugins", plugins_, editor_id_))
                    key_ = php_array_search("spellchecker", plugins_)
                    if False != key_:
                        plugins_[key_] = None
                    # end if
                    if (not php_empty(lambda : mce_external_plugins_)):
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
                        mce_external_languages_ = apply_filters("mce_external_languages", Array(), editor_id_)
                        loaded_langs_ = Array()
                        strings_ = ""
                        if (not php_empty(lambda : mce_external_languages_)):
                            for name_,path_ in mce_external_languages_.items():
                                if php_no_error(lambda: php_is_file(path_)) and php_no_error(lambda: php_is_readable(path_)):
                                    php_include_file(path_, once=False)
                                    ext_plugins_ += strings_ + "\n"
                                    loaded_langs_[-1] = name_
                                # end if
                            # end for
                        # end if
                        for name_,url_ in mce_external_plugins_.items():
                            if php_in_array(name_, plugins_, True):
                                mce_external_plugins_[name_] = None
                                continue
                            # end if
                            url_ = set_url_scheme(url_)
                            mce_external_plugins_[name_] = url_
                            plugurl_ = php_dirname(url_)
                            strings_ = ""
                            #// Try to load langs/[locale].js and langs/[locale]_dlg.js.
                            if (not php_in_array(name_, loaded_langs_, True)):
                                path_ = php_str_replace(content_url(), "", plugurl_)
                                path_ = WP_CONTENT_DIR + path_ + "/langs/"
                                path_ = trailingslashit(php_realpath(path_))
                                if php_no_error(lambda: php_is_file(path_ + mce_locale_ + ".js")):
                                    strings_ += php_no_error(lambda: php_file_get_contents(path_ + mce_locale_ + ".js")) + "\n"
                                # end if
                                if php_no_error(lambda: php_is_file(path_ + mce_locale_ + "_dlg.js")):
                                    strings_ += php_no_error(lambda: php_file_get_contents(path_ + mce_locale_ + "_dlg.js")) + "\n"
                                # end if
                                if "en" != mce_locale_ and php_empty(lambda : strings_):
                                    if php_no_error(lambda: php_is_file(path_ + "en.js")):
                                        str1_ = php_no_error(lambda: php_file_get_contents(path_ + "en.js"))
                                        strings_ += php_preg_replace("/(['\"])en\\./", "$1" + mce_locale_ + ".", str1_, 1) + "\n"
                                    # end if
                                    if php_no_error(lambda: php_is_file(path_ + "en_dlg.js")):
                                        str2_ = php_no_error(lambda: php_file_get_contents(path_ + "en_dlg.js"))
                                        strings_ += php_preg_replace("/(['\"])en\\./", "$1" + mce_locale_ + ".", str2_, 1) + "\n"
                                    # end if
                                # end if
                                if (not php_empty(lambda : strings_)):
                                    ext_plugins_ += "\n" + strings_ + "\n"
                                # end if
                            # end if
                            ext_plugins_ += "tinyMCEPreInit.load_ext(\"" + plugurl_ + "\", \"" + mce_locale_ + "\");" + "\n"
                        # end for
                    # end if
                # end if
                self.plugins = plugins_
                self.ext_plugins = ext_plugins_
                settings_ = self.default_settings()
                settings_["plugins"] = php_implode(",", plugins_)
                if (not php_empty(lambda : mce_external_plugins_)):
                    settings_["external_plugins"] = wp_json_encode(mce_external_plugins_)
                # end if
                #// This filter is documented in wp-admin/includes/media.php
                if apply_filters("disable_captions", ""):
                    settings_["wpeditimage_disable_captions"] = True
                # end if
                mce_css_ = settings_["content_css"]
                #// 
                #// The `editor-style.css` added by the theme is generally intended for the editor instance on the Edit Post screen.
                #// Plugins that use wp_editor() on the front-end can decide whether to add the theme stylesheet
                #// by using `get_editor_stylesheets()` and the `mce_css` or `tiny_mce_before_init` filters, see below.
                #//
                if is_admin():
                    editor_styles_ = get_editor_stylesheets()
                    if (not php_empty(lambda : editor_styles_)):
                        #// Force urlencoding of commas.
                        for key_,url_ in editor_styles_.items():
                            if php_strpos(url_, ",") != False:
                                editor_styles_[key_] = php_str_replace(",", "%2C", url_)
                            # end if
                        # end for
                        mce_css_ += "," + php_implode(",", editor_styles_)
                    # end if
                # end if
                #// 
                #// Filters the comma-delimited list of stylesheets to load in TinyMCE.
                #// 
                #// @since 2.1.0
                #// 
                #// @param string $stylesheets Comma-delimited list of stylesheets.
                #//
                mce_css_ = php_trim(apply_filters("mce_css", mce_css_), " ,")
                if (not php_empty(lambda : mce_css_)):
                    settings_["content_css"] = mce_css_
                else:
                    settings_["content_css"] = None
                # end if
                self.first_init = settings_
            # end if
            if set_["teeny"]:
                mce_buttons_ = Array("bold", "italic", "underline", "blockquote", "strikethrough", "bullist", "numlist", "alignleft", "aligncenter", "alignright", "undo", "redo", "link", "fullscreen")
                #// 
                #// Filters the list of teenyMCE buttons (Text tab).
                #// 
                #// @since 2.7.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mce_buttons An array of teenyMCE buttons.
                #// @param string $editor_id   Unique editor identifier, e.g. 'content'.
                #//
                mce_buttons_ = apply_filters("teeny_mce_buttons", mce_buttons_, editor_id_)
                mce_buttons_2_ = Array()
                mce_buttons_3_ = Array()
                mce_buttons_4_ = Array()
            else:
                mce_buttons_ = Array("formatselect", "bold", "italic", "bullist", "numlist", "blockquote", "alignleft", "aligncenter", "alignright", "link", "wp_more", "spellchecker")
                if (not wp_is_mobile()):
                    if set_["_content_editor_dfw"]:
                        mce_buttons_[-1] = "wp_adv"
                        mce_buttons_[-1] = "dfw"
                    else:
                        mce_buttons_[-1] = "fullscreen"
                        mce_buttons_[-1] = "wp_adv"
                    # end if
                else:
                    mce_buttons_[-1] = "wp_adv"
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
                mce_buttons_ = apply_filters("mce_buttons", mce_buttons_, editor_id_)
                mce_buttons_2_ = Array("strikethrough", "hr", "forecolor", "pastetext", "removeformat", "charmap", "outdent", "indent", "undo", "redo")
                if (not wp_is_mobile()):
                    mce_buttons_2_[-1] = "wp_help"
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
                mce_buttons_2_ = apply_filters("mce_buttons_2", mce_buttons_2_, editor_id_)
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
                mce_buttons_3_ = apply_filters("mce_buttons_3", Array(), editor_id_)
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
                mce_buttons_4_ = apply_filters("mce_buttons_4", Array(), editor_id_)
            # end if
            body_class_ = editor_id_
            post_ = get_post()
            if post_:
                body_class_ += " post-type-" + sanitize_html_class(post_.post_type) + " post-status-" + sanitize_html_class(post_.post_status)
                if post_type_supports(post_.post_type, "post-formats"):
                    post_format_ = get_post_format(post_)
                    if post_format_ and (not is_wp_error(post_format_)):
                        body_class_ += " post-format-" + sanitize_html_class(post_format_)
                    else:
                        body_class_ += " post-format-standard"
                    # end if
                # end if
                page_template_ = get_page_template_slug(post_)
                if False != page_template_:
                    page_template_ = "default" if php_empty(lambda : page_template_) else php_str_replace(".", "-", php_basename(page_template_, ".php"))
                    body_class_ += " page-template-" + sanitize_html_class(page_template_)
                # end if
            # end if
            body_class_ += " locale-" + sanitize_html_class(php_strtolower(php_str_replace("_", "-", get_user_locale())))
            if (not php_empty(lambda : set_["tinymce"]["body_class"])):
                body_class_ += " " + set_["tinymce"]["body_class"]
                set_["tinymce"]["body_class"] = None
            # end if
            mceInit_ = Array({"selector": str("#") + str(editor_id_), "wpautop": php_bool(set_["wpautop"]), "indent": (not set_["wpautop"]), "toolbar1": php_implode(",", mce_buttons_), "toolbar2": php_implode(",", mce_buttons_2_), "toolbar3": php_implode(",", mce_buttons_3_), "toolbar4": php_implode(",", mce_buttons_4_), "tabfocus_elements": set_["tabfocus_elements"], "body_class": body_class_})
            #// Merge with the first part of the init array.
            mceInit_ = php_array_merge(self.first_init, mceInit_)
            if php_is_array(set_["tinymce"]):
                mceInit_ = php_array_merge(mceInit_, set_["tinymce"])
            # end if
            #// 
            #// For people who really REALLY know what they're doing with TinyMCE
            #// You can modify $mceInit to add, remove, change elements of the config
            #// before tinyMCE.init. Setting "valid_elements", "invalid_elements"
            #// and "extended_valid_elements" can be done through this filter. Best
            #// is to use the default cleanup by not specifying valid_elements,
            #// as TinyMCE checks against the full set of HTML 5.0 elements and attributes.
            #//
            if set_["teeny"]:
                #// 
                #// Filters the teenyMCE config before init.
                #// 
                #// @since 2.7.0
                #// @since 3.3.0 The `$editor_id` parameter was added.
                #// 
                #// @param array  $mceInit   An array with teenyMCE config.
                #// @param string $editor_id Unique editor identifier, e.g. 'content'.
                #//
                mceInit_ = apply_filters("teeny_mce_before_init", mceInit_, editor_id_)
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
                mceInit_ = apply_filters("tiny_mce_before_init", mceInit_, editor_id_)
            # end if
            if php_empty(lambda : mceInit_["toolbar3"]) and (not php_empty(lambda : mceInit_["toolbar4"])):
                mceInit_["toolbar3"] = mceInit_["toolbar4"]
                mceInit_["toolbar4"] = ""
            # end if
            self.mce_settings[editor_id_] = mceInit_
        # end if
        pass
    # end def editor_settings
    #// 
    #// @since 3.3.0
    #// 
    #// @param array $init
    #// @return string
    #//
    def _parse_init(self, init_=None):
        
        
        options_ = ""
        for key_,value_ in init_.items():
            if php_is_bool(value_):
                val_ = "true" if value_ else "false"
                options_ += key_ + ":" + val_ + ","
                continue
            elif (not php_empty(lambda : value_)) and php_is_string(value_) and "{" == value_[0] and "}" == value_[php_strlen(value_) - 1] or "[" == value_[0] and "]" == value_[php_strlen(value_) - 1] or php_preg_match("/^\\(?function ?\\(/", value_):
                options_ += key_ + ":" + value_ + ","
                continue
            # end if
            options_ += key_ + ":\"" + value_ + "\","
        # end for
        return "{" + php_trim(options_, " ,") + "}"
    # end def _parse_init
    #// 
    #// @since 3.3.0
    #// 
    #// @param bool $default_scripts Optional. Whether default scripts should be enqueued. Default false.
    #//
    @classmethod
    def enqueue_scripts(self, default_scripts_=None):
        if default_scripts_ is None:
            default_scripts_ = False
        # end if
        
        if default_scripts_ or self.has_tinymce:
            wp_enqueue_script("editor")
        # end if
        if default_scripts_ or self.has_quicktags:
            wp_enqueue_script("quicktags")
            wp_enqueue_style("buttons")
        # end if
        if default_scripts_ or php_in_array("wplink", self.plugins, True) or php_in_array("link", self.qt_buttons, True):
            wp_enqueue_script("wplink")
            wp_enqueue_script("jquery-ui-autocomplete")
        # end if
        if self.has_medialib:
            add_thickbox()
            wp_enqueue_script("media-upload")
            wp_enqueue_script("wp-embed")
        elif default_scripts_:
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
        do_action("wp_enqueue_editor", Array({"tinymce": default_scripts_ or self.has_tinymce, "quicktags": default_scripts_ or self.has_quicktags}))
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
        
        
        user_can_richedit_ = user_can_richedit()
        if user_can_richedit_:
            settings_ = self.default_settings()
            settings_["toolbar1"] = "bold,italic,bullist,numlist,link"
            settings_["wpautop"] = False
            settings_["indent"] = True
            settings_["elementpath"] = False
            if is_rtl():
                settings_["directionality"] = "rtl"
            # end if
            #// 
            #// In production all plugins are loaded (they are in wp-editor.js.gz).
            #// The 'wpview', 'wpdialogs', and 'media' TinyMCE plugins are not initialized by default.
            #// Can be added from js by using the 'wp-before-tinymce-init' event.
            #//
            settings_["plugins"] = php_implode(",", Array("charmap", "colorpicker", "hr", "lists", "paste", "tabfocus", "textcolor", "fullscreen", "wordpress", "wpautoresize", "wpeditimage", "wpemoji", "wpgallery", "wplink", "wptextpattern"))
            settings_ = self._parse_init(settings_)
        else:
            settings_ = "{}"
        # end if
        php_print("""       <script type=\"text/javascript\">
        window.wp = window.wp || {};
        window.wp.editor = window.wp.editor || {};
        window.wp.editor.getDefaultSettings = function() {
        return {
        tinymce: """)
        php_print(settings_)
        php_print(""",
        quicktags: {
        buttons: 'strong,em,link,ul,ol,li,code'
        }
        };
        };
        """)
        if user_can_richedit_:
            suffix_ = "" if SCRIPT_DEBUG else ".min"
            baseurl_ = self.get_baseurl()
            php_print("         var tinyMCEPreInit = {\n                baseURL: \"")
            php_print(baseurl_)
            php_print("\",\n                suffix: \"")
            php_print(suffix_)
            php_print("""\",
            mceInit: {},
            qtInit: {},
            load_ext: function(url,lang){var sl=tinymce.ScriptLoader;sl.markDone(url+'/langs/'+lang+'.js');sl.markDone(url+'/langs/'+lang+'_dlg.js');}
            };
            """)
        # end if
        php_print("     </script>\n     ")
        if user_can_richedit_:
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
            mce_locale_ = get_user_locale()
            self.mce_locale = "en" if php_empty(lambda : mce_locale_) else php_strtolower(php_substr(mce_locale_, 0, 2))
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
        
        
        global tinymce_version_
        php_check_if_defined("tinymce_version_")
        shortcut_labels_ = Array()
        for name_,value_ in self.get_translation().items():
            if php_is_array(value_):
                shortcut_labels_[name_] = value_[1]
            # end if
        # end for
        settings_ = Array({"theme": "modern", "skin": "lightgray", "language": self.get_mce_locale(), "formats": "{" + "alignleft: [" + "{selector: \"p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li\", styles: {textAlign:\"left\"}}," + "{selector: \"img,table,dl.wp-caption\", classes: \"alignleft\"}" + "]," + "aligncenter: [" + "{selector: \"p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li\", styles: {textAlign:\"center\"}}," + "{selector: \"img,table,dl.wp-caption\", classes: \"aligncenter\"}" + "]," + "alignright: [" + "{selector: \"p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li\", styles: {textAlign:\"right\"}}," + "{selector: \"img,table,dl.wp-caption\", classes: \"alignright\"}" + "]," + "strikethrough: {inline: \"del\"}" + "}"}, {"relative_urls": False, "remove_script_host": False, "convert_urls": False, "browser_spellcheck": True, "fix_list_elements": True, "entities": "38,amp,60,lt,62,gt", "entity_encoding": "raw", "keep_styles": False, "cache_suffix": "wp-mce-" + tinymce_version_, "resize": "vertical", "menubar": False, "branding": False, "preview_styles": "font-family font-size font-weight font-style text-decoration text-transform", "end_container_on_empty_block": True, "wpeditimage_html5_captions": True, "wp_lang_attr": get_bloginfo("language"), "wp_keep_scroll_position": False, "wp_shortcut_labels": wp_json_encode(shortcut_labels_)})
        suffix_ = "" if SCRIPT_DEBUG else ".min"
        version_ = "ver=" + get_bloginfo("version")
        #// Default stylesheets.
        settings_["content_css"] = includes_url(str("css/dashicons") + str(suffix_) + str(".css?") + str(version_)) + "," + includes_url(str("js/tinymce/skins/wordpress/wp-content.css?") + str(version_))
        return settings_
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
    def wp_mce_translation(self, mce_locale_="", json_only_=None):
        if json_only_ is None:
            json_only_ = False
        # end if
        
        if (not mce_locale_):
            mce_locale_ = self.get_mce_locale()
        # end if
        mce_translation_ = self.get_translation()
        for name_,value_ in mce_translation_.items():
            if php_is_array(value_):
                mce_translation_[name_] = value_[0]
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
        mce_translation_ = apply_filters("wp_mce_translation", mce_translation_, mce_locale_)
        for key_,value_ in mce_translation_.items():
            #// Remove strings that are not translated.
            if key_ == value_:
                mce_translation_[key_] = None
                continue
            # end if
            if False != php_strpos(value_, "&"):
                mce_translation_[key_] = html_entity_decode(value_, ENT_QUOTES, "UTF-8")
            # end if
        # end for
        #// Set direction.
        if is_rtl():
            mce_translation_["_dir"] = "rtl"
        # end if
        if json_only_:
            return wp_json_encode(mce_translation_)
        # end if
        baseurl_ = self.get_baseurl()
        return str("tinymce.addI18n( '") + str(mce_locale_) + str("', ") + wp_json_encode(mce_translation_) + ");\n" + str("tinymce.ScriptLoader.markDone( '") + str(baseurl_) + str("/langs/") + str(mce_locale_) + str(".js' );\n")
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
        
        
        has_custom_theme_ = False
        for init_ in self.mce_settings:
            if (not php_empty(lambda : init_["theme_url"])):
                has_custom_theme_ = True
                break
            # end if
        # end for
        if (not has_custom_theme_):
            return
        # end if
        wp_scripts_ = wp_scripts()
        wp_scripts_.remove("wp-tinymce")
        wp_register_tinymce_scripts(wp_scripts_, True)
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
        
        
        global concatenate_scripts_
        php_check_if_defined("concatenate_scripts_")
        if self.tinymce_scripts_printed:
            return
        # end if
        self.tinymce_scripts_printed = True
        if (not (php_isset(lambda : concatenate_scripts_))):
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
        
        
        global tinymce_version_
        php_check_if_defined("tinymce_version_")
        tmce_on_ = (not php_empty(lambda : self.mce_settings))
        mceInit_ = ""
        qtInit_ = ""
        if tmce_on_:
            for editor_id_,init_ in self.mce_settings.items():
                options_ = self._parse_init(init_)
                mceInit_ += str("'") + str(editor_id_) + str("':") + str(options_) + str(",")
            # end for
            mceInit_ = "{" + php_trim(mceInit_, ",") + "}"
        else:
            mceInit_ = "{}"
        # end if
        if (not php_empty(lambda : self.qt_settings)):
            for editor_id_,init_ in self.qt_settings.items():
                options_ = self._parse_init(init_)
                qtInit_ += str("'") + str(editor_id_) + str("':") + str(options_) + str(",")
            # end for
            qtInit_ = "{" + php_trim(qtInit_, ",") + "}"
        else:
            qtInit_ = "{}"
        # end if
        ref_ = Array({"plugins": php_implode(",", self.plugins), "theme": "modern", "language": self.mce_locale})
        suffix_ = "" if SCRIPT_DEBUG else ".min"
        baseurl_ = self.get_baseurl()
        version_ = "ver=" + tinymce_version_
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
        php_print(baseurl_)
        php_print("\",\n            suffix: \"")
        php_print(suffix_)
        php_print("\",\n            ")
        if self.drag_drop_upload:
            php_print("dragDropUpload: true,")
        # end if
        php_print("         mceInit: ")
        php_print(mceInit_)
        php_print(",\n          qtInit: ")
        php_print(qtInit_)
        php_print(",\n          ref: ")
        php_print(self._parse_init(ref_))
        php_print(""",
        load_ext: function(url,lang){var sl=tinymce.ScriptLoader;sl.markDone(url+'/langs/'+lang+'.js');sl.markDone(url+'/langs/'+lang+'_dlg.js');}
        };
        </script>
        """)
        if tmce_on_:
            self.print_tinymce_scripts()
            if self.ext_plugins:
                #// Load the old-format English strings to prevent unsightly labels in old style popups.
                php_print(str("<script type='text/javascript' src='") + str(baseurl_) + str("/langs/wp-langs-en.js?") + str(version_) + str("'></script>\n"))
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
    def wp_link_query(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        pts_ = get_post_types(Array({"public": True}), "objects")
        pt_names_ = php_array_keys(pts_)
        query_ = Array({"post_type": pt_names_, "suppress_filters": True, "update_post_term_cache": False, "update_post_meta_cache": False, "post_status": "publish", "posts_per_page": 20})
        args_["pagenum"] = absint(args_["pagenum"]) if (php_isset(lambda : args_["pagenum"])) else 1
        if (php_isset(lambda : args_["s"])):
            query_["s"] = args_["s"]
        # end if
        query_["offset"] = query_["posts_per_page"] * args_["pagenum"] - 1 if args_["pagenum"] > 1 else 0
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
        query_ = apply_filters("wp_link_query_args", query_)
        #// Do main query.
        get_posts_ = php_new_class("WP_Query", lambda : WP_Query())
        posts_ = get_posts_.query(query_)
        #// Build results.
        results_ = Array()
        for post_ in posts_:
            if "post" == post_.post_type:
                info_ = mysql2date(__("Y/m/d"), post_.post_date)
            else:
                info_ = pts_[post_.post_type].labels.singular_name
            # end if
            results_[-1] = Array({"ID": post_.ID, "title": php_trim(esc_html(strip_tags(get_the_title(post_)))), "permalink": get_permalink(post_.ID), "info": info_})
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
        results_ = apply_filters("wp_link_query", results_, query_)
        return results_ if (not php_empty(lambda : results_)) else False
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
