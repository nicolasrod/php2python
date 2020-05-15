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
#// RSS 1 RDF Feed Template for displaying RSS 1 Posts feed.
#// 
#// @package WordPress
#//
php_header("Content-Type: " + feed_content_type("rdf") + "; charset=" + get_option("blog_charset"), True)
more = 1
php_print("<?xml version=\"1.0\" encoding=\"" + get_option("blog_charset") + "\"?" + ">")
#// This action is documented in wp-includes/feed-rss2.php
do_action("rss_tag_pre", "rdf")
php_print("""<rdf:RDF
xmlns=\"http://purl.org/rss/1.0/\"
xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"
xmlns:dc=\"http://purl.org/dc/elements/1.1/\"
xmlns:sy=\"http://purl.org/rss/1.0/modules/syndication/\"
xmlns:admin=\"http://webns.net/mvcb/\"
xmlns:content=\"http://purl.org/rss/1.0/modules/content/\"
""")
#// 
#// Fires at the end of the feed root to add namespaces.
#// 
#// @since 2.0.0
#//
do_action("rdf_ns")
php_print(">\n<channel rdf:about=\"")
bloginfo_rss("url")
php_print("\">\n    <title>")
wp_title_rss()
php_print("</title>\n   <link>")
bloginfo_rss("url")
php_print("</link>\n    <description>")
bloginfo_rss("description")
php_print("</description>\n <dc:date>")
php_print(get_feed_build_date("Y-m-d\\TH:i:s\\Z"))
php_print(" </dc:date>\n    <sy:updatePeriod>\n ")
#// This filter is documented in wp-includes/feed-rss2.php
php_print(apply_filters("rss_update_period", "hourly"))
php_print(" </sy:updatePeriod>\n    <sy:updateFrequency>\n  ")
#// This filter is documented in wp-includes/feed-rss2.php
php_print(apply_filters("rss_update_frequency", "1"))
php_print(" </sy:updateFrequency>\n <sy:updateBase>2000-01-01T12:00+00:00</sy:updateBase>\n ")
#// 
#// Fires at the end of the RDF feed header.
#// 
#// @since 2.0.0
#//
do_action("rdf_header")
php_print(" <items>\n       <rdf:Seq>\n     ")
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    php_print("         <rdf:li rdf:resource=\"")
    the_permalink_rss()
    php_print("\"/>\n       ")
# end while
php_print("""       </rdf:Seq>
</items>
</channel>
""")
rewind_posts()
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    php_print("<item rdf:about=\"")
    the_permalink_rss()
    php_print("\">\n    <title>")
    the_title_rss()
    php_print("</title>\n   <link>")
    the_permalink_rss()
    php_print("</link>\n\n  <dc:creator><![CDATA[")
    the_author()
    php_print("]]></dc:creator>\n   <dc:date>")
    php_print(mysql2date("Y-m-d\\TH:i:s\\Z", post.post_date_gmt, False))
    php_print("</dc:date>\n ")
    the_category_rss("rdf")
    php_print("\n   ")
    if get_option("rss_use_excerpt"):
        php_print("     <description><![CDATA[")
        the_excerpt_rss()
        php_print("]]></description>\n  ")
    else:
        php_print("     <description><![CDATA[")
        the_excerpt_rss()
        php_print("]]></description>\n      <content:encoded><![CDATA[")
        the_content_feed("rdf")
        php_print("]]></content:encoded>\n  ")
    # end if
    php_print("\n   ")
    #// 
    #// Fires at the end of each RDF feed item.
    #// 
    #// @since 2.0.0
    #//
    do_action("rdf_item")
    php_print("</item>\n")
# end while
php_print("</rdf:RDF>\n")
