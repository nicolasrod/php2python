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
#// Atom Feed Template for displaying Atom Comments feed.
#// 
#// @package WordPress
#//
php_header("Content-Type: " + feed_content_type("atom") + "; charset=" + get_option("blog_charset"), True)
php_print("<?xml version=\"1.0\" encoding=\"" + get_option("blog_charset") + "\" ?" + ">")
#// This action is documented in wp-includes/feed-rss2.php
do_action("rss_tag_pre", "atom-comments")
php_print("<feed\n  xmlns=\"http://www.w3.org/2005/Atom\"\n xml:lang=\"")
bloginfo_rss("language")
php_print("\"\n xmlns:thr=\"http://purl.org/syndication/thread/1.0\"\n  ")
#// This action is documented in wp-includes/feed-atom.php
do_action("atom_ns")
#// 
#// Fires inside the feed tag in the Atom comment feed.
#// 
#// @since 2.8.0
#//
do_action("atom_comments_ns")
php_print(">\n  <title type=\"text\">\n ")
if is_singular():
    #// translators: Comments feed title. %s: Post title.
    printf(ent2ncr(__("Comments on %s")), get_the_title_rss())
elif is_search():
    #// translators: Comments feed title. 1: Site title, 2: Search query.
    printf(ent2ncr(__("Comments for %1$s searching on %2$s")), get_bloginfo_rss("name"), get_search_query())
else:
    #// translators: Comments feed title. %s: Site title.
    printf(ent2ncr(__("Comments for %s")), get_wp_title_rss())
# end if
php_print(" </title>\n  <subtitle type=\"text\">")
bloginfo_rss("description")
php_print("</subtitle>\n\n  <updated>")
php_print(get_feed_build_date("Y-m-d\\TH:i:s\\Z"))
php_print("</updated>\n\n")
if is_singular():
    php_print(" <link rel=\"alternate\" type=\"")
    bloginfo_rss("html_type")
    php_print("\" href=\"")
    comments_link_feed()
    php_print("\" />\n  <link rel=\"self\" type=\"application/atom+xml\" href=\"")
    php_print(esc_url(get_post_comments_feed_link("", "atom")))
    php_print("\" />\n  <id>")
    php_print(esc_url(get_post_comments_feed_link("", "atom")))
    php_print("</id>\n")
elif is_search():
    php_print(" <link rel=\"alternate\" type=\"")
    bloginfo_rss("html_type")
    php_print("\" href=\"")
    php_print(home_url() + "?s=" + get_search_query())
    php_print("\" />\n  <link rel=\"self\" type=\"application/atom+xml\" href=\"")
    php_print(get_search_comments_feed_link("", "atom"))
    php_print("\" />\n  <id>")
    php_print(get_search_comments_feed_link("", "atom"))
    php_print("</id>\n")
else:
    php_print(" <link rel=\"alternate\" type=\"")
    bloginfo_rss("html_type")
    php_print("\" href=\"")
    bloginfo_rss("url")
    php_print("\" />\n  <link rel=\"self\" type=\"application/atom+xml\" href=\"")
    bloginfo_rss("comments_atom_url")
    php_print("\" />\n  <id>")
    bloginfo_rss("comments_atom_url")
    php_print("</id>\n")
# end if
#// 
#// Fires at the end of the Atom comment feed header.
#// 
#// @since 2.8.0
#//
do_action("comments_atom_head")
while True:
    
    if not (have_comments()):
        break
    # end if
    the_comment()
    comment_post_ = get_post(comment_.comment_post_ID)
    PHP_GLOBALS["post"] = comment_post_
    php_print(" <entry>\n       <title>\n       ")
    if (not is_singular()):
        title_ = get_the_title(comment_post_.ID)
        #// This filter is documented in wp-includes/feed.php
        title_ = apply_filters("the_title_rss", title_)
        #// translators: Individual comment title. 1: Post title, 2: Comment author name.
        printf(ent2ncr(__("Comment on %1$s by %2$s")), title_, get_comment_author_rss())
    else:
        #// translators: Comment author title. %s: Comment author name.
        printf(ent2ncr(__("By: %s")), get_comment_author_rss())
    # end if
    php_print("     </title>\n      <link rel=\"alternate\" href=\"")
    comment_link()
    php_print("\" type=\"")
    bloginfo_rss("html_type")
    php_print("""\" />
    <author>
    <name>""")
    comment_author_rss()
    php_print("</name>\n            ")
    if get_comment_author_url():
        php_print("<uri>" + get_comment_author_url() + "</uri>")
    # end if
    php_print("""
    </author>
    <id>""")
    comment_guid()
    php_print("</id>\n      <updated>")
    php_print(mysql2date("Y-m-d\\TH:i:s\\Z", get_comment_time("Y-m-d H:i:s", True, False), False))
    php_print("</updated>\n     <published>")
    php_print(mysql2date("Y-m-d\\TH:i:s\\Z", get_comment_time("Y-m-d H:i:s", True, False), False))
    php_print("</published>\n\n     ")
    if post_password_required(comment_post_):
        php_print("         <content type=\"html\" xml:base=\"")
        comment_link()
        php_print("\"><![CDATA[")
        php_print(get_the_password_form())
        php_print("]]></content>\n      ")
    else:
        php_print("         <content type=\"html\" xml:base=\"")
        comment_link()
        php_print("\"><![CDATA[")
        comment_text()
        php_print("]]></content>\n      ")
    # end if
    pass
    php_print("\n       ")
    #// Return comment threading information (https://www.ietf.org/rfc/rfc4685.txt).
    if 0 == comment_.comment_parent:
        pass
        php_print("         <thr:in-reply-to ref=\"")
        the_guid()
        php_print("\" href=\"")
        the_permalink_rss()
        php_print("\" type=\"")
        bloginfo_rss("html_type")
        php_print("\" />\n          ")
    else:
        #// This comment is in reply to another comment.
        parent_comment_ = get_comment(comment_.comment_parent)
        pass
        php_print("         <thr:in-reply-to ref=\"")
        comment_guid(parent_comment_)
        php_print("\" href=\"")
        php_print(get_comment_link(parent_comment_))
        php_print("\" type=\"")
        bloginfo_rss("html_type")
        php_print("\" />\n          ")
    # end if
    #// 
    #// Fires at the end of each Atom comment feed item.
    #// 
    #// @since 2.2.0
    #// 
    #// @param int $comment_id      ID of the current comment.
    #// @param int $comment_post_id ID of the post the current comment is connected to.
    #//
    do_action("comment_atom_entry", comment_.comment_ID, comment_post_.ID)
    php_print(" </entry>\n  ")
# end while
php_print("</feed>\n")
