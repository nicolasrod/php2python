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
#// @package WordPress
#// @subpackage Theme_Compat
#// @deprecated 3.0.0
#// 
#// This file is here for backward compatibility with old themes and will be removed in a future version.
#//
_deprecated_file(php_sprintf(__("Theme without %s"), php_basename(__FILE__)), "3.0.0", None, php_sprintf(__("Please include a %s template in your theme."), php_basename(__FILE__)))
php_print(" <div id=\"sidebar\" role=\"complementary\">\n       <ul>\n          ")
#// Widgetized sidebar, if you have the plugin installed.
if (not php_function_exists("dynamic_sidebar")) or (not dynamic_sidebar()):
    php_print("         <li>\n              ")
    get_search_form()
    php_print("""           </li>
    <!-- Author information is disabled per default. Uncomment and fill in your details if you want to use it.
    <li><h2>""")
    _e("Author")
    php_print("""</h2>
    <p>A little something about you, the author. Nothing lengthy, just an overview.</p>
    </li>
    -->
    """)
    if is_404() or is_category() or is_day() or is_month() or is_year() or is_search() or is_paged():
        php_print("         <li>\n\n                    ")
        if is_404():
            pass
            php_print("         ")
        elif is_category():
            pass
            php_print("             <p>\n               ")
            php_printf(__("You are currently browsing the archives for the %s category."), single_cat_title("", False))
            php_print("             </p>\n\n            ")
        elif is_day():
            pass
            php_print("             <p>\n               ")
            php_printf(__("You are currently browsing the %1$s blog archives for the day %2$s."), php_sprintf("<a href=\"%1$s/\">%2$s</a>", get_bloginfo("url"), get_bloginfo("name")), get_the_time(__("l, F jS, Y")))
            php_print("             </p>\n\n            ")
        elif is_month():
            pass
            php_print("             <p>\n               ")
            php_printf(__("You are currently browsing the %1$s blog archives for %2$s."), php_sprintf("<a href=\"%1$s/\">%2$s</a>", get_bloginfo("url"), get_bloginfo("name")), get_the_time(__("F, Y")))
            php_print("             </p>\n\n            ")
        elif is_year():
            pass
            php_print("             <p>\n               ")
            php_printf(__("You are currently browsing the %1$s blog archives for the year %2$s."), php_sprintf("<a href=\"%1$s/\">%2$s</a>", get_bloginfo("url"), get_bloginfo("name")), get_the_time("Y"))
            php_print("             </p>\n\n            ")
        elif is_search():
            pass
            php_print("             <p>\n               ")
            php_printf(__("You have searched the %1$s blog archives for <strong>&#8216;%2$s&#8217;</strong>. If you are unable to find anything in these search results, you can try one of these links."), php_sprintf("<a href=\"%1$s/\">%2$s</a>", get_bloginfo("url"), get_bloginfo("name")), esc_html(get_search_query()))
            php_print("             </p>\n\n            ")
        elif (php_isset(lambda : PHP_REQUEST["paged"])) and (not php_empty(lambda : PHP_REQUEST["paged"])):
            pass
            php_print("             <p>\n               ")
            php_printf(__("You are currently browsing the %s blog archives."), php_sprintf("<a href=\"%1$s/\">%2$s</a>", get_bloginfo("url"), get_bloginfo("name")))
            php_print("             </p>\n\n            ")
        # end if
        php_print("\n           </li>\n         ")
    # end if
    php_print("     </ul>\n     <ul role=\"navigation\">\n              ")
    wp_list_pages("title_li=<h2>" + __("Pages") + "</h2>")
    php_print("\n           <li><h2>")
    _e("Archives")
    php_print("</h2>\n              <ul>\n              ")
    wp_get_archives(Array({"type": "monthly"}))
    php_print("""               </ul>
    </li>
    """)
    wp_list_categories(Array({"show_count": 1, "title_li": "<h2>" + __("Categories") + "</h2>"}))
    php_print("     </ul>\n     <ul>\n              ")
    if is_home() or is_page():
        pass
        php_print("                 ")
        wp_list_bookmarks()
        php_print("\n               <li><h2>")
        _e("Meta")
        php_print("</h2>\n              <ul>\n                  ")
        wp_register()
        php_print("                 <li>")
        wp_loginout()
        php_print("</li>\n                  ")
        wp_meta()
        php_print("             </ul>\n             </li>\n         ")
    # end if
    php_print("\n           ")
# end if
pass
php_print("     </ul>\n </div>\n")
