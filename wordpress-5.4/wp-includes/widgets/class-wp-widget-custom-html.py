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
#// Widget API: WP_Widget_Custom_HTML class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.8.1
#// 
#// 
#// Core class used to implement a Custom HTML widget.
#// 
#// @since 4.8.1
#// 
#// @see WP_Widget
#//
class WP_Widget_Custom_HTML(WP_Widget):
    #// 
    #// Whether or not the widget has been registered yet.
    #// 
    #// @since 4.9.0
    #// @var bool
    #//
    registered = False
    #// 
    #// Default instance.
    #// 
    #// @since 4.8.1
    #// @var array
    #//
    default_instance = Array({"title": "", "content": ""})
    #// 
    #// Sets up a new Custom HTML widget instance.
    #// 
    #// @since 4.8.1
    #//
    def __init__(self):
        
        
        widget_ops_ = Array({"classname": "widget_custom_html", "description": __("Arbitrary HTML code."), "customize_selective_refresh": True})
        control_ops_ = Array({"width": 400, "height": 350})
        super().__init__("custom_html", __("Custom HTML"), widget_ops_, control_ops_)
    # end def __init__
    #// 
    #// Add hooks for enqueueing assets when registering all widget instances of this widget class.
    #// 
    #// @since 4.9.0
    #// 
    #// @param integer $number Optional. The unique order number of this widget instance
    #// compared to other instances of the same class. Default -1.
    #//
    def _register_one(self, number_=None):
        if number_ is None:
            number_ = -1
        # end if
        
        super()._register_one(number_)
        if self.registered:
            return
        # end if
        self.registered = True
        wp_add_inline_script("custom-html-widgets", php_sprintf("wp.customHtmlWidgets.idBases.push( %s );", wp_json_encode(self.id_base)))
        #// Note that the widgets component in the customizer will also do
        #// the 'admin_print_scripts-widgets.php' action in WP_Customize_Widgets::print_scripts().
        add_action("admin_print_scripts-widgets.php", Array(self, "enqueue_admin_scripts"))
        #// Note that the widgets component in the customizer will also do
        #// the 'admin_footer-widgets.php' action in WP_Customize_Widgets::print_footer_scripts().
        add_action("admin_footer-widgets.php", Array("WP_Widget_Custom_HTML", "render_control_template_scripts"))
        #// Note this action is used to ensure the help text is added to the end.
        add_action("admin_head-widgets.php", Array("WP_Widget_Custom_HTML", "add_help_text"))
    # end def _register_one
    #// 
    #// Filter gallery shortcode attributes.
    #// 
    #// Prevents all of a site's attachments from being shown in a gallery displayed on a
    #// non-singular template where a $post context is not available.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $attrs Attributes.
    #// @return array Attributes.
    #//
    def _filter_gallery_shortcode_attrs(self, attrs_=None):
        
        
        if (not is_singular()) and php_empty(lambda : attrs_["id"]) and php_empty(lambda : attrs_["include"]):
            attrs_["id"] = -1
        # end if
        return attrs_
    # end def _filter_gallery_shortcode_attrs
    #// 
    #// Outputs the content for the current Custom HTML widget instance.
    #// 
    #// @since 4.8.1
    #// 
    #// @global WP_Post $post Global post object.
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Custom HTML widget instance.
    #//
    def widget(self, args_=None, instance_=None):
        
        
        global post_
        php_check_if_defined("post_")
        #// Override global $post so filters (and shortcodes) apply in a consistent context.
        original_post_ = post_
        if is_singular():
            #// Make sure post is always the queried object on singular queries (not from another sub-query that failed to clean up the global $post).
            post_ = get_queried_object()
        else:
            #// Nullify the $post global during widget rendering to prevent shortcodes from running with the unexpected context on archive queries.
            post_ = None
        # end if
        #// Prevent dumping out all attachments from the media library.
        add_filter("shortcode_atts_gallery", Array(self, "_filter_gallery_shortcode_attrs"))
        instance_ = php_array_merge(self.default_instance, instance_)
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title_ = apply_filters("widget_title", instance_["title"], instance_, self.id_base)
        #// Prepare instance data that looks like a normal Text widget.
        simulated_text_widget_instance_ = php_array_merge(instance_, Array({"text": instance_["content"] if (php_isset(lambda : instance_["content"])) else "", "filter": False, "visual": False}))
        simulated_text_widget_instance_["content"] = None
        #// Was moved to 'text' prop.
        #// This filter is documented in wp-includes/widgets/class-wp-widget-text.php
        content_ = apply_filters("widget_text", instance_["content"], simulated_text_widget_instance_, self)
        #// Adds noreferrer and noopener relationships, without duplicating values, to all HTML A elements that have a target.
        content_ = wp_targeted_link_rel(content_)
        #// 
        #// Filters the content of the Custom HTML widget.
        #// 
        #// @since 4.8.1
        #// 
        #// @param string                $content  The widget content.
        #// @param array                 $instance Array of settings for the current widget.
        #// @param WP_Widget_Custom_HTML $this     Current Custom HTML widget instance.
        #//
        content_ = apply_filters("widget_custom_html_content", content_, instance_, self)
        #// Restore post global.
        post_ = original_post_
        remove_filter("shortcode_atts_gallery", Array(self, "_filter_gallery_shortcode_attrs"))
        #// Inject the Text widget's container class name alongside this widget's class name for theme styling compatibility.
        args_["before_widget"] = php_preg_replace("/(?<=\\sclass=[\"'])/", "widget_text ", args_["before_widget"])
        php_print(args_["before_widget"])
        if (not php_empty(lambda : title_)):
            php_print(args_["before_title"] + title_ + args_["after_title"])
        # end if
        php_print("<div class=\"textwidget custom-html-widget\">")
        #// The textwidget class is for theme styling compatibility.
        php_print(content_)
        php_print("</div>")
        php_print(args_["after_widget"])
    # end def widget
    #// 
    #// Handles updating settings for the current Custom HTML widget instance.
    #// 
    #// @since 4.8.1
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Settings to save or bool false to cancel saving.
    #//
    def update(self, new_instance_=None, old_instance_=None):
        
        
        instance_ = php_array_merge(self.default_instance, old_instance_)
        instance_["title"] = sanitize_text_field(new_instance_["title"])
        if current_user_can("unfiltered_html"):
            instance_["content"] = new_instance_["content"]
        else:
            instance_["content"] = wp_kses_post(new_instance_["content"])
        # end if
        return instance_
    # end def update
    #// 
    #// Loads the required scripts and styles for the widget control.
    #// 
    #// @since 4.9.0
    #//
    def enqueue_admin_scripts(self):
        
        
        settings_ = wp_enqueue_code_editor(Array({"type": "text/html", "codemirror": Array({"indentUnit": 2, "tabSize": 2})}))
        wp_enqueue_script("custom-html-widgets")
        if php_empty(lambda : settings_):
            settings_ = Array({"disabled": True})
        # end if
        wp_add_inline_script("custom-html-widgets", php_sprintf("wp.customHtmlWidgets.init( %s );", wp_json_encode(settings_)), "after")
        l10n_ = Array({"errorNotice": Array({"singular": _n("There is %d error which must be fixed before you can save.", "There are %d errors which must be fixed before you can save.", 1), "plural": _n("There is %d error which must be fixed before you can save.", "There are %d errors which must be fixed before you can save.", 2)})})
        wp_add_inline_script("custom-html-widgets", php_sprintf("jQuery.extend( wp.customHtmlWidgets.l10n, %s );", wp_json_encode(l10n_)), "after")
    # end def enqueue_admin_scripts
    #// 
    #// Outputs the Custom HTML widget settings form.
    #// 
    #// @since 4.8.1
    #// @since 4.9.0 The form contains only hidden sync inputs. For the control UI, see `WP_Widget_Custom_HTML::render_control_template_scripts()`.
    #// 
    #// @see WP_Widget_Custom_HTML::render_control_template_scripts()
    #// 
    #// @param array $instance Current instance.
    #//
    def form(self, instance_=None):
        
        
        instance_ = wp_parse_args(instance_, self.default_instance)
        php_print("     <input id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" class=\"title sync-input\" type=\"hidden\" value=\"")
        php_print(esc_attr(instance_["title"]))
        php_print("\"/>\n       <textarea id=\"")
        php_print(self.get_field_id("content"))
        php_print("\" name=\"")
        php_print(self.get_field_name("content"))
        php_print("\" class=\"content sync-input\" hidden>")
        php_print(esc_textarea(instance_["content"]))
        php_print("</textarea>\n        ")
    # end def form
    #// 
    #// Render form template scripts.
    #// 
    #// @since 4.9.0
    #//
    @classmethod
    def render_control_template_scripts(self):
        
        
        php_print("""       <script type=\"text/html\" id=\"tmpl-widget-custom-html-control-fields\">
        <# var elementIdPrefix = 'el' + String( Math.random() ).replace( /\\D/g, '' ) + '_' #>
        <p>
        <label for=\"{{ elementIdPrefix }}title\">""")
        esc_html_e("Title:")
        php_print("""</label>
        <input id=\"{{ elementIdPrefix }}title\" type=\"text\" class=\"widefat title\">
        </p>
        <p>
        <label for=\"{{ elementIdPrefix }}content\" id=\"{{ elementIdPrefix }}content-label\">""")
        esc_html_e("Content:")
        php_print("""</label>
        <textarea id=\"{{ elementIdPrefix }}content\" class=\"widefat code content\" rows=\"16\" cols=\"20\"></textarea>
        </p>
        """)
        if (not current_user_can("unfiltered_html")):
            php_print("             ")
            probably_unsafe_html_ = Array("script", "iframe", "form", "input", "style")
            allowed_html_ = wp_kses_allowed_html("post")
            disallowed_html_ = php_array_diff(probably_unsafe_html_, php_array_keys(allowed_html_))
            php_print("             ")
            if (not php_empty(lambda : disallowed_html_)):
                php_print("                 <# if ( data.codeEditorDisabled ) { #>\n                        <p>\n                           ")
                _e("Some HTML tags are not permitted, including:")
                php_print("                         <code>")
                php_print(join("</code>, <code>", disallowed_html_))
                php_print("""</code>
                </p>
                <# } #>
                """)
            # end if
            php_print("         ")
        # end if
        php_print("""
        <div class=\"code-editor-error-container\"></div>
        </script>
        """)
    # end def render_control_template_scripts
    #// 
    #// Add help text to widgets admin screen.
    #// 
    #// @since 4.9.0
    #//
    @classmethod
    def add_help_text(self):
        
        
        screen_ = get_current_screen()
        content_ = "<p>"
        content_ += __("Use the Custom HTML widget to add arbitrary HTML code to your widget areas.")
        content_ += "</p>"
        if "false" != wp_get_current_user().syntax_highlighting:
            content_ += "<p>"
            content_ += php_sprintf(__("The edit field automatically highlights code syntax. You can disable this in your <a href=\"%1$s\" %2$s>user profile%3$s</a> to work in plain text mode."), esc_url(get_edit_profile_url()), "class=\"external-link\" target=\"_blank\"", php_sprintf("<span class=\"screen-reader-text\"> %s</span>", __("(opens in a new tab)")))
            content_ += "</p>"
            content_ += "<p id=\"editor-keyboard-trap-help-1\">" + __("When using a keyboard to navigate:") + "</p>"
            content_ += "<ul>"
            content_ += "<li id=\"editor-keyboard-trap-help-2\">" + __("In the editing area, the Tab key enters a tab character.") + "</li>"
            content_ += "<li id=\"editor-keyboard-trap-help-3\">" + __("To move away from this area, press the Esc key followed by the Tab key.") + "</li>"
            content_ += "<li id=\"editor-keyboard-trap-help-4\">" + __("Screen reader users: when in forms mode, you may need to press the Esc key twice.") + "</li>"
            content_ += "</ul>"
        # end if
        screen_.add_help_tab(Array({"id": "custom_html_widget", "title": __("Custom HTML Widget"), "content": content_}))
    # end def add_help_text
# end class WP_Widget_Custom_HTML
