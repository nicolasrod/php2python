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
#// API for fetching the HTML to embed remote content based on a provided URL.
#// 
#// This file is deprecated, use 'wp-includes/class-wp-oembed.php' instead.
#// 
#// @deprecated 5.3.0
#// @package WordPress
#// @subpackage oEmbed
#//
_deprecated_file(php_basename(__FILE__), "5.3.0", "wp-includes/class-wp-oembed.php")
#// WP_oEmbed class
php_include_file(ABSPATH + "wp-includes/class-wp-oembed.php", once=True)
