#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
pass
php_print("\n<article ")
post_class()
php_print(" id=\"post-")
the_ID()
php_print("\">\n\n  ")
get_template_part("template-parts/entry-header")
if (not is_search()):
    get_template_part("template-parts/featured-image")
# end if
php_print("\n   <div class=\"post-inner ")
php_print("" if is_page_template("templates/template-full-width.php") else "thin")
php_print(""" \">
<div class=\"entry-content\">
""")
if is_search() or (not is_singular()) and "summary" == get_theme_mod("blog_content", "full"):
    the_excerpt()
else:
    the_content(__("Continue reading", "twentytwenty"))
# end if
php_print("""
</div><!-- .entry-content -->
</div><!-- .post-inner -->
<div class=\"section-inner\">
""")
wp_link_pages(Array({"before": "<nav class=\"post-nav-links bg-light-background\" aria-label=\"" + esc_attr__("Page", "twentytwenty") + "\"><span class=\"label\">" + __("Pages:", "twentytwenty") + "</span>", "after": "</nav>", "link_before": "<span class=\"page-number\">", "link_after": "</span>"}))
edit_post_link()
#// Single bottom post meta.
twentytwenty_the_post_meta(get_the_ID(), "single-bottom")
if is_single():
    get_template_part("template-parts/entry-author-bio")
# end if
php_print("""
</div><!-- .section-inner -->
""")
if is_single():
    get_template_part("template-parts/navigation")
# end if
#// 
#// Output comments wrapper if it's a post, or if comments are open,
#// or if there's a comment number – and check for password.
#//
if is_single() or is_page() and comments_open() or get_comments_number() and (not post_password_required()):
    php_print("""
    <div class=\"comments-wrapper section-inner\">
    """)
    comments_template()
    php_print("""
    </div><!-- .comments-wrapper -->
    """)
# end if
php_print("\n</article><!-- .post -->\n")
