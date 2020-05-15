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
php_print(">\n  <header class=\"entry-header\">\n       ")
if is_sticky() and is_home() and (not is_paged()):
    printf("<span class=\"sticky-post\">%s</span>", _x("Featured", "post", "twentynineteen"))
# end if
the_title(php_sprintf("<h2 class=\"entry-title\"><a href=\"%s\" rel=\"bookmark\">", esc_url(get_permalink())), "</a></h2>")
php_print(" </header><!-- .entry-header -->\n\n ")
twentynineteen_post_thumbnail()
php_print("\n   <div class=\"entry-content\">\n     ")
the_excerpt()
php_print("""   </div><!-- .entry-content -->
<footer class=\"entry-footer\">
""")
twentynineteen_entry_footer()
php_print(" </footer><!-- .entry-footer -->\n</article><!-- #post-")
the_ID()
php_print(" -->\n")
