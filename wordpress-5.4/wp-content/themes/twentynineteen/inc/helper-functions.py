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
#// Common theme functions
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.5
#// 
#// 
#// Determines if post thumbnail can be displayed.
#//
def twentynineteen_can_show_post_thumbnail(*_args_):
    
    
    return apply_filters("twentynineteen_can_show_post_thumbnail", (not post_password_required()) and (not is_attachment()) and has_post_thumbnail())
# end def twentynineteen_can_show_post_thumbnail
#// 
#// Returns true if image filters are enabled on the theme options.
#//
def twentynineteen_image_filters_enabled(*_args_):
    
    
    return 0 != get_theme_mod("image_filter", 1)
# end def twentynineteen_image_filters_enabled
#// 
#// Returns the size for avatars used in the theme.
#//
def twentynineteen_get_avatar_size(*_args_):
    
    
    return 60
# end def twentynineteen_get_avatar_size
#// 
#// Returns true if comment is by author of the post.
#// 
#// @see get_comment_class()
#//
def twentynineteen_is_comment_by_post_author(comment_=None, *_args_):
    if comment_ is None:
        comment_ = None
    # end if
    
    if php_is_object(comment_) and comment_.user_id > 0:
        user_ = get_userdata(comment_.user_id)
        post_ = get_post(comment_.comment_post_ID)
        if (not php_empty(lambda : user_)) and (not php_empty(lambda : post_)):
            return comment_.user_id == post_.post_author
        # end if
    # end if
    return False
# end def twentynineteen_is_comment_by_post_author
#// 
#// Returns information about the current post's discussion, with cache support.
#//
def twentynineteen_get_discussion_data(*_args_):
    
    
    discussion_ = None
    post_id_ = None
    current_post_id_ = get_the_ID()
    if current_post_id_ == post_id_:
        return discussion_
        pass
    else:
        post_id_ = current_post_id_
    # end if
    comments_ = get_comments(Array({"post_id": current_post_id_, "orderby": "comment_date_gmt", "order": get_option("comment_order", "asc"), "status": "approve", "number": 20}))
    authors_ = Array()
    for comment_ in comments_:
        authors_[-1] = php_int(comment_.user_id) if php_int(comment_.user_id) > 0 else comment_.comment_author_email
    # end for
    authors_ = array_unique(authors_)
    discussion_ = Array({"authors": php_array_slice(authors_, 0, 6), "responses": get_comments_number(current_post_id_)})
    return discussion_
# end def twentynineteen_get_discussion_data
#// 
#// Converts HSL to HEX colors.
#//
def twentynineteen_hsl_hex(h_=None, s_=None, l_=None, to_hex_=None, *_args_):
    if to_hex_ is None:
        to_hex_ = True
    # end if
    
    h_ /= 360
    s_ /= 100
    l_ /= 100
    r_ = l_
    g_ = l_
    b_ = l_
    v_ = l_ * 1 + s_ if l_ <= 0.5 else l_ + s_ - l_ * s_
    if v_ > 0:
        m_
        sv_
        sextant_
        fract_
        vsf_
        mid1_
        mid2_
        m_ = l_ + l_ - v_
        sv_ = v_ - m_ / v_
        h_ *= 6
        sextant_ = floor(h_)
        fract_ = h_ - sextant_
        vsf_ = v_ * sv_ * fract_
        mid1_ = m_ + vsf_
        mid2_ = v_ - vsf_
        for case in Switch(sextant_):
            if case(0):
                r_ = v_
                g_ = mid1_
                b_ = m_
                break
            # end if
            if case(1):
                r_ = mid2_
                g_ = v_
                b_ = m_
                break
            # end if
            if case(2):
                r_ = m_
                g_ = v_
                b_ = mid1_
                break
            # end if
            if case(3):
                r_ = m_
                g_ = mid2_
                b_ = v_
                break
            # end if
            if case(4):
                r_ = mid1_
                g_ = m_
                b_ = v_
                break
            # end if
            if case(5):
                r_ = v_
                g_ = m_
                b_ = mid2_
                break
            # end if
        # end for
    # end if
    r_ = round(r_ * 255, 0)
    g_ = round(g_ * 255, 0)
    b_ = round(b_ * 255, 0)
    if to_hex_:
        r_ = "0" + dechex(r_) if r_ < 15 else dechex(r_)
        g_ = "0" + dechex(g_) if g_ < 15 else dechex(g_)
        b_ = "0" + dechex(b_) if b_ < 15 else dechex(b_)
        return str("#") + str(r_) + str(g_) + str(b_)
    # end if
    return str("rgb(") + str(r_) + str(", ") + str(g_) + str(", ") + str(b_) + str(")")
# end def twentynineteen_hsl_hex
