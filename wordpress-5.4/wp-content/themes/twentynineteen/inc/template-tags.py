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
#// Custom template tags for this theme
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
if (not php_function_exists("twentynineteen_posted_on")):
    #// 
    #// Prints HTML with meta information for the current post-date/time.
    #//
    def twentynineteen_posted_on(*_args_):
        
        
        time_string_ = "<time class=\"entry-date published updated\" datetime=\"%1$s\">%2$s</time>"
        if get_the_time("U") != get_the_modified_time("U"):
            time_string_ = "<time class=\"entry-date published\" datetime=\"%1$s\">%2$s</time><time class=\"updated\" datetime=\"%3$s\">%4$s</time>"
        # end if
        time_string_ = php_sprintf(time_string_, esc_attr(get_the_date(DATE_W3C)), esc_html(get_the_date()), esc_attr(get_the_modified_date(DATE_W3C)), esc_html(get_the_modified_date()))
        php_printf("<span class=\"posted-on\">%1$s<a href=\"%2$s\" rel=\"bookmark\">%3$s</a></span>", twentynineteen_get_icon_svg("watch", 16), esc_url(get_permalink()), time_string_)
    # end def twentynineteen_posted_on
# end if
if (not php_function_exists("twentynineteen_posted_by")):
    #// 
    #// Prints HTML with meta information about theme author.
    #//
    def twentynineteen_posted_by(*_args_):
        
        
        php_printf("<span class=\"byline\">%1$s<span class=\"screen-reader-text\">%2$s</span><span class=\"author vcard\"><a class=\"url fn n\" href=\"%3$s\">%4$s</a></span></span>", twentynineteen_get_icon_svg("person", 16), __("Posted by", "twentynineteen"), esc_url(get_author_posts_url(get_the_author_meta("ID"))), esc_html(get_the_author()))
    # end def twentynineteen_posted_by
# end if
if (not php_function_exists("twentynineteen_comment_count")):
    #// 
    #// Prints HTML with the comment count for the current post.
    #//
    def twentynineteen_comment_count(*_args_):
        
        
        if (not post_password_required()) and comments_open() or get_comments_number():
            php_print("<span class=\"comments-link\">")
            php_print(twentynineteen_get_icon_svg("comment", 16))
            #// translators: %s: Post title. Only visible to screen readers.
            comments_popup_link(php_sprintf(__("Leave a comment<span class=\"screen-reader-text\"> on %s</span>", "twentynineteen"), get_the_title()))
            php_print("</span>")
        # end if
    # end def twentynineteen_comment_count
# end if
if (not php_function_exists("twentynineteen_entry_footer")):
    #// 
    #// Prints HTML with meta information for the categories, tags and comments.
    #//
    def twentynineteen_entry_footer(*_args_):
        
        
        #// Hide author, post date, category and tag text for pages.
        if "post" == get_post_type():
            #// Posted by.
            twentynineteen_posted_by()
            #// Posted on.
            twentynineteen_posted_on()
            #// translators: Used between list items, there is a space after the comma.
            categories_list_ = get_the_category_list(__(", ", "twentynineteen"))
            if categories_list_:
                php_printf("<span class=\"cat-links\">%1$s<span class=\"screen-reader-text\">%2$s</span>%3$s</span>", twentynineteen_get_icon_svg("archive", 16), __("Posted in", "twentynineteen"), categories_list_)
                pass
            # end if
            #// translators: Used between list items, there is a space after the comma.
            tags_list_ = get_the_tag_list("", __(", ", "twentynineteen"))
            if tags_list_:
                php_printf("<span class=\"tags-links\">%1$s<span class=\"screen-reader-text\">%2$s </span>%3$s</span>", twentynineteen_get_icon_svg("tag", 16), __("Tags:", "twentynineteen"), tags_list_)
                pass
            # end if
        # end if
        #// Comment count.
        if (not is_singular()):
            twentynineteen_comment_count()
        # end if
        #// Edit post link.
        edit_post_link(php_sprintf(wp_kses(__("Edit <span class=\"screen-reader-text\">%s</span>", "twentynineteen"), Array({"span": Array({"class": Array()})})), get_the_title()), "<span class=\"edit-link\">" + twentynineteen_get_icon_svg("edit", 16), "</span>")
    # end def twentynineteen_entry_footer
# end if
if (not php_function_exists("twentynineteen_post_thumbnail")):
    #// 
    #// Displays an optional post thumbnail.
    #// 
    #// Wraps the post thumbnail in an anchor element on index views, or a div
    #// element when on single views.
    #//
    def twentynineteen_post_thumbnail(*_args_):
        
        
        if (not twentynineteen_can_show_post_thumbnail()):
            return
        # end if
        if is_singular():
            php_print("\n           <figure class=\"post-thumbnail\">\n             ")
            the_post_thumbnail()
            php_print("         </figure><!-- .post-thumbnail -->\n\n           ")
        else:
            php_print("\n       <figure class=\"post-thumbnail\">\n         <a class=\"post-thumbnail-inner\" href=\"")
            the_permalink()
            php_print("\" aria-hidden=\"true\" tabindex=\"-1\">\n               ")
            the_post_thumbnail("post-thumbnail")
            php_print("""           </a>
            </figure>
            """)
        # end if
        pass
    # end def twentynineteen_post_thumbnail
# end if
if (not php_function_exists("twentynineteen_get_user_avatar_markup")):
    #// 
    #// Returns the HTML markup to generate a user avatar.
    #//
    def twentynineteen_get_user_avatar_markup(id_or_email_=None, *_args_):
        if id_or_email_ is None:
            id_or_email_ = None
        # end if
        
        if (not (php_isset(lambda : id_or_email_))):
            id_or_email_ = get_current_user_id()
        # end if
        return php_sprintf("<div class=\"comment-user-avatar comment-author vcard\">%s</div>", get_avatar(id_or_email_, twentynineteen_get_avatar_size()))
    # end def twentynineteen_get_user_avatar_markup
# end if
if (not php_function_exists("twentynineteen_discussion_avatars_list")):
    #// 
    #// Displays a list of avatars involved in a discussion for a given post.
    #//
    def twentynineteen_discussion_avatars_list(comment_authors_=None, *_args_):
        
        
        if php_empty(lambda : comment_authors_):
            return
        # end if
        php_print("<ol class=\"discussion-avatar-list\">", "\n")
        for id_or_email_ in comment_authors_:
            php_printf("<li>%s</li>\n", twentynineteen_get_user_avatar_markup(id_or_email_))
        # end for
        php_print("</ol><!-- .discussion-avatar-list -->", "\n")
    # end def twentynineteen_discussion_avatars_list
# end if
if (not php_function_exists("twentynineteen_comment_form")):
    #// 
    #// Documentation for function.
    #//
    def twentynineteen_comment_form(order_=None, *_args_):
        
        
        if True == order_ or php_strtolower(order_) == php_strtolower(get_option("comment_order", "asc")):
            comment_form(Array({"logged_in_as": None, "title_reply": None}))
        # end if
    # end def twentynineteen_comment_form
# end if
if (not php_function_exists("twentynineteen_the_posts_navigation")):
    #// 
    #// Documentation for function.
    #//
    def twentynineteen_the_posts_navigation(*_args_):
        
        
        the_posts_pagination(Array({"mid_size": 2, "prev_text": php_sprintf("%s <span class=\"nav-prev-text\">%s</span>", twentynineteen_get_icon_svg("chevron_left", 22), __("Newer posts", "twentynineteen")), "next_text": php_sprintf("<span class=\"nav-next-text\">%s</span> %s", __("Older posts", "twentynineteen"), twentynineteen_get_icon_svg("chevron_right", 22))}))
    # end def twentynineteen_the_posts_navigation
# end if
if (not php_function_exists("wp_body_open")):
    #// 
    #// Fire the wp_body_open action.
    #// 
    #// Added for backward compatibility to support pre-5.2.0 WordPress versions.
    #// 
    #// @since Twenty Nineteen 1.4
    #//
    def wp_body_open(*_args_):
        
        
        #// 
        #// Triggered after the opening <body> tag.
        #// 
        #// @since Twenty Nineteen 1.4
        #//
        do_action("wp_body_open")
    # end def wp_body_open
# end if
