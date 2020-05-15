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
#// Comment API: Walker_Comment class
#// 
#// @package WordPress
#// @subpackage Comments
#// @since 4.4.0
#// 
#// 
#// Core walker class used to create an HTML list of comments.
#// 
#// @since 2.7.0
#// 
#// @see Walker
#//
class Walker_Comment(Walker):
    tree_type = "comment"
    db_fields = Array({"parent": "comment_parent", "id": "comment_ID"})
    #// 
    #// Starts the list before the elements are added.
    #// 
    #// @since 2.7.0
    #// 
    #// @see Walker::start_lvl()
    #// @global int $comment_depth
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param int    $depth  Optional. Depth of the current comment. Default 0.
    #// @param array  $args   Optional. Uses 'style' argument for type of HTML list. Default empty array.
    #//
    def start_lvl(self, output=None, depth=0, args=Array()):
        global PHP_GLOBALS
        PHP_GLOBALS["comment_depth"] = depth + 1
        for case in Switch(args["style"]):
            if case("div"):
                break
            # end if
            if case("ol"):
                output += "<ol class=\"children\">" + "\n"
                break
            # end if
            if case("ul"):
                pass
            # end if
            if case():
                output += "<ul class=\"children\">" + "\n"
                break
            # end if
        # end for
    # end def start_lvl
    #// 
    #// Ends the list of items after the elements are added.
    #// 
    #// @since 2.7.0
    #// 
    #// @see Walker::end_lvl()
    #// @global int $comment_depth
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param int    $depth  Optional. Depth of the current comment. Default 0.
    #// @param array  $args   Optional. Will only append content if style argument value is 'ol' or 'ul'.
    #// Default empty array.
    #//
    def end_lvl(self, output=None, depth=0, args=Array()):
        global PHP_GLOBALS
        PHP_GLOBALS["comment_depth"] = depth + 1
        for case in Switch(args["style"]):
            if case("div"):
                break
            # end if
            if case("ol"):
                output += "</ol><!-- .children -->\n"
                break
            # end if
            if case("ul"):
                pass
            # end if
            if case():
                output += "</ul><!-- .children -->\n"
                break
            # end if
        # end for
    # end def end_lvl
    #// 
    #// Traverses elements to create list from elements.
    #// 
    #// This function is designed to enhance Walker::display_element() to
    #// display children of higher nesting levels than selected inline on
    #// the highest depth level displayed. This prevents them being orphaned
    #// at the end of the comment list.
    #// 
    #// Example: max_depth = 2, with 5 levels of nested content.
    #// 1
    #// 1.1
    #// 1.1.1
    #// 1.1.1.1
    #// 1.1.1.1.1
    #// 1.1.2
    #// 1.1.2.1
    #// 2
    #// 2.2
    #// 
    #// @since 2.7.0
    #// 
    #// @see Walker::display_element()
    #// @see wp_list_comments()
    #// 
    #// @param WP_Comment $element           Comment data object.
    #// @param array      $children_elements List of elements to continue traversing. Passed by reference.
    #// @param int        $max_depth         Max depth to traverse.
    #// @param int        $depth             Depth of the current element.
    #// @param array      $args              An array of arguments.
    #// @param string     $output            Used to append additional content. Passed by reference.
    #//
    def display_element(self, element=None, children_elements=None, max_depth=None, depth=None, args=None, output=None):
        
        if (not element):
            return
        # end if
        id_field = self.db_fields["id"]
        id = element.id_field
        super().display_element(element, children_elements, max_depth, depth, args, output)
        #// 
        #// If at the max depth, and the current element still has children, loop over those
        #// and display them at this level. This is to prevent them being orphaned to the end
        #// of the list.
        #//
        if max_depth <= depth + 1 and (php_isset(lambda : children_elements[id])):
            for child in children_elements[id]:
                self.display_element(child, children_elements, max_depth, depth, args, output)
            # end for
            children_elements[id] = None
        # end if
    # end def display_element
    #// 
    #// Starts the element output.
    #// 
    #// @since 2.7.0
    #// 
    #// @see Walker::start_el()
    #// @see wp_list_comments()
    #// @global int        $comment_depth
    #// @global WP_Comment $comment       Global comment object.
    #// 
    #// @param string     $output  Used to append additional content. Passed by reference.
    #// @param WP_Comment $comment Comment data object.
    #// @param int        $depth   Optional. Depth of the current comment in reference to parents. Default 0.
    #// @param array      $args    Optional. An array of arguments. Default empty array.
    #// @param int        $id      Optional. ID of the current comment. Default 0 (unused).
    #//
    def start_el(self, output=None, comment=None, depth=0, args=Array(), id=0):
        global PHP_GLOBALS
        depth += 1
        PHP_GLOBALS["comment_depth"] = depth
        PHP_GLOBALS["comment"] = comment
        if (not php_empty(lambda : args["callback"])):
            ob_start()
            php_call_user_func(args["callback"], comment, args, depth)
            output += ob_get_clean()
            return
        # end if
        if "pingback" == comment.comment_type or "trackback" == comment.comment_type and args["short_ping"]:
            ob_start()
            self.ping(comment, depth, args)
            output += ob_get_clean()
        elif "html5" == args["format"]:
            ob_start()
            self.html5_comment(comment, depth, args)
            output += ob_get_clean()
        else:
            ob_start()
            self.comment(comment, depth, args)
            output += ob_get_clean()
        # end if
    # end def start_el
    #// 
    #// Ends the element output, if needed.
    #// 
    #// @since 2.7.0
    #// 
    #// @see Walker::end_el()
    #// @see wp_list_comments()
    #// 
    #// @param string     $output  Used to append additional content. Passed by reference.
    #// @param WP_Comment $comment The current comment object. Default current comment.
    #// @param int        $depth   Optional. Depth of the current comment. Default 0.
    #// @param array      $args    Optional. An array of arguments. Default empty array.
    #//
    def end_el(self, output=None, comment=None, depth=0, args=Array()):
        
        if (not php_empty(lambda : args["end-callback"])):
            ob_start()
            php_call_user_func(args["end-callback"], comment, args, depth)
            output += ob_get_clean()
            return
        # end if
        if "div" == args["style"]:
            output += "</div><!-- #comment-## -->\n"
        else:
            output += "</li><!-- #comment-## -->\n"
        # end if
    # end def end_el
    #// 
    #// Outputs a pingback comment.
    #// 
    #// @since 3.6.0
    #// 
    #// @see wp_list_comments()
    #// 
    #// @param WP_Comment $comment The comment object.
    #// @param int        $depth   Depth of the current comment.
    #// @param array      $args    An array of arguments.
    #//
    def ping(self, comment=None, depth=None, args=None):
        
        tag = "div" if "div" == args["style"] else "li"
        php_print("     <")
        php_print(tag)
        php_print(" id=\"comment-")
        comment_ID()
        php_print("\" ")
        comment_class("", comment)
        php_print(">\n          <div class=\"comment-body\">\n              ")
        _e("Pingback:")
        php_print(" ")
        comment_author_link(comment)
        php_print(" ")
        edit_comment_link(__("Edit"), "<span class=\"edit-link\">", "</span>")
        php_print("         </div>\n        ")
    # end def ping
    #// 
    #// Outputs a single comment.
    #// 
    #// @since 3.6.0
    #// 
    #// @see wp_list_comments()
    #// 
    #// @param WP_Comment $comment Comment to display.
    #// @param int        $depth   Depth of the current comment.
    #// @param array      $args    An array of arguments.
    #//
    def comment(self, comment=None, depth=None, args=None):
        
        if "div" == args["style"]:
            tag = "div"
            add_below = "comment"
        else:
            tag = "li"
            add_below = "div-comment"
        # end if
        commenter = wp_get_current_commenter()
        if commenter["comment_author_email"]:
            moderation_note = __("Your comment is awaiting moderation.")
        else:
            moderation_note = __("Your comment is awaiting moderation. This is a preview, your comment will be visible after it has been approved.")
        # end if
        php_print("     <")
        php_print(tag)
        php_print(" ")
        comment_class("parent" if self.has_children else "", comment)
        php_print(" id=\"comment-")
        comment_ID()
        php_print("\">\n        ")
        if "div" != args["style"]:
            php_print("     <div id=\"div-comment-")
            comment_ID()
            php_print("\" class=\"comment-body\">\n     ")
        # end if
        php_print("     <div class=\"comment-author vcard\">\n          ")
        if 0 != args["avatar_size"]:
            php_print(get_avatar(comment, args["avatar_size"]))
        # end if
        php_print("         ")
        printf(__("%s <span class=\"says\">says:</span>"), php_sprintf("<cite class=\"fn\">%s</cite>", get_comment_author_link(comment)))
        php_print("     </div>\n        ")
        if "0" == comment.comment_approved:
            php_print("     <em class=\"comment-awaiting-moderation\">")
            php_print(moderation_note)
            php_print("</em>\n      <br />\n        ")
        # end if
        php_print("\n       <div class=\"comment-meta commentmetadata\"><a href=\"")
        php_print(esc_url(get_comment_link(comment, args)))
        php_print("\">\n            ")
        #// translators: 1: Comment date, 2: Comment time.
        printf(__("%1$s at %2$s"), get_comment_date("", comment), get_comment_time())
        php_print("             </a>\n              ")
        edit_comment_link(__("(Edit)"), "&nbsp;&nbsp;", "")
        php_print("     </div>\n\n      ")
        comment_text(comment, php_array_merge(args, Array({"add_below": add_below, "depth": depth, "max_depth": args["max_depth"]})))
        php_print("\n       ")
        comment_reply_link(php_array_merge(args, Array({"add_below": add_below, "depth": depth, "max_depth": args["max_depth"], "before": "<div class=\"reply\">", "after": "</div>"})))
        php_print("\n       ")
        if "div" != args["style"]:
            php_print("     </div>\n        ")
        # end if
        php_print("     ")
    # end def comment
    #// 
    #// Outputs a comment in the HTML5 format.
    #// 
    #// @since 3.6.0
    #// 
    #// @see wp_list_comments()
    #// 
    #// @param WP_Comment $comment Comment to display.
    #// @param int        $depth   Depth of the current comment.
    #// @param array      $args    An array of arguments.
    #//
    def html5_comment(self, comment=None, depth=None, args=None):
        
        tag = "div" if "div" == args["style"] else "li"
        commenter = wp_get_current_commenter()
        if commenter["comment_author_email"]:
            moderation_note = __("Your comment is awaiting moderation.")
        else:
            moderation_note = __("Your comment is awaiting moderation. This is a preview, your comment will be visible after it has been approved.")
        # end if
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
        if 0 != args["avatar_size"]:
            php_print(get_avatar(comment, args["avatar_size"]))
        # end if
        php_print("                     ")
        printf(__("%s <span class=\"says\">says:</span>"), php_sprintf("<b class=\"fn\">%s</b>", get_comment_author_link(comment)))
        php_print("""                   </div><!-- .comment-author -->
        <div class=\"comment-metadata\">
        <a href=\"""")
        php_print(esc_url(get_comment_link(comment, args)))
        php_print("\">\n                            <time datetime=\"")
        comment_time("c")
        php_print("\">\n                                ")
        #// translators: 1: Comment date, 2: Comment time.
        printf(__("%1$s at %2$s"), get_comment_date("", comment), get_comment_time())
        php_print("                         </time>\n                       </a>\n                      ")
        edit_comment_link(__("Edit"), "<span class=\"edit-link\">", "</span>")
        php_print("                 </div><!-- .comment-metadata -->\n\n                    ")
        if "0" == comment.comment_approved:
            php_print("                 <em class=\"comment-awaiting-moderation\">")
            php_print(moderation_note)
            php_print("</em>\n                  ")
        # end if
        php_print("""               </footer><!-- .comment-meta -->
        <div class=\"comment-content\">
        """)
        comment_text()
        php_print("             </div><!-- .comment-content -->\n\n             ")
        comment_reply_link(php_array_merge(args, Array({"add_below": "div-comment", "depth": depth, "max_depth": args["max_depth"], "before": "<div class=\"reply\">", "after": "</div>"})))
        php_print("         </article><!-- .comment-body -->\n      ")
    # end def html5_comment
# end class Walker_Comment
