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
#// Back-compat placeholder for the base embed template
#// 
#// @package WordPress
#// @subpackage oEmbed
#// @since 4.4.0
#// @deprecated 4.5.0 Moved to wp-includes/theme-compat/embed.php
#//
_deprecated_file(php_basename(__FILE__), "4.5.0", "wp-includes/theme-compat/embed.php")
php_include_file(ABSPATH + WPINC + "/theme-compat/embed.php", once=False)
