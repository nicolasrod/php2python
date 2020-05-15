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
#// @package WordPress
#// @subpackage Theme_Compat
#// @deprecated 3.0.0
#// 
#// This file is here for backward compatibility with old themes and will be removed in a future version
#//
_deprecated_file(php_sprintf(__("Theme without %s"), php_basename(__FILE__)), "3.0.0", None, php_sprintf(__("Please include a %s template in your theme."), php_basename(__FILE__)))
php_print("""
<hr />
<div id=\"footer\" role=\"contentinfo\">
<!-- If you'd like to support WordPress, having the \"powered by\" link somewhere on your blog is the best way; it's our only promotion or advertising. -->
<p>
""")
printf(__("%1$s is proudly powered by %2$s"), get_bloginfo("name"), "<a href=\"https://wordpress.org/\">WordPress</a>")
php_print("""   </p>
</div>
</div>
<!-- Gorgeous design by Michael Heilemann - http://binarybonsai.com/kubrick/ -->
""")
pass
php_print("\n       ")
wp_footer()
php_print("</body>\n</html>\n")
