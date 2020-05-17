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
#// Non-latin language handling.
#// 
#// Handle non-latin language styles.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if (not php_class_exists("TwentyTwenty_Non_Latin_Languages")):
    #// 
    #// Language handling.
    #//
    class TwentyTwenty_Non_Latin_Languages():
        #// 
        #// Get custom CSS.
        #// 
        #// Return CSS for non-latin language, if available, or null
        #// 
        #// @param string $type Whether to return CSS for the "front-end", "block-editor" or "classic-editor".
        #// 
        #// @return void
        #//
        @classmethod
        def get_non_latin_css(self, type_="front-end"):
            
            
            #// Fetch site locale.
            locale_ = get_bloginfo("language")
            #// Define fallback fonts for non-latin languages.
            font_family_ = apply_filters("twentytwenty_get_localized_font_family_types", Array({"ar": Array("Tahoma", "Arial", "sans-serif"), "ary": Array("Tahoma", "Arial", "sans-serif"), "azb": Array("Tahoma", "Arial", "sans-serif"), "ckb": Array("Tahoma", "Arial", "sans-serif"), "fa-IR": Array("Tahoma", "Arial", "sans-serif"), "haz": Array("Tahoma", "Arial", "sans-serif"), "ps": Array("Tahoma", "Arial", "sans-serif"), "zh-CN": Array("'PingFang SC'", "'Helvetica Neue'", "'Microsoft YaHei New'", "'STHeiti Light'", "sans-serif"), "zh-TW": Array("'PingFang TC'", "'Helvetica Neue'", "'Microsoft YaHei New'", "'STHeiti Light'", "sans-serif"), "zh-HK": Array("'PingFang HK'", "'Helvetica Neue'", "'Microsoft YaHei New'", "'STHeiti Light'", "sans-serif"), "bel": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "bg-BG": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "kk": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "mk-MK": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "mn": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "ru-RU": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "sah": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "sr-RS": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "tt-RU": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "uk": Array("'Helvetica Neue'", "Helvetica", "'Segoe UI'", "Arial", "sans-serif"), "bn-BD": Array("Arial", "sans-serif"), "hi-IN": Array("Arial", "sans-serif"), "mr": Array("Arial", "sans-serif"), "ne-NP": Array("Arial", "sans-serif"), "el": Array("'Helvetica Neue', Helvetica, Arial, sans-serif"), "gu": Array("Arial", "sans-serif"), "he-IL": Array("'Arial Hebrew'", "Arial", "sans-serif"), "ja": Array("sans-serif"), "ko-KR": Array("'Apple SD Gothic Neo'", "'Malgun Gothic'", "'Nanum Gothic'", "Dotum", "sans-serif"), "th": Array("'Sukhumvit Set'", "'Helvetica Neue'", "Helvetica", "Arial", "sans-serif"), "vi": Array("'Libre Franklin'", "sans-serif")}))
            #// Return if the selected language has no fallback fonts.
            if php_empty(lambda : font_family_[locale_]):
                return
            # end if
            #// Define elements to apply fallback fonts to.
            elements_ = apply_filters("twentytwenty_get_localized_font_family_elements", Array({"front-end": Array("body", "input", "textarea", "button", ".button", ".faux-button", ".wp-block-button__link", ".wp-block-file__button", ".has-drop-cap:not(:focus)::first-letter", ".has-drop-cap:not(:focus)::first-letter", ".entry-content .wp-block-archives", ".entry-content .wp-block-categories", ".entry-content .wp-block-cover-image", ".entry-content .wp-block-latest-comments", ".entry-content .wp-block-latest-posts", ".entry-content .wp-block-pullquote", ".entry-content .wp-block-quote.is-large", ".entry-content .wp-block-quote.is-style-large", ".entry-content .wp-block-archives *", ".entry-content .wp-block-categories *", ".entry-content .wp-block-latest-posts *", ".entry-content .wp-block-latest-comments *", ".entry-content p", ".entry-content ol", ".entry-content ul", ".entry-content dl", ".entry-content dt", ".entry-content cite", ".entry-content figcaption", ".entry-content .wp-caption-text", ".comment-content p", ".comment-content ol", ".comment-content ul", ".comment-content dl", ".comment-content dt", ".comment-content cite", ".comment-content figcaption", ".comment-content .wp-caption-text", ".widget_text p", ".widget_text ol", ".widget_text ul", ".widget_text dl", ".widget_text dt", ".widget-content .rssSummary", ".widget-content cite", ".widget-content figcaption", ".widget-content .wp-caption-text"), "block-editor": Array(".editor-styles-wrapper > *", ".editor-styles-wrapper p", ".editor-styles-wrapper ol", ".editor-styles-wrapper ul", ".editor-styles-wrapper dl", ".editor-styles-wrapper dt", ".editor-post-title__block .editor-post-title__input", ".editor-styles-wrapper .wp-block h1", ".editor-styles-wrapper .wp-block h2", ".editor-styles-wrapper .wp-block h3", ".editor-styles-wrapper .wp-block h4", ".editor-styles-wrapper .wp-block h5", ".editor-styles-wrapper .wp-block h6", ".editor-styles-wrapper .has-drop-cap:not(:focus)::first-letter", ".editor-styles-wrapper cite", ".editor-styles-wrapper figcaption", ".editor-styles-wrapper .wp-caption-text"), "classic-editor": Array("body#tinymce.wp-editor", "body#tinymce.wp-editor p", "body#tinymce.wp-editor ol", "body#tinymce.wp-editor ul", "body#tinymce.wp-editor dl", "body#tinymce.wp-editor dt", "body#tinymce.wp-editor figcaption", "body#tinymce.wp-editor .wp-caption-text", "body#tinymce.wp-editor .wp-caption-dd", "body#tinymce.wp-editor cite", "body#tinymce.wp-editor table")}))
            #// Return if the specified type doesn't exist.
            if php_empty(lambda : elements_[type_]):
                return
            # end if
            #// Return the specified styles.
            return twentytwenty_generate_css(php_implode(",", elements_[type_]), "font-family", php_implode(",", font_family_[locale_]), None, None, False)
        # end def get_non_latin_css
    # end class TwentyTwenty_Non_Latin_Languages
# end if
