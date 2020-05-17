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
php_print("<!doctype html>\n<html ")
language_attributes()
php_print(">\n<head>\n  <meta charset=\"")
bloginfo("charset")
php_print("""\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
<link rel=\"profile\" href=\"https://gmpg.org/xfn/11\" />
""")
wp_head()
php_print("</head>\n\n<body ")
body_class()
php_print(">\n")
wp_body_open()
php_print("<div id=\"page\" class=\"site\">\n   <a class=\"skip-link screen-reader-text\" href=\"#content\">")
_e("Skip to content", "twentynineteen")
php_print("</a>\n\n     <header id=\"masthead\" class=\"")
php_print("site-header featured-image" if is_singular() and twentynineteen_can_show_post_thumbnail() else "site-header")
php_print("""\">
<div class=\"site-branding-container\">
""")
get_template_part("template-parts/header/site", "branding")
php_print("         </div><!-- .site-branding-container -->\n\n         ")
if is_singular() and twentynineteen_can_show_post_thumbnail():
    php_print("             <div class=\"site-featured-image\">\n                   ")
    twentynineteen_post_thumbnail()
    the_post()
    discussion_ = twentynineteen_get_discussion_data() if (not is_page()) and twentynineteen_can_show_post_thumbnail() else None
    classes_ = "entry-header"
    if (not php_empty(lambda : discussion_)) and absint(discussion_.responses) > 0:
        classes_ = "entry-header has-discussion"
    # end if
    php_print("                 <div class=\"")
    php_print(classes_)
    php_print("\">\n                        ")
    get_template_part("template-parts/header/entry", "header")
    php_print("                 </div><!-- .entry-header -->\n                  ")
    rewind_posts()
    php_print("             </div>\n            ")
# end if
php_print("""       </header><!-- #masthead -->
<div id=\"content\" class=\"site-content\">
""")
