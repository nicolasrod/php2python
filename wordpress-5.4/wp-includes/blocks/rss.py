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
def render_block_core_rss(attributes_=None, *_args_):
    
    
    rss_ = fetch_feed(attributes_["feedURL"])
    if is_wp_error(rss_):
        return "<div class=\"components-placeholder\"><div class=\"notice notice-error\"><strong>" + __("RSS Error:") + "</strong> " + rss_.get_error_message() + "</div></div>"
    # end if
    if (not rss_.get_item_quantity()):
        return "<div class=\"components-placeholder\"><div class=\"notice notice-error\">" + __("An error has occurred, which probably means the feed is down. Try again later.") + "</div></div>"
    # end if
    rss_items_ = rss_.get_items(0, attributes_["itemsToShow"])
    list_items_ = ""
    for item_ in rss_items_:
        title_ = esc_html(php_trim(strip_tags(item_.get_title())))
        if php_empty(lambda : title_):
            title_ = __("(no title)")
        # end if
        link_ = item_.get_link()
        link_ = esc_url(link_)
        if link_:
            title_ = str("<a href='") + str(link_) + str("'>") + str(title_) + str("</a>")
        # end if
        title_ = str("<div class='wp-block-rss__item-title'>") + str(title_) + str("</div>")
        date_ = ""
        if attributes_["displayDate"]:
            date_ = item_.get_date("U")
            if date_:
                date_ = php_sprintf("<time datetime=\"%1$s\" class=\"wp-block-rss__item-publish-date\">%2$s</time> ", date_i18n(get_option("c"), date_), date_i18n(get_option("date_format"), date_))
            # end if
        # end if
        author_ = ""
        if attributes_["displayAuthor"]:
            author_ = item_.get_author()
            if php_is_object(author_):
                author_ = author_.get_name()
                author_ = "<span class=\"wp-block-rss__item-author\">" + __("by") + " " + esc_html(strip_tags(author_)) + "</span>"
            # end if
        # end if
        excerpt_ = ""
        if attributes_["displayExcerpt"]:
            excerpt_ = html_entity_decode(item_.get_description(), ENT_QUOTES, get_option("blog_charset"))
            excerpt_ = esc_attr(wp_trim_words(excerpt_, attributes_["excerptLength"], " [&hellip;]"))
            #// Change existing [...] to [&hellip;].
            if "[...]" == php_substr(excerpt_, -5):
                excerpt_ = php_substr(excerpt_, 0, -5) + "[&hellip;]"
            # end if
            excerpt_ = "<div class=\"wp-block-rss__item-excerpt\">" + esc_html(excerpt_) + "</div>"
        # end if
        list_items_ += str("<li class='wp-block-rss__item'>") + str(title_) + str(date_) + str(author_) + str(excerpt_) + str("</li>")
    # end for
    class_ = "wp-block-rss"
    if (php_isset(lambda : attributes_["align"])):
        class_ += " align" + attributes_["align"]
    # end if
    if (php_isset(lambda : attributes_["blockLayout"])) and "grid" == attributes_["blockLayout"]:
        class_ += " is-grid"
    # end if
    if (php_isset(lambda : attributes_["columns"])) and "grid" == attributes_["blockLayout"]:
        class_ += " columns-" + attributes_["columns"]
    # end if
    if (php_isset(lambda : attributes_["className"])):
        class_ += " " + attributes_["className"]
    # end if
    return str("<ul class='") + str(class_) + str("'>") + str(list_items_) + str("</ul>")
# end def render_block_core_rss
#// 
#// Registers the `core/rss` block on server.
#//
def register_block_core_rss(*_args_):
    
    
    register_block_type("core/rss", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"columns": Array({"type": "number", "default": 2})}, {"blockLayout": Array({"type": "string", "default": "list"})}, {"feedURL": Array({"type": "string", "default": ""})}, {"itemsToShow": Array({"type": "number", "default": 5})}, {"displayExcerpt": Array({"type": "boolean", "default": False})}, {"displayAuthor": Array({"type": "boolean", "default": False})}, {"displayDate": Array({"type": "boolean", "default": False})}, {"excerptLength": Array({"type": "number", "default": 55})})}, {"render_callback": "render_block_core_rss"}))
# end def register_block_core_rss
add_action("init", "register_block_core_rss")
