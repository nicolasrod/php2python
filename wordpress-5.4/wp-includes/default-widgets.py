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
#// Widget API: Default core widgets
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 2.8.0
#// 
#// WP_Widget_Pages class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-pages.php", once=True)
#// WP_Widget_Links class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-links.php", once=True)
#// WP_Widget_Search class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-search.php", once=True)
#// WP_Widget_Archives class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-archives.php", once=True)
#// WP_Widget_Media class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-media.php", once=True)
#// WP_Widget_Media_Audio class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-media-audio.php", once=True)
#// WP_Widget_Media_Image class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-media-image.php", once=True)
#// WP_Widget_Media_Video class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-media-video.php", once=True)
#// WP_Widget_Media_Gallery class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-media-gallery.php", once=True)
#// WP_Widget_Meta class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-meta.php", once=True)
#// WP_Widget_Calendar class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-calendar.php", once=True)
#// WP_Widget_Text class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-text.php", once=True)
#// WP_Widget_Categories class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-categories.php", once=True)
#// WP_Widget_Recent_Posts class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-recent-posts.php", once=True)
#// WP_Widget_Recent_Comments class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-recent-comments.php", once=True)
#// WP_Widget_RSS class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-rss.php", once=True)
#// WP_Widget_Tag_Cloud class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-tag-cloud.php", once=True)
#// WP_Nav_Menu_Widget class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-nav-menu-widget.php", once=True)
#// WP_Widget_Custom_HTML class
php_include_file(ABSPATH + WPINC + "/widgets/class-wp-widget-custom-html.php", once=True)
