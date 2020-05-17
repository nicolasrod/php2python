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
#// RSS 0.92 Feed Template for displaying RSS 0.92 Posts feed.
#// 
#// @package WordPress
#//
php_header("Content-Type: " + feed_content_type("rss") + "; charset=" + get_option("blog_charset"), True)
more_ = 1
php_print("<?xml version=\"1.0\" encoding=\"" + get_option("blog_charset") + "\"?" + ">")
php_print("<rss version=\"0.92\">\n<channel>\n  <title>")
wp_title_rss()
php_print("</title>\n   <link>")
bloginfo_rss("url")
php_print("</link>\n    <description>")
bloginfo_rss("description")
php_print("</description>\n <lastBuildDate>")
php_print(get_feed_build_date("D, d M Y H:i:s +0000"))
php_print("</lastBuildDate>\n   <docs>http://backend.userland.com/rss092</docs>\n   <language>")
bloginfo_rss("language")
php_print("</language>\n    ")
#// 
#// Fires at the end of the RSS Feed Header.
#// 
#// @since 2.0.0
#//
do_action("rss_head")
php_print("\n")
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    php_print(" <item>\n        <title>")
    the_title_rss()
    php_print("</title>\n       <description><![CDATA[")
    the_excerpt_rss()
    php_print("]]></description>\n      <link>")
    the_permalink_rss()
    php_print("</link>\n        ")
    #// 
    #// Fires at the end of each RSS feed item.
    #// 
    #// @since 2.0.0
    #//
    do_action("rss_item")
    php_print(" </item>\n")
# end while
php_print("</channel>\n</rss>\n")
