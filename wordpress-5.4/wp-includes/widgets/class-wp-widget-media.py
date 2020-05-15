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
#// Widget API: WP_Media_Widget class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.8.0
#// 
#// 
#// Core class that implements a media widget.
#// 
#// @since 4.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Media(WP_Widget):
    l10n = Array({"add_to_widget": "", "replace_media": "", "edit_media": "", "media_library_state_multi": "", "media_library_state_single": "", "missing_attachment": "", "no_media_selected": "", "add_media": ""})
    registered = False
    #// 
    #// Constructor.
    #// 
    #// @since 4.8.0
    #// 
    #// @param string $id_base         Base ID for the widget, lowercase and unique.
    #// @param string $name            Name for the widget displayed on the configuration page.
    #// @param array  $widget_options  Optional. Widget options. See wp_register_sidebar_widget() for
    #// information on accepted arguments. Default empty array.
    #// @param array  $control_options Optional. Widget control options. See wp_register_widget_control()
    #// for information on accepted arguments. Default empty array.
    #//
    def __init__(self, id_base=None, name=None, widget_options=Array(), control_options=Array()):
        
        widget_opts = wp_parse_args(widget_options, Array({"description": __("A media item."), "customize_selective_refresh": True, "mime_type": ""}))
        control_opts = wp_parse_args(control_options, Array())
        l10n_defaults = Array({"no_media_selected": __("No media selected"), "add_media": _x("Add Media", "label for button in the media widget"), "replace_media": _x("Replace Media", "label for button in the media widget; should preferably not be longer than ~13 characters long"), "edit_media": _x("Edit Media", "label for button in the media widget; should preferably not be longer than ~13 characters long"), "add_to_widget": __("Add to Widget"), "missing_attachment": php_sprintf(__("We can&#8217;t find that file. Check your <a href=\"%s\">media library</a> and make sure it wasn&#8217;t deleted."), esc_url(admin_url("upload.php"))), "media_library_state_multi": _n_noop("Media Widget (%d)", "Media Widget (%d)"), "media_library_state_single": __("Media Widget"), "unsupported_file_type": __("Looks like this isn&#8217;t the correct kind of file. Please link to an appropriate file instead.")})
        self.l10n = php_array_merge(l10n_defaults, php_array_filter(self.l10n))
        super().__init__(id_base, name, widget_opts, control_opts)
    # end def __init__
    #// 
    #// Add hooks while registering all widget instances of this widget class.
    #// 
    #// @since 4.8.0
    #// 
    #// @param integer $number Optional. The unique order number of this widget instance
    #// compared to other instances of the same class. Default -1.
    #//
    def _register_one(self, number=-1):
        
        super()._register_one(number)
        if self.registered:
            return
        # end if
        self.registered = True
        #// Note that the widgets component in the customizer will also do
        #// the 'admin_print_scripts-widgets.php' action in WP_Customize_Widgets::print_scripts().
        add_action("admin_print_scripts-widgets.php", Array(self, "enqueue_admin_scripts"))
        if self.is_preview():
            add_action("wp_enqueue_scripts", Array(self, "enqueue_preview_scripts"))
        # end if
        #// Note that the widgets component in the customizer will also do
        #// the 'admin_footer-widgets.php' action in WP_Customize_Widgets::print_footer_scripts().
        add_action("admin_footer-widgets.php", Array(self, "render_control_template_scripts"))
        add_filter("display_media_states", Array(self, "display_media_state"), 10, 2)
    # end def _register_one
    #// 
    #// Get schema for properties of a widget instance (item).
    #// 
    #// @since 4.8.0
    #// 
    #// @see WP_REST_Controller::get_item_schema()
    #// @see WP_REST_Controller::get_additional_fields()
    #// @link https://core.trac.wordpress.org/ticket/35574
    #// 
    #// @return array Schema for properties.
    #//
    def get_instance_schema(self):
        
        schema = Array({"attachment_id": Array({"type": "integer", "default": 0, "minimum": 0, "description": __("Attachment post ID"), "media_prop": "id"})}, {"url": Array({"type": "string", "default": "", "format": "uri", "description": __("URL to the media file")})}, {"title": Array({"type": "string", "default": "", "sanitize_callback": "sanitize_text_field", "description": __("Title for the widget"), "should_preview_update": False})})
        #// 
        #// Filters the media widget instance schema to add additional properties.
        #// 
        #// @since 4.9.0
        #// 
        #// @param array           $schema Instance schema.
        #// @param WP_Widget_Media $this   Widget object.
        #//
        schema = apply_filters(str("widget_") + str(self.id_base) + str("_instance_schema"), schema, self)
        return schema
    # end def get_instance_schema
    #// 
    #// Determine if the supplied attachment is for a valid attachment post with the specified MIME type.
    #// 
    #// @since 4.8.0
    #// 
    #// @param int|WP_Post $attachment Attachment post ID or object.
    #// @param string      $mime_type  MIME type.
    #// @return bool Is matching MIME type.
    #//
    def is_attachment_with_mime_type(self, attachment=None, mime_type=None):
        
        if php_empty(lambda : attachment):
            return False
        # end if
        attachment = get_post(attachment)
        if (not attachment):
            return False
        # end if
        if "attachment" != attachment.post_type:
            return False
        # end if
        return wp_attachment_is(mime_type, attachment)
    # end def is_attachment_with_mime_type
    #// 
    #// Sanitize a token list string, such as used in HTML rel and class attributes.
    #// 
    #// @since 4.8.0
    #// 
    #// @link http://w3c.github.io/html/infrastructure.html#space-separated-tokens
    #// @link https://developer.mozilla.org/en-US/docs/Web/API/DOMTokenList
    #// @param string|array $tokens List of tokens separated by spaces, or an array of tokens.
    #// @return string Sanitized token string list.
    #//
    def sanitize_token_list(self, tokens=None):
        
        if php_is_string(tokens):
            tokens = php_preg_split("/\\s+/", php_trim(tokens))
        # end if
        tokens = php_array_map("sanitize_html_class", tokens)
        tokens = php_array_filter(tokens)
        return join(" ", tokens)
    # end def sanitize_token_list
    #// 
    #// Displays the widget on the front-end.
    #// 
    #// @since 4.8.0
    #// 
    #// @see WP_Widget::widget()
    #// 
    #// @param array $args     Display arguments including before_title, after_title, before_widget, and after_widget.
    #// @param array $instance Saved setting from the database.
    #//
    def widget(self, args=None, instance=None):
        
        instance = wp_parse_args(instance, wp_list_pluck(self.get_instance_schema(), "default"))
        #// Short-circuit if no media is selected.
        if (not self.has_content(instance)):
            return
        # end if
        php_print(args["before_widget"])
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", instance["title"], instance, self.id_base)
        if title:
            php_print(args["before_title"] + title + args["after_title"])
        # end if
        #// 
        #// Filters the media widget instance prior to rendering the media.
        #// 
        #// @since 4.8.0
        #// 
        #// @param array           $instance Instance data.
        #// @param array           $args     Widget args.
        #// @param WP_Widget_Media $this     Widget object.
        #//
        instance = apply_filters(str("widget_") + str(self.id_base) + str("_instance"), instance, args, self)
        self.render_media(instance)
        php_print(args["after_widget"])
    # end def widget
    #// 
    #// Sanitizes the widget form values as they are saved.
    #// 
    #// @since 4.8.0
    #// 
    #// @see WP_Widget::update()
    #// @see WP_REST_Request::has_valid_params()
    #// @see WP_REST_Request::sanitize_params()
    #// 
    #// @param array $new_instance Values just sent to be saved.
    #// @param array $instance     Previously saved values from database.
    #// @return array Updated safe values to be saved.
    #//
    def update(self, new_instance=None, instance=None):
        
        schema = self.get_instance_schema()
        for field,field_schema in schema:
            if (not php_array_key_exists(field, new_instance)):
                continue
            # end if
            value = new_instance[field]
            #// 
            #// Workaround for rest_validate_value_from_schema() due to the fact that
            #// rest_is_boolean( '' ) === false, while rest_is_boolean( '1' ) is true.
            #//
            if "boolean" == field_schema["type"] and "" == value:
                value = False
            # end if
            if True != rest_validate_value_from_schema(value, field_schema, field):
                continue
            # end if
            value = rest_sanitize_value_from_schema(value, field_schema)
            #// @codeCoverageIgnoreStart
            if is_wp_error(value):
                continue
                pass
            # end if
            #// @codeCoverageIgnoreEnd
            if (php_isset(lambda : field_schema["sanitize_callback"])):
                value = php_call_user_func(field_schema["sanitize_callback"], value)
            # end if
            if is_wp_error(value):
                continue
            # end if
            instance[field] = value
        # end for
        return instance
    # end def update
    #// 
    #// Render the media on the frontend.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array $instance Widget instance props.
    #// @return string
    #//
    def render_media(self, instance=None):
        
        pass
    # end def render_media
    #// 
    #// Outputs the settings update form.
    #// 
    #// Note that the widget UI itself is rendered with JavaScript via `MediaWidgetControl#render()`.
    #// 
    #// @since 4.8.0
    #// 
    #// @see \WP_Widget_Media::render_control_template_scripts() Where the JS template is located.
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        instance_schema = self.get_instance_schema()
        instance = wp_array_slice_assoc(wp_parse_args(instance, wp_list_pluck(instance_schema, "default")), php_array_keys(instance_schema))
        for name,value in instance:
            php_print("         <input\n                type=\"hidden\"\n               data-property=\"")
            php_print(esc_attr(name))
            php_print("\"\n             class=\"media-widget-instance-property\"\n              name=\"")
            php_print(esc_attr(self.get_field_name(name)))
            php_print("\"\n             id=\"")
            php_print(esc_attr(self.get_field_id(name)))
            pass
            php_print("\"\n             value=\"")
            php_print(esc_attr(join(",", value) if php_is_array(value) else php_strval(value)))
            php_print("\"\n         />\n            ")
        # end for
    # end def form
    #// 
    #// Filters the default media display states for items in the Media list table.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array   $states An array of media states.
    #// @param WP_Post $post   The current attachment object.
    #// @return array
    #//
    def display_media_state(self, states=None, post=None):
        
        if (not post):
            post = get_post()
        # end if
        #// Count how many times this attachment is used in widgets.
        use_count = 0
        for instance in self.get_settings():
            if (php_isset(lambda : instance["attachment_id"])) and instance["attachment_id"] == post.ID:
                use_count += 1
            # end if
        # end for
        if 1 == use_count:
            states[-1] = self.l10n["media_library_state_single"]
        elif use_count > 0:
            states[-1] = php_sprintf(translate_nooped_plural(self.l10n["media_library_state_multi"], use_count), number_format_i18n(use_count))
        # end if
        return states
    # end def display_media_state
    #// 
    #// Enqueue preview scripts.
    #// 
    #// These scripts normally are enqueued just-in-time when a widget is rendered.
    #// In the customizer, however, widgets can be dynamically added and rendered via
    #// selective refresh, and so it is important to unconditionally enqueue them in
    #// case a widget does get added.
    #// 
    #// @since 4.8.0
    #//
    def enqueue_preview_scripts(self):
        
        pass
    # end def enqueue_preview_scripts
    #// 
    #// Loads the required scripts and styles for the widget control.
    #// 
    #// @since 4.8.0
    #//
    def enqueue_admin_scripts(self):
        
        wp_enqueue_media()
        wp_enqueue_script("media-widgets")
    # end def enqueue_admin_scripts
    #// 
    #// Render form template scripts.
    #// 
    #// @since 4.8.0
    #//
    def render_control_template_scripts(self):
        
        php_print("     <script type=\"text/html\" id=\"tmpl-widget-media-")
        php_print(esc_attr(self.id_base))
        php_print("""-control\">
        <# var elementIdPrefix = 'el' + String( Math.random() ) + '_' #>
        <p>
        <label for=\"{{ elementIdPrefix }}title\">""")
        esc_html_e("Title:")
        php_print("""</label>
        <input id=\"{{ elementIdPrefix }}title\" type=\"text\" class=\"widefat title\">
        </p>
        <div class=\"media-widget-preview """)
        php_print(esc_attr(self.id_base))
        php_print("""\">
        <div class=\"attachment-media-view\">
        <button type=\"button\" class=\"select-media button-add-media not-selected\">
        """)
        php_print(esc_html(self.l10n["add_media"]))
        php_print("""                   </button>
        </div>
        </div>
        <p class=\"media-widget-buttons\">
        <button type=\"button\" class=\"button edit-media selected\">
        """)
        php_print(esc_html(self.l10n["edit_media"]))
        php_print("             </button>\n         ")
        if (not php_empty(lambda : self.l10n["replace_media"])):
            php_print("             <button type=\"button\" class=\"button change-media select-media selected\">\n                  ")
            php_print(esc_html(self.l10n["replace_media"]))
            php_print("             </button>\n         ")
        # end if
        php_print("""           </p>
        <div class=\"media-widget-fields\">
        </div>
        </script>
        """)
    # end def render_control_template_scripts
    #// 
    #// Whether the widget has content to show.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array $instance Widget instance props.
    #// @return bool Whether widget has content.
    #//
    def has_content(self, instance=None):
        
        return instance["attachment_id"] and "attachment" == get_post_type(instance["attachment_id"]) or instance["url"]
    # end def has_content
# end class WP_Widget_Media
