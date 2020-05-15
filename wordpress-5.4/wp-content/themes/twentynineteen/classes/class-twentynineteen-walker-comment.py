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
#// Custom comment walker for this theme
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#// 
#// 
#// This class outputs custom comment walker for HTML5 friendly WordPress comment and threaded replies.
#// 
#// @since Twenty Nineteen 1.0
#//
class TwentyNineteen_Walker_Comment(Walker_Comment):
    #// 
    #// Outputs a comment in the HTML5 format.
    #// 
    #// @see wp_list_comments()
    #// 
    #// @param WP_Comment $comment Comment to display.
    #// @param int        $depth   Depth of the current comment.
    #// @param array      $args    An array of arguments.
    #//
    def html5_comment(self, comment=None, depth=None, args=None):
        
        tag = "div" if "div" == args["style"] else "li"
        php_print("     <")
        php_print(tag)
        php_print(" id=\"comment-")
        comment_ID()
        php_print("\" ")
        comment_class("parent" if self.has_children else "", comment)
        php_print(">\n          <article id=\"div-comment-")
        comment_ID()
        php_print("""\" class=\"comment-body\">
        <footer class=\"comment-meta\">
        <div class=\"comment-author vcard\">
        """)
        comment_author_url = get_comment_author_url(comment)
        comment_author = get_comment_author(comment)
        avatar = get_avatar(comment, args["avatar_size"])
        if 0 != args["avatar_size"]:
            if php_empty(lambda : comment_author_url):
                php_print(avatar)
            else:
                printf("<a href=\"%s\" rel=\"external nofollow\" class=\"url\">", comment_author_url)
                php_print(avatar)
            # end if
        # end if
        #// 
        #// Using the `check` icon instead of `check_circle`, since we can't add a
        #// fill color to the inner check shape when in circle form.
        #//
        if twentynineteen_is_comment_by_post_author(comment):
            printf("<span class=\"post-author-badge\" aria-hidden=\"true\">%s</span>", twentynineteen_get_icon_svg("check", 24))
        # end if
        printf(wp_kses(__("%s <span class=\"screen-reader-text says\">says:</span>", "twentynineteen"), Array({"span": Array({"class": Array()})})), "<b class=\"fn\">" + comment_author + "</b>")
        if (not php_empty(lambda : comment_author_url)):
            php_print("</a>")
        # end if
        php_print("""                   </div><!-- .comment-author -->
        <div class=\"comment-metadata\">
        <a href=\"""")
        php_print(esc_url(get_comment_link(comment, args)))
        php_print("\">\n                            ")
        #// translators: 1: Comment date, 2: Comment time.
        comment_timestamp = php_sprintf(__("%1$s at %2$s", "twentynineteen"), get_comment_date("", comment), get_comment_time())
        php_print("                         <time datetime=\"")
        comment_time("c")
        php_print("\" title=\"")
        php_print(comment_timestamp)
        php_print("\">\n                                ")
        php_print(comment_timestamp)
        php_print("                         </time>\n                       </a>\n                      ")
        edit_comment_icon = twentynineteen_get_icon_svg("edit", 16)
        edit_comment_link(__("Edit", "twentynineteen"), "<span class=\"edit-link-sep\">&mdash;</span> <span class=\"edit-link\">" + edit_comment_icon, "</span>")
        php_print("                 </div><!-- .comment-metadata -->\n\n                    ")
        commenter = wp_get_current_commenter()
        if commenter["comment_author_email"]:
            moderation_note = __("Your comment is awaiting moderation.", "twentynineteen")
        else:
            moderation_note = __("Your comment is awaiting moderation. This is a preview, your comment will be visible after it has been approved.", "twentynineteen")
        # end if
        php_print("\n                   ")
        if "0" == comment.comment_approved:
            php_print("                 <p class=\"comment-awaiting-moderation\">")
            php_print(moderation_note)
            php_print("</p>\n                   ")
        # end if
        php_print("""
        </footer><!-- .comment-meta -->
        <div class=\"comment-content\">
        """)
        comment_text()
        php_print("""               </div><!-- .comment-content -->
        </article><!-- .comment-body -->
        """)
        comment_reply_link(php_array_merge(args, Array({"add_below": "div-comment", "depth": depth, "max_depth": args["max_depth"], "before": "<div class=\"comment-reply\">", "after": "</div>"})))
        php_print("     ")
    # end def html5_comment
# end class TwentyNineteen_Walker_Comment
