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
php_print(""">
<header class=\"entry-header\">
""")
if "post" == get_post_type():
    php_print("         <div class=\"entry-meta\">\n                ")
    php_print(twentyseventeen_time_link())
    twentyseventeen_edit_link()
    php_print("         </div><!-- .entry-meta -->\n        ")
elif "page" == get_post_type() and get_edit_post_link():
    php_print("         <div class=\"entry-meta\">\n                ")
    twentyseventeen_edit_link()
    php_print("         </div><!-- .entry-meta -->\n        ")
# end if
php_print("\n       ")
if is_front_page() and (not is_home()):
    #// The excerpt is being displayed within a front page section, so it's a lower hierarchy than h2.
    the_title(php_sprintf("<h3 class=\"entry-title\"><a href=\"%s\" rel=\"bookmark\">", esc_url(get_permalink())), "</a></h3>")
else:
    the_title(php_sprintf("<h2 class=\"entry-title\"><a href=\"%s\" rel=\"bookmark\">", esc_url(get_permalink())), "</a></h2>")
# end if
php_print("""   </header><!-- .entry-header -->
<div class=\"entry-summary\">
""")
the_excerpt()
php_print(" </div><!-- .entry-summary -->\n\n</article><!-- #post-")
the_ID()
php_print(" -->\n")
