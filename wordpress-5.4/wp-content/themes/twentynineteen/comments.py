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
#// The template for displaying comments
#// 
#// This is the template that displays the area of the page that contains both the current comments
#// and the comment form.
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#// 
#// 
#// If the current post is protected by a password and
#// the visitor has not yet entered the password we will
#// return early without loading the comments.
#//
if post_password_required():
    sys.exit(-1)
# end if
discussion = twentynineteen_get_discussion_data()
php_print("\n<div id=\"comments\" class=\"")
php_print("comments-area" if comments_open() else "comments-area comments-closed")
php_print("\">\n    <div class=\"")
php_print("comments-title-wrap" if discussion.responses > 0 else "comments-title-wrap no-responses")
php_print("\">\n        <h2 class=\"comments-title\">\n     ")
if comments_open():
    if have_comments():
        _e("Join the Conversation", "twentynineteen")
    else:
        _e("Leave a comment", "twentynineteen")
    # end if
else:
    if "1" == discussion.responses:
        #// translators: %s: Post title.
        printf(_x("One reply on &ldquo;%s&rdquo;", "comments title", "twentynineteen"), get_the_title())
    else:
        printf(_nx("%1$s reply on &ldquo;%2$s&rdquo;", "%1$s replies on &ldquo;%2$s&rdquo;", discussion.responses, "comments title", "twentynineteen"), number_format_i18n(discussion.responses), get_the_title())
    # end if
# end if
php_print("     </h2><!-- .comments-title -->\n     ")
#// Only show discussion meta information when comments are open and available.
if have_comments() and comments_open():
    get_template_part("template-parts/post/discussion", "meta")
# end if
php_print(" </div><!-- .comments-title-flex -->\n   ")
if have_comments():
    #// Show comment form at top if showing newest comments at the top.
    if comments_open():
        twentynineteen_comment_form("desc")
    # end if
    php_print("     <ol class=\"comment-list\">\n           ")
    wp_list_comments(Array({"walker": php_new_class("TwentyNineteen_Walker_Comment", lambda : TwentyNineteen_Walker_Comment()), "avatar_size": twentynineteen_get_avatar_size(), "short_ping": True, "style": "ol"}))
    php_print("     </ol><!-- .comment-list -->\n       ")
    #// Show comment navigation.
    if have_comments():
        prev_icon = twentynineteen_get_icon_svg("chevron_left", 22)
        next_icon = twentynineteen_get_icon_svg("chevron_right", 22)
        comments_text = __("Comments", "twentynineteen")
        the_comments_navigation(Array({"prev_text": php_sprintf("%s <span class=\"nav-prev-text\"><span class=\"primary-text\">%s</span> <span class=\"secondary-text\">%s</span></span>", prev_icon, __("Previous", "twentynineteen"), __("Comments", "twentynineteen")), "next_text": php_sprintf("<span class=\"nav-next-text\"><span class=\"primary-text\">%s</span> <span class=\"secondary-text\">%s</span></span> %s", __("Next", "twentynineteen"), __("Comments", "twentynineteen"), next_icon)}))
    # end if
    #// Show comment form at bottom if showing newest comments at the bottom.
    if comments_open() and "asc" == php_strtolower(get_option("comment_order", "asc")):
        php_print("         <div class=\"comment-form-flex\">\n             <span class=\"screen-reader-text\">")
        _e("Leave a comment", "twentynineteen")
        php_print("</span>\n                ")
        twentynineteen_comment_form("asc")
        php_print("             <h2 class=\"comments-title\" aria-hidden=\"true\">")
        _e("Leave a comment", "twentynineteen")
        php_print("</h2>\n          </div>\n            ")
    # end if
    #// If comments are closed and there are comments, let's leave a little note, shall we?
    if (not comments_open()):
        php_print("         <p class=\"no-comments\">\n             ")
        _e("Comments are closed.", "twentynineteen")
        php_print("         </p>\n          ")
    # end if
else:
    #// Show comment form.
    twentynineteen_comment_form(True)
# end if
pass
php_print("</div><!-- #comments -->\n")
