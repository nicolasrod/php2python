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
#// The template for displaying comments
#// 
#// This is the template that displays the area of the page that contains both the current comments
#// and the comment form.
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// @version 1.0
#// 
#// 
#// If the current post is protected by a password and
#// the visitor has not yet entered the password we will
#// return early without loading the comments.
#//
if post_password_required():
    sys.exit(-1)
# end if
php_print("""
<div id=\"comments\" class=\"comments-area\">
""")
#// You can start editing here -- including this comment!
if have_comments():
    php_print("     <h2 class=\"comments-title\">\n         ")
    comments_number_ = get_comments_number()
    if "1" == comments_number_:
        #// translators: %s: Post title.
        php_printf(_x("One Reply to &ldquo;%s&rdquo;", "comments title", "twentyseventeen"), get_the_title())
    else:
        php_printf(_nx("%1$s Reply to &ldquo;%2$s&rdquo;", "%1$s Replies to &ldquo;%2$s&rdquo;", comments_number_, "comments title", "twentyseventeen"), number_format_i18n(comments_number_), get_the_title())
    # end if
    php_print("""       </h2>
    <ol class=\"comment-list\">
    """)
    wp_list_comments(Array({"avatar_size": 100, "style": "ol", "short_ping": True, "reply_text": twentyseventeen_get_svg(Array({"icon": "mail-reply"})) + __("Reply", "twentyseventeen")}))
    php_print("     </ol>\n\n       ")
    the_comments_pagination(Array({"prev_text": twentyseventeen_get_svg(Array({"icon": "arrow-left"})) + "<span class=\"screen-reader-text\">" + __("Previous", "twentyseventeen") + "</span>"}, {"next_text": "<span class=\"screen-reader-text\">" + __("Next", "twentyseventeen") + "</span>" + twentyseventeen_get_svg(Array({"icon": "arrow-right"}))}))
# end if
#// Check for have_comments().
#// If comments are closed and there are comments, let's leave a little note, shall we?
if (not comments_open()) and get_comments_number() and post_type_supports(get_post_type(), "comments"):
    php_print("\n       <p class=\"no-comments\">")
    _e("Comments are closed.", "twentyseventeen")
    php_print("</p>\n       ")
# end if
comment_form()
php_print("\n</div><!-- #comments -->\n")
