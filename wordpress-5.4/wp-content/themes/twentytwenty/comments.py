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
#// The template file for displaying the comments and comment form for the
#// Twenty Twenty theme.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#// 
#// 
#// If the current post is protected by a password and
#// the visitor has not yet entered the password we will
#// return early without loading the comments.
#//
if post_password_required():
    sys.exit(-1)
# end if
if comments:
    php_print("""
    <div class=\"comments\" id=\"comments\">
    """)
    comments_number = absint(get_comments_number())
    php_print("""
    <div class=\"comments-header section-inner small max-percentage\">
    <h2 class=\"comment-reply-title\">
    """)
    if (not have_comments()):
        _e("Leave a comment", "twentytwenty")
    elif "1" == comments_number:
        #// translators: %s: Post title.
        printf(_x("One reply on &ldquo;%s&rdquo;", "comments title", "twentytwenty"), get_the_title())
    else:
        printf(_nx("%1$s reply on &ldquo;%2$s&rdquo;", "%1$s replies on &ldquo;%2$s&rdquo;", comments_number, "comments title", "twentytwenty"), number_format_i18n(comments_number), get_the_title())
    # end if
    php_print("""           </h2><!-- .comments-title -->
    </div><!-- .comments-header -->
    <div class=\"comments-inner section-inner thin max-percentage\">
    """)
    wp_list_comments(Array({"walker": php_new_class("TwentyTwenty_Walker_Comment", lambda : TwentyTwenty_Walker_Comment()), "avatar_size": 120, "style": "div"}))
    comment_pagination = paginate_comments_links(Array({"echo": False, "end_size": 0, "mid_size": 0, "next_text": __("Newer Comments", "twentytwenty") + " <span aria-hidden=\"true\">&rarr;</span>", "prev_text": "<span aria-hidden=\"true\">&larr;</span> " + __("Older Comments", "twentytwenty")}))
    if comment_pagination:
        pagination_classes = ""
        #// If we're only showing the "Next" link, add a class indicating so.
        if False == php_strpos(comment_pagination, "prev page-numbers"):
            pagination_classes = " only-next"
        # end if
        php_print("\n               <nav class=\"comments-pagination pagination")
        php_print(pagination_classes)
        pass
        php_print("\" aria-label=\"")
        esc_attr_e("Comments", "twentytwenty")
        php_print("\">\n                    ")
        php_print(wp_kses_post(comment_pagination))
        php_print("             </nav>\n\n              ")
    # end if
    php_print("""
    </div><!-- .comments-inner -->
    </div><!-- comments -->
    """)
# end if
if comments_open() or pings_open():
    if comments:
        php_print("<hr class=\"styled-separator is-style-wide\" aria-hidden=\"true\" />")
    # end if
    comment_form(Array({"class_form": "section-inner thin max-percentage", "title_reply_before": "<h2 id=\"reply-title\" class=\"comment-reply-title\">", "title_reply_after": "</h2>"}))
elif is_single():
    if comments:
        php_print("<hr class=\"styled-separator is-style-wide\" aria-hidden=\"true\" />")
    # end if
    php_print("""
    <div class=\"comment-respond\" id=\"respond\">
    <p class=\"comments-closed\">""")
    _e("Comments are closed.", "twentytwenty")
    php_print("""</p>
    </div><!-- #respond -->
    """)
# end if
