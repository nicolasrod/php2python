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
#// Widget API: WP_Widget_Media_Gallery class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.9.0
#// 
#// 
#// Core class that implements a gallery widget.
#// 
#// @since 4.9.0
#// 
#// @see WP_Widget_Media
#// @see WP_Widget
#//
class WP_Widget_Media_Gallery(WP_Widget_Media):
    #// 
    #// Constructor.
    #// 
    #// @since 4.9.0
    #//
    def __init__(self):
        
        
        super().__init__("media_gallery", __("Gallery"), Array({"description": __("Displays an image gallery."), "mime_type": "image"}))
        self.l10n = php_array_merge(self.l10n, Array({"no_media_selected": __("No images selected"), "add_media": _x("Add Images", "label for button in the gallery widget; should not be longer than ~13 characters long"), "replace_media": "", "edit_media": _x("Edit Gallery", "label for button in the gallery widget; should not be longer than ~13 characters long")}))
    # end def __init__
    #// 
    #// Get schema for properties of a widget instance (item).
    #// 
    #// @since 4.9.0
    #// 
    #// @see WP_REST_Controller::get_item_schema()
    #// @see WP_REST_Controller::get_additional_fields()
    #// @link https://core.trac.wordpress.org/ticket/35574
    #// 
    #// @return array Schema for properties.
    #//
    def get_instance_schema(self):
        
        
        schema_ = Array({"title": Array({"type": "string", "default": "", "sanitize_callback": "sanitize_text_field", "description": __("Title for the widget"), "should_preview_update": False})}, {"ids": Array({"type": "array", "items": Array({"type": "integer"})}, {"default": Array(), "sanitize_callback": "wp_parse_id_list"})}, {"columns": Array({"type": "integer", "default": 3, "minimum": 1, "maximum": 9})}, {"size": Array({"type": "string", "enum": php_array_merge(get_intermediate_image_sizes(), Array("full", "custom")), "default": "thumbnail"})}, {"link_type": Array({"type": "string", "enum": Array("post", "file", "none"), "default": "post", "media_prop": "link", "should_preview_update": False})}, {"orderby_random": Array({"type": "boolean", "default": False, "media_prop": "_orderbyRandom", "should_preview_update": False})})
        #// This filter is documented in wp-includes/widgets/class-wp-widget-media.php
        schema_ = apply_filters(str("widget_") + str(self.id_base) + str("_instance_schema"), schema_, self)
        return schema_
    # end def get_instance_schema
    #// 
    #// Render the media on the frontend.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $instance Widget instance props.
    #//
    def render_media(self, instance_=None):
        
        
        instance_ = php_array_merge(wp_list_pluck(self.get_instance_schema(), "default"), instance_)
        shortcode_atts_ = php_array_merge(instance_, Array({"link": instance_["link_type"]}))
        #// @codeCoverageIgnoreStart
        if instance_["orderby_random"]:
            shortcode_atts_["orderby"] = "rand"
        # end if
        #// @codeCoverageIgnoreEnd
        php_print(gallery_shortcode(shortcode_atts_))
    # end def render_media
    #// 
    #// Loads the required media files for the media manager and scripts for media widgets.
    #// 
    #// @since 4.9.0
    #//
    def enqueue_admin_scripts(self):
        
        
        super().enqueue_admin_scripts()
        handle_ = "media-gallery-widget"
        wp_enqueue_script(handle_)
        exported_schema_ = Array()
        for field_,field_schema_ in self.get_instance_schema():
            exported_schema_[field_] = wp_array_slice_assoc(field_schema_, Array("type", "default", "enum", "minimum", "format", "media_prop", "should_preview_update", "items"))
        # end for
        wp_add_inline_script(handle_, php_sprintf("wp.mediaWidgets.modelConstructors[ %s ].prototype.schema = %s;", wp_json_encode(self.id_base), wp_json_encode(exported_schema_)))
        wp_add_inline_script(handle_, php_sprintf("""
        wp.mediaWidgets.controlConstructors[ %1$s ].prototype.mime_type = %2$s;
        _.extend( wp.mediaWidgets.controlConstructors[ %1$s ].prototype.l10n, %3$s );
        """, wp_json_encode(self.id_base), wp_json_encode(self.widget_options["mime_type"]), wp_json_encode(self.l10n)))
    # end def enqueue_admin_scripts
    #// 
    #// Render form template scripts.
    #// 
    #// @since 4.9.0
    #//
    def render_control_template_scripts(self):
        
        
        super().render_control_template_scripts()
        php_print("""       <script type=\"text/html\" id=\"tmpl-wp-media-widget-gallery-preview\">
        <#
        var ids = _.filter( data.ids, function( id ) {
        return ( id in data.attachments );
        } );
        #>
        <# if ( ids.length ) { #>
        <ul class=\"gallery media-widget-gallery-preview\" role=\"list\">
        <# _.each( ids, function( id, index ) { #>
        <# var attachment = data.attachments[ id ]; #>
        <# if ( index < 6 ) { #>
        <li class=\"gallery-item\">
        <div class=\"gallery-icon\">
        <img alt=\"{{ attachment.alt }}\"
        <# if ( index === 5 && data.ids.length > 6 ) { #> aria-hidden=\"true\" <# } #>
        <# if ( attachment.sizes.thumbnail ) { #>
        src=\"{{ attachment.sizes.thumbnail.url }}\" width=\"{{ attachment.sizes.thumbnail.width }}\" height=\"{{ attachment.sizes.thumbnail.height }}\"
        <# } else { #>
        src=\"{{ attachment.url }}\"
        <# } #>
        <# if ( ! attachment.alt && attachment.filename ) { #>
        aria-label=\"
        """)
        php_print(esc_attr(php_sprintf(__("The current image has no alternative text. The file name is: %s"), "{{ attachment.filename }}")))
        php_print("""                                           \"
        <# } #>
        />
        <# if ( index === 5 && data.ids.length > 6 ) { #>
        <div class=\"gallery-icon-placeholder\">
        <p class=\"gallery-icon-placeholder-text\" aria-label=\"
        """)
        printf(__("Additional images added to this gallery: %s"), "{{ data.ids.length - 5 }}")
        php_print("""                                       \">+{{ data.ids.length - 5 }}</p>
        </div>
        <# } #>
        </div>
        </li>
        <# } #>
        <# } ); #>
        </ul>
        <# } else { #>
        <div class=\"attachment-media-view\">
        <button type=\"button\" class=\"placeholder button-add-media\">""")
        php_print(esc_html(self.l10n["add_media"]))
        php_print("""</button>
        </div>
        <# } #>
        </script>
        """)
    # end def render_control_template_scripts
    #// 
    #// Whether the widget has content to show.
    #// 
    #// @since 4.9.0
    #// @access protected
    #// 
    #// @param array $instance Widget instance props.
    #// @return bool Whether widget has content.
    #//
    def has_content(self, instance_=None):
        
        
        if (not php_empty(lambda : instance_["ids"])):
            attachments_ = wp_parse_id_list(instance_["ids"])
            for attachment_ in attachments_:
                if "attachment" != get_post_type(attachment_):
                    return False
                # end if
            # end for
            return True
        # end if
        return False
    # end def has_content
# end class WP_Widget_Media_Gallery
