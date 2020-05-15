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
#// Feed API
#// 
#// @package WordPress
#// @subpackage Feed
#// @deprecated 4.7.0
#//
_deprecated_file(php_basename(__FILE__), "4.7.0", "fetch_feed()")
if (not php_class_exists("SimplePie", False)):
    php_include_file(ABSPATH + WPINC + "/class-simplepie.php", once=True)
# end if
php_include_file(ABSPATH + WPINC + "/class-wp-feed-cache.php", once=True)
php_include_file(ABSPATH + WPINC + "/class-wp-feed-cache-transient.php", once=True)
php_include_file(ABSPATH + WPINC + "/class-wp-simplepie-file.php", once=True)
php_include_file(ABSPATH + WPINC + "/class-wp-simplepie-sanitize-kses.php", once=True)
