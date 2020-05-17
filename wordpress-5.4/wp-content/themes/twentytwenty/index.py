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
#// The main template file
#// 
#// This is the most generic template file in a WordPress theme
#// and one of the two required files for a theme (the other being style.css).
#// It is used to display a page when nothing more specific matches a query.
#// E.g., it puts together the home page when no home.php file exists.
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
get_header()
php_print("""
<main id=\"site-content\" role=\"main\">
""")
archive_title_ = ""
archive_subtitle_ = ""
if is_search():
    global wp_query_
    php_check_if_defined("wp_query_")
    archive_title_ = php_sprintf("%1$s %2$s", "<span class=\"color-accent\">" + __("Search:", "twentytwenty") + "</span>", "&ldquo;" + get_search_query() + "&rdquo;")
    if wp_query_.found_posts:
        archive_subtitle_ = php_sprintf(_n("We found %s result for your search.", "We found %s results for your search.", wp_query_.found_posts, "twentytwenty"), number_format_i18n(wp_query_.found_posts))
    else:
        archive_subtitle_ = __("We could not find any results for your search. You can give it another try through the search form below.", "twentytwenty")
    # end if
elif (not is_home()):
    archive_title_ = get_the_archive_title()
    archive_subtitle_ = get_the_archive_description()
# end if
if archive_title_ or archive_subtitle_:
    php_print("""
    <header class=\"archive-header has-text-align-center header-footer-group\">
    <div class=\"archive-header-inner section-inner medium\">
    """)
    if archive_title_:
        php_print("                 <h1 class=\"archive-title\">")
        php_print(wp_kses_post(archive_title_))
        php_print("</h1>\n              ")
    # end if
    php_print("\n               ")
    if archive_subtitle_:
        php_print("                 <div class=\"archive-subtitle section-inner thin max-percentage intro-text\">")
        php_print(wp_kses_post(wpautop(archive_subtitle_)))
        php_print("</div>\n             ")
    # end if
    php_print("""
    </div><!-- .archive-header-inner -->
    </header><!-- .archive-header -->
    """)
# end if
if have_posts():
    i_ = 0
    while True:
        
        if not (have_posts()):
            break
        # end if
        i_ += 1
        if i_ > 1:
            php_print("<hr class=\"post-separator styled-separator is-style-wide section-inner\" aria-hidden=\"true\" />")
        # end if
        the_post()
        get_template_part("template-parts/content", get_post_type())
    # end while
elif is_search():
    php_print("""
    <div class=\"no-search-results-form section-inner thin\">
    """)
    get_search_form(Array({"label": __("search again", "twentytwenty")}))
    php_print("""
    </div><!-- .no-search-results -->
    """)
# end if
php_print("\n   ")
get_template_part("template-parts/pagination")
php_print("""
</main><!-- #site-content -->
""")
get_template_part("template-parts/footer-menus-widgets")
php_print("\n")
get_footer()
