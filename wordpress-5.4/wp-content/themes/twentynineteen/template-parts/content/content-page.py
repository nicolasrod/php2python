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
php_print("\n<article id=\"post-")
the_ID()
php_print("\" ")
post_class()
php_print(">\n  ")
if (not twentynineteen_can_show_post_thumbnail()):
    php_print(" <header class=\"entry-header\">\n       ")
    get_template_part("template-parts/header/entry", "header")
    php_print(" </header>\n ")
# end if
php_print("\n   <div class=\"entry-content\">\n     ")
the_content()
wp_link_pages(Array({"before": "<div class=\"page-links\">" + __("Pages:", "twentynineteen"), "after": "</div>"}))
php_print(" </div><!-- .entry-content -->\n\n   ")
if get_edit_post_link():
    php_print("     <footer class=\"entry-footer\">\n           ")
    edit_post_link(php_sprintf(wp_kses(__("Edit <span class=\"screen-reader-text\">%s</span>", "twentynineteen"), Array({"span": Array({"class": Array()})})), get_the_title()), "<span class=\"edit-link\">" + twentynineteen_get_icon_svg("edit", 16), "</span>")
    php_print("     </footer><!-- .entry-footer -->\n   ")
# end if
php_print("</article><!-- #post-")
the_ID()
php_print(" -->\n")
