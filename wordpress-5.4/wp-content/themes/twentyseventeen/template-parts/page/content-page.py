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
php_print(">\n  <header class=\"entry-header\">\n       ")
the_title("<h1 class=\"entry-title\">", "</h1>")
php_print("     ")
twentyseventeen_edit_link(get_the_ID())
php_print(" </header><!-- .entry-header -->\n   <div class=\"entry-content\">\n     ")
the_content()
wp_link_pages(Array({"before": "<div class=\"page-links\">" + __("Pages:", "twentyseventeen"), "after": "</div>"}))
php_print(" </div><!-- .entry-content -->\n</article><!-- #post-")
the_ID()
php_print(" -->\n")
