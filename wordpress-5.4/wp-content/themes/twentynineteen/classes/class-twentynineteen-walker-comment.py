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
    def html5_comment(self, comment_=None, depth_=None, args_=None):
        
        
        tag_ = "div" if "div" == args_["style"] else "li"
        php_print("     <")
        php_print(tag_)
        php_print(" id=\"comment-")
        comment_ID()
        php_print("\" ")
        comment_class("parent" if self.has_children else "", comment_)
        php_print(">\n          <article id=\"div-comment-")
        comment_ID()
        php_print("""\" class=\"comment-body\">
        <footer class=\"comment-meta\">
        <div class=\"comment-author vcard\">
        """)
        comment_author_url_ = get_comment_author_url(comment_)
        comment_author_ = get_comment_author(comment_)
        avatar_ = get_avatar(comment_, args_["avatar_size"])
        if 0 != args_["avatar_size"]:
            if php_empty(lambda : comment_author_url_):
                php_print(avatar_)
            else:
                php_printf("<a href=\"%s\" rel=\"external nofollow\" class=\"url\">", comment_author_url_)
                php_print(avatar_)
            # end if
        # end if
        #// 
        #// Using the `check` icon instead of `check_circle`, since we can't add a
        #// fill color to the inner check shape when in circle form.
        #//
        if twentynineteen_is_comment_by_post_author(comment_):
            php_printf("<span class=\"post-author-badge\" aria-hidden=\"true\">%s</span>", twentynineteen_get_icon_svg("check", 24))
        # end if
        php_printf(wp_kses(__("%s <span class=\"screen-reader-text says\">says:</span>", "twentynineteen"), Array({"span": Array({"class": Array()})})), "<b class=\"fn\">" + comment_author_ + "</b>")
        if (not php_empty(lambda : comment_author_url_)):
            php_print("</a>")
        # end if
        php_print("""                   </div><!-- .comment-author -->
        <div class=\"comment-metadata\">
        <a href=\"""")
        php_print(esc_url(get_comment_link(comment_, args_)))
        php_print("\">\n                            ")
        #// translators: 1: Comment date, 2: Comment time.
        comment_timestamp_ = php_sprintf(__("%1$s at %2$s", "twentynineteen"), get_comment_date("", comment_), get_comment_time())
        php_print("                         <time datetime=\"")
        comment_time("c")
        php_print("\" title=\"")
        php_print(comment_timestamp_)
        php_print("\">\n                                ")
        php_print(comment_timestamp_)
        php_print("                         </time>\n                       </a>\n                      ")
        edit_comment_icon_ = twentynineteen_get_icon_svg("edit", 16)
        edit_comment_link(__("Edit", "twentynineteen"), "<span class=\"edit-link-sep\">&mdash;</span> <span class=\"edit-link\">" + edit_comment_icon_, "</span>")
        php_print("                 </div><!-- .comment-metadata -->\n\n                    ")
        commenter_ = wp_get_current_commenter()
        if commenter_["comment_author_email"]:
            moderation_note_ = __("Your comment is awaiting moderation.", "twentynineteen")
        else:
            moderation_note_ = __("Your comment is awaiting moderation. This is a preview, your comment will be visible after it has been approved.", "twentynineteen")
        # end if
        php_print("\n                   ")
        if "0" == comment_.comment_approved:
            php_print("                 <p class=\"comment-awaiting-moderation\">")
            php_print(moderation_note_)
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
        comment_reply_link(php_array_merge(args_, Array({"add_below": "div-comment", "depth": depth_, "max_depth": args_["max_depth"], "before": "<div class=\"comment-reply\">", "after": "</div>"})))
        php_print("     ")
    # end def html5_comment
# end class TwentyNineteen_Walker_Comment
