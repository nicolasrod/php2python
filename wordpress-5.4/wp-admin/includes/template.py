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
#// Template WordPress Administration API.
#// 
#// A Big Mess. Also some neat functions that are nicely written.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Walker_Category_Checklist class
php_include_file(ABSPATH + "wp-admin/includes/class-walker-category-checklist.php", once=True)
#// WP_Internal_Pointers class
php_include_file(ABSPATH + "wp-admin/includes/class-wp-internal-pointers.php", once=True)
#// 
#// Category Checklists.
#// 
#// 
#// Output an unordered list of checkbox input elements labeled with category names.
#// 
#// @since 2.5.1
#// 
#// @see wp_terms_checklist()
#// 
#// @param int    $post_id              Optional. Post to generate a categories checklist for. Default 0.
#// $selected_cats must not be an array. Default 0.
#// @param int    $descendants_and_self Optional. ID of the category to output along with its descendants.
#// Default 0.
#// @param int[]  $selected_cats        Optional. Array of category IDs to mark as checked. Default false.
#// @param int[]  $popular_cats         Optional. Array of category IDs to receive the "popular-category" class.
#// Default false.
#// @param Walker $walker               Optional. Walker object to use to build the output.
#// Default is a Walker_Category_Checklist instance.
#// @param bool   $checked_ontop        Optional. Whether to move checked items out of the hierarchy and to
#// the top of the list. Default true.
#//
def wp_category_checklist(post_id_=0, descendants_and_self_=0, selected_cats_=None, popular_cats_=None, walker_=None, checked_ontop_=None, *_args_):
    if selected_cats_ is None:
        selected_cats_ = False
    # end if
    if popular_cats_ is None:
        popular_cats_ = False
    # end if
    if walker_ is None:
        walker_ = None
    # end if
    if checked_ontop_ is None:
        checked_ontop_ = True
    # end if
    
    wp_terms_checklist(post_id_, Array({"taxonomy": "category", "descendants_and_self": descendants_and_self_, "selected_cats": selected_cats_, "popular_cats": popular_cats_, "walker": walker_, "checked_ontop": checked_ontop_}))
# end def wp_category_checklist
#// 
#// Output an unordered list of checkbox input elements labelled with term names.
#// 
#// Taxonomy-independent version of wp_category_checklist().
#// 
#// @since 3.0.0
#// @since 4.4.0 Introduced the `$echo` argument.
#// 
#// @param int          $post_id Optional. Post ID. Default 0.
#// @param array|string $args {
#// Optional. Array or string of arguments for generating a terms checklist. Default empty array.
#// 
#// @type int    $descendants_and_self ID of the category to output along with its descendants.
#// Default 0.
#// @type int[]  $selected_cats        Array of category IDs to mark as checked. Default false.
#// @type int[]  $popular_cats         Array of category IDs to receive the "popular-category" class.
#// Default false.
#// @type Walker $walker               Walker object to use to build the output.
#// Default is a Walker_Category_Checklist instance.
#// @type string $taxonomy             Taxonomy to generate the checklist for. Default 'category'.
#// @type bool   $checked_ontop        Whether to move checked items out of the hierarchy and to
#// the top of the list. Default true.
#// @type bool   $echo                 Whether to echo the generated markup. False to return the markup instead
#// of echoing it. Default true.
#// }
#// @return string HTML list of input elements.
#//
def wp_terms_checklist(post_id_=0, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"descendants_and_self": 0, "selected_cats": False, "popular_cats": False, "walker": None, "taxonomy": "category", "checked_ontop": True, "echo": True})
    #// 
    #// Filters the taxonomy terms checklist arguments.
    #// 
    #// @since 3.4.0
    #// 
    #// @see wp_terms_checklist()
    #// 
    #// @param array $args    An array of arguments.
    #// @param int   $post_id The post ID.
    #//
    params_ = apply_filters("wp_terms_checklist_args", args_, post_id_)
    parsed_args_ = wp_parse_args(params_, defaults_)
    if php_empty(lambda : parsed_args_["walker"]) or (not type(parsed_args_["walker"]).__name__ == "Walker"):
        walker_ = php_new_class("Walker_Category_Checklist", lambda : Walker_Category_Checklist())
    else:
        walker_ = parsed_args_["walker"]
    # end if
    taxonomy_ = parsed_args_["taxonomy"]
    descendants_and_self_ = php_int(parsed_args_["descendants_and_self"])
    args_ = Array({"taxonomy": taxonomy_})
    tax_ = get_taxonomy(taxonomy_)
    args_["disabled"] = (not current_user_can(tax_.cap.assign_terms))
    args_["list_only"] = (not php_empty(lambda : parsed_args_["list_only"]))
    if php_is_array(parsed_args_["selected_cats"]):
        args_["selected_cats"] = parsed_args_["selected_cats"]
    elif post_id_:
        args_["selected_cats"] = wp_get_object_terms(post_id_, taxonomy_, php_array_merge(args_, Array({"fields": "ids"})))
    else:
        args_["selected_cats"] = Array()
    # end if
    if php_is_array(parsed_args_["popular_cats"]):
        args_["popular_cats"] = parsed_args_["popular_cats"]
    else:
        args_["popular_cats"] = get_terms(Array({"taxonomy": taxonomy_, "fields": "ids", "orderby": "count", "order": "DESC", "number": 10, "hierarchical": False}))
    # end if
    if descendants_and_self_:
        categories_ = get_terms(Array({"taxonomy": taxonomy_, "child_of": descendants_and_self_, "hierarchical": 0, "hide_empty": 0}))
        self_ = get_term(descendants_and_self_, taxonomy_)
        array_unshift(categories_, self_)
    else:
        categories_ = get_terms(Array({"taxonomy": taxonomy_, "get": "all"}))
    # end if
    output_ = ""
    if parsed_args_["checked_ontop"]:
        #// Post-process $categories rather than adding an exclude to the get_terms() query
        #// to keep the query the same across all posts (for any query cache).
        checked_categories_ = Array()
        keys_ = php_array_keys(categories_)
        for k_ in keys_:
            if php_in_array(categories_[k_].term_id, args_["selected_cats"]):
                checked_categories_[-1] = categories_[k_]
                categories_[k_] = None
            # end if
        # end for
        #// Put checked categories on top.
        output_ += walker_.walk(checked_categories_, 0, args_)
    # end if
    #// Then the rest of them.
    output_ += walker_.walk(categories_, 0, args_)
    if parsed_args_["echo"]:
        php_print(output_)
    # end if
    return output_
# end def wp_terms_checklist
#// 
#// Retrieve a list of the most popular terms from the specified taxonomy.
#// 
#// If the $echo argument is true then the elements for a list of checkbox
#// `<input>` elements labelled with the names of the selected terms is output.
#// If the $post_ID global isn't empty then the terms associated with that
#// post will be marked as checked.
#// 
#// @since 2.5.0
#// 
#// @param string $taxonomy Taxonomy to retrieve terms from.
#// @param int    $default  Not used.
#// @param int    $number   Number of terms to retrieve. Defaults to 10.
#// @param bool   $echo     Optionally output the list as well. Defaults to true.
#// @return int[] Array of popular term IDs.
#//
def wp_popular_terms_checklist(taxonomy_=None, default_=0, number_=10, echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    post_ = get_post()
    if post_ and post_.ID:
        checked_terms_ = wp_get_object_terms(post_.ID, taxonomy_, Array({"fields": "ids"}))
    else:
        checked_terms_ = Array()
    # end if
    terms_ = get_terms(Array({"taxonomy": taxonomy_, "orderby": "count", "order": "DESC", "number": number_, "hierarchical": False}))
    tax_ = get_taxonomy(taxonomy_)
    popular_ids_ = Array()
    for term_ in terms_:
        popular_ids_[-1] = term_.term_id
        if (not echo_):
            continue
        # end if
        id_ = str("popular-") + str(taxonomy_) + str("-") + str(term_.term_id)
        checked_ = "checked=\"checked\"" if php_in_array(term_.term_id, checked_terms_) else ""
        php_print("\n       <li id=\"")
        php_print(id_)
        php_print("\" class=\"popular-category\">\n         <label class=\"selectit\">\n                <input id=\"in-")
        php_print(id_)
        php_print("\" type=\"checkbox\" ")
        php_print(checked_)
        php_print(" value=\"")
        php_print(php_int(term_.term_id))
        php_print("\" ")
        disabled((not current_user_can(tax_.cap.assign_terms)))
        php_print(" />\n                ")
        #// This filter is documented in wp-includes/category-template.php
        php_print(esc_html(apply_filters("the_category", term_.name, "", "")))
        php_print("""           </label>
        </li>
        """)
    # end for
    return popular_ids_
# end def wp_popular_terms_checklist
#// 
#// Outputs a link category checklist element.
#// 
#// @since 2.5.1
#// 
#// @param int $link_id
#//
def wp_link_category_checklist(link_id_=0, *_args_):
    
    
    default_ = 1
    checked_categories_ = Array()
    if link_id_:
        checked_categories_ = wp_get_link_cats(link_id_)
        #// No selected categories, strange.
        if (not php_count(checked_categories_)):
            checked_categories_[-1] = default_
        # end if
    else:
        checked_categories_[-1] = default_
    # end if
    categories_ = get_terms(Array({"taxonomy": "link_category", "orderby": "name", "hide_empty": 0}))
    if php_empty(lambda : categories_):
        return
    # end if
    for category_ in categories_:
        cat_id_ = category_.term_id
        #// This filter is documented in wp-includes/category-template.php
        name_ = esc_html(apply_filters("the_category", category_.name, "", ""))
        checked_ = " checked=\"checked\"" if php_in_array(cat_id_, checked_categories_) else ""
        php_print("<li id=\"link-category-", cat_id_, "\"><label for=\"in-link-category-", cat_id_, "\" class=\"selectit\"><input value=\"", cat_id_, "\" type=\"checkbox\" name=\"link_category[]\" id=\"in-link-category-", cat_id_, "\"", checked_, "/> ", name_, "</label></li>")
    # end for
# end def wp_link_category_checklist
#// 
#// Adds hidden fields with the data for use in the inline editor for posts and pages.
#// 
#// @since 2.7.0
#// 
#// @param WP_Post $post Post object.
#//
def get_inline_data(post_=None, *_args_):
    
    
    post_type_object_ = get_post_type_object(post_.post_type)
    if (not current_user_can("edit_post", post_.ID)):
        return
    # end if
    title_ = esc_textarea(php_trim(post_.post_title))
    php_print("\n<div class=\"hidden\" id=\"inline_" + post_.ID + "\">\n    <div class=\"post_title\">" + title_ + "</div>" + "<div class=\"post_name\">" + apply_filters("editable_slug", post_.post_name, post_) + "</div>\n  <div class=\"post_author\">" + post_.post_author + "</div>\n    <div class=\"comment_status\">" + esc_html(post_.comment_status) + "</div>\n    <div class=\"ping_status\">" + esc_html(post_.ping_status) + "</div>\n  <div class=\"_status\">" + esc_html(post_.post_status) + "</div>\n  <div class=\"jj\">" + mysql2date("d", post_.post_date, False) + "</div>\n   <div class=\"mm\">" + mysql2date("m", post_.post_date, False) + "</div>\n   <div class=\"aa\">" + mysql2date("Y", post_.post_date, False) + "</div>\n   <div class=\"hh\">" + mysql2date("H", post_.post_date, False) + "</div>\n   <div class=\"mn\">" + mysql2date("i", post_.post_date, False) + "</div>\n   <div class=\"ss\">" + mysql2date("s", post_.post_date, False) + "</div>\n   <div class=\"post_password\">" + esc_html(post_.post_password) + "</div>")
    if post_type_object_.hierarchical:
        php_print("<div class=\"post_parent\">" + post_.post_parent + "</div>")
    # end if
    php_print("<div class=\"page_template\">" + esc_html(post_.page_template) if post_.page_template else "default" + "</div>")
    if post_type_supports(post_.post_type, "page-attributes"):
        php_print("<div class=\"menu_order\">" + post_.menu_order + "</div>")
    # end if
    taxonomy_names_ = get_object_taxonomies(post_.post_type)
    for taxonomy_name_ in taxonomy_names_:
        taxonomy_ = get_taxonomy(taxonomy_name_)
        if taxonomy_.hierarchical and taxonomy_.show_ui:
            terms_ = get_object_term_cache(post_.ID, taxonomy_name_)
            if False == terms_:
                terms_ = wp_get_object_terms(post_.ID, taxonomy_name_)
                wp_cache_add(post_.ID, wp_list_pluck(terms_, "term_id"), taxonomy_name_ + "_relationships")
            # end if
            term_ids_ = Array() if php_empty(lambda : terms_) else wp_list_pluck(terms_, "term_id")
            php_print("<div class=\"post_category\" id=\"" + taxonomy_name_ + "_" + post_.ID + "\">" + php_implode(",", term_ids_) + "</div>")
        elif taxonomy_.show_ui:
            terms_to_edit_ = get_terms_to_edit(post_.ID, taxonomy_name_)
            if (not php_is_string(terms_to_edit_)):
                terms_to_edit_ = ""
            # end if
            php_print("<div class=\"tags_input\" id=\"" + taxonomy_name_ + "_" + post_.ID + "\">" + esc_html(php_str_replace(",", ", ", terms_to_edit_)) + "</div>")
        # end if
    # end for
    if (not post_type_object_.hierarchical):
        php_print("<div class=\"sticky\">" + "sticky" if is_sticky(post_.ID) else "" + "</div>")
    # end if
    if post_type_supports(post_.post_type, "post-formats"):
        php_print("<div class=\"post_format\">" + esc_html(get_post_format(post_.ID)) + "</div>")
    # end if
    #// 
    #// Fires after outputting the fields for the inline editor for posts and pages.
    #// 
    #// @since 4.9.8
    #// 
    #// @param WP_Post      $post             The current post object.
    #// @param WP_Post_Type $post_type_object The current post's post type object.
    #//
    do_action("add_inline_data", post_, post_type_object_)
    php_print("</div>")
# end def get_inline_data
#// 
#// Outputs the in-line comment reply-to form in the Comments list table.
#// 
#// @since 2.7.0
#// 
#// @global WP_List_Table $wp_list_table
#// 
#// @param int    $position
#// @param bool   $checkbox
#// @param string $mode
#// @param bool   $table_row
#//
def wp_comment_reply(position_=1, checkbox_=None, mode_="single", table_row_=None, *_args_):
    if checkbox_ is None:
        checkbox_ = False
    # end if
    if table_row_ is None:
        table_row_ = True
    # end if
    
    global wp_list_table_
    php_check_if_defined("wp_list_table_")
    #// 
    #// Filters the in-line comment reply-to form output in the Comments
    #// list table.
    #// 
    #// Returning a non-empty value here will short-circuit display
    #// of the in-line comment-reply form in the Comments list table,
    #// echoing the returned value instead.
    #// 
    #// @since 2.7.0
    #// 
    #// @see wp_comment_reply()
    #// 
    #// @param string $content The reply-to form content.
    #// @param array  $args    An array of default args.
    #//
    content_ = apply_filters("wp_comment_reply", "", Array({"position": position_, "checkbox": checkbox_, "mode": mode_}))
    if (not php_empty(lambda : content_)):
        php_print(content_)
        return
    # end if
    if (not wp_list_table_):
        if "single" == mode_:
            wp_list_table_ = _get_list_table("WP_Post_Comments_List_Table")
        else:
            wp_list_table_ = _get_list_table("WP_Comments_List_Table")
        # end if
    # end if
    php_print("<form method=\"get\">\n  ")
    if table_row_:
        php_print("<table style=\"display:none;\"><tbody id=\"com-reply\"><tr id=\"replyrow\" class=\"inline-edit-row\" style=\"display:none;\"><td colspan=\"")
        php_print(wp_list_table_.get_column_count())
        php_print("\" class=\"colspanchange\">\n")
    else:
        php_print("<div id=\"com-reply\" style=\"display:none;\"><div id=\"replyrow\" style=\"display:none;\">\n")
    # end if
    php_print(" <fieldset class=\"comment-reply\">\n    <legend>\n      <span class=\"hidden\" id=\"editlegend\">")
    _e("Edit Comment")
    php_print("</span>\n        <span class=\"hidden\" id=\"replyhead\">")
    _e("Reply to Comment")
    php_print("</span>\n        <span class=\"hidden\" id=\"addhead\">")
    _e("Add new Comment")
    php_print("""</span>
    </legend>
    <div id=\"replycontainer\">
    <label for=\"replycontent\" class=\"screen-reader-text\">""")
    _e("Comment")
    php_print("</label>\n   ")
    quicktags_settings_ = Array({"buttons": "strong,em,link,block,del,ins,img,ul,ol,li,code,close"})
    wp_editor("", "replycontent", Array({"media_buttons": False, "tinymce": False, "quicktags": quicktags_settings_}))
    php_print("""   </div>
    <div id=\"edithead\" style=\"display:none;\">
    <div class=\"inside\">
    <label for=\"author-name\">""")
    _e("Name")
    php_print("""</label>
    <input type=\"text\" name=\"newcomment_author\" size=\"50\" value=\"\" id=\"author-name\" />
    </div>
    <div class=\"inside\">
    <label for=\"author-email\">""")
    _e("Email")
    php_print("""</label>
    <input type=\"text\" name=\"newcomment_author_email\" size=\"50\" value=\"\" id=\"author-email\" />
    </div>
    <div class=\"inside\">
    <label for=\"author-url\">""")
    _e("URL")
    php_print("""</label>
    <input type=\"text\" id=\"author-url\" name=\"newcomment_author_url\" class=\"code\" size=\"103\" value=\"\" />
    </div>
    </div>
    <div id=\"replysubmit\" class=\"submit\">
    <p class=\"reply-submit-buttons\">
    <button type=\"button\" class=\"save button button-primary\">
    <span id=\"addbtn\" style=\"display: none;\">""")
    _e("Add Comment")
    php_print("</span>\n                <span id=\"savebtn\" style=\"display: none;\">")
    _e("Update Comment")
    php_print("</span>\n                <span id=\"replybtn\" style=\"display: none;\">")
    _e("Submit Reply")
    php_print("</span>\n            </button>\n         <button type=\"button\" class=\"cancel button\">")
    _e("Cancel")
    php_print("""</button>
    <span class=\"waiting spinner\"></span>
    </p>
    <div class=\"notice notice-error notice-alt inline hidden\">
    <p class=\"error\"></p>
    </div>
    </div>
    <input type=\"hidden\" name=\"action\" id=\"action\" value=\"\" />
    <input type=\"hidden\" name=\"comment_ID\" id=\"comment_ID\" value=\"\" />
    <input type=\"hidden\" name=\"comment_post_ID\" id=\"comment_post_ID\" value=\"\" />
    <input type=\"hidden\" name=\"status\" id=\"status\" value=\"\" />
    <input type=\"hidden\" name=\"position\" id=\"position\" value=\"""")
    php_print(position_)
    php_print("\" />\n  <input type=\"hidden\" name=\"checkbox\" id=\"checkbox\" value=\"")
    php_print(1 if checkbox_ else 0)
    php_print("\" />\n  <input type=\"hidden\" name=\"mode\" id=\"mode\" value=\"")
    php_print(esc_attr(mode_))
    php_print("\" />\n  ")
    wp_nonce_field("replyto-comment", "_ajax_nonce-replyto-comment", False)
    if current_user_can("unfiltered_html"):
        wp_nonce_field("unfiltered-html-comment", "_wp_unfiltered_html_comment", False)
    # end if
    php_print(" </fieldset>\n   ")
    if table_row_:
        php_print("</td></tr></tbody></table>\n ")
    else:
        php_print("</div></div>\n   ")
    # end if
    php_print("</form>\n    ")
# end def wp_comment_reply
#// 
#// Output 'undo move to Trash' text for comments
#// 
#// @since 2.9.0
#//
def wp_comment_trashnotice(*_args_):
    
    
    php_print("<div class=\"hidden\" id=\"trash-undo-holder\">\n    <div class=\"trash-undo-inside\">\n     ")
    #// translators: %s: Comment author, filled by AJAX.
    php_printf(__("Comment by %s moved to the Trash."), "<strong></strong>")
    php_print("     <span class=\"undo untrash\"><a href=\"#\">")
    _e("Undo")
    php_print("""</a></span>
    </div>
    </div>
    <div class=\"hidden\" id=\"spam-undo-holder\">
    <div class=\"spam-undo-inside\">
    """)
    #// translators: %s: Comment author, filled by AJAX.
    php_printf(__("Comment by %s marked as spam."), "<strong></strong>")
    php_print("     <span class=\"undo unspam\"><a href=\"#\">")
    _e("Undo")
    php_print("""</a></span>
    </div>
    </div>
    """)
# end def wp_comment_trashnotice
#// 
#// Outputs a post's public meta data in the Custom Fields meta box.
#// 
#// @since 1.2.0
#// 
#// @param array $meta
#//
def list_meta(meta_=None, *_args_):
    
    
    #// Exit if no meta.
    if (not meta_):
        php_print("""
        <table id=\"list-table\" style=\"display: none;\">
        <thead>
        <tr>
        <th class=\"left\">""" + _x("Name", "meta name") + "</th>\n     <th>" + __("Value") + """</th>
        </tr>
        </thead>
        <tbody id=\"the-list\" data-wp-lists=\"list:meta\">
        <tr><td></td></tr>
        </tbody>
        </table>""")
        #// TBODY needed for list-manipulation JS.
        return
    # end if
    count_ = 0
    php_print("""<table id=\"list-table\">
    <thead>
    <tr>
    <th class=\"left\">""")
    _ex("Name", "meta name")
    php_print("</th>\n      <th>")
    _e("Value")
    php_print("""</th>
    </tr>
    </thead>
    <tbody id='the-list' data-wp-lists='list:meta'>
    """)
    for entry_ in meta_:
        php_print(_list_meta_row(entry_, count_))
    # end for
    php_print(" </tbody>\n</table>\n    ")
# end def list_meta
#// 
#// Outputs a single row of public meta data in the Custom Fields meta box.
#// 
#// @since 2.5.0
#// 
#// @staticvar string $update_nonce
#// 
#// @param array $entry
#// @param int   $count
#// @return string
#//
def _list_meta_row(entry_=None, count_=None, *_args_):
    
    
    update_nonce_ = ""
    if is_protected_meta(entry_["meta_key"], "post"):
        return ""
    # end if
    if (not update_nonce_):
        update_nonce_ = wp_create_nonce("add-meta")
    # end if
    r_ = ""
    count_ += 1
    if is_serialized(entry_["meta_value"]):
        if is_serialized_string(entry_["meta_value"]):
            #// This is a serialized string, so we should display it.
            entry_["meta_value"] = maybe_unserialize(entry_["meta_value"])
        else:
            #// This is a serialized array/object so we should NOT display it.
            count_ -= 1
            return ""
        # end if
    # end if
    entry_["meta_key"] = esc_attr(entry_["meta_key"])
    entry_["meta_value"] = esc_textarea(entry_["meta_value"])
    #// Using a <textarea />.
    entry_["meta_id"] = php_int(entry_["meta_id"])
    delete_nonce_ = wp_create_nonce("delete-meta_" + entry_["meta_id"])
    r_ += str("\n   <tr id='meta-") + str(entry_["meta_id"]) + str("'>")
    r_ += str("\n       <td class='left'><label class='screen-reader-text' for='meta-") + str(entry_["meta_id"]) + str("-key'>") + __("Key") + str("</label><input name='meta[") + str(entry_["meta_id"]) + str("][key]' id='meta-") + str(entry_["meta_id"]) + str("-key' type='text' size='20' value='") + str(entry_["meta_key"]) + str("' />")
    r_ += "\n       <div class='submit'>"
    r_ += get_submit_button(__("Delete"), "deletemeta small", str("deletemeta[") + str(entry_["meta_id"]) + str("]"), False, Array({"data-wp-lists": str("delete:the-list:meta-") + str(entry_["meta_id"]) + str("::_ajax_nonce=") + str(delete_nonce_)}))
    r_ += "\n       "
    r_ += get_submit_button(__("Update"), "updatemeta small", str("meta-") + str(entry_["meta_id"]) + str("-submit"), False, Array({"data-wp-lists": str("add:the-list:meta-") + str(entry_["meta_id"]) + str("::_ajax_nonce-add-meta=") + str(update_nonce_)}))
    r_ += "</div>"
    r_ += wp_nonce_field("change-meta", "_ajax_nonce", False, False)
    r_ += "</td>"
    r_ += str("\n       <td><label class='screen-reader-text' for='meta-") + str(entry_["meta_id"]) + str("-value'>") + __("Value") + str("</label><textarea name='meta[") + str(entry_["meta_id"]) + str("][value]' id='meta-") + str(entry_["meta_id"]) + str("-value' rows='2' cols='30'>") + str(entry_["meta_value"]) + str("</textarea></td>\n    </tr>")
    return r_
# end def _list_meta_row
#// 
#// Prints the form in the Custom Fields meta box.
#// 
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param WP_Post $post Optional. The post being edited.
#//
def meta_form(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post(post_)
    #// 
    #// Filters values for the meta key dropdown in the Custom Fields meta box.
    #// 
    #// Returning a non-null value will effectively short-circuit and avoid a
    #// potentially expensive query against postmeta.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array|null $keys Pre-defined meta keys to be used in place of a postmeta query. Default null.
    #// @param WP_Post    $post The current post object.
    #//
    keys_ = apply_filters("postmeta_form_keys", None, post_)
    if None == keys_:
        #// 
        #// Filters the number of custom fields to retrieve for the drop-down
        #// in the Custom Fields meta box.
        #// 
        #// @since 2.1.0
        #// 
        #// @param int $limit Number of custom fields to retrieve. Default 30.
        #//
        limit_ = apply_filters("postmeta_form_limit", 30)
        sql_ = str("SELECT DISTINCT meta_key\n          FROM ") + str(wpdb_.postmeta) + str("""\n           WHERE meta_key NOT BETWEEN '_' AND '_z'\n           HAVING meta_key NOT LIKE %s\n           ORDER BY meta_key\n         LIMIT %d""")
        keys_ = wpdb_.get_col(wpdb_.prepare(sql_, wpdb_.esc_like("_") + "%", limit_))
    # end if
    if keys_:
        natcasesort(keys_)
        meta_key_input_id_ = "metakeyselect"
    else:
        meta_key_input_id_ = "metakeyinput"
    # end if
    php_print("<p><strong>")
    _e("Add New Custom Field:")
    php_print("""</strong></p>
    <table id=\"newmeta\">
    <thead>
    <tr>
    <th class=\"left\"><label for=\"""")
    php_print(meta_key_input_id_)
    php_print("\">")
    _ex("Name", "meta name")
    php_print("</label></th>\n<th><label for=\"metavalue\">")
    _e("Value")
    php_print("""</label></th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td id=\"newmetaleft\" class=\"left\">
    """)
    if keys_:
        php_print("<select id=\"metakeyselect\" name=\"metakeyselect\">\n<option value=\"#NONE#\">")
        _e("&mdash; Select &mdash;")
        php_print("</option>\n      ")
        for key_ in keys_:
            if is_protected_meta(key_, "post") or (not current_user_can("add_post_meta", post_.ID, key_)):
                continue
            # end if
            php_print("\n<option value='" + esc_attr(key_) + "'>" + esc_html(key_) + "</option>")
        # end for
        php_print("""</select>
        <input class=\"hide-if-js\" type=\"text\" id=\"metakeyinput\" name=\"metakeyinput\" value=\"\" />
        <a href=\"#postcustomstuff\" class=\"hide-if-no-js\" onclick=\"jQuery('#metakeyinput, #metakeyselect, #enternew, #cancelnew').toggle();return false;\">
        <span id=\"enternew\">""")
        _e("Enter new")
        php_print("</span>\n<span id=\"cancelnew\" class=\"hidden\">")
        _e("Cancel")
        php_print("</span></a>\n")
    else:
        php_print("<input type=\"text\" id=\"metakeyinput\" name=\"metakeyinput\" value=\"\" />\n")
    # end if
    php_print("""</td>
    <td><textarea id=\"metavalue\" name=\"metavalue\" rows=\"2\" cols=\"25\"></textarea></td>
    </tr>
    <tr><td colspan=\"2\">
    <div class=\"submit\">
    """)
    submit_button(__("Add Custom Field"), "", "addmeta", False, Array({"id": "newmeta-submit", "data-wp-lists": "add:the-list:newmeta"}))
    php_print("</div>\n ")
    wp_nonce_field("add-meta", "_ajax_nonce-add-meta", False)
    php_print("""</td></tr>
    </tbody>
    </table>
    """)
# end def meta_form
#// 
#// Print out HTML form date elements for editing post or comment publish date.
#// 
#// @since 0.71
#// @since 4.4.0 Converted to use get_comment() instead of the global `$comment`.
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @param int|bool $edit      Accepts 1|true for editing the date, 0|false for adding the date.
#// @param int|bool $for_post  Accepts 1|true for applying the date to a post, 0|false for a comment.
#// @param int      $tab_index The tabindex attribute to add. Default 0.
#// @param int|bool $multi     Optional. Whether the additional fields and buttons should be added.
#// Default 0|false.
#//
def touch_time(edit_=1, for_post_=1, tab_index_=0, multi_=0, *_args_):
    
    
    global wp_locale_
    php_check_if_defined("wp_locale_")
    post_ = get_post()
    if for_post_:
        edit_ = (not php_in_array(post_.post_status, Array("draft", "pending")) and (not post_.post_date_gmt) or "0000-00-00 00:00:00" == post_.post_date_gmt)
    # end if
    tab_index_attribute_ = ""
    if php_int(tab_index_) > 0:
        tab_index_attribute_ = str(" tabindex=\"") + str(tab_index_) + str("\"")
    # end if
    #// @todo Remove this?
    #// echo '<label for="timestamp" style="display: block;"><input type="checkbox" class="checkbox" name="edit_date" value="1" id="timestamp"'.$tab_index_attribute.' /> '.__( 'Edit timestamp' ).'</label><br />';
    post_date_ = post_.post_date if for_post_ else get_comment().comment_date
    jj_ = mysql2date("d", post_date_, False) if edit_ else current_time("d")
    mm_ = mysql2date("m", post_date_, False) if edit_ else current_time("m")
    aa_ = mysql2date("Y", post_date_, False) if edit_ else current_time("Y")
    hh_ = mysql2date("H", post_date_, False) if edit_ else current_time("H")
    mn_ = mysql2date("i", post_date_, False) if edit_ else current_time("i")
    ss_ = mysql2date("s", post_date_, False) if edit_ else current_time("s")
    cur_jj_ = current_time("d")
    cur_mm_ = current_time("m")
    cur_aa_ = current_time("Y")
    cur_hh_ = current_time("H")
    cur_mn_ = current_time("i")
    month_ = "<label><span class=\"screen-reader-text\">" + __("Month") + "</span><select " + "" if multi_ else "id=\"mm\" " + "name=\"mm\"" + tab_index_attribute_ + ">\n"
    i_ = 1
    while i_ < 13:
        
        monthnum_ = zeroise(i_, 2)
        monthtext_ = wp_locale_.get_month_abbrev(wp_locale_.get_month(i_))
        month_ += "         " + "<option value=\"" + monthnum_ + "\" data-text=\"" + monthtext_ + "\" " + selected(monthnum_, mm_, False) + ">"
        #// translators: 1: Month number (01, 02, etc.), 2: Month abbreviation.
        month_ += php_sprintf(__("%1$s-%2$s"), monthnum_, monthtext_) + "</option>\n"
        i_ = i_ + 1
    # end while
    month_ += "</select></label>"
    day_ = "<label><span class=\"screen-reader-text\">" + __("Day") + "</span><input type=\"text\" " + "" if multi_ else "id=\"jj\" " + "name=\"jj\" value=\"" + jj_ + "\" size=\"2\" maxlength=\"2\"" + tab_index_attribute_ + " autocomplete=\"off\" /></label>"
    year_ = "<label><span class=\"screen-reader-text\">" + __("Year") + "</span><input type=\"text\" " + "" if multi_ else "id=\"aa\" " + "name=\"aa\" value=\"" + aa_ + "\" size=\"4\" maxlength=\"4\"" + tab_index_attribute_ + " autocomplete=\"off\" /></label>"
    hour_ = "<label><span class=\"screen-reader-text\">" + __("Hour") + "</span><input type=\"text\" " + "" if multi_ else "id=\"hh\" " + "name=\"hh\" value=\"" + hh_ + "\" size=\"2\" maxlength=\"2\"" + tab_index_attribute_ + " autocomplete=\"off\" /></label>"
    minute_ = "<label><span class=\"screen-reader-text\">" + __("Minute") + "</span><input type=\"text\" " + "" if multi_ else "id=\"mn\" " + "name=\"mn\" value=\"" + mn_ + "\" size=\"2\" maxlength=\"2\"" + tab_index_attribute_ + " autocomplete=\"off\" /></label>"
    php_print("<div class=\"timestamp-wrap\">")
    #// translators: 1: Month, 2: Day, 3: Year, 4: Hour, 5: Minute.
    php_printf(__("%1$s %2$s, %3$s at %4$s:%5$s"), month_, day_, year_, hour_, minute_)
    php_print("</div><input type=\"hidden\" id=\"ss\" name=\"ss\" value=\"" + ss_ + "\" />")
    if multi_:
        return
    # end if
    php_print("\n\n")
    map_ = Array({"mm": Array(mm_, cur_mm_), "jj": Array(jj_, cur_jj_), "aa": Array(aa_, cur_aa_), "hh": Array(hh_, cur_hh_), "mn": Array(mn_, cur_mn_)})
    for timeunit_,value_ in map_.items():
        unit_, curr_ = value_
        php_print("<input type=\"hidden\" id=\"hidden_" + timeunit_ + "\" name=\"hidden_" + timeunit_ + "\" value=\"" + unit_ + "\" />" + "\n")
        cur_timeunit_ = "cur_" + timeunit_
        php_print("<input type=\"hidden\" id=\"" + cur_timeunit_ + "\" name=\"" + cur_timeunit_ + "\" value=\"" + curr_ + "\" />" + "\n")
    # end for
    php_print("\n<p>\n<a href=\"#edit_timestamp\" class=\"save-timestamp hide-if-no-js button\">")
    _e("OK")
    php_print("</a>\n<a href=\"#edit_timestamp\" class=\"cancel-timestamp hide-if-no-js button-cancel\">")
    _e("Cancel")
    php_print("</a>\n</p>\n ")
# end def touch_time
#// 
#// Print out option HTML elements for the page templates drop-down.
#// 
#// @since 1.5.0
#// @since 4.7.0 Added the `$post_type` parameter.
#// 
#// @param string $default   Optional. The template file name. Default empty.
#// @param string $post_type Optional. Post type to get templates for. Default 'post'.
#//
def page_template_dropdown(default_="", post_type_="page", *_args_):
    
    
    templates_ = get_page_templates(None, post_type_)
    php_ksort(templates_)
    for template_ in php_array_keys(templates_):
        selected_ = selected(default_, templates_[template_], False)
        php_print("\n   <option value='" + esc_attr(templates_[template_]) + str("' ") + str(selected_) + str(">") + esc_html(template_) + "</option>")
    # end for
# end def page_template_dropdown
#// 
#// Print out option HTML elements for the page parents drop-down.
#// 
#// @since 1.5.0
#// @since 4.4.0 `$post` argument was added.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int         $default Optional. The default page ID to be pre-selected. Default 0.
#// @param int         $parent  Optional. The parent page ID. Default 0.
#// @param int         $level   Optional. Page depth level. Default 0.
#// @param int|WP_Post $post    Post ID or WP_Post object.
#// @return void|false Void on success, false if the page has no children.
#//
def parent_dropdown(default_=0, parent_=0, level_=0, post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post(post_)
    items_ = wpdb_.get_results(wpdb_.prepare(str("SELECT ID, post_parent, post_title FROM ") + str(wpdb_.posts) + str(" WHERE post_parent = %d AND post_type = 'page' ORDER BY menu_order"), parent_))
    if items_:
        for item_ in items_:
            #// A page cannot be its own parent.
            if post_ and post_.ID and item_.ID == post_.ID:
                continue
            # end if
            pad_ = php_str_repeat("&nbsp;", level_ * 3)
            selected_ = selected(default_, item_.ID, False)
            php_print(str("\n   <option class='level-") + str(level_) + str("' value='") + str(item_.ID) + str("' ") + str(selected_) + str(">") + str(pad_) + str(" ") + esc_html(item_.post_title) + "</option>")
            parent_dropdown(default_, item_.ID, level_ + 1)
        # end for
    else:
        return False
    # end if
# end def parent_dropdown
#// 
#// Print out option html elements for role selectors.
#// 
#// @since 2.1.0
#// 
#// @param string $selected Slug for the role that should be already selected.
#//
def wp_dropdown_roles(selected_="", *_args_):
    
    
    r_ = ""
    editable_roles_ = php_array_reverse(get_editable_roles())
    for role_,details_ in editable_roles_.items():
        name_ = translate_user_role(details_["name"])
        #// Preselect specified role.
        if selected_ == role_:
            r_ += "\n   <option selected='selected' value='" + esc_attr(role_) + str("'>") + str(name_) + str("</option>")
        else:
            r_ += "\n   <option value='" + esc_attr(role_) + str("'>") + str(name_) + str("</option>")
        # end if
    # end for
    php_print(r_)
# end def wp_dropdown_roles
#// 
#// Outputs the form used by the importers to accept the data to be imported
#// 
#// @since 2.0.0
#// 
#// @param string $action The action attribute for the form.
#//
def wp_import_upload_form(action_=None, *_args_):
    
    
    #// 
    #// Filters the maximum allowed upload size for import files.
    #// 
    #// @since 2.3.0
    #// 
    #// @see wp_max_upload_size()
    #// 
    #// @param int $max_upload_size Allowed upload size. Default 1 MB.
    #//
    bytes_ = apply_filters("import_upload_size_limit", wp_max_upload_size())
    size_ = size_format(bytes_)
    upload_dir_ = wp_upload_dir()
    if (not php_empty(lambda : upload_dir_["error"])):
        php_print("     <div class=\"error\"><p>")
        _e("Before you can upload your import file, you will need to fix the following error:")
        php_print("</p>\n       <p><strong>")
        php_print(upload_dir_["error"])
        php_print("</strong></p></div>\n                                ")
    else:
        php_print("<form enctype=\"multipart/form-data\" id=\"import-upload-form\" method=\"post\" class=\"wp-upload-form\" action=\"")
        php_print(esc_url(wp_nonce_url(action_, "import-upload")))
        php_print("\">\n<p>\n       ")
        php_printf("<label for=\"upload\">%s</label> (%s)", __("Choose a file from your computer:"), php_sprintf(__("Maximum size: %s"), size_))
        php_print("<input type=\"file\" id=\"upload\" name=\"import\" size=\"25\" />\n<input type=\"hidden\" name=\"action\" value=\"save\" />\n<input type=\"hidden\" name=\"max_file_size\" value=\"")
        php_print(bytes_)
        php_print("\" />\n</p>\n        ")
        submit_button(__("Upload file and import"), "primary")
        php_print("</form>\n        ")
    # end if
# end def wp_import_upload_form
#// 
#// Adds a meta box to one or more screens.
#// 
#// @since 2.5.0
#// @since 4.4.0 The `$screen` parameter now accepts an array of screen IDs.
#// 
#// @global array $wp_meta_boxes
#// 
#// @param string                 $id            Meta box ID (used in the 'id' attribute for the meta box).
#// @param string                 $title         Title of the meta box.
#// @param callable               $callback      Function that fills the box with the desired content.
#// The function should echo its output.
#// @param string|array|WP_Screen $screen        Optional. The screen or screens on which to show the box
#// (such as a post type, 'link', or 'comment'). Accepts a single
#// screen ID, WP_Screen object, or array of screen IDs. Default
#// is the current screen.  If you have used add_menu_page() or
#// add_submenu_page() to create a new screen (and hence screen_id),
#// make sure your menu slug conforms to the limits of sanitize_key()
#// otherwise the 'screen' menu may not correctly render on your page.
#// @param string                 $context       Optional. The context within the screen where the boxes
#// should display. Available contexts vary from screen to
#// screen. Post edit screen contexts include 'normal', 'side',
#// and 'advanced'. Comments screen contexts include 'normal'
#// and 'side'. Menus meta boxes (accordion sections) all use
#// the 'side' context. Global default is 'advanced'.
#// @param string                 $priority      Optional. The priority within the context where the boxes
#// should show ('high', 'low'). Default 'default'.
#// @param array                  $callback_args Optional. Data that should be set as the $args property
#// of the box array (which is the second parameter passed
#// to your callback). Default null.
#//
def add_meta_box(id_=None, title_=None, callback_=None, screen_=None, context_="advanced", priority_="default", callback_args_=None, *_args_):
    if screen_ is None:
        screen_ = None
    # end if
    if callback_args_ is None:
        callback_args_ = None
    # end if
    
    global wp_meta_boxes_
    php_check_if_defined("wp_meta_boxes_")
    if php_empty(lambda : screen_):
        screen_ = get_current_screen()
    elif php_is_string(screen_):
        screen_ = convert_to_screen(screen_)
    elif php_is_array(screen_):
        for single_screen_ in screen_:
            add_meta_box(id_, title_, callback_, single_screen_, context_, priority_, callback_args_)
        # end for
    # end if
    if (not (php_isset(lambda : screen_.id))):
        return
    # end if
    page_ = screen_.id
    if (not (php_isset(lambda : wp_meta_boxes_))):
        wp_meta_boxes_ = Array()
    # end if
    if (not (php_isset(lambda : wp_meta_boxes_[page_]))):
        wp_meta_boxes_[page_] = Array()
    # end if
    if (not (php_isset(lambda : wp_meta_boxes_[page_][context_]))):
        wp_meta_boxes_[page_][context_] = Array()
    # end if
    for a_context_ in php_array_keys(wp_meta_boxes_[page_]):
        for a_priority_ in Array("high", "core", "default", "low"):
            if (not (php_isset(lambda : wp_meta_boxes_[page_][a_context_][a_priority_][id_]))):
                continue
            # end if
            #// If a core box was previously added or removed by a plugin, don't add.
            if "core" == priority_:
                #// If core box previously deleted, don't add.
                if False == wp_meta_boxes_[page_][a_context_][a_priority_][id_]:
                    return
                # end if
                #// 
                #// If box was added with default priority, give it core priority to
                #// maintain sort order.
                #//
                if "default" == a_priority_:
                    wp_meta_boxes_[page_][a_context_]["core"][id_] = wp_meta_boxes_[page_][a_context_]["default"][id_]
                    wp_meta_boxes_[page_][a_context_]["default"][id_] = None
                # end if
                return
            # end if
            #// If no priority given and ID already present, use existing priority.
            if php_empty(lambda : priority_):
                priority_ = a_priority_
                pass
            elif "sorted" == priority_:
                title_ = wp_meta_boxes_[page_][a_context_][a_priority_][id_]["title"]
                callback_ = wp_meta_boxes_[page_][a_context_][a_priority_][id_]["callback"]
                callback_args_ = wp_meta_boxes_[page_][a_context_][a_priority_][id_]["args"]
            # end if
            #// An ID can be in only one priority and one context.
            if priority_ != a_priority_ or context_ != a_context_:
                wp_meta_boxes_[page_][a_context_][a_priority_][id_] = None
            # end if
        # end for
    # end for
    if php_empty(lambda : priority_):
        priority_ = "low"
    # end if
    if (not (php_isset(lambda : wp_meta_boxes_[page_][context_][priority_]))):
        wp_meta_boxes_[page_][context_][priority_] = Array()
    # end if
    wp_meta_boxes_[page_][context_][priority_][id_] = Array({"id": id_, "title": title_, "callback": callback_, "args": callback_args_})
# end def add_meta_box
#// 
#// Function that renders a "fake" meta box with an information message,
#// shown on the block editor, when an incompatible meta box is found.
#// 
#// @since 5.0.0
#// 
#// @param mixed $object The data object being rendered on this screen.
#// @param array $box    {
#// Custom formats meta box arguments.
#// 
#// @type string   $id           Meta box 'id' attribute.
#// @type string   $title        Meta box title.
#// @type callable $old_callback The original callback for this meta box.
#// @type array    $args         Extra meta box arguments.
#// }
#//
def do_block_editor_incompatible_meta_box(object_=None, box_=None, *_args_):
    
    
    plugin_ = _get_plugin_from_callback(box_["old_callback"])
    plugins_ = get_plugins()
    php_print("<p>")
    if plugin_:
        #// translators: %s: The name of the plugin that generated this meta box.
        php_printf(__("This meta box, from the %s plugin, isn't compatible with the block editor."), str("<strong>") + str(plugin_["Name"]) + str("</strong>"))
    else:
        _e("This meta box isn't compatible with the block editor.")
    # end if
    php_print("</p>")
    if php_empty(lambda : plugins_["classic-editor/classic-editor.php"]):
        if current_user_can("install_plugins"):
            php_print("<p>")
            php_printf(__("Please install the <a href=\"%s\">Classic Editor plugin</a> to use this meta box."), esc_url(wp_nonce_url(self_admin_url("plugin-install.php?tab=favorites&user=wordpressdotorg&save=0"), "save_wporg_username_" + get_current_user_id())))
            php_print("</p>")
        # end if
    elif is_plugin_inactive("classic-editor/classic-editor.php"):
        if current_user_can("activate_plugins"):
            activate_url_ = wp_nonce_url(self_admin_url("plugins.php?action=activate&plugin=classic-editor/classic-editor.php"), "activate-plugin_classic-editor/classic-editor.php")
            php_print("<p>")
            #// translators: %s: A link to activate the Classic Editor plugin.
            php_printf(__("Please activate the <a href=\"%s\">Classic Editor plugin</a> to use this meta box."), esc_url(activate_url_))
            php_print("</p>")
        # end if
    elif type(object_).__name__ == "WP_Post":
        edit_url_ = add_query_arg(Array({"classic-editor": "", "classic-editor__forget": ""}), get_edit_post_link(object_))
        php_print("<p>")
        #// translators: %s: A link to use the Classic Editor plugin.
        php_printf(__("Please open the <a href=\"%s\">classic editor</a> to use this meta box."), esc_url(edit_url_))
        php_print("</p>")
    # end if
# end def do_block_editor_incompatible_meta_box
#// 
#// Internal helper function to find the plugin from a meta box callback.
#// 
#// @since 5.0.0
#// 
#// @access private
#// 
#// @param callable $callback The callback function to check.
#// @return array|null The plugin that the callback belongs to, or null if it doesn't belong to a plugin.
#//
def _get_plugin_from_callback(callback_=None, *_args_):
    
    
    try: 
        if php_is_array(callback_):
            reflection_ = php_new_class("ReflectionMethod", lambda : ReflectionMethod(callback_[0], callback_[1]))
        elif php_is_string(callback_) and False != php_strpos(callback_, "::"):
            reflection_ = php_new_class("ReflectionMethod", lambda : ReflectionMethod(callback_))
        else:
            reflection_ = php_new_class("ReflectionFunction", lambda : ReflectionFunction(callback_))
        # end if
    except ReflectionException as exception_:
        #// We could not properly reflect on the callable, so we abort here.
        return None
    # end try
    #// Don't show an error if it's an internal PHP function.
    if (not reflection_.isinternal()):
        #// Only show errors if the meta box was registered by a plugin.
        filename_ = wp_normalize_path(reflection_.getfilename())
        plugin_dir_ = wp_normalize_path(WP_PLUGIN_DIR)
        if php_strpos(filename_, plugin_dir_) == 0:
            filename_ = php_str_replace(plugin_dir_, "", filename_)
            filename_ = php_preg_replace("|^/([^/]*/).*$|", "\\1", filename_)
            plugins_ = get_plugins()
            for name_,plugin_ in plugins_.items():
                if php_strpos(name_, filename_) == 0:
                    return plugin_
                # end if
            # end for
        # end if
    # end if
    return None
# end def _get_plugin_from_callback
#// 
#// Meta-Box template function.
#// 
#// @since 2.5.0
#// 
#// @global array $wp_meta_boxes
#// 
#// @staticvar bool $already_sorted
#// 
#// @param string|WP_Screen $screen  Screen identifier. If you have used add_menu_page() or
#// add_submenu_page() to create a new screen (and hence screen_id)
#// make sure your menu slug conforms to the limits of sanitize_key()
#// otherwise the 'screen' menu may not correctly render on your page.
#// @param string           $context The screen context for which to display meta boxes.
#// @param mixed            $object  Gets passed to the first parameter of the meta box callback function.
#// Often this is the object that's the focus of the current screen, for
#// example a `WP_Post` or `WP_Comment` object.
#// @return int number of meta_boxes
#//
def do_meta_boxes(screen_=None, context_=None, object_=None, *_args_):
    
    
    global wp_meta_boxes_
    php_check_if_defined("wp_meta_boxes_")
    already_sorted_ = False
    if php_empty(lambda : screen_):
        screen_ = get_current_screen()
    elif php_is_string(screen_):
        screen_ = convert_to_screen(screen_)
    # end if
    page_ = screen_.id
    hidden_ = get_hidden_meta_boxes(screen_)
    php_printf("<div id=\"%s-sortables\" class=\"meta-box-sortables\">", esc_attr(context_))
    #// Grab the ones the user has manually sorted.
    #// Pull them out of their previous context/priority and into the one the user chose.
    sorted_ = get_user_option(str("meta-box-order_") + str(page_))
    if (not already_sorted_) and sorted_:
        for box_context_,ids_ in sorted_.items():
            for id_ in php_explode(",", ids_):
                if id_ and "dashboard_browser_nag" != id_:
                    add_meta_box(id_, None, None, screen_, box_context_, "sorted")
                # end if
            # end for
        # end for
    # end if
    already_sorted_ = True
    i_ = 0
    if (php_isset(lambda : wp_meta_boxes_[page_][context_])):
        for priority_ in Array("high", "sorted", "core", "default", "low"):
            if (php_isset(lambda : wp_meta_boxes_[page_][context_][priority_])):
                for box_ in wp_meta_boxes_[page_][context_][priority_]:
                    if False == box_ or (not box_["title"]):
                        continue
                    # end if
                    block_compatible_ = True
                    if php_is_array(box_["args"]):
                        #// If a meta box is just here for back compat, don't show it in the block editor.
                        if screen_.is_block_editor() and (php_isset(lambda : box_["args"]["__back_compat_meta_box"])) and box_["args"]["__back_compat_meta_box"]:
                            continue
                        # end if
                        if (php_isset(lambda : box_["args"]["__block_editor_compatible_meta_box"])):
                            block_compatible_ = php_bool(box_["args"]["__block_editor_compatible_meta_box"])
                            box_["args"]["__block_editor_compatible_meta_box"] = None
                        # end if
                        #// If the meta box is declared as incompatible with the block editor, override the callback function.
                        if (not block_compatible_) and screen_.is_block_editor():
                            box_["old_callback"] = box_["callback"]
                            box_["callback"] = "do_block_editor_incompatible_meta_box"
                        # end if
                        if (php_isset(lambda : box_["args"]["__back_compat_meta_box"])):
                            block_compatible_ = block_compatible_ or php_bool(box_["args"]["__back_compat_meta_box"])
                            box_["args"]["__back_compat_meta_box"] = None
                        # end if
                    # end if
                    i_ += 1
                    #// get_hidden_meta_boxes() doesn't apply in the block editor.
                    hidden_class_ = " hide-if-js" if (not screen_.is_block_editor()) and php_in_array(box_["id"], hidden_) else ""
                    php_print("<div id=\"" + box_["id"] + "\" class=\"postbox " + postbox_classes(box_["id"], page_) + hidden_class_ + "\" " + ">" + "\n")
                    if "dashboard_browser_nag" != box_["id"]:
                        widget_title_ = box_["title"]
                        if php_is_array(box_["args"]) and (php_isset(lambda : box_["args"]["__widget_basename"])):
                            widget_title_ = box_["args"]["__widget_basename"]
                            box_["args"]["__widget_basename"] = None
                        # end if
                        php_print("<button type=\"button\" class=\"handlediv\" aria-expanded=\"true\">")
                        php_print("<span class=\"screen-reader-text\">" + php_sprintf(__("Toggle panel: %s"), widget_title_) + "</span>")
                        php_print("<span class=\"toggle-indicator\" aria-hidden=\"true\"></span>")
                        php_print("</button>")
                    # end if
                    php_print("<h2 class=\"hndle\">")
                    if "dashboard_php_nag" == box_["id"]:
                        php_print("<span aria-hidden=\"true\" class=\"dashicons dashicons-warning\"></span>")
                        php_print("<span class=\"screen-reader-text\">" + __("Warning:") + " </span>")
                    # end if
                    php_print(str("<span>") + str(box_["title"]) + str("</span>"))
                    php_print("</h2>\n")
                    php_print("<div class=\"inside\">" + "\n")
                    if WP_DEBUG and (not block_compatible_) and "edit" == screen_.parent_base and (not screen_.is_block_editor()) and (not (php_isset(lambda : PHP_REQUEST["meta-box-loader"]))):
                        plugin_ = _get_plugin_from_callback(box_["callback"])
                        if plugin_:
                            php_print("                         <div class=\"error inline\">\n                              <p>\n                                   ")
                            #// translators: %s: The name of the plugin that generated this meta box.
                            php_printf(__("This meta box, from the %s plugin, isn't compatible with the block editor."), str("<strong>") + str(plugin_["Name"]) + str("</strong>"))
                            php_print("                             </p>\n                          </div>\n                            ")
                        # end if
                    # end if
                    php_call_user_func(box_["callback"], object_, box_)
                    php_print("</div>\n")
                    php_print("</div>\n")
                # end for
            # end if
        # end for
    # end if
    php_print("</div>")
    return i_
# end def do_meta_boxes
#// 
#// Removes a meta box from one or more screens.
#// 
#// @since 2.6.0
#// @since 4.4.0 The `$screen` parameter now accepts an array of screen IDs.
#// 
#// @global array $wp_meta_boxes
#// 
#// @param string                 $id      Meta box ID (used in the 'id' attribute for the meta box).
#// @param string|array|WP_Screen $screen  The screen or screens on which the meta box is shown (such as a
#// post type, 'link', or 'comment'). Accepts a single screen ID,
#// WP_Screen object, or array of screen IDs.
#// @param string                 $context The context within the screen where the box is set to display.
#// Contexts vary from screen to screen. Post edit screen contexts
#// include 'normal', 'side', and 'advanced'. Comments screen contexts
#// include 'normal' and 'side'. Menus meta boxes (accordion sections)
#// all use the 'side' context.
#//
def remove_meta_box(id_=None, screen_=None, context_=None, *_args_):
    
    
    global wp_meta_boxes_
    php_check_if_defined("wp_meta_boxes_")
    if php_empty(lambda : screen_):
        screen_ = get_current_screen()
    elif php_is_string(screen_):
        screen_ = convert_to_screen(screen_)
    elif php_is_array(screen_):
        for single_screen_ in screen_:
            remove_meta_box(id_, single_screen_, context_)
        # end for
    # end if
    if (not (php_isset(lambda : screen_.id))):
        return
    # end if
    page_ = screen_.id
    if (not (php_isset(lambda : wp_meta_boxes_))):
        wp_meta_boxes_ = Array()
    # end if
    if (not (php_isset(lambda : wp_meta_boxes_[page_]))):
        wp_meta_boxes_[page_] = Array()
    # end if
    if (not (php_isset(lambda : wp_meta_boxes_[page_][context_]))):
        wp_meta_boxes_[page_][context_] = Array()
    # end if
    for priority_ in Array("high", "core", "default", "low"):
        wp_meta_boxes_[page_][context_][priority_][id_] = False
    # end for
# end def remove_meta_box
#// 
#// Meta Box Accordion Template Function.
#// 
#// Largely made up of abstracted code from do_meta_boxes(), this
#// function serves to build meta boxes as list items for display as
#// a collapsible accordion.
#// 
#// @since 3.6.0
#// 
#// @uses global $wp_meta_boxes Used to retrieve registered meta boxes.
#// 
#// @param string|object $screen  The screen identifier.
#// @param string        $context The meta box context.
#// @param mixed         $object  gets passed to the section callback function as first parameter.
#// @return int number of meta boxes as accordion sections.
#//
def do_accordion_sections(screen_=None, context_=None, object_=None, *_args_):
    
    
    global wp_meta_boxes_
    php_check_if_defined("wp_meta_boxes_")
    wp_enqueue_script("accordion")
    if php_empty(lambda : screen_):
        screen_ = get_current_screen()
    elif php_is_string(screen_):
        screen_ = convert_to_screen(screen_)
    # end if
    page_ = screen_.id
    hidden_ = get_hidden_meta_boxes(screen_)
    php_print(" <div id=\"side-sortables\" class=\"accordion-container\">\n     <ul class=\"outer-border\">\n   ")
    i_ = 0
    first_open_ = False
    if (php_isset(lambda : wp_meta_boxes_[page_][context_])):
        for priority_ in Array("high", "core", "default", "low"):
            if (php_isset(lambda : wp_meta_boxes_[page_][context_][priority_])):
                for box_ in wp_meta_boxes_[page_][context_][priority_]:
                    if False == box_ or (not box_["title"]):
                        continue
                    # end if
                    i_ += 1
                    hidden_class_ = "hide-if-js" if php_in_array(box_["id"], hidden_) else ""
                    open_class_ = ""
                    if (not first_open_) and php_empty(lambda : hidden_class_):
                        first_open_ = True
                        open_class_ = "open"
                    # end if
                    php_print("                 <li class=\"control-section accordion-section ")
                    php_print(hidden_class_)
                    php_print(" ")
                    php_print(open_class_)
                    php_print(" ")
                    php_print(esc_attr(box_["id"]))
                    php_print("\" id=\"")
                    php_print(esc_attr(box_["id"]))
                    php_print("\">\n                        <h3 class=\"accordion-section-title hndle\" tabindex=\"0\">\n                           ")
                    php_print(esc_html(box_["title"]))
                    php_print("                         <span class=\"screen-reader-text\">")
                    _e("Press return or enter to open this section")
                    php_print("</span>\n                        </h3>\n                     <div class=\"accordion-section-content ")
                    postbox_classes(box_["id"], page_)
                    php_print("\">\n                            <div class=\"inside\">\n                                ")
                    php_call_user_func(box_["callback"], object_, box_)
                    php_print("""                           </div><!-- .inside -->
                    </div><!-- .accordion-section-content -->
                    </li><!-- .accordion-section -->
                    """)
                # end for
            # end if
        # end for
    # end if
    php_print("     </ul><!-- .outer-border -->\n   </div><!-- .accordion-container -->\n   ")
    return i_
# end def do_accordion_sections
#// 
#// Add a new section to a settings page.
#// 
#// Part of the Settings API. Use this to define new settings sections for an admin page.
#// Show settings sections in your admin page callback function with do_settings_sections().
#// Add settings fields to your section with add_settings_field().
#// 
#// The $callback argument should be the name of a function that echoes out any
#// content you want to show at the top of the settings section before the actual
#// fields. It can output nothing if you want.
#// 
#// @since 2.7.0
#// 
#// @global $wp_settings_sections Storage array of all settings sections added to admin pages.
#// 
#// @param string   $id       Slug-name to identify the section. Used in the 'id' attribute of tags.
#// @param string   $title    Formatted title of the section. Shown as the heading for the section.
#// @param callable $callback Function that echos out any content at the top of the section (between heading and fields).
#// @param string   $page     The slug-name of the settings page on which to show the section. Built-in pages include
#// 'general', 'reading', 'writing', 'discussion', 'media', etc. Create your own using
#// add_options_page();
#//
def add_settings_section(id_=None, title_=None, callback_=None, page_=None, *_args_):
    
    
    global wp_settings_sections_
    php_check_if_defined("wp_settings_sections_")
    if "misc" == page_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.0.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "misc"))
        page_ = "general"
    # end if
    if "privacy" == page_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.5.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "privacy"))
        page_ = "reading"
    # end if
    wp_settings_sections_[page_][id_] = Array({"id": id_, "title": title_, "callback": callback_})
# end def add_settings_section
#// 
#// Add a new field to a section of a settings page.
#// 
#// Part of the Settings API. Use this to define a settings field that will show
#// as part of a settings section inside a settings page. The fields are shown using
#// do_settings_fields() in do_settings-sections()
#// 
#// The $callback argument should be the name of a function that echoes out the
#// html input tags for this setting field. Use get_option() to retrieve existing
#// values to show.
#// 
#// @since 2.7.0
#// @since 4.2.0 The `$class` argument was added.
#// 
#// @global $wp_settings_fields Storage array of settings fields and info about their pages/sections.
#// 
#// @param string   $id       Slug-name to identify the field. Used in the 'id' attribute of tags.
#// @param string   $title    Formatted title of the field. Shown as the label for the field
#// during output.
#// @param callable $callback Function that fills the field with the desired form inputs. The
#// function should echo its output.
#// @param string   $page     The slug-name of the settings page on which to show the section
#// (general, reading, writing, ...).
#// @param string   $section  Optional. The slug-name of the section of the settings page
#// in which to show the box. Default 'default'.
#// @param array    $args {
#// Optional. Extra arguments used when outputting the field.
#// 
#// @type string $label_for When supplied, the setting title will be wrapped
#// in a `<label>` element, its `for` attribute populated
#// with this value.
#// @type string $class     CSS Class to be added to the `<tr>` element when the
#// field is output.
#// }
#//
def add_settings_field(id_=None, title_=None, callback_=None, page_=None, section_="default", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_settings_fields_
    php_check_if_defined("wp_settings_fields_")
    if "misc" == page_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.0.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "misc"))
        page_ = "general"
    # end if
    if "privacy" == page_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.5.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "privacy"))
        page_ = "reading"
    # end if
    wp_settings_fields_[page_][section_][id_] = Array({"id": id_, "title": title_, "callback": callback_, "args": args_})
# end def add_settings_field
#// 
#// Prints out all settings sections added to a particular settings page
#// 
#// Part of the Settings API. Use this in a settings page callback function
#// to output all the sections and fields that were added to that $page with
#// add_settings_section() and add_settings_field()
#// 
#// @global $wp_settings_sections Storage array of all settings sections added to admin pages.
#// @global $wp_settings_fields Storage array of settings fields and info about their pages/sections.
#// @since 2.7.0
#// 
#// @param string $page The slug name of the page whose settings sections you want to output.
#//
def do_settings_sections(page_=None, *_args_):
    
    
    global wp_settings_sections_
    global wp_settings_fields_
    php_check_if_defined("wp_settings_sections_","wp_settings_fields_")
    if (not (php_isset(lambda : wp_settings_sections_[page_]))):
        return
    # end if
    for section_ in wp_settings_sections_[page_]:
        if section_["title"]:
            php_print(str("<h2>") + str(section_["title"]) + str("</h2>\n"))
        # end if
        if section_["callback"]:
            php_call_user_func(section_["callback"], section_)
        # end if
        if (not (php_isset(lambda : wp_settings_fields_))) or (not (php_isset(lambda : wp_settings_fields_[page_]))) or (not (php_isset(lambda : wp_settings_fields_[page_][section_["id"]]))):
            continue
        # end if
        php_print("<table class=\"form-table\" role=\"presentation\">")
        do_settings_fields(page_, section_["id"])
        php_print("</table>")
    # end for
# end def do_settings_sections
#// 
#// Print out the settings fields for a particular settings section.
#// 
#// Part of the Settings API. Use this in a settings page to output
#// a specific section. Should normally be called by do_settings_sections()
#// rather than directly.
#// 
#// @global $wp_settings_fields Storage array of settings fields and their pages/sections.
#// 
#// @since 2.7.0
#// 
#// @param string $page Slug title of the admin page whose settings fields you want to show.
#// @param string $section Slug title of the settings section whose fields you want to show.
#//
def do_settings_fields(page_=None, section_=None, *_args_):
    
    
    global wp_settings_fields_
    php_check_if_defined("wp_settings_fields_")
    if (not (php_isset(lambda : wp_settings_fields_[page_][section_]))):
        return
    # end if
    for field_ in wp_settings_fields_[page_][section_]:
        class_ = ""
        if (not php_empty(lambda : field_["args"]["class"])):
            class_ = " class=\"" + esc_attr(field_["args"]["class"]) + "\""
        # end if
        php_print(str("<tr") + str(class_) + str(">"))
        if (not php_empty(lambda : field_["args"]["label_for"])):
            php_print("<th scope=\"row\"><label for=\"" + esc_attr(field_["args"]["label_for"]) + "\">" + field_["title"] + "</label></th>")
        else:
            php_print("<th scope=\"row\">" + field_["title"] + "</th>")
        # end if
        php_print("<td>")
        php_call_user_func(field_["callback"], field_["args"])
        php_print("</td>")
        php_print("</tr>")
    # end for
# end def do_settings_fields
#// 
#// Register a settings error to be displayed to the user.
#// 
#// Part of the Settings API. Use this to show messages to users about settings validation
#// problems, missing settings or anything else.
#// 
#// Settings errors should be added inside the $sanitize_callback function defined in
#// register_setting() for a given setting to give feedback about the submission.
#// 
#// By default messages will show immediately after the submission that generated the error.
#// Additional calls to settings_errors() can be used to show errors even when the settings
#// page is first accessed.
#// 
#// @since 3.0.0
#// @since 5.3.0 Added `warning` and `info` as possible values for `$type`.
#// 
#// @global array $wp_settings_errors Storage array of errors registered during this pageload
#// 
#// @param string $setting Slug title of the setting to which this error applies.
#// @param string $code    Slug-name to identify the error. Used as part of 'id' attribute in HTML output.
#// @param string $message The formatted message text to display to the user (will be shown inside styled
#// `<div>` and `<p>` tags).
#// @param string $type    Optional. Message type, controls HTML class. Possible values include 'error',
#// 'success', 'warning', 'info'. Default 'error'.
#//
def add_settings_error(setting_=None, code_=None, message_=None, type_="error", *_args_):
    
    
    global wp_settings_errors_
    php_check_if_defined("wp_settings_errors_")
    wp_settings_errors_[-1] = Array({"setting": setting_, "code": code_, "message": message_, "type": type_})
# end def add_settings_error
#// 
#// Fetch settings errors registered by add_settings_error().
#// 
#// Checks the $wp_settings_errors array for any errors declared during the current
#// pageload and returns them.
#// 
#// If changes were just submitted ($_GET['settings-updated']) and settings errors were saved
#// to the 'settings_errors' transient then those errors will be returned instead. This
#// is used to pass errors back across pageloads.
#// 
#// Use the $sanitize argument to manually re-sanitize the option before returning errors.
#// This is useful if you have errors or notices you want to show even when the user
#// hasn't submitted data (i.e. when they first load an options page, or in the {@see 'admin_notices'}
#// action hook).
#// 
#// @since 3.0.0
#// 
#// @global array $wp_settings_errors Storage array of errors registered during this pageload
#// 
#// @param string $setting Optional slug title of a specific setting whose errors you want.
#// @param boolean $sanitize Whether to re-sanitize the setting value before returning errors.
#// @return array Array of settings errors.
#//
def get_settings_errors(setting_="", sanitize_=None, *_args_):
    if sanitize_ is None:
        sanitize_ = False
    # end if
    
    global wp_settings_errors_
    php_check_if_defined("wp_settings_errors_")
    #// 
    #// If $sanitize is true, manually re-run the sanitization for this option
    #// This allows the $sanitize_callback from register_setting() to run, adding
    #// any settings errors you want to show by default.
    #//
    if sanitize_:
        sanitize_option(setting_, get_option(setting_))
    # end if
    #// If settings were passed back from options.php then use them.
    if (php_isset(lambda : PHP_REQUEST["settings-updated"])) and PHP_REQUEST["settings-updated"] and get_transient("settings_errors"):
        wp_settings_errors_ = php_array_merge(wp_settings_errors_, get_transient("settings_errors"))
        delete_transient("settings_errors")
    # end if
    #// Check global in case errors have been added on this pageload.
    if php_empty(lambda : wp_settings_errors_):
        return Array()
    # end if
    #// Filter the results to those of a specific setting if one was set.
    if setting_:
        setting_errors_ = Array()
        for key_,details_ in wp_settings_errors_.items():
            if setting_ == details_["setting"]:
                setting_errors_[-1] = wp_settings_errors_[key_]
            # end if
        # end for
        return setting_errors_
    # end if
    return wp_settings_errors_
# end def get_settings_errors
#// 
#// Display settings errors registered by add_settings_error().
#// 
#// Part of the Settings API. Outputs a div for each error retrieved by
#// get_settings_errors().
#// 
#// This is called automatically after a settings page based on the
#// Settings API is submitted. Errors should be added during the validation
#// callback function for a setting defined in register_setting().
#// 
#// The $sanitize option is passed into get_settings_errors() and will
#// re-run the setting sanitization
#// on its current value.
#// 
#// The $hide_on_update option will cause errors to only show when the settings
#// page is first loaded. if the user has already saved new values it will be
#// hidden to avoid repeating messages already shown in the default error
#// reporting after submission. This is useful to show general errors like
#// missing settings when the user arrives at the settings page.
#// 
#// @since 3.0.0
#// @since 5.3.0 Legacy `error` and `updated` CSS classes are mapped to
#// `notice-error` and `notice-success`.
#// 
#// @param string $setting        Optional slug title of a specific setting whose errors you want.
#// @param bool   $sanitize       Whether to re-sanitize the setting value before returning errors.
#// @param bool   $hide_on_update If set to true errors will not be shown if the settings page has
#// already been submitted.
#//
def settings_errors(setting_="", sanitize_=None, hide_on_update_=None, *_args_):
    if sanitize_ is None:
        sanitize_ = False
    # end if
    if hide_on_update_ is None:
        hide_on_update_ = False
    # end if
    
    if hide_on_update_ and (not php_empty(lambda : PHP_REQUEST["settings-updated"])):
        return
    # end if
    settings_errors_ = get_settings_errors(setting_, sanitize_)
    if php_empty(lambda : settings_errors_):
        return
    # end if
    output_ = ""
    for key_,details_ in settings_errors_.items():
        if "updated" == details_["type"]:
            details_["type"] = "success"
        # end if
        if php_in_array(details_["type"], Array("error", "success", "warning", "info")):
            details_["type"] = "notice-" + details_["type"]
        # end if
        css_id_ = php_sprintf("setting-error-%s", esc_attr(details_["code"]))
        css_class_ = php_sprintf("notice %s settings-error is-dismissible", esc_attr(details_["type"]))
        output_ += str("<div id='") + str(css_id_) + str("' class='") + str(css_class_) + str("'> \n")
        output_ += str("<p><strong>") + str(details_["message"]) + str("</strong></p>")
        output_ += "</div> \n"
    # end for
    php_print(output_)
# end def settings_errors
#// 
#// Outputs the modal window used for attaching media to posts or pages in the media-listing screen.
#// 
#// @since 2.7.0
#// 
#// @param string $found_action
#//
def find_posts_div(found_action_="", *_args_):
    
    
    php_print(" <div id=\"find-posts\" class=\"find-box\" style=\"display: none;\">\n       <div id=\"find-posts-head\" class=\"find-box-head\">\n          ")
    _e("Attach to existing content")
    php_print("         <button type=\"button\" id=\"find-posts-close\"><span class=\"screen-reader-text\">")
    _e("Close media attachment panel")
    php_print("""</span></button>
    </div>
    <div class=\"find-box-inside\">
    <div class=\"find-box-search\">
    """)
    if found_action_:
        php_print("                 <input type=\"hidden\" name=\"found_action\" value=\"")
        php_print(esc_attr(found_action_))
        php_print("\" />\n              ")
    # end if
    php_print("             <input type=\"hidden\" name=\"affected\" id=\"affected\" value=\"\" />\n                ")
    wp_nonce_field("find-posts", "_ajax_nonce", False)
    php_print("             <label class=\"screen-reader-text\" for=\"find-posts-input\">")
    _e("Search")
    php_print("""</label>
    <input type=\"text\" id=\"find-posts-input\" name=\"ps\" value=\"\" />
    <span class=\"spinner\"></span>
    <input type=\"button\" id=\"find-posts-search\" value=\"""")
    esc_attr_e("Search")
    php_print("""\" class=\"button\" />
    <div class=\"clear\"></div>
    </div>
    <div id=\"find-posts-response\"></div>
    </div>
    <div class=\"find-box-buttons\">
    """)
    submit_button(__("Select"), "primary alignright", "find-posts-submit", False)
    php_print("""           <div class=\"clear\"></div>
    </div>
    </div>
    """)
# end def find_posts_div
#// 
#// Displays the post password.
#// 
#// The password is passed through esc_attr() to ensure that it is safe for placing in an html attribute.
#// 
#// @since 2.7.0
#//
def the_post_password(*_args_):
    
    
    post_ = get_post()
    if (php_isset(lambda : post_.post_password)):
        php_print(esc_attr(post_.post_password))
    # end if
# end def the_post_password
#// 
#// Get the post title.
#// 
#// The post title is fetched and if it is blank then a default string is
#// returned.
#// 
#// @since 2.7.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return string The post title if set.
#//
def _draft_or_post_title(post_=0, *_args_):
    
    
    title_ = get_the_title(post_)
    if php_empty(lambda : title_):
        title_ = __("(no title)")
    # end if
    return esc_html(title_)
# end def _draft_or_post_title
#// 
#// Displays the search query.
#// 
#// A simple wrapper to display the "s" parameter in a `GET` URI. This function
#// should only be used when the_search_query() cannot.
#// 
#// @since 2.7.0
#//
def _admin_search_query(*_args_):
    
    
    php_print(esc_attr(wp_unslash(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else "")
# end def _admin_search_query
#// 
#// Generic Iframe header for use with Thickbox
#// 
#// @since 2.7.0
#// 
#// @global string    $hook_suffix
#// @global string    $admin_body_class
#// @global WP_Locale $wp_locale        WordPress date and time locale object.
#// 
#// @param string $title      Optional. Title of the Iframe page. Default empty.
#// @param bool   $deprecated Not used.
#//
def iframe_header(title_="", deprecated_=None, *_args_):
    if deprecated_ is None:
        deprecated_ = False
    # end if
    
    show_admin_bar(False)
    global hook_suffix_
    global admin_body_class_
    global wp_locale_
    php_check_if_defined("hook_suffix_","admin_body_class_","wp_locale_")
    admin_body_class_ = php_preg_replace("/[^a-z0-9_-]+/i", "-", hook_suffix_)
    current_screen_ = get_current_screen()
    php_header("Content-Type: " + get_option("html_type") + "; charset=" + get_option("blog_charset"))
    _wp_admin_html_begin()
    php_print("<title>")
    bloginfo("name")
    php_print(" &rsaquo; ")
    php_print(title_)
    php_print(" &#8212; ")
    _e("WordPress")
    php_print("</title>\n   ")
    wp_enqueue_style("colors")
    php_print("""<script type=\"text/javascript\">
    addLoadEvent = function(func){if(typeof jQuery!=\"undefined\")jQuery(document).ready(func);else if(typeof wpOnload!='function'){wpOnload=func;}else{var oldonload=wpOnload;wpOnload=function(){oldonload();func();}}};
    function tb_close(){var win=window.dialogArguments||opener||parent||top;win.tb_remove();}
    var ajaxurl = '""")
    php_print(admin_url("admin-ajax.php", "relative"))
    php_print("',\n pagenow = '")
    php_print(current_screen_.id)
    php_print("',\n typenow = '")
    php_print(current_screen_.post_type)
    php_print("',\n adminpage = '")
    php_print(admin_body_class_)
    php_print("',\n thousandsSeparator = '")
    php_print(addslashes(wp_locale_.number_format["thousands_sep"]))
    php_print("',\n decimalPoint = '")
    php_print(addslashes(wp_locale_.number_format["decimal_point"]))
    php_print("',\n isRtl = ")
    php_print(php_int(is_rtl()))
    php_print(";\n</script>\n   ")
    #// This action is documented in wp-admin/admin-header.php
    do_action("admin_enqueue_scripts", hook_suffix_)
    #// This action is documented in wp-admin/admin-header.php
    do_action(str("admin_print_styles-") + str(hook_suffix_))
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/admin-header.php
    do_action("admin_print_styles")
    #// This action is documented in wp-admin/admin-header.php
    do_action(str("admin_print_scripts-") + str(hook_suffix_))
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/admin-header.php
    do_action("admin_print_scripts")
    #// This action is documented in wp-admin/admin-header.php
    do_action(str("admin_head-") + str(hook_suffix_))
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/admin-header.php
    do_action("admin_head")
    admin_body_class_ += " locale-" + sanitize_html_class(php_strtolower(php_str_replace("_", "-", get_user_locale())))
    if is_rtl():
        admin_body_class_ += " rtl"
    # end if
    php_print("</head>\n    ")
    #// 
    #// @global string $body_id
    #//
    admin_body_id_ = "id=\"" + PHP_GLOBALS["body_id"] + "\" " if (php_isset(lambda : PHP_GLOBALS["body_id"])) else ""
    #// This filter is documented in wp-admin/admin-header.php
    admin_body_classes_ = apply_filters("admin_body_class", "")
    admin_body_classes_ = php_ltrim(admin_body_classes_ + " " + admin_body_class_)
    php_print("<body ")
    php_print(admin_body_id_)
    php_print("class=\"wp-admin wp-core-ui no-js iframe ")
    php_print(admin_body_classes_)
    php_print("""\">
    <script type=\"text/javascript\">
    (function(){
    var c = document.body.className;
    c = c.replace(/no-js/, 'js');
    document.body.className = c;
    })();
    </script>
    """)
# end def iframe_header
#// 
#// Generic Iframe footer for use with Thickbox
#// 
#// @since 2.7.0
#//
def iframe_footer(*_args_):
    
    
    #// 
    #// We're going to hide any footer output on iFrame pages,
    #// but run the hooks anyway since they output JavaScript
    #// or other needed content.
    #// 
    #// 
    #// @global string $hook_suffix
    #//
    global hook_suffix_
    php_check_if_defined("hook_suffix_")
    php_print(" <div class=\"hidden\">\n    ")
    #// This action is documented in wp-admin/admin-footer.php
    do_action("admin_footer", hook_suffix_)
    #// This action is documented in wp-admin/admin-footer.php
    do_action(str("admin_print_footer_scripts-") + str(hook_suffix_))
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/admin-footer.php
    do_action("admin_print_footer_scripts")
    php_print("""   </div>
    <script type=\"text/javascript\">if(typeof wpOnload==\"function\")wpOnload();</script>
    </body>
    </html>
    """)
# end def iframe_footer
#// 
#// Function to echo or return the post states as HTML.
#// 
#// @since 2.7.0
#// @since 5.3.0 Added the `$echo` parameter and a return value.
#// 
#// @see get_post_states()
#// 
#// @param WP_Post $post The post to retrieve states for.
#// @param bool    $echo Optional. Whether to echo the post states as an HTML string. Default true.
#// @return string Post states string.
#//
def _post_states(post_=None, echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    post_states_ = get_post_states(post_)
    post_states_string_ = ""
    if (not php_empty(lambda : post_states_)):
        state_count_ = php_count(post_states_)
        i_ = 0
        post_states_string_ += " &mdash; "
        for state_ in post_states_:
            i_ += 1
            sep_ = "" if i_ == state_count_ else ", "
            post_states_string_ += str("<span class='post-state'>") + str(state_) + str(sep_) + str("</span>")
        # end for
    # end if
    if echo_:
        php_print(post_states_string_)
    # end if
    return post_states_string_
# end def _post_states
#// 
#// Retrieves an array of post states from a post.
#// 
#// @since 5.3.0
#// 
#// @param WP_Post $post The post to retrieve states for.
#// @return string[] Array of post state labels keyed by their state.
#//
def get_post_states(post_=None, *_args_):
    
    
    post_states_ = Array()
    if (php_isset(lambda : PHP_REQUEST["post_status"])):
        post_status_ = PHP_REQUEST["post_status"]
    else:
        post_status_ = ""
    # end if
    if (not php_empty(lambda : post_.post_password)):
        post_states_["protected"] = _x("Password protected", "post status")
    # end if
    if "private" == post_.post_status and "private" != post_status_:
        post_states_["private"] = _x("Private", "post status")
    # end if
    if "draft" == post_.post_status:
        if get_post_meta(post_.ID, "_customize_changeset_uuid", True):
            post_states_[-1] = __("Customization Draft")
        elif "draft" != post_status_:
            post_states_["draft"] = _x("Draft", "post status")
        # end if
    elif "trash" == post_.post_status and get_post_meta(post_.ID, "_customize_changeset_uuid", True):
        post_states_[-1] = _x("Customization Draft", "post status")
    # end if
    if "pending" == post_.post_status and "pending" != post_status_:
        post_states_["pending"] = _x("Pending", "post status")
    # end if
    if is_sticky(post_.ID):
        post_states_["sticky"] = _x("Sticky", "post status")
    # end if
    if "future" == post_.post_status:
        post_states_["scheduled"] = _x("Scheduled", "post status")
    # end if
    if "page" == get_option("show_on_front"):
        if php_intval(get_option("page_on_front")) == post_.ID:
            post_states_["page_on_front"] = _x("Front Page", "page label")
        # end if
        if php_intval(get_option("page_for_posts")) == post_.ID:
            post_states_["page_for_posts"] = _x("Posts Page", "page label")
        # end if
    # end if
    if php_intval(get_option("wp_page_for_privacy_policy")) == post_.ID:
        post_states_["page_for_privacy_policy"] = _x("Privacy Policy Page", "page label")
    # end if
    #// 
    #// Filters the default post display states used in the posts list table.
    #// 
    #// @since 2.8.0
    #// @since 3.6.0 Added the `$post` parameter.
    #// 
    #// @param string[] $post_states An array of post display states.
    #// @param WP_Post  $post        The current post object.
    #//
    return apply_filters("display_post_states", post_states_, post_)
# end def get_post_states
#// 
#// Function to echo the attachment media states as HTML.
#// 
#// @since 3.2.0
#// 
#// @param WP_Post $post The attachment post to retrieve states for.
#// @return string Media states string.
#//
def _media_states(post_=None, *_args_):
    
    
    media_states_ = Array()
    stylesheet_ = get_option("stylesheet")
    if current_theme_supports("custom-header"):
        meta_header_ = get_post_meta(post_.ID, "_wp_attachment_is_custom_header", True)
        if is_random_header_image():
            header_images_ = wp_list_pluck(get_uploaded_header_images(), "attachment_id")
            if meta_header_ == stylesheet_ and php_in_array(post_.ID, header_images_):
                media_states_[-1] = __("Header Image")
            # end if
        else:
            header_image_ = get_header_image()
            #// Display "Header Image" if the image was ever used as a header image.
            if (not php_empty(lambda : meta_header_)) and meta_header_ == stylesheet_ and wp_get_attachment_url(post_.ID) != header_image_:
                media_states_[-1] = __("Header Image")
            # end if
            #// Display "Current Header Image" if the image is currently the header image.
            if header_image_ and wp_get_attachment_url(post_.ID) == header_image_:
                media_states_[-1] = __("Current Header Image")
            # end if
        # end if
    # end if
    if current_theme_supports("custom-background"):
        meta_background_ = get_post_meta(post_.ID, "_wp_attachment_is_custom_background", True)
        if (not php_empty(lambda : meta_background_)) and meta_background_ == stylesheet_:
            media_states_[-1] = __("Background Image")
            background_image_ = get_background_image()
            if background_image_ and wp_get_attachment_url(post_.ID) == background_image_:
                media_states_[-1] = __("Current Background Image")
            # end if
        # end if
    # end if
    if get_option("site_icon") == post_.ID:
        media_states_[-1] = __("Site Icon")
    # end if
    if get_theme_mod("custom_logo") == post_.ID:
        media_states_[-1] = __("Logo")
    # end if
    #// 
    #// Filters the default media display states for items in the Media list table.
    #// 
    #// @since 3.2.0
    #// @since 4.8.0 Added the `$post` parameter.
    #// 
    #// @param string[] $media_states An array of media states. Default 'Header Image',
    #// 'Background Image', 'Site Icon', 'Logo'.
    #// @param WP_Post  $post         The current attachment object.
    #//
    media_states_ = apply_filters("display_media_states", media_states_, post_)
    if (not php_empty(lambda : media_states_)):
        state_count_ = php_count(media_states_)
        i_ = 0
        php_print(" &mdash; ")
        for state_ in media_states_:
            i_ += 1
            sep_ = "" if i_ == state_count_ else ", "
            php_print(str("<span class='post-state'>") + str(state_) + str(sep_) + str("</span>"))
        # end for
    # end if
# end def _media_states
#// 
#// Test support for compressing JavaScript from PHP
#// 
#// Outputs JavaScript that tests if compression from PHP works as expected
#// and sets an option with the result. Has no effect when the current user
#// is not an administrator. To run the test again the option 'can_compress_scripts'
#// has to be deleted.
#// 
#// @since 2.8.0
#//
def compression_test(*_args_):
    
    
    php_print(" <script type=\"text/javascript\">\n var compressionNonce = ")
    php_print(wp_json_encode(wp_create_nonce("update_can_compress_scripts")))
    php_print(""";
    var testCompression = {
    get : function(test) {
    var x;
if ( window.XMLHttpRequest ) {
    x = new XMLHttpRequest();
    } else {
try{x=new ActiveXObject('Msxml2.XMLHTTP');}catch(e){try{x=new ActiveXObject('Microsoft.XMLHTTP');}catch(e){};}
    }
if (x) {
    x.onreadystatechange = function() {
    var r, h;
if ( x.readyState == 4 ) {
    r = x.responseText.substr(0, 18);
    h = x.getResponseHeader('Content-Encoding');
    testCompression.check(r, h, test);
    }
    };
    x.open('GET', ajaxurl + '?action=wp-compression-test&test='+test+'&_ajax_nonce='+compressionNonce+'&'+(new Date()).getTime(), true);
    x.send('');
    }
    },
    check : function(r, h, test) {
if ( ! r && ! test )
    this.get(1);
if ( 1 == test ) {
if ( h && ( h.match(/deflate/i) || h.match(/gzip/i) ) )
    this.get('no');
else
    this.get(2);
    return;
    }
if ( 2 == test ) {
if ( '\"wpCompressionTest' == r )
    this.get('yes');
else
    this.get('no');
    }
    }
    };
    testCompression.check();
    </script>
    """)
# end def compression_test
#// 
#// Echoes a submit button, with provided text and appropriate class(es).
#// 
#// @since 3.1.0
#// 
#// @see get_submit_button()
#// 
#// @param string       $text             The text of the button (defaults to 'Save Changes')
#// @param string       $type             Optional. The type and CSS class(es) of the button. Core values
#// include 'primary', 'small', and 'large'. Default 'primary'.
#// @param string       $name             The HTML name of the submit button. Defaults to "submit". If no
#// id attribute is given in $other_attributes below, $name will be
#// used as the button's id.
#// @param bool         $wrap             True if the output button should be wrapped in a paragraph tag,
#// false otherwise. Defaults to true.
#// @param array|string $other_attributes Other attributes that should be output with the button, mapping
#// attributes to their values, such as setting tabindex to 1, etc.
#// These key/value attribute pairs will be output as attribute="value",
#// where attribute is the key. Other attributes can also be provided
#// as a string such as 'tabindex="1"', though the array format is
#// preferred. Default null.
#//
def submit_button(text_=None, type_="primary", name_="submit", wrap_=None, other_attributes_=None, *_args_):
    if text_ is None:
        text_ = None
    # end if
    if wrap_ is None:
        wrap_ = True
    # end if
    if other_attributes_ is None:
        other_attributes_ = None
    # end if
    
    php_print(get_submit_button(text_, type_, name_, wrap_, other_attributes_))
# end def submit_button
#// 
#// Returns a submit button, with provided text and appropriate class
#// 
#// @since 3.1.0
#// 
#// @param string       $text             Optional. The text of the button. Default 'Save Changes'.
#// @param string       $type             Optional. The type and CSS class(es) of the button. Core values
#// include 'primary', 'small', and 'large'. Default 'primary large'.
#// @param string       $name             Optional. The HTML name of the submit button. Defaults to "submit".
#// If no id attribute is given in $other_attributes below, `$name` will
#// be used as the button's id. Default 'submit'.
#// @param bool         $wrap             Optional. True if the output button should be wrapped in a paragraph
#// tag, false otherwise. Default true.
#// @param array|string $other_attributes Optional. Other attributes that should be output with the button,
#// mapping attributes to their values, such as `array( 'tabindex' => '1' )`.
#// These attributes will be output as `attribute="value"`, such as
#// `tabindex="1"`. Other attributes can also be provided as a string such
#// as `tabindex="1"`, though the array format is typically cleaner.
#// Default empty.
#// @return string Submit button HTML.
#//
def get_submit_button(text_="", type_="primary large", name_="submit", wrap_=None, other_attributes_="", *_args_):
    if wrap_ is None:
        wrap_ = True
    # end if
    
    if (not php_is_array(type_)):
        type_ = php_explode(" ", type_)
    # end if
    button_shorthand_ = Array("primary", "small", "large")
    classes_ = Array("button")
    for t_ in type_:
        if "secondary" == t_ or "button-secondary" == t_:
            continue
        # end if
        classes_[-1] = "button-" + t_ if php_in_array(t_, button_shorthand_) else t_
    # end for
    #// Remove empty items, remove duplicate items, and finally build a string.
    class_ = php_implode(" ", array_unique(php_array_filter(classes_)))
    text_ = text_ if text_ else __("Save Changes")
    #// Default the id attribute to $name unless an id was specifically provided in $other_attributes.
    id_ = name_
    if php_is_array(other_attributes_) and (php_isset(lambda : other_attributes_["id"])):
        id_ = other_attributes_["id"]
        other_attributes_["id"] = None
    # end if
    attributes_ = ""
    if php_is_array(other_attributes_):
        for attribute_,value_ in other_attributes_.items():
            attributes_ += attribute_ + "=\"" + esc_attr(value_) + "\" "
            pass
        # end for
    elif (not php_empty(lambda : other_attributes_)):
        #// Attributes provided as a string.
        attributes_ = other_attributes_
    # end if
    #// Don't output empty name and id attributes.
    name_attr_ = " name=\"" + esc_attr(name_) + "\"" if name_ else ""
    id_attr_ = " id=\"" + esc_attr(id_) + "\"" if id_ else ""
    button_ = "<input type=\"submit\"" + name_attr_ + id_attr_ + " class=\"" + esc_attr(class_)
    button_ += "\" value=\"" + esc_attr(text_) + "\" " + attributes_ + " />"
    if wrap_:
        button_ = "<p class=\"submit\">" + button_ + "</p>"
    # end if
    return button_
# end def get_submit_button
#// 
#// @global bool $is_IE
#//
def _wp_admin_html_begin(*_args_):
    
    
    global is_IE_
    php_check_if_defined("is_IE_")
    admin_html_class_ = "wp-toolbar" if is_admin_bar_showing() else ""
    if is_IE_:
        php_header("X-UA-Compatible: IE=edge")
    # end if
    php_print("<!DOCTYPE html>\n<!--[if IE 8]>\n<html xmlns=\"http://www.w3.org/1999/xhtml\" class=\"ie8 ")
    php_print(admin_html_class_)
    php_print("\"\n ")
    #// 
    #// Fires inside the HTML tag in the admin header.
    #// 
    #// @since 2.2.0
    #//
    do_action("admin_xml_ns")
    language_attributes()
    php_print("""   >
    <![endif]-->
    <!--[if !(IE 8) ]><!-->
    <html xmlns=\"http://www.w3.org/1999/xhtml\" class=\"""")
    php_print(admin_html_class_)
    php_print("\"\n ")
    #// This action is documented in wp-admin/includes/template.php
    do_action("admin_xml_ns")
    language_attributes()
    php_print("""   >
    <!--<![endif]-->
    <head>
    <meta http-equiv=\"Content-Type\" content=\"""")
    bloginfo("html_type")
    php_print("; charset=")
    php_print(get_option("blog_charset"))
    php_print("\" />\n  ")
# end def _wp_admin_html_begin
#// 
#// Convert a screen string to a screen object
#// 
#// @since 3.0.0
#// 
#// @param string $hook_name The hook name (also known as the hook suffix) used to determine the screen.
#// @return WP_Screen Screen object.
#//
def convert_to_screen(hook_name_=None, *_args_):
    
    
    if (not php_class_exists("WP_Screen")):
        _doing_it_wrong("convert_to_screen(), add_meta_box()", php_sprintf(__("Likely direct inclusion of %1$s in order to use %2$s. This is very wrong. Hook the %2$s call into the %3$s action instead."), "<code>wp-admin/includes/template.php</code>", "<code>add_meta_box()</code>", "<code>add_meta_boxes</code>"), "3.3.0")
        return Array({"id": "_invalid", "base": "_are_belong_to_us"})
    # end if
    return WP_Screen.get(hook_name_)
# end def convert_to_screen
#// 
#// Output the HTML for restoring the post data from DOM storage
#// 
#// @since 3.6.0
#// @access private
#//
def _local_storage_notice(*_args_):
    
    
    php_print(" <div id=\"local-storage-notice\" class=\"hidden notice is-dismissible\">\n  <p class=\"local-restore\">\n       ")
    _e("The backup of this post in your browser is different from the version below.")
    php_print("     <button type=\"button\" class=\"button restore-backup\">")
    _e("Restore the backup")
    php_print("""</button>
    </p>
    <p class=\"help\">
    """)
    _e("This will replace the current editor content with the last backup version. You can use undo and redo in the editor to get the old content back or to return to the restored version.")
    php_print(" </p>\n  </div>\n    ")
# end def _local_storage_notice
#// 
#// Output a HTML element with a star rating for a given rating.
#// 
#// Outputs a HTML element with the star rating exposed on a 0..5 scale in
#// half star increments (ie. 1, 1.5, 2 stars). Optionally, if specified, the
#// number of ratings may also be displayed by passing the $number parameter.
#// 
#// @since 3.8.0
#// @since 4.4.0 Introduced the `echo` parameter.
#// 
#// @param array $args {
#// Optional. Array of star ratings arguments.
#// 
#// @type int|float $rating The rating to display, expressed in either a 0.5 rating increment,
#// or percentage. Default 0.
#// @type string    $type   Format that the $rating is in. Valid values are 'rating' (default),
#// or, 'percent'. Default 'rating'.
#// @type int       $number The number of ratings that makes up this rating. Default 0.
#// @type bool      $echo   Whether to echo the generated markup. False to return the markup instead
#// of echoing it. Default true.
#// }
#// @return string Star rating HTML.
#//
def wp_star_rating(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"rating": 0, "type": "rating", "number": 0, "echo": True})
    parsed_args_ = wp_parse_args(args_, defaults_)
    #// Non-English decimal places when the $rating is coming from a string.
    rating_ = php_float(php_str_replace(",", ".", parsed_args_["rating"]))
    #// Convert percentage to star rating, 0..5 in .5 increments.
    if "percent" == parsed_args_["type"]:
        rating_ = round(rating_ / 10, 0) / 2
    # end if
    #// Calculate the number of each type of star needed.
    full_stars_ = floor(rating_)
    half_stars_ = ceil(rating_ - full_stars_)
    empty_stars_ = 5 - full_stars_ - half_stars_
    if parsed_args_["number"]:
        #// translators: 1: The rating, 2: The number of ratings.
        format_ = _n("%1$s rating based on %2$s rating", "%1$s rating based on %2$s ratings", parsed_args_["number"])
        title_ = php_sprintf(format_, number_format_i18n(rating_, 1), number_format_i18n(parsed_args_["number"]))
    else:
        #// translators: %s: The rating.
        title_ = php_sprintf(__("%s rating"), number_format_i18n(rating_, 1))
    # end if
    output_ = "<div class=\"star-rating\">"
    output_ += "<span class=\"screen-reader-text\">" + title_ + "</span>"
    output_ += php_str_repeat("<div class=\"star star-full\" aria-hidden=\"true\"></div>", full_stars_)
    output_ += php_str_repeat("<div class=\"star star-half\" aria-hidden=\"true\"></div>", half_stars_)
    output_ += php_str_repeat("<div class=\"star star-empty\" aria-hidden=\"true\"></div>", empty_stars_)
    output_ += "</div>"
    if parsed_args_["echo"]:
        php_print(output_)
    # end if
    return output_
# end def wp_star_rating
#// 
#// Output a notice when editing the page for posts (internal use only).
#// 
#// @ignore
#// @since 4.2.0
#//
def _wp_posts_page_notice(*_args_):
    
    
    php_print("<div class=\"notice notice-warning inline\"><p>" + __("You are currently editing the page that shows your latest posts.") + "</p></div>")
# end def _wp_posts_page_notice
