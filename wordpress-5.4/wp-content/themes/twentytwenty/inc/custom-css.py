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
#// Twenty Twenty Custom CSS
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if (not php_function_exists("twentytwenty_generate_css")):
    #// 
    #// Generate CSS.
    #// 
    #// @param string $selector The CSS selector.
    #// @param string $style The CSS style.
    #// @param string $value The CSS value.
    #// @param string $prefix The CSS prefix.
    #// @param string $suffix The CSS suffix.
    #// @param bool   $echo Echo the styles.
    #//
    def twentytwenty_generate_css(selector_=None, style_=None, value_=None, prefix_="", suffix_="", echo_=None, *_args_):
        if echo_ is None:
            echo_ = True
        # end if
        
        return_ = ""
        #// 
        #// Bail early if we have no $selector elements or properties and $value.
        #//
        if (not value_) or (not selector_):
            return
        # end if
        return_ = php_sprintf("%s { %s: %s; }", selector_, style_, prefix_ + value_ + suffix_)
        if echo_:
            php_print(return_)
            pass
        # end if
        return return_
    # end def twentytwenty_generate_css
# end if
if (not php_function_exists("twentytwenty_get_customizer_css")):
    #// 
    #// Get CSS Built from Customizer Options.
    #// Build CSS reflecting colors, fonts and other options set in the Customizer, and return them for output.
    #// 
    #// @param string $type Whether to return CSS for the "front-end", "block-editor" or "classic-editor".
    #//
    def twentytwenty_get_customizer_css(type_="front-end", *_args_):
        
        
        #// Get variables.
        body_ = sanitize_hex_color(twentytwenty_get_color_for_area("content", "text"))
        body_default_ = "#000000"
        secondary_ = sanitize_hex_color(twentytwenty_get_color_for_area("content", "secondary"))
        secondary_default_ = "#6d6d6d"
        borders_ = sanitize_hex_color(twentytwenty_get_color_for_area("content", "borders"))
        borders_default_ = "#dcd7ca"
        accent_ = sanitize_hex_color(twentytwenty_get_color_for_area("content", "accent"))
        accent_default_ = "#cd2653"
        #// Header.
        header_footer_background_ = sanitize_hex_color(twentytwenty_get_color_for_area("header-footer", "background"))
        header_footer_background_default_ = "#ffffff"
        #// Cover.
        cover_ = sanitize_hex_color(get_theme_mod("cover_template_overlay_text_color"))
        cover_default_ = "#ffffff"
        #// Background.
        background_ = sanitize_hex_color_no_hash(get_theme_mod("background_color"))
        background_default_ = "f5efe0"
        ob_start()
        #// 
        #// Note – Styles are applied in this order:
        #// 1. Element specific
        #// 2. Helper classes
        #// 
        #// This enables all helper classes to overwrite base element styles,
        #// meaning that any color classes applied in the block editor will
        #// have a higher priority than the base element styles.
        #// 
        #// Front-End Styles.
        if "front-end" == type_:
            #// Auto-calculated colors.
            elements_definitions_ = twentytwenty_get_elements_array()
            for context_,props_ in elements_definitions_.items():
                for key_,definitions_ in props_.items():
                    for property_,elements_ in definitions_.items():
                        #// 
                        #// If we don't have an elements array or it is empty
                        #// then skip this iteration early;
                        #//
                        if (not php_is_array(elements_)) or php_empty(lambda : elements_):
                            continue
                        # end if
                        val_ = twentytwenty_get_color_for_area(context_, key_)
                        if val_:
                            twentytwenty_generate_css(php_implode(",", elements_), property_, val_)
                        # end if
                    # end for
                # end for
            # end for
            if cover_ and cover_ != cover_default_:
                twentytwenty_generate_css(".overlay-header .header-inner", "color", cover_)
                twentytwenty_generate_css(".cover-header .entry-header *", "color", cover_)
            # end if
            pass
        elif "block-editor" == type_:
            #// Colors.
            #// Accent color.
            if accent_ and accent_ != accent_default_:
                twentytwenty_generate_css(".has-accent-color, .editor-styles-wrapper .editor-block-list__layout a, .editor-styles-wrapper .has-drop-cap:not(:focus)::first-letter, .editor-styles-wrapper .wp-block-button.is-style-outline .wp-block-button__link, .editor-styles-wrapper .wp-block-pullquote::before, .editor-styles-wrapper .wp-block-file .wp-block-file__textlink", "color", accent_)
                twentytwenty_generate_css(".editor-styles-wrapper .wp-block-quote", "border-color", accent_, "")
                twentytwenty_generate_css(".has-accent-background-color, .editor-styles-wrapper .wp-block-button__link, .editor-styles-wrapper .wp-block-file__button", "background-color", accent_)
            # end if
            #// Background color.
            if background_ and background_ != background_default_:
                twentytwenty_generate_css(".editor-styles-wrapper", "background-color", "#" + background_)
                twentytwenty_generate_css(".has-background.has-primary-background-color:not(.has-text-color),.has-background.has-primary-background-color *:not(.has-text-color),.has-background.has-accent-background-color:not(.has-text-color),.has-background.has-accent-background-color *:not(.has-text-color)", "color", "#" + background_)
            # end if
            #// Borders color.
            if borders_ and borders_ != borders_default_:
                twentytwenty_generate_css(".editor-styles-wrapper .wp-block-code, .editor-styles-wrapper pre, .editor-styles-wrapper .wp-block-preformatted pre, .editor-styles-wrapper .wp-block-verse pre, .editor-styles-wrapper fieldset, .editor-styles-wrapper .wp-block-table, .editor-styles-wrapper .wp-block-table *, .editor-styles-wrapper .wp-block-table.is-style-stripes, .editor-styles-wrapper .wp-block-latest-posts.is-grid li", "border-color", borders_)
                twentytwenty_generate_css(".editor-styles-wrapper .wp-block-table caption, .editor-styles-wrapper .wp-block-table.is-style-stripes tbody tr:nth-child(odd)", "background-color", borders_)
            # end if
            #// Text color.
            if body_ and body_ != body_default_:
                twentytwenty_generate_css("body .editor-styles-wrapper, .editor-post-title__block .editor-post-title__input, .editor-post-title__block .editor-post-title__input:focus", "color", body_)
            # end if
            #// Secondary color.
            if secondary_ and secondary_ != secondary_default_:
                twentytwenty_generate_css(".editor-styles-wrapper figcaption, .editor-styles-wrapper cite, .editor-styles-wrapper .wp-block-quote__citation, .editor-styles-wrapper .wp-block-quote cite, .editor-styles-wrapper .wp-block-quote footer, .editor-styles-wrapper .wp-block-pullquote__citation, .editor-styles-wrapper .wp-block-pullquote cite, .editor-styles-wrapper .wp-block-pullquote footer, .editor-styles-wrapper ul.wp-block-archives li, .editor-styles-wrapper ul.wp-block-categories li, .editor-styles-wrapper ul.wp-block-latest-posts li, .editor-styles-wrapper ul.wp-block-categories__list li, .editor-styles-wrapper .wp-block-latest-comments time, .editor-styles-wrapper .wp-block-latest-posts time", "color", secondary_)
            # end if
            #// Header Footer Background Color.
            if header_footer_background_ and header_footer_background_ != header_footer_background_default_:
                twentytwenty_generate_css(".editor-styles-wrapper .wp-block-pullquote::before", "background-color", header_footer_background_)
            # end if
        elif "classic-editor" == type_:
            #// Colors.
            #// Accent color.
            if accent_ and accent_ != accent_default_:
                twentytwenty_generate_css("body#tinymce.wp-editor.content a, body#tinymce.wp-editor.content a:focus, body#tinymce.wp-editor.content a:hover", "color", accent_)
                twentytwenty_generate_css("body#tinymce.wp-editor.content blockquote, body#tinymce.wp-editor.content .wp-block-quote", "border-color", accent_, "", " !important")
                twentytwenty_generate_css("body#tinymce.wp-editor.content button, body#tinymce.wp-editor.content .faux-button, body#tinymce.wp-editor.content .wp-block-button__link, body#tinymce.wp-editor.content .wp-block-file__button, body#tinymce.wp-editor.content input[type='button'], body#tinymce.wp-editor.content input[type='reset'], body#tinymce.wp-editor.content input[type='submit']", "background-color", accent_)
            # end if
            #// Background color.
            if background_ and background_ != background_default_:
                twentytwenty_generate_css("body#tinymce.wp-editor.content", "background-color", "#" + background_)
            # end if
            #// Text color.
            if body_ and body_ != body_default_:
                twentytwenty_generate_css("body#tinymce.wp-editor.content", "color", body_)
            # end if
            #// Secondary color.
            if secondary_ and secondary_ != secondary_default_:
                twentytwenty_generate_css("body#tinymce.wp-editor.content hr:not(.is-style-dots), body#tinymce.wp-editor.content cite, body#tinymce.wp-editor.content figcaption, body#tinymce.wp-editor.content .wp-caption-text, body#tinymce.wp-editor.content .wp-caption-dd, body#tinymce.wp-editor.content .gallery-caption", "color", secondary_)
            # end if
            #// Borders color.
            if borders_ and borders_ != borders_default_:
                twentytwenty_generate_css("body#tinymce.wp-editor.content pre, body#tinymce.wp-editor.content hr, body#tinymce.wp-editor.content fieldset,body#tinymce.wp-editor.content input, body#tinymce.wp-editor.content textarea", "border-color", borders_)
            # end if
        # end if
        #// Return the results.
        return ob_get_clean()
    # end def twentytwenty_get_customizer_css
# end if
