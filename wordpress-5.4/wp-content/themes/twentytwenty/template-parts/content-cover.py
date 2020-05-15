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
pass
php_print("\n<article ")
post_class()
php_print(" id=\"post-")
the_ID()
php_print("\">\n    ")
#// On the cover page template, output the cover header.
cover_header_style = ""
cover_header_classes = ""
color_overlay_style = ""
color_overlay_classes = ""
image_url = get_the_post_thumbnail_url(get_the_ID(), "twentytwenty-fullscreen") if (not post_password_required()) else ""
if image_url:
    cover_header_style = " style=\"background-image: url( " + esc_url(image_url) + " );\""
    cover_header_classes = " bg-image"
# end if
#// Get the color used for the color overlay.
color_overlay_color = get_theme_mod("cover_template_overlay_background_color")
if color_overlay_color:
    color_overlay_style = " style=\"color: " + esc_attr(color_overlay_color) + ";\""
else:
    color_overlay_style = ""
# end if
#// Get the fixed background attachment option.
if get_theme_mod("cover_template_fixed_background", True):
    cover_header_classes += " bg-attachment-fixed"
# end if
#// Get the opacity of the color overlay.
color_overlay_opacity = get_theme_mod("cover_template_overlay_opacity")
color_overlay_opacity = 80 if False == color_overlay_opacity else color_overlay_opacity
color_overlay_classes += " opacity-" + color_overlay_opacity
php_print("\n   <div class=\"cover-header ")
php_print(cover_header_classes)
pass
php_print("\"")
php_print(cover_header_style)
pass
php_print(""">
<div class=\"cover-header-inner-wrapper screen-height\">
<div class=\"cover-header-inner\">
<div class=\"cover-color-overlay color-accent""")
php_print(esc_attr(color_overlay_classes))
php_print("\"")
php_print(color_overlay_style)
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
show_categories = apply_filters("twentytwenty_show_categories_in_entry_header", True)
if True == show_categories and has_category():
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
    intro_text_width = ""
    if is_singular():
        intro_text_width = " small"
    else:
        intro_text_width = " thin"
    # end if
    if has_excerpt():
        php_print("\n                                   <div class=\"intro-text section-inner max-percentage")
        php_print(esc_attr(intro_text_width))
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
