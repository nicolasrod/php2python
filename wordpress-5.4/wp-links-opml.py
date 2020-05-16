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
#// Outputs the OPML XML format for getting the links defined in the link
#// administration. This can be used to export links from one blog over to
#// another. Links aren't exported by the WordPress export, so this file handles
#// that.
#// 
#// This file is not added by default to WordPress theme pages when outputting
#// feed links. It will have to be added manually for browsers and users to pick
#// up that this file exists.
#// 
#// @package WordPress
#//
php_include_file(__DIR__ + "/wp-load.php", once=True)
php_header("Content-Type: text/xml; charset=" + get_option("blog_charset"), True)
link_cat = ""
if (not php_empty(lambda : PHP_REQUEST["link_cat"])):
    link_cat = PHP_REQUEST["link_cat"]
    if (not php_in_array(link_cat, Array("all", "0"), True)):
        link_cat = absint(php_str(urldecode(link_cat)))
    # end if
# end if
php_print("<?xml version=\"1.0\"?" + ">\n")
php_print("""<opml version=\"1.0\">
<head>
<title>
""")
#// translators: %s: Site title.
printf(__("Links for %s"), esc_attr(get_bloginfo("name", "display")))
php_print("     </title>\n      <dateCreated>")
php_print(gmdate("D, d M Y H:i:s"))
php_print(" GMT</dateCreated>\n     ")
#// 
#// Fires in the OPML header.
#// 
#// @since 3.0.0
#//
do_action("opml_head")
php_print(" </head>\n   <body>\n")
if php_empty(lambda : link_cat):
    cats = get_categories(Array({"taxonomy": "link_category", "hierarchical": 0}))
else:
    cats = get_categories(Array({"taxonomy": "link_category", "hierarchical": 0, "include": link_cat}))
# end if
for cat in cats:
    #// This filter is documented in wp-includes/bookmark-template.php
    catname = apply_filters("link_category", cat.name)
    php_print("<outline type=\"category\" title=\"")
    php_print(esc_attr(catname))
    php_print("\">\n    ")
    bookmarks = get_bookmarks(Array({"category": cat.term_id}))
    for bookmark in bookmarks:
        #// 
        #// Filters the OPML outline link title text.
        #// 
        #// @since 2.2.0
        #// 
        #// @param string $title The OPML outline title text.
        #//
        title = apply_filters("link_title", bookmark.link_name)
        php_print("<outline text=\"")
        php_print(esc_attr(title))
        php_print("\" type=\"link\" xmlUrl=\"")
        php_print(esc_attr(bookmark.link_rss))
        php_print("\" htmlUrl=\"")
        php_print(esc_attr(bookmark.link_url))
        php_print("\" updated=\"\n                          ")
        if "0000-00-00 00:00:00" != bookmark.link_updated:
            php_print(bookmark.link_updated)
        # end if
        php_print("\" />\n      ")
    # end for
    pass
    php_print("</outline>\n ")
# end for
pass
php_print("</body>\n</opml>\n")
