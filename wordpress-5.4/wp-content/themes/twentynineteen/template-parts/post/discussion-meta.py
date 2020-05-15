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
#// The template for displaying Current Discussion on posts
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#// 
#// Get data from current discussion on post.
discussion = twentynineteen_get_discussion_data()
has_responses = discussion.responses > 0
if has_responses:
    #// translators: %d: Number of comments.
    meta_label = php_sprintf(_n("%d Comment", "%d Comments", discussion.responses, "twentynineteen"), discussion.responses)
else:
    meta_label = __("No comments", "twentynineteen")
# end if
php_print("\n<div class=\"discussion-meta\">\n  ")
if has_responses:
    twentynineteen_discussion_avatars_list(discussion.authors)
# end if
php_print(" <p class=\"discussion-meta-info\">\n        ")
php_print(twentynineteen_get_icon_svg("comment", 24))
php_print("     <span>")
php_print(esc_html(meta_label))
php_print("""</span>
</p>
</div><!-- .discussion-meta -->
""")
