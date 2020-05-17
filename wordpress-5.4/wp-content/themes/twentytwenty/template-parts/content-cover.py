#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
pass
php_print("\n<article ")
post_class()
php_print(" id=\"post-")
the_ID()
php_print("\">\n    ")
#// On the cover page template, output the cover header.
cover_header_style_ = ""
cover_header_classes_ = ""
color_overlay_style_ = ""
color_overlay_classes_ = ""
image_url_ = get_the_post_thumbnail_url(get_the_ID(), "twentytwenty-fullscreen") if (not post_password_required()) else ""
if image_url_:
    cover_header_style_ = " style=\"background-image: url( " + esc_url(image_url_) + " );\""
    cover_header_classes_ = " bg-image"
# end if
#// Get the color used for the color overlay.
color_overlay_color_ = get_theme_mod("cover_template_overlay_background_color")
if color_overlay_color_:
    color_overlay_style_ = " style=\"color: " + esc_attr(color_overlay_color_) + ";\""
else:
    color_overlay_style_ = ""
# end if
#// Get the fixed background attachment option.
if get_theme_mod("cover_template_fixed_background", True):
    cover_header_classes_ += " bg-attachment-fixed"
# end if
#// Get the opacity of the color overlay.
color_overlay_opacity_ = get_theme_mod("cover_template_overlay_opacity")
color_overlay_opacity_ = 80 if False == color_overlay_opacity_ else color_overlay_opacity_
color_overlay_classes_ += " opacity-" + color_overlay_opacity_
php_print("\n   <div class=\"cover-header ")
php_print(cover_header_classes_)
pass
php_print("\"")
php_print(cover_header_style_)
pass
php_print(""">
<div class=\"cover-header-inner-wrapper screen-height\">
<div class=\"cover-header-inner\">
<div class=\"cover-color-overlay color-accent""")
php_print(esc_attr(color_overlay_classes_))
php_print("\"")
php_print(color_overlay_style_)
pass
php_print("""></div>
<header class=\"entry-header has-text-align-center\">
<div class=\"entry-header-inner section-inner medium\">
""")
#// 
#// Allow child themes and plugins to filter the display of the categories in the article header.
#// 
#// @since Twenty Twenty 1.0
#// 
#// @param bool Whether to show the categories in article header, Default true.
#//
show_categories_ = apply_filters("twentytwenty_show_categories_in_entry_header", True)
if True == show_categories_ and has_category():
    php_print("\n                               <div class=\"entry-categories\">\n                                  <span class=\"screen-reader-text\">")
    _e("Categories", "twentytwenty")
    php_print("</span>\n                                    <div class=\"entry-categories-inner\">\n                                        ")
    the_category(" ")
    php_print("""                                   </div><!-- .entry-categories-inner -->
    </div><!-- .entry-categories -->
    """)
# end if
the_title("<h1 class=\"entry-title\">", "</h1>")
if is_page():
    php_print("""
    <div class=\"to-the-content-wrapper\">
    <a href=\"#post-inner\" class=\"to-the-content fill-children-current-color\">
    """)
    twentytwenty_the_theme_svg("arrow-down")
    php_print("                                     <div class=\"screen-reader-text\">")
    _e("Scroll Down", "twentytwenty")
    php_print("""</div>
    </a><!-- .to-the-content -->
    </div><!-- .to-the-content-wrapper -->
    """)
else:
    intro_text_width_ = ""
    if is_singular():
        intro_text_width_ = " small"
    else:
        intro_text_width_ = " thin"
    # end if
    if has_excerpt():
        php_print("\n                                   <div class=\"intro-text section-inner max-percentage")
        php_print(esc_attr(intro_text_width_))
        php_print("\">\n                                        ")
        the_excerpt()
        php_print("                                 </div>\n\n                                  ")
    # end if
    twentytwenty_the_post_meta(get_the_ID(), "single-top")
# end if
php_print("""
</div><!-- .entry-header-inner -->
</header><!-- .entry-header -->
</div><!-- .cover-header-inner -->
</div><!-- .cover-header-inner-wrapper -->
</div><!-- .cover-header -->
<div class=\"post-inner\" id=\"post-inner\">
<div class=\"entry-content\">
""")
the_content()
php_print("\n       </div><!-- .entry-content -->\n     ")
wp_link_pages(Array({"before": "<nav class=\"post-nav-links bg-light-background\" aria-label=\"" + esc_attr__("Page", "twentytwenty") + "\"><span class=\"label\">" + __("Pages:", "twentytwenty") + "</span>", "after": "</nav>", "link_before": "<span class=\"page-number\">", "link_after": "</span>"}))
edit_post_link()
#// Single bottom post meta.
twentytwenty_the_post_meta(get_the_ID(), "single-bottom")
if is_single():
    get_template_part("template-parts/entry-author-bio")
# end if
php_print("""
</div><!-- .post-inner -->
""")
if is_single():
    get_template_part("template-parts/navigation")
# end if
#// 
#// Output comments wrapper if it's a post, or if comments are open,
#// or if there's a comment number – and check for password.
#//
if is_single() or is_page() and comments_open() or get_comments_number() and (not post_password_required()):
    php_print("""
    <div class=\"comments-wrapper section-inner\">
    """)
    comments_template()
    php_print("""
    </div><!-- .comments-wrapper -->
    """)
# end if
php_print("\n</article><!-- .post -->\n")
