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
#// Atom Feed Template for displaying Atom Posts feed.
#// 
#// @package WordPress
#//
php_header("Content-Type: " + feed_content_type("atom") + "; charset=" + get_option("blog_charset"), True)
more_ = 1
php_print("<?xml version=\"1.0\" encoding=\"" + get_option("blog_charset") + "\"?" + ">")
#// This action is documented in wp-includes/feed-rss2.php
do_action("rss_tag_pre", "atom")
php_print("""<feed
xmlns=\"http://www.w3.org/2005/Atom\"
xmlns:thr=\"http://purl.org/syndication/thread/1.0\"
xml:lang=\"""")
bloginfo_rss("language")
php_print("\"\n xml:base=\"")
bloginfo_rss("url")
php_print("/wp-atom.php\"\n ")
#// 
#// Fires at end of the Atom feed root to add namespaces.
#// 
#// @since 2.0.0
#//
do_action("atom_ns")
php_print(">\n  <title type=\"text\">")
wp_title_rss()
php_print("</title>\n   <subtitle type=\"text\">")
bloginfo_rss("description")
php_print("</subtitle>\n\n  <updated>")
php_print(get_feed_build_date("Y-m-d\\TH:i:s\\Z"))
php_print("</updated>\n\n   <link rel=\"alternate\" type=\"")
bloginfo_rss("html_type")
php_print("\" href=\"")
bloginfo_rss("url")
php_print("\" />\n  <id>")
bloginfo("atom_url")
php_print("</id>\n  <link rel=\"self\" type=\"application/atom+xml\" href=\"")
self_link()
php_print("\" />\n\n    ")
#// 
#// Fires just before the first Atom feed entry.
#// 
#// @since 2.0.0
#//
do_action("atom_head")
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    php_print(" <entry>\n       <author>\n          <name>")
    the_author()
    php_print("</name>\n            ")
    author_url_ = get_the_author_meta("url")
    if (not php_empty(lambda : author_url_)):
        php_print("             <uri>")
        the_author_meta("url")
        php_print("</uri>\n             ")
    # end if
    #// 
    #// Fires at the end of each Atom feed author entry.
    #// 
    #// @since 3.2.0
    #//
    do_action("atom_author")
    php_print("     </author>\n\n       <title type=\"")
    html_type_rss()
    php_print("\"><![CDATA[")
    the_title_rss()
    php_print("]]></title>\n        <link rel=\"alternate\" type=\"")
    bloginfo_rss("html_type")
    php_print("\" href=\"")
    the_permalink_rss()
    php_print("\" />\n\n        <id>")
    the_guid()
    php_print("</id>\n      <updated>")
    php_print(get_post_modified_time("Y-m-d\\TH:i:s\\Z", True))
    php_print("</updated>\n     <published>")
    php_print(get_post_time("Y-m-d\\TH:i:s\\Z", True))
    php_print("</published>\n       ")
    the_category_rss("atom")
    php_print("\n       <summary type=\"")
    html_type_rss()
    php_print("\"><![CDATA[")
    the_excerpt_rss()
    php_print("]]></summary>\n\n        ")
    if (not get_option("rss_use_excerpt")):
        php_print("         <content type=\"")
        html_type_rss()
        php_print("\" xml:base=\"")
        the_permalink_rss()
        php_print("\"><![CDATA[")
        the_content_feed("atom")
        php_print("]]></content>\n      ")
    # end if
    php_print("\n       ")
    atom_enclosure()
    #// 
    #// Fires at the end of each Atom feed item.
    #// 
    #// @since 2.0.0
    #//
    do_action("atom_entry")
    if get_comments_number() or comments_open():
        php_print("         <link rel=\"replies\" type=\"")
        bloginfo_rss("html_type")
        php_print("\" href=\"")
        the_permalink_rss()
        php_print("#comments\" thr:count=\"")
        php_print(get_comments_number())
        php_print("\"/>\n           <link rel=\"replies\" type=\"application/atom+xml\" href=\"")
        php_print(esc_url(get_post_comments_feed_link(0, "atom")))
        php_print("\" thr:count=\"")
        php_print(get_comments_number())
        php_print("\"/>\n           <thr:total>")
        php_print(get_comments_number())
        php_print("</thr:total>\n       ")
    # end if
    php_print(" </entry>\n  ")
# end while
php_print("</feed>\n")
