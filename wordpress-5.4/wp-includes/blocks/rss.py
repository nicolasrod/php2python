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
#// Server-side rendering of the `core/rss` block.
#// 
#// @package WordPress
#// 
#// 
#// Renders the `core/rss` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the block content with received rss items.
#//
def render_block_core_rss(attributes=None, *args_):
    
    rss = fetch_feed(attributes["feedURL"])
    if is_wp_error(rss):
        return "<div class=\"components-placeholder\"><div class=\"notice notice-error\"><strong>" + __("RSS Error:") + "</strong> " + rss.get_error_message() + "</div></div>"
    # end if
    if (not rss.get_item_quantity()):
        return "<div class=\"components-placeholder\"><div class=\"notice notice-error\">" + __("An error has occurred, which probably means the feed is down. Try again later.") + "</div></div>"
    # end if
    rss_items = rss.get_items(0, attributes["itemsToShow"])
    list_items = ""
    for item in rss_items:
        title = esc_html(php_trim(strip_tags(item.get_title())))
        if php_empty(lambda : title):
            title = __("(no title)")
        # end if
        link = item.get_link()
        link = esc_url(link)
        if link:
            title = str("<a href='") + str(link) + str("'>") + str(title) + str("</a>")
        # end if
        title = str("<div class='wp-block-rss__item-title'>") + str(title) + str("</div>")
        date = ""
        if attributes["displayDate"]:
            date = item.get_date("U")
            if date:
                date = php_sprintf("<time datetime=\"%1$s\" class=\"wp-block-rss__item-publish-date\">%2$s</time> ", date_i18n(get_option("c"), date), date_i18n(get_option("date_format"), date))
            # end if
        # end if
        author = ""
        if attributes["displayAuthor"]:
            author = item.get_author()
            if php_is_object(author):
                author = author.get_name()
                author = "<span class=\"wp-block-rss__item-author\">" + __("by") + " " + esc_html(strip_tags(author)) + "</span>"
            # end if
        # end if
        excerpt = ""
        if attributes["displayExcerpt"]:
            excerpt = html_entity_decode(item.get_description(), ENT_QUOTES, get_option("blog_charset"))
            excerpt = esc_attr(wp_trim_words(excerpt, attributes["excerptLength"], " [&hellip;]"))
            #// Change existing [...] to [&hellip;].
            if "[...]" == php_substr(excerpt, -5):
                excerpt = php_substr(excerpt, 0, -5) + "[&hellip;]"
            # end if
            excerpt = "<div class=\"wp-block-rss__item-excerpt\">" + esc_html(excerpt) + "</div>"
        # end if
        list_items += str("<li class='wp-block-rss__item'>") + str(title) + str(date) + str(author) + str(excerpt) + str("</li>")
    # end for
    class_ = "wp-block-rss"
    if (php_isset(lambda : attributes["align"])):
        class_ += " align" + attributes["align"]
    # end if
    if (php_isset(lambda : attributes["blockLayout"])) and "grid" == attributes["blockLayout"]:
        class_ += " is-grid"
    # end if
    if (php_isset(lambda : attributes["columns"])) and "grid" == attributes["blockLayout"]:
        class_ += " columns-" + attributes["columns"]
    # end if
    if (php_isset(lambda : attributes["className"])):
        class_ += " " + attributes["className"]
    # end if
    return str("<ul class='") + str(class_) + str("'>") + str(list_items) + str("</ul>")
# end def render_block_core_rss
#// 
#// Registers the `core/rss` block on server.
#//
def register_block_core_rss(*args_):
    
    register_block_type("core/rss", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"columns": Array({"type": "number", "default": 2})}, {"blockLayout": Array({"type": "string", "default": "list"})}, {"feedURL": Array({"type": "string", "default": ""})}, {"itemsToShow": Array({"type": "number", "default": 5})}, {"displayExcerpt": Array({"type": "boolean", "default": False})}, {"displayAuthor": Array({"type": "boolean", "default": False})}, {"displayDate": Array({"type": "boolean", "default": False})}, {"excerptLength": Array({"type": "number", "default": 55})})}, {"render_callback": "render_block_core_rss"}))
# end def register_block_core_rss
add_action("init", "register_block_core_rss")
