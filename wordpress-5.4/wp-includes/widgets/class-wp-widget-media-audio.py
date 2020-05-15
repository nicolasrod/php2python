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
#// Widget API: WP_Widget_Media_Audio class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.8.0
#// 
#// 
#// Core class that implements an audio widget.
#// 
#// @since 4.8.0
#// 
#// @see WP_Widget_Media
#// @see WP_Widget
#//
class WP_Widget_Media_Audio(WP_Widget_Media):
    #// 
    #// Constructor.
    #// 
    #// @since 4.8.0
    #//
    def __init__(self):
        
        super().__init__("media_audio", __("Audio"), Array({"description": __("Displays an audio player."), "mime_type": "audio"}))
        self.l10n = php_array_merge(self.l10n, Array({"no_media_selected": __("No audio selected"), "add_media": _x("Add Audio", "label for button in the audio widget"), "replace_media": _x("Replace Audio", "label for button in the audio widget; should preferably not be longer than ~13 characters long"), "edit_media": _x("Edit Audio", "label for button in the audio widget; should preferably not be longer than ~13 characters long"), "missing_attachment": php_sprintf(__("We can&#8217;t find that audio file. Check your <a href=\"%s\">media library</a> and make sure it wasn&#8217;t deleted."), esc_url(admin_url("upload.php"))), "media_library_state_multi": _n_noop("Audio Widget (%d)", "Audio Widget (%d)"), "media_library_state_single": __("Audio Widget"), "unsupported_file_type": __("Looks like this isn&#8217;t the correct kind of file. Please link to an audio file instead.")}))
    # end def __init__
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
        
        schema = Array({"preload": Array({"type": "string", "enum": Array("none", "auto", "metadata"), "default": "none", "description": __("Preload")})}, {"loop": Array({"type": "boolean", "default": False, "description": __("Loop")})})
        for audio_extension in wp_get_audio_extensions():
            schema[audio_extension] = Array({"type": "string", "default": "", "format": "uri", "description": php_sprintf(__("URL to the %s audio source file"), audio_extension)})
        # end for
        return php_array_merge(schema, super().get_instance_schema())
    # end def get_instance_schema
    #// 
    #// Render the media on the frontend.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array $instance Widget instance props.
    #//
    def render_media(self, instance=None):
        
        instance = php_array_merge(wp_list_pluck(self.get_instance_schema(), "default"), instance)
        attachment = None
        if self.is_attachment_with_mime_type(instance["attachment_id"], self.widget_options["mime_type"]):
            attachment = get_post(instance["attachment_id"])
        # end if
        if attachment:
            src = wp_get_attachment_url(attachment.ID)
        else:
            src = instance["url"]
        # end if
        php_print(wp_audio_shortcode(php_array_merge(instance, compact("src"))))
    # end def render_media
    #// 
    #// Enqueue preview scripts.
    #// 
    #// These scripts normally are enqueued just-in-time when an audio shortcode is used.
    #// In the customizer, however, widgets can be dynamically added and rendered via
    #// selective refresh, and so it is important to unconditionally enqueue them in
    #// case a widget does get added.
    #// 
    #// @since 4.8.0
    #//
    def enqueue_preview_scripts(self):
        
        #// This filter is documented in wp-includes/media.php
        if "mediaelement" == apply_filters("wp_audio_shortcode_library", "mediaelement"):
            wp_enqueue_style("wp-mediaelement")
            wp_enqueue_script("wp-mediaelement")
        # end if
    # end def enqueue_preview_scripts
    #// 
    #// Loads the required media files for the media manager and scripts for media widgets.
    #// 
    #// @since 4.8.0
    #//
    def enqueue_admin_scripts(self):
        
        super().enqueue_admin_scripts()
        wp_enqueue_style("wp-mediaelement")
        wp_enqueue_script("wp-mediaelement")
        handle = "media-audio-widget"
        wp_enqueue_script(handle)
        exported_schema = Array()
        for field,field_schema in self.get_instance_schema():
            exported_schema[field] = wp_array_slice_assoc(field_schema, Array("type", "default", "enum", "minimum", "format", "media_prop", "should_preview_update"))
        # end for
        wp_add_inline_script(handle, php_sprintf("wp.mediaWidgets.modelConstructors[ %s ].prototype.schema = %s;", wp_json_encode(self.id_base), wp_json_encode(exported_schema)))
        wp_add_inline_script(handle, php_sprintf("""
        wp.mediaWidgets.controlConstructors[ %1$s ].prototype.mime_type = %2$s;
        wp.mediaWidgets.controlConstructors[ %1$s ].prototype.l10n = _.extend( {}, wp.mediaWidgets.controlConstructors[ %1$s ].prototype.l10n, %3$s );
        """, wp_json_encode(self.id_base), wp_json_encode(self.widget_options["mime_type"]), wp_json_encode(self.l10n)))
    # end def enqueue_admin_scripts
    #// 
    #// Render form template scripts.
    #// 
    #// @since 4.8.0
    #//
    def render_control_template_scripts(self):
        
        super().render_control_template_scripts()
        php_print("""       <script type=\"text/html\" id=\"tmpl-wp-media-widget-audio-preview\">
        <# if ( data.error && 'missing_attachment' === data.error ) { #>
        <div class=\"notice notice-error notice-alt notice-missing-attachment\">
        <p>""")
        php_print(self.l10n["missing_attachment"])
        php_print("""</p>
        </div>
        <# } else if ( data.error ) { #>
        <div class=\"notice notice-error notice-alt\">
        <p>""")
        _e("Unable to preview media due to an unknown error.")
        php_print("""</p>
        </div>
        <# } else if ( data.model && data.model.src ) { #>
        """)
        wp_underscore_audio_template()
        php_print("         <# } #>\n       </script>\n     ")
    # end def render_control_template_scripts
# end class WP_Widget_Media_Audio
