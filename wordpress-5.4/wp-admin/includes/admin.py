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
#// Core Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 2.3.0
#//
if (not php_defined("WP_ADMIN")):
    #// 
    #// This file is being included from a file other than wp-admin/admin.php, so
    #// some setup was skipped. Make sure the admin message catalog is loaded since
    #// load_default_textdomain() will not have done so in this context.
    #//
    load_textdomain("default", WP_LANG_DIR + "/admin-" + get_locale() + ".mo")
# end if
#// WordPress Administration Hooks
php_include_file(ABSPATH + "wp-admin/includes/admin-filters.php", once=True)
#// WordPress Bookmark Administration API
php_include_file(ABSPATH + "wp-admin/includes/bookmark.php", once=True)
#// WordPress Comment Administration API
php_include_file(ABSPATH + "wp-admin/includes/comment.php", once=True)
#// WordPress Administration File API
php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
#// WordPress Image Administration API
php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
#// WordPress Media Administration API
php_include_file(ABSPATH + "wp-admin/includes/media.php", once=True)
#// WordPress Import Administration API
php_include_file(ABSPATH + "wp-admin/includes/import.php", once=True)
#// WordPress Misc Administration API
php_include_file(ABSPATH + "wp-admin/includes/misc.php", once=True)
#// WordPress Misc Administration API
php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-policy-content.php", once=True)
#// WordPress Options Administration API
php_include_file(ABSPATH + "wp-admin/includes/options.php", once=True)
#// WordPress Plugin Administration API
php_include_file(ABSPATH + "wp-admin/includes/plugin.php", once=True)
#// WordPress Post Administration API
php_include_file(ABSPATH + "wp-admin/includes/post.php", once=True)
#// WordPress Administration Screen API
php_include_file(ABSPATH + "wp-admin/includes/class-wp-screen.php", once=True)
php_include_file(ABSPATH + "wp-admin/includes/screen.php", once=True)
#// WordPress Taxonomy Administration API
php_include_file(ABSPATH + "wp-admin/includes/taxonomy.php", once=True)
#// WordPress Template Administration API
php_include_file(ABSPATH + "wp-admin/includes/template.php", once=True)
#// WordPress List Table Administration API and base class
php_include_file(ABSPATH + "wp-admin/includes/class-wp-list-table.php", once=True)
php_include_file(ABSPATH + "wp-admin/includes/class-wp-list-table-compat.php", once=True)
php_include_file(ABSPATH + "wp-admin/includes/list-table.php", once=True)
#// WordPress Theme Administration API
php_include_file(ABSPATH + "wp-admin/includes/theme.php", once=True)
#// WordPress Privacy Functions
php_include_file(ABSPATH + "wp-admin/includes/privacy-tools.php", once=True)
#// WordPress Privacy List Table classes.
#// Previously in wp-admin/includes/user.php. Need to be loaded for backward compatibility.
php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-requests-table.php", once=True)
php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-data-export-requests-list-table.php", once=True)
php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-data-removal-requests-list-table.php", once=True)
#// WordPress User Administration API
php_include_file(ABSPATH + "wp-admin/includes/user.php", once=True)
#// WordPress Site Icon API
php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-icon.php", once=True)
#// WordPress Update Administration API
php_include_file(ABSPATH + "wp-admin/includes/update.php", once=True)
#// WordPress Deprecated Administration API
php_include_file(ABSPATH + "wp-admin/includes/deprecated.php", once=True)
#// WordPress Multisite support API
if is_multisite():
    php_include_file(ABSPATH + "wp-admin/includes/ms-admin-filters.php", once=True)
    php_include_file(ABSPATH + "wp-admin/includes/ms.php", once=True)
    php_include_file(ABSPATH + "wp-admin/includes/ms-deprecated.php", once=True)
# end if
