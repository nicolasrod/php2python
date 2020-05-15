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
#// Do not delete these lines.
if (not php_empty(lambda : PHP_SERVER["SCRIPT_FILENAME"])) and "comments.php" == php_basename(PHP_SERVER["SCRIPT_FILENAME"]):
    php_print("Please do not load this page directly. Thanks!")
    php_exit()
# end if
if post_password_required():
    php_print("     <p class=\"nocomments\">")
    _e("This post is password protected. Enter the password to view comments.")
    php_print("</p>\n   ")
    sys.exit(-1)
# end if
php_print("""
<!-- You can start editing here. -->
""")
if have_comments():
    php_print(" <h3 id=\"comments\">\n      ")
    if 1 == get_comments_number():
        printf(__("One response to %s"), "&#8220;" + get_the_title() + "&#8221;")
    else:
        printf(_n("%1$s response to %2$s", "%1$s responses to %2$s", get_comments_number()), number_format_i18n(get_comments_number()), "&#8220;" + get_the_title() + "&#8221;")
    # end if
    php_print("""   </h3>
    <div class=\"navigation\">
    <div class=\"alignleft\">""")
    previous_comments_link()
    php_print("</div>\n     <div class=\"alignright\">")
    next_comments_link()
    php_print("""</div>
    </div>
    <ol class=\"commentlist\">
    """)
    wp_list_comments()
    php_print("""   </ol>
    <div class=\"navigation\">
    <div class=\"alignleft\">""")
    previous_comments_link()
    php_print("</div>\n     <div class=\"alignright\">")
    next_comments_link()
    php_print("</div>\n </div>\n")
else:
    pass
    php_print("\n   ")
    if comments_open():
        php_print("     <!-- If comments are open, but there are no comments. -->\n\n   ")
    else:
        pass
        php_print("     <!-- If comments are closed. -->\n      <p class=\"nocomments\">")
        _e("Comments are closed.")
        php_print("</p>\n\n ")
    # end if
# end if
php_print("\n")
comment_form()
