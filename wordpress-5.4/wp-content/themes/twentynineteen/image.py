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
#// The template for displaying image attachments
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
get_header()
php_print("""
<div id=\"primary\" class=\"content-area\">
<main id=\"main\" class=\"site-main\">
""")
#// Start the Loop.
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    php_print("\n               <article id=\"post-")
    the_ID()
    php_print("\" ")
    post_class()
    php_print(""">
    <header class=\"entry-header\">
    """)
    the_title("<h1 class=\"entry-title\">", "</h1>")
    php_print("""                   </header><!-- .entry-header -->
    <div class=\"entry-content\">
    <figure class=\"entry-attachment wp-block-image\">
    """)
    #// 
    #// Filter the default twentynineteen image attachment size.
    #// 
    #// @since Twenty Sixteen 1.0
    #// 
    #// @param string $image_size Image size. Default 'large'.
    #//
    image_size = apply_filters("twentynineteen_attachment_size", "full")
    php_print(wp_get_attachment_image(get_the_ID(), image_size))
    php_print("\n                           <figcaption class=\"wp-caption-text\">")
    the_excerpt()
    php_print("""</figcaption>
    </figure><!-- .entry-attachment -->
    """)
    the_content()
    wp_link_pages(Array({"before": "<div class=\"page-links\"><span class=\"page-links-title\">" + __("Pages:", "twentynineteen") + "</span>", "after": "</div>", "link_before": "<span>", "link_after": "</span>", "pagelink": "<span class=\"screen-reader-text\">" + __("Page", "twentynineteen") + " </span>%", "separator": "<span class=\"screen-reader-text\">, </span>"}))
    php_print("""                   </div><!-- .entry-content -->
    <footer class=\"entry-footer\">
    """)
    #// Retrieve attachment metadata.
    metadata = wp_get_attachment_metadata()
    if metadata:
        printf("<span class=\"full-size-link\"><span class=\"screen-reader-text\">%1$s</span><a href=\"%2$s\">%3$s &times; %4$s</a></span>", _x("Full size", "Used before full size attachment link.", "twentynineteen"), esc_url(wp_get_attachment_url()), absint(metadata["width"]), absint(metadata["height"]))
    # end if
    php_print("\n                       ")
    twentynineteen_entry_footer()
    php_print("\n                   </footer><!-- .entry-footer -->\n               </article><!-- #post-")
    the_ID()
    php_print(" -->\n\n             ")
    #// Parent post navigation.
    the_post_navigation(Array({"prev_text": _x("<span class=\"meta-nav\">Published in</span><br><span class=\"post-title\">%title</span>", "Parent post link", "twentynineteen")}))
    #// If comments are open or we have at least one comment, load up the comment template.
    if comments_open() or get_comments_number():
        comments_template()
    # end if
    pass
# end while
php_print("""
</main><!-- .site-main -->
</div><!-- .content-area -->
""")
get_footer()
