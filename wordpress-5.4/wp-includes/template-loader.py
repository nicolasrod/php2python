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
#// Loads the correct template based on the visitor's url
#// 
#// @package WordPress
#//
if wp_using_themes():
    #// 
    #// Fires before determining which template to load.
    #// 
    #// @since 1.5.0
    #//
    do_action("template_redirect")
# end if
#// 
#// Filters whether to allow 'HEAD' requests to generate content.
#// 
#// Provides a significant performance bump by exiting before the page
#// content loads for 'HEAD' requests. See #14348.
#// 
#// @since 3.5.0
#// 
#// @param bool $exit Whether to exit without generating any content for 'HEAD' requests. Default true.
#//
if "HEAD" == PHP_SERVER["REQUEST_METHOD"] and apply_filters("exit_on_http_head", True):
    php_exit(0)
# end if
#// Process feeds and trackbacks even if not using themes.
if is_robots():
    #// 
    #// Fired when the template loader determines a robots.txt request.
    #// 
    #// @since 2.1.0
    #//
    do_action("do_robots")
    sys.exit(-1)
elif is_favicon():
    #// 
    #// Fired when the template loader determines a favicon.ico request.
    #// 
    #// @since 5.4.0
    #//
    do_action("do_favicon")
    sys.exit(-1)
elif is_feed():
    do_feed()
    sys.exit(-1)
elif is_trackback():
    php_include_file(ABSPATH + "wp-trackback.php", once=False)
    sys.exit(-1)
# end if
if wp_using_themes():
    tag_templates_ = Array({"is_embed": "get_embed_template", "is_404": "get_404_template", "is_search": "get_search_template", "is_front_page": "get_front_page_template", "is_home": "get_home_template", "is_privacy_policy": "get_privacy_policy_template", "is_post_type_archive": "get_post_type_archive_template", "is_tax": "get_taxonomy_template", "is_attachment": "get_attachment_template", "is_single": "get_single_template", "is_page": "get_page_template", "is_singular": "get_singular_template", "is_category": "get_category_template", "is_tag": "get_tag_template", "is_author": "get_author_template", "is_date": "get_date_template", "is_archive": "get_archive_template"})
    template_ = False
    #// Loop through each of the template conditionals, and find the appropriate template file.
    for tag_,template_getter_ in tag_templates_:
        if php_call_user_func(tag_):
            template_ = php_call_user_func(template_getter_)
        # end if
        if template_:
            if "is_attachment" == tag_:
                remove_filter("the_content", "prepend_attachment")
            # end if
            break
        # end if
    # end for
    if (not template_):
        template_ = get_index_template()
    # end if
    #// 
    #// Filters the path of the current template before including it.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $template The path of the template to include.
    #//
    template_ = apply_filters("template_include", template_)
    if template_:
        php_include_file(template_, once=False)
    elif current_user_can("switch_themes"):
        theme_ = wp_get_theme()
        if theme_.errors():
            wp_die(theme_.errors())
        # end if
    # end if
    sys.exit(-1)
# end if
