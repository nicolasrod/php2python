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
php_print("\n<article id=\"post-")
the_ID()
php_print("\" ")
post_class()
php_print(">\n  ")
if is_sticky() and is_home():
    php_print(twentyseventeen_get_svg(Array({"icon": "thumb-tack"})))
# end if
php_print(" <header class=\"entry-header\">\n       ")
if "post" == get_post_type():
    php_print("<div class=\"entry-meta\">")
    if is_single():
        twentyseventeen_posted_on()
    else:
        php_print(twentyseventeen_time_link())
        twentyseventeen_edit_link()
    # end if
    php_print("</div><!-- .entry-meta -->")
# end if
if is_single():
    the_title("<h1 class=\"entry-title\">", "</h1>")
elif is_front_page() and is_home():
    the_title("<h3 class=\"entry-title\"><a href=\"" + esc_url(get_permalink()) + "\" rel=\"bookmark\">", "</a></h3>")
else:
    the_title("<h2 class=\"entry-title\"><a href=\"" + esc_url(get_permalink()) + "\" rel=\"bookmark\">", "</a></h2>")
# end if
php_print(" </header><!-- .entry-header -->\n\n ")
if "" != get_the_post_thumbnail() and (not is_single()):
    php_print("     <div class=\"post-thumbnail\">\n            <a href=\"")
    the_permalink()
    php_print("\">\n                ")
    the_post_thumbnail("twentyseventeen-featured-image")
    php_print("         </a>\n      </div><!-- .post-thumbnail -->\n    ")
# end if
php_print("""
<div class=\"entry-content\">
""")
if is_single() or "" == get_the_post_thumbnail():
    #// Only show content if is a single post, or if there's no featured image.
    the_content(php_sprintf(__("Continue reading<span class=\"screen-reader-text\"> \"%s\"</span>", "twentyseventeen"), get_the_title()))
    wp_link_pages(Array({"before": "<div class=\"page-links\">" + __("Pages:", "twentyseventeen"), "after": "</div>", "link_before": "<span class=\"page-number\">", "link_after": "</span>"}))
# end if
php_print("""
</div><!-- .entry-content -->
""")
if is_single():
    twentyseventeen_entry_footer()
# end if
php_print("\n</article><!-- #post-")
the_ID()
php_print(" -->\n")
