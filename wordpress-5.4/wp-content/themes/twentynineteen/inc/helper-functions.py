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
#// Common theme functions
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.5
#// 
#// 
#// Determines if post thumbnail can be displayed.
#//
def twentynineteen_can_show_post_thumbnail(*args_):
    
    return apply_filters("twentynineteen_can_show_post_thumbnail", (not post_password_required()) and (not is_attachment()) and has_post_thumbnail())
# end def twentynineteen_can_show_post_thumbnail
#// 
#// Returns true if image filters are enabled on the theme options.
#//
def twentynineteen_image_filters_enabled(*args_):
    
    return 0 != get_theme_mod("image_filter", 1)
# end def twentynineteen_image_filters_enabled
#// 
#// Returns the size for avatars used in the theme.
#//
def twentynineteen_get_avatar_size(*args_):
    
    return 60
# end def twentynineteen_get_avatar_size
#// 
#// Returns true if comment is by author of the post.
#// 
#// @see get_comment_class()
#//
def twentynineteen_is_comment_by_post_author(comment=None, *args_):
    
    if php_is_object(comment) and comment.user_id > 0:
        user = get_userdata(comment.user_id)
        post = get_post(comment.comment_post_ID)
        if (not php_empty(lambda : user)) and (not php_empty(lambda : post)):
            return comment.user_id == post.post_author
        # end if
    # end if
    return False
# end def twentynineteen_is_comment_by_post_author
#// 
#// Returns information about the current post's discussion, with cache support.
#//
def twentynineteen_get_discussion_data(*args_):
    
    discussion = None
    post_id = None
    current_post_id = get_the_ID()
    if current_post_id == post_id:
        return discussion
        pass
    else:
        post_id = current_post_id
    # end if
    comments = get_comments(Array({"post_id": current_post_id, "orderby": "comment_date_gmt", "order": get_option("comment_order", "asc"), "status": "approve", "number": 20}))
    authors = Array()
    for comment in comments:
        authors[-1] = int(comment.user_id) if int(comment.user_id) > 0 else comment.comment_author_email
    # end for
    authors = array_unique(authors)
    discussion = Array({"authors": php_array_slice(authors, 0, 6), "responses": get_comments_number(current_post_id)})
    return discussion
# end def twentynineteen_get_discussion_data
#// 
#// Converts HSL to HEX colors.
#//
def twentynineteen_hsl_hex(h=None, s=None, l=None, to_hex=True, *args_):
    
    h /= 360
    s /= 100
    l /= 100
    r = l
    g = l
    b = l
    v = l * 1 + s if l <= 0.5 else l + s - l * s
    if v > 0:
        m
        sv
        sextant
        fract
        vsf
        mid1
        mid2
        m = l + l - v
        sv = v - m / v
        h *= 6
        sextant = floor(h)
        fract = h - sextant
        vsf = v * sv * fract
        mid1 = m + vsf
        mid2 = v - vsf
        for case in Switch(sextant):
            if case(0):
                r = v
                g = mid1
                b = m
                break
            # end if
            if case(1):
                r = mid2
                g = v
                b = m
                break
            # end if
            if case(2):
                r = m
                g = v
                b = mid1
                break
            # end if
            if case(3):
                r = m
                g = mid2
                b = v
                break
            # end if
            if case(4):
                r = mid1
                g = m
                b = v
                break
            # end if
            if case(5):
                r = v
                g = m
                b = mid2
                break
            # end if
        # end for
    # end if
    r = round(r * 255, 0)
    g = round(g * 255, 0)
    b = round(b * 255, 0)
    if to_hex:
        r = "0" + dechex(r) if r < 15 else dechex(r)
        g = "0" + dechex(g) if g < 15 else dechex(g)
        b = "0" + dechex(b) if b < 15 else dechex(b)
        return str("#") + str(r) + str(g) + str(b)
    # end if
    return str("rgb(") + str(r) + str(", ") + str(g) + str(", ") + str(b) + str(")")
# end def twentynineteen_hsl_hex
