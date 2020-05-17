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
#// Contains the post embed footer template
#// 
#// When a post is embedded in an iframe, this file is used to create the footer output
#// if the active theme does not include a footer-embed.php template.
#// 
#// @package WordPress
#// @subpackage Theme_Compat
#// @since 4.5.0
#// 
#// 
#// Prints scripts or data before the closing body tag in the embed template.
#// 
#// @since 4.4.0
#//
do_action("embed_footer")
php_print("</body>\n</html>\n")
