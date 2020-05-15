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
#// RSS2 Feed Template for displaying RSS2 Posts feed.
#// 
#// @package WordPress
#//
php_header("Content-Type: " + feed_content_type("rss2") + "; charset=" + get_option("blog_charset"), True)
more = 1
php_print("<?xml version=\"1.0\" encoding=\"" + get_option("blog_charset") + "\"?" + ">")
#// 
#// Fires between the xml and rss tags in a feed.
#// 
#// @since 4.0.0
#// 
#// @param string $context Type of feed. Possible values include 'rss2', 'rss2-comments',
#// 'rdf', 'atom', and 'atom-comments'.
#//
do_action("rss_tag_pre", "rss2")
php_print("""<rss version=\"2.0\"
xmlns:content=\"http://purl.org/rss/1.0/modules/content/\"
xmlns:wfw=\"http://wellformedweb.org/CommentAPI/\"
xmlns:dc=\"http://purl.org/dc/elements/1.1/\"
xmlns:atom=\"http://www.w3.org/2005/Atom\"
xmlns:sy=\"http://purl.org/rss/1.0/modules/syndication/\"
xmlns:slash=\"http://purl.org/rss/1.0/modules/slash/\"
""")
#// 
#// Fires at the end of the RSS root to add namespaces.
#// 
#// @since 2.0.0
#//
do_action("rss2_ns")
php_print(""">
<channel>
<title>""")
wp_title_rss()
php_print("</title>\n   <atom:link href=\"")
self_link()
php_print("\" rel=\"self\" type=\"application/rss+xml\" />\n    <link>")
bloginfo_rss("url")
php_print("</link>\n    <description>")
bloginfo_rss("description")
php_print("</description>\n <lastBuildDate>")
php_print(get_feed_build_date("r"))
php_print("</lastBuildDate>\n   <language>")
bloginfo_rss("language")
php_print("</language>\n    <sy:updatePeriod>\n ")
duration = "hourly"
#// 
#// Filters how often to update the RSS feed.
#// 
#// @since 2.1.0
#// 
#// @param string $duration The update period. Accepts 'hourly', 'daily', 'weekly', 'monthly',
#// 'yearly'. Default 'hourly'.
#//
php_print(apply_filters("rss_update_period", duration))
php_print(" </sy:updatePeriod>\n    <sy:updateFrequency>\n  ")
frequency = "1"
#// 
#// Filters the RSS update frequency.
#// 
#// @since 2.1.0
#// 
#// @param string $frequency An integer passed as a string representing the frequency
#// of RSS updates within the update period. Default '1'.
#//
php_print(apply_filters("rss_update_frequency", frequency))
php_print(" </sy:updateFrequency>\n ")
#// 
#// Fires at the end of the RSS2 Feed Header.
#// 
#// @since 2.0.0
#//
do_action("rss2_head")
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    php_print(" <item>\n        <title>")
    the_title_rss()
    php_print("</title>\n       <link>")
    the_permalink_rss()
    php_print("</link>\n        ")
    if get_comments_number() or comments_open():
        php_print("         <comments>")
        comments_link_feed()
        php_print("</comments>\n        ")
    # end if
    php_print("\n       <dc:creator><![CDATA[")
    the_author()
    php_print("]]></dc:creator>\n       <pubDate>")
    php_print(mysql2date("D, d M Y H:i:s +0000", get_post_time("Y-m-d H:i:s", True), False))
    php_print("</pubDate>\n     ")
    the_category_rss("rss2")
    php_print("     <guid isPermaLink=\"false\">")
    the_guid()
    php_print("</guid>\n\n      ")
    if get_option("rss_use_excerpt"):
        php_print("         <description><![CDATA[")
        the_excerpt_rss()
        php_print("]]></description>\n      ")
    else:
        php_print("         <description><![CDATA[")
        the_excerpt_rss()
        php_print("]]></description>\n          ")
        content = get_the_content_feed("rss2")
        php_print("         ")
        if php_strlen(content) > 0:
            php_print("             <content:encoded><![CDATA[")
            php_print(content)
            php_print("]]></content:encoded>\n          ")
        else:
            php_print("             <content:encoded><![CDATA[")
            the_excerpt_rss()
            php_print("]]></content:encoded>\n          ")
        # end if
        php_print("     ")
    # end if
    php_print("\n       ")
    if get_comments_number() or comments_open():
        php_print("         <wfw:commentRss>")
        php_print(esc_url(get_post_comments_feed_link(None, "rss2")))
        php_print("</wfw:commentRss>\n          <slash:comments>")
        php_print(get_comments_number())
        php_print("</slash:comments>\n      ")
    # end if
    php_print("\n       ")
    rss_enclosure()
    php_print("\n       ")
    #// 
    #// Fires at the end of each RSS2 feed item.
    #// 
    #// @since 2.0.0
    #//
    do_action("rss2_item")
    php_print(" </item>\n   ")
# end while
php_print("</channel>\n</rss>\n")
