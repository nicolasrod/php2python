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
#// Custom comment walker for this theme.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if (not php_class_exists("TwentyTwenty_Walker_Comment")):
    #// 
    #// CUSTOM COMMENT WALKER
    #// A custom walker for comments, based on the walker in Twenty Nineteen.
    #//
    class TwentyTwenty_Walker_Comment(Walker_Comment):
        #// 
        #// Outputs a comment in the HTML5 format.
        #// 
        #// @see wp_list_comments()
        #// @see https://developer.wordpress.org/reference/functions/get_comment_author_url
        #// @see https://developer.wordpress.org/reference/functions/get_comment_author
        #// @see https://developer.wordpress.org/reference/functions/get_avatar
        #// @see https://developer.wordpress.org/reference/functions/get_comment_reply_link
        #// @see https://developer.wordpress.org/reference/functions/get_edit_comment_link
        #// 
        #// @param WP_Comment $comment Comment to display.
        #// @param int        $depth   Depth of the current comment.
        #// @param array      $args    An array of arguments.
        #//
        def html5_comment(self, comment_=None, depth_=None, args_=None):
            
            
            tag_ = "div" if "div" == args_["style"] else "li"
            php_print("         <")
            php_print(tag_)
            pass
            php_print(" id=\"comment-")
            comment_ID()
            php_print("\" ")
            comment_class("parent" if self.has_children else "", comment_)
            php_print(">\n              <article id=\"div-comment-")
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
                    php_print(wp_kses_post(avatar_))
                else:
                    printf("<a href=\"%s\" rel=\"external nofollow\" class=\"url\">", comment_author_url_)
                    #// phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped --Escaped in https://developer.wordpress.org/reference/functions/get_comment_author_url
                    php_print(wp_kses_post(avatar_))
                # end if
            # end if
            printf("<span class=\"fn\">%1$s</span><span class=\"screen-reader-text says\">%2$s</span>", esc_html(comment_author_), __("says:", "twentytwenty"))
            if (not php_empty(lambda : comment_author_url_)):
                php_print("</a>")
            # end if
            php_print("""                       </div><!-- .comment-author -->
            <div class=\"comment-metadata\">
            <a href=\"""")
            php_print(esc_url(get_comment_link(comment_, args_)))
            php_print("\">\n                                ")
            #// translators: 1: Comment date, 2: Comment time.
            comment_timestamp_ = php_sprintf(__("%1$s at %2$s", "twentytwenty"), get_comment_date("", comment_), get_comment_time())
            php_print("                             <time datetime=\"")
            comment_time("c")
            php_print("\" title=\"")
            php_print(esc_attr(comment_timestamp_))
            php_print("\">\n                                    ")
            php_print(esc_html(comment_timestamp_))
            php_print("                             </time>\n                           </a>\n                          ")
            if get_edit_comment_link():
                php_print(" <span aria-hidden=\"true\">&bull;</span> <a class=\"comment-edit-link\" href=\"" + esc_url(get_edit_comment_link()) + "\">" + __("Edit", "twentytwenty") + "</a>")
            # end if
            php_print("""                       </div><!-- .comment-metadata -->
            </footer><!-- .comment-meta -->
            <div class=\"comment-content entry-content\">
            """)
            comment_text()
            if "0" == comment_.comment_approved:
                php_print("                         <p class=\"comment-awaiting-moderation\">")
                _e("Your comment is awaiting moderation.", "twentytwenty")
                php_print("</p>\n                           ")
            # end if
            php_print("""
            </div><!-- .comment-content -->
            """)
            comment_reply_link_ = get_comment_reply_link(php_array_merge(args_, Array({"add_below": "div-comment", "depth": depth_, "max_depth": args_["max_depth"], "before": "<span class=\"comment-reply\">", "after": "</span>"})))
            by_post_author_ = twentytwenty_is_comment_by_post_author(comment_)
            if comment_reply_link_ or by_post_author_:
                php_print("""
                <footer class=\"comment-footer-meta\">
                """)
                if comment_reply_link_:
                    php_print(comment_reply_link_)
                    pass
                # end if
                if by_post_author_:
                    php_print("<span class=\"by-post-author\">" + __("By Post Author", "twentytwenty") + "</span>")
                # end if
                php_print("""
                </footer>
                """)
            # end if
            php_print("""
            </article><!-- .comment-body -->
            """)
        # end def html5_comment
    # end class TwentyTwenty_Walker_Comment
# end if
