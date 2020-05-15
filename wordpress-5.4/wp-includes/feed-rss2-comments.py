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
#// RSS2 Feed Template for displaying RSS2 Comments feed.
#// 
#// @package WordPress
#//
php_header("Content-Type: " + feed_content_type("rss2") + "; charset=" + get_option("blog_charset"), True)
php_print("<?xml version=\"1.0\" encoding=\"" + get_option("blog_charset") + "\"?" + ">")
#// This action is documented in wp-includes/feed-rss2.php
do_action("rss_tag_pre", "rss2-comments")
php_print("""<rss version=\"2.0\"
xmlns:content=\"http://purl.org/rss/1.0/modules/content/\"
xmlns:dc=\"http://purl.org/dc/elements/1.1/\"
xmlns:atom=\"http://www.w3.org/2005/Atom\"
xmlns:sy=\"http://purl.org/rss/1.0/modules/syndication/\"
""")
#// This action is documented in wp-includes/feed-rss2.php
do_action("rss2_ns")
php_print("\n   ")
#// 
#// Fires at the end of the RSS root to add namespaces.
#// 
#// @since 2.8.0
#//
do_action("rss2_comments_ns")
php_print(""">
<channel>
<title>
""")
if is_singular():
    #// translators: Comments feed title. %s: Post title.
    printf(ent2ncr(__("Comments on: %s")), get_the_title_rss())
elif is_search():
    #// translators: Comments feed title. 1: Site title, 2: Search query.
    printf(ent2ncr(__("Comments for %1$s searching on %2$s")), get_bloginfo_rss("name"), get_search_query())
else:
    #// translators: Comments feed title. %s: Site title.
    printf(ent2ncr(__("Comments for %s")), get_wp_title_rss())
# end if
php_print(" </title>\n  <atom:link href=\"")
self_link()
php_print("\" rel=\"self\" type=\"application/rss+xml\" />\n    <link>")
the_permalink_rss() if is_single() else bloginfo_rss("url")
php_print("</link>\n    <description>")
bloginfo_rss("description")
php_print("</description>\n <lastBuildDate>")
php_print(get_feed_build_date("r"))
php_print("</lastBuildDate>\n   <sy:updatePeriod>\n ")
#// This filter is documented in wp-includes/feed-rss2.php
php_print(apply_filters("rss_update_period", "hourly"))
php_print(" </sy:updatePeriod>\n    <sy:updateFrequency>\n  ")
#// This filter is documented in wp-includes/feed-rss2.php
php_print(apply_filters("rss_update_frequency", "1"))
php_print(" </sy:updateFrequency>\n ")
#// 
#// Fires at the end of the RSS2 comment feed header.
#// 
#// @since 2.3.0
#//
do_action("commentsrss2_head")
while True:
    
    if not (have_comments()):
        break
    # end if
    the_comment()
    comment_post = get_post(comment.comment_post_ID)
    PHP_GLOBALS["post"] = comment_post
    php_print(" <item>\n        <title>\n       ")
    if (not is_singular()):
        title = get_the_title(comment_post.ID)
        #// This filter is documented in wp-includes/feed.php
        title = apply_filters("the_title_rss", title)
        #// translators: Individual comment title. 1: Post title, 2: Comment author name.
        printf(ent2ncr(__("Comment on %1$s by %2$s")), title, get_comment_author_rss())
    else:
        #// translators: Comment author title. %s: Comment author name.
        printf(ent2ncr(__("By: %s")), get_comment_author_rss())
    # end if
    php_print("     </title>\n      <link>")
    comment_link()
    php_print("</link>\n\n      <dc:creator><![CDATA[")
    php_print(get_comment_author_rss())
    php_print("]]></dc:creator>\n       <pubDate>")
    php_print(mysql2date("D, d M Y H:i:s +0000", get_comment_time("Y-m-d H:i:s", True, False), False))
    php_print("</pubDate>\n     <guid isPermaLink=\"false\">")
    comment_guid()
    php_print("</guid>\n\n      ")
    if post_password_required(comment_post):
        php_print("         <description>")
        php_print(ent2ncr(__("Protected Comments: Please enter your password to view comments.")))
        php_print("</description>\n         <content:encoded><![CDATA[")
        php_print(get_the_password_form())
        php_print("]]></content:encoded>\n      ")
    else:
        php_print("         <description><![CDATA[")
        comment_text_rss()
        php_print("]]></description>\n          <content:encoded><![CDATA[")
        comment_text()
        php_print("]]></content:encoded>\n      ")
    # end if
    pass
    php_print("\n       ")
    #// 
    #// Fires at the end of each RSS2 comment feed item.
    #// 
    #// @since 2.1.0
    #// 
    #// @param int $comment->comment_ID The ID of the comment being displayed.
    #// @param int $comment_post->ID    The ID of the post the comment is connected to.
    #//
    do_action("commentrss2_item", comment.comment_ID, comment_post.ID)
    php_print(" </item>\n   ")
# end while
php_print("</channel>\n</rss>\n")
