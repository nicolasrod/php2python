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
#// Contains the post embed base template
#// 
#// When a post is embedded in an iframe, this file is used to create the output
#// if the active theme does not include an embed.php template.
#// 
#// @package WordPress
#// @subpackage oEmbed
#// @since 4.4.0
#//
get_header("embed")
if have_posts():
    while True:
        
        if not (have_posts()):
            break
        # end if
        the_post()
        get_template_part("embed", "content")
    # end while
else:
    get_template_part("embed", "404")
# end if
get_footer("embed")
