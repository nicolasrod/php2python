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
#// Eventually, some of the functionality here could be replaced by core features.
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#//
if (not php_function_exists("twentyseventeen_posted_on")):
    #// 
    #// Prints HTML with meta information for the current post-date/time and author.
    #//
    def twentyseventeen_posted_on(*_args_):
        
        
        #// Get the author name; wrap it in a link.
        byline_ = php_sprintf(__("by %s", "twentyseventeen"), "<span class=\"author vcard\"><a class=\"url fn n\" href=\"" + esc_url(get_author_posts_url(get_the_author_meta("ID"))) + "\">" + get_the_author() + "</a></span>")
        #// Finally, let's write all of this to the page.
        php_print("<span class=\"posted-on\">" + twentyseventeen_time_link() + "</span><span class=\"byline\"> " + byline_ + "</span>")
    # end def twentyseventeen_posted_on
# end if
if (not php_function_exists("twentyseventeen_time_link")):
    #// 
    #// Gets a nicely formatted string for the published date.
    #//
    def twentyseventeen_time_link(*_args_):
        
        
        time_string_ = "<time class=\"entry-date published updated\" datetime=\"%1$s\">%2$s</time>"
        if get_the_time("U") != get_the_modified_time("U"):
            time_string_ = "<time class=\"entry-date published\" datetime=\"%1$s\">%2$s</time><time class=\"updated\" datetime=\"%3$s\">%4$s</time>"
        # end if
        time_string_ = php_sprintf(time_string_, get_the_date(DATE_W3C), get_the_date(), get_the_modified_date(DATE_W3C), get_the_modified_date())
        #// Wrap the time string in a link, and preface it with 'Posted on'.
        return php_sprintf(__("<span class=\"screen-reader-text\">Posted on</span> %s", "twentyseventeen"), "<a href=\"" + esc_url(get_permalink()) + "\" rel=\"bookmark\">" + time_string_ + "</a>")
    # end def twentyseventeen_time_link
# end if
if (not php_function_exists("twentyseventeen_entry_footer")):
    #// 
    #// Prints HTML with meta information for the categories, tags and comments.
    #//
    def twentyseventeen_entry_footer(*_args_):
        
        
        #// translators: Used between list items, there is a space after the comma.
        separate_meta_ = __(", ", "twentyseventeen")
        #// Get Categories for posts.
        categories_list_ = get_the_category_list(separate_meta_)
        #// Get Tags for posts.
        tags_list_ = get_the_tag_list("", separate_meta_)
        #// We don't want to output .entry-footer if it will be empty, so make sure its not.
        if twentyseventeen_categorized_blog() and categories_list_ or tags_list_ or get_edit_post_link():
            php_print("<footer class=\"entry-footer\">")
            if "post" == get_post_type():
                if categories_list_ and twentyseventeen_categorized_blog() or tags_list_:
                    php_print("<span class=\"cat-tags-links\">")
                    #// Make sure there's more than one category before displaying.
                    if categories_list_ and twentyseventeen_categorized_blog():
                        php_print("<span class=\"cat-links\">" + twentyseventeen_get_svg(Array({"icon": "folder-open"})) + "<span class=\"screen-reader-text\">" + __("Categories", "twentyseventeen") + "</span>" + categories_list_ + "</span>")
                    # end if
                    if tags_list_ and (not is_wp_error(tags_list_)):
                        php_print("<span class=\"tags-links\">" + twentyseventeen_get_svg(Array({"icon": "hashtag"})) + "<span class=\"screen-reader-text\">" + __("Tags", "twentyseventeen") + "</span>" + tags_list_ + "</span>")
                    # end if
                    php_print("</span>")
                # end if
            # end if
            twentyseventeen_edit_link()
            php_print("</footer> <!-- .entry-footer -->")
        # end if
    # end def twentyseventeen_entry_footer
# end if
if (not php_function_exists("twentyseventeen_edit_link")):
    #// 
    #// Returns an accessibility-friendly link to edit a post or page.
    #// 
    #// This also gives us a little context about what exactly we're editing
    #// (post or page?) so that users understand a bit more where they are in terms
    #// of the template hierarchy and their content. Helpful when/if the single-page
    #// layout with multiple posts/pages shown gets confusing.
    #//
    def twentyseventeen_edit_link(*_args_):
        
        
        edit_post_link(php_sprintf(__("Edit<span class=\"screen-reader-text\"> \"%s\"</span>", "twentyseventeen"), get_the_title()), "<span class=\"edit-link\">", "</span>")
    # end def twentyseventeen_edit_link
# end if
#// 
#// Display a front page section.
#// 
#// @param WP_Customize_Partial $partial Partial associated with a selective refresh request.
#// @param integer              $id Front page section to display.
#//
def twentyseventeen_front_page_section(partial_=None, id_=0, *_args_):
    if partial_ is None:
        partial_ = None
    # end if
    
    if php_is_a(partial_, "WP_Customize_Partial"):
        #// Find out the id and set it up during a selective refresh.
        global twentyseventeencounter_
        php_check_if_defined("twentyseventeencounter_")
        id_ = php_str_replace("panel_", "", partial_.id)
        twentyseventeencounter_ = id_
    # end if
    global post_
    php_check_if_defined("post_")
    #// Modify the global post object before setting up post data.
    if get_theme_mod("panel_" + id_):
        post_ = get_post(get_theme_mod("panel_" + id_))
        setup_postdata(post_)
        set_query_var("panel", id_)
        get_template_part("template-parts/page/content", "front-page-panels")
        wp_reset_postdata()
    elif is_customize_preview():
        #// The output placeholder anchor.
        printf("<article class=\"panel-placeholder panel twentyseventeen-panel twentyseventeen-panel%1$s\" id=\"panel%1$s\">" + "<span class=\"twentyseventeen-panel-title\">%2$s</span></article>", id_, php_sprintf(__("Front Page Section %s Placeholder", "twentyseventeen"), id_))
    # end if
# end def twentyseventeen_front_page_section
#// 
#// Returns true if a blog has more than 1 category.
#// 
#// @return bool
#//
def twentyseventeen_categorized_blog(*_args_):
    
    
    category_count_ = get_transient("twentyseventeen_categories")
    if False == category_count_:
        #// Create an array of all the categories that are attached to posts.
        categories_ = get_categories(Array({"fields": "ids", "hide_empty": 1, "number": 2}))
        #// Count the number of categories that are attached to the posts.
        category_count_ = php_count(categories_)
        set_transient("twentyseventeen_categories", category_count_)
    # end if
    #// Allow viewing case of 0 or 1 categories in post preview.
    if is_preview():
        return True
    # end if
    return category_count_ > 1
# end def twentyseventeen_categorized_blog
#// 
#// Flush out the transients used in twentyseventeen_categorized_blog.
#//
def twentyseventeen_category_transient_flusher(*_args_):
    
    
    if php_defined("DOING_AUTOSAVE") and DOING_AUTOSAVE:
        return
    # end if
    #// Like, beat it. Dig?
    delete_transient("twentyseventeen_categories")
# end def twentyseventeen_category_transient_flusher
add_action("edit_category", "twentyseventeen_category_transient_flusher")
add_action("save_post", "twentyseventeen_category_transient_flusher")
if (not php_function_exists("wp_body_open")):
    #// 
    #// Fire the wp_body_open action.
    #// 
    #// Added for backward compatibility to support pre-5.2.0 WordPress versions.
    #// 
    #// @since Twenty Seventeen 2.2
    #//
    def wp_body_open(*_args_):
        
        
        #// 
        #// Triggered after the opening <body> tag.
        #// 
        #// @since Twenty Seventeen 2.2
        #//
        do_action("wp_body_open")
    # end def wp_body_open
# end if
