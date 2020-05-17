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
#// Displays the post header
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
discussion_ = twentynineteen_get_discussion_data() if (not is_page()) and twentynineteen_can_show_post_thumbnail() else None
php_print("\n")
the_title("<h1 class=\"entry-title\">", "</h1>")
php_print("\n")
if (not is_page()):
    php_print("<div class=\"entry-meta\">\n ")
    twentynineteen_posted_by()
    php_print(" ")
    twentynineteen_posted_on()
    php_print(" <span class=\"comment-count\">\n        ")
    if (not php_empty(lambda : discussion_)):
        twentynineteen_discussion_avatars_list(discussion_.authors)
    # end if
    php_print("     ")
    twentynineteen_comment_count()
    php_print(" </span>\n   ")
    #// Edit post link.
    edit_post_link(php_sprintf(wp_kses(__("Edit <span class=\"screen-reader-text\">%s</span>", "twentynineteen"), Array({"span": Array({"class": Array()})})), get_the_title()), "<span class=\"edit-link\">" + twentynineteen_get_icon_svg("edit", 16), "</span>")
    php_print("</div><!-- .entry-meta -->\n")
# end if
