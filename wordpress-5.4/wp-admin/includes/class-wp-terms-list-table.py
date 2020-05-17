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
#// List Table API: WP_Terms_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying terms in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Terms_List_Table(WP_List_Table):
    callback_args = Array()
    level = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 3.1.0
    #// 
    #// @see WP_List_Table::__construct() for more information on default arguments.
    #// 
    #// @global string $post_type
    #// @global string $taxonomy
    #// @global string $action
    #// @global object $tax
    #// 
    #// @param array $args An associative array of arguments.
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        global post_type_
        global taxonomy_
        global action_
        global tax_
        php_check_if_defined("post_type_","taxonomy_","action_","tax_")
        super().__init__(Array({"plural": "tags", "singular": "tag", "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
        action_ = self.screen.action
        post_type_ = self.screen.post_type
        taxonomy_ = self.screen.taxonomy
        if php_empty(lambda : taxonomy_):
            taxonomy_ = "post_tag"
        # end if
        if (not taxonomy_exists(taxonomy_)):
            wp_die(__("Invalid taxonomy."))
        # end if
        tax_ = get_taxonomy(taxonomy_)
        #// @todo Still needed? Maybe just the show_ui part.
        if php_empty(lambda : post_type_) or (not php_in_array(post_type_, get_post_types(Array({"show_ui": True})))):
            post_type_ = "post"
        # end if
    # end def __init__
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        
        return current_user_can(get_taxonomy(self.screen.taxonomy).cap.manage_terms)
    # end def ajax_user_can
    #// 
    #//
    def prepare_items(self):
        
        
        tags_per_page_ = self.get_items_per_page("edit_" + self.screen.taxonomy + "_per_page")
        if "post_tag" == self.screen.taxonomy:
            #// 
            #// Filters the number of terms displayed per page for the Tags list table.
            #// 
            #// @since 2.8.0
            #// 
            #// @param int $tags_per_page Number of tags to be displayed. Default 20.
            #//
            tags_per_page_ = apply_filters("edit_tags_per_page", tags_per_page_)
            #// 
            #// Filters the number of terms displayed per page for the Tags list table.
            #// 
            #// @since 2.7.0
            #// @deprecated 2.8.0 Use {@see 'edit_tags_per_page'} instead.
            #// 
            #// @param int $tags_per_page Number of tags to be displayed. Default 20.
            #//
            tags_per_page_ = apply_filters_deprecated("tagsperpage", Array(tags_per_page_), "2.8.0", "edit_tags_per_page")
        elif "category" == self.screen.taxonomy:
            #// 
            #// Filters the number of terms displayed per page for the Categories list table.
            #// 
            #// @since 2.8.0
            #// 
            #// @param int $tags_per_page Number of categories to be displayed. Default 20.
            #//
            tags_per_page_ = apply_filters("edit_categories_per_page", tags_per_page_)
        # end if
        search_ = php_trim(wp_unslash(PHP_REQUEST["s"])) if (not php_empty(lambda : PHP_REQUEST["s"])) else ""
        args_ = Array({"search": search_, "page": self.get_pagenum(), "number": tags_per_page_})
        if (not php_empty(lambda : PHP_REQUEST["orderby"])):
            args_["orderby"] = php_trim(wp_unslash(PHP_REQUEST["orderby"]))
        # end if
        if (not php_empty(lambda : PHP_REQUEST["order"])):
            args_["order"] = php_trim(wp_unslash(PHP_REQUEST["order"]))
        # end if
        self.callback_args = args_
        self.set_pagination_args(Array({"total_items": wp_count_terms(self.screen.taxonomy, php_compact("search")), "per_page": tags_per_page_}))
    # end def prepare_items
    #// 
    #// @return bool
    #//
    def has_items(self):
        
        
        #// @todo Populate $this->items in prepare_items().
        return True
    # end def has_items
    #// 
    #//
    def no_items(self):
        
        
        php_print(get_taxonomy(self.screen.taxonomy).labels.not_found)
    # end def no_items
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        actions_ = Array()
        if current_user_can(get_taxonomy(self.screen.taxonomy).cap.delete_terms):
            actions_["delete"] = __("Delete")
        # end if
        return actions_
    # end def get_bulk_actions
    #// 
    #// @return string
    #//
    def current_action(self):
        
        
        if (php_isset(lambda : PHP_REQUEST["action"])) and (php_isset(lambda : PHP_REQUEST["delete_tags"])) and "delete" == PHP_REQUEST["action"] or "delete" == PHP_REQUEST["action2"]:
            return "bulk-delete"
        # end if
        return super().current_action()
    # end def current_action
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        columns_ = Array({"cb": "<input type=\"checkbox\" />", "name": _x("Name", "term name"), "description": __("Description"), "slug": __("Slug")})
        if "link_category" == self.screen.taxonomy:
            columns_["links"] = __("Links")
        else:
            columns_["posts"] = _x("Count", "Number/count of items")
        # end if
        return columns_
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        
        return Array({"name": "name", "description": "description", "slug": "slug", "posts": "count", "links": "count"})
    # end def get_sortable_columns
    #// 
    #//
    def display_rows_or_placeholder(self):
        
        
        taxonomy_ = self.screen.taxonomy
        args_ = wp_parse_args(self.callback_args, Array({"taxonomy": taxonomy_, "page": 1, "number": 20, "search": "", "hide_empty": 0}))
        page_ = args_["page"]
        #// Set variable because $args['number'] can be subsequently overridden.
        number_ = args_["number"]
        offset_ = page_ - 1 * number_
        args_["offset"] = offset_
        #// Convert it to table rows.
        count_ = 0
        if is_taxonomy_hierarchical(taxonomy_) and (not (php_isset(lambda : args_["orderby"]))):
            #// We'll need the full set of terms then.
            args_["number"] = 0
            args_["offset"] = args_["number"]
        # end if
        terms_ = get_terms(args_)
        if php_empty(lambda : terms_) or (not php_is_array(terms_)):
            php_print("<tr class=\"no-items\"><td class=\"colspanchange\" colspan=\"" + self.get_column_count() + "\">")
            self.no_items()
            php_print("</td></tr>")
            return
        # end if
        if is_taxonomy_hierarchical(taxonomy_) and (not (php_isset(lambda : args_["orderby"]))):
            if (not php_empty(lambda : args_["search"])):
                #// Ignore children on searches.
                children_ = Array()
            else:
                children_ = _get_term_hierarchy(taxonomy_)
            # end if
            #// 
            #// Some funky recursion to get the job done (paging & parents mainly) is contained within.
            #// Skip it for non-hierarchical taxonomies for performance sake.
            #//
            self._rows(taxonomy_, terms_, children_, offset_, number_, count_)
        else:
            for term_ in terms_:
                self.single_row(term_)
            # end for
        # end if
    # end def display_rows_or_placeholder
    #// 
    #// @param string $taxonomy
    #// @param array $terms
    #// @param array $children
    #// @param int   $start
    #// @param int   $per_page
    #// @param int   $count
    #// @param int   $parent
    #// @param int   $level
    #//
    def _rows(self, taxonomy_=None, terms_=None, children_=None, start_=None, per_page_=None, count_=None, parent_=0, level_=0):
        
        
        end_ = start_ + per_page_
        for key_,term_ in terms_:
            if count_ >= end_:
                break
            # end if
            if term_.parent != parent_ and php_empty(lambda : PHP_REQUEST["s"]):
                continue
            # end if
            #// If the page starts in a subtree, print the parents.
            if count_ == start_ and term_.parent > 0 and php_empty(lambda : PHP_REQUEST["s"]):
                my_parents_ = Array()
                parent_ids_ = Array()
                p_ = term_.parent
                while True:
                    
                    if not (p_):
                        break
                    # end if
                    my_parent_ = get_term(p_, taxonomy_)
                    my_parents_[-1] = my_parent_
                    p_ = my_parent_.parent
                    if php_in_array(p_, parent_ids_):
                        break
                    # end if
                    parent_ids_[-1] = p_
                # end while
                parent_ids_ = None
                num_parents_ = php_count(my_parents_)
                while True:
                    my_parent_ = php_array_pop(my_parents_)
                    if not (my_parent_):
                        break
                    # end if
                    php_print(" ")
                    self.single_row(my_parent_, level_ - num_parents_)
                    num_parents_ -= 1
                # end while
            # end if
            if count_ >= start_:
                php_print(" ")
                self.single_row(term_, level_)
            # end if
            count_ += 1
            terms_[key_] = None
            if (php_isset(lambda : children_[term_.term_id])) and php_empty(lambda : PHP_REQUEST["s"]):
                self._rows(taxonomy_, terms_, children_, start_, per_page_, count_, term_.term_id, level_ + 1)
            # end if
        # end for
    # end def _rows
    #// 
    #// @global string $taxonomy
    #// @param WP_Term $tag Term object.
    #// @param int $level
    #//
    def single_row(self, tag_=None, level_=0):
        
        
        global taxonomy_
        php_check_if_defined("taxonomy_")
        tag_ = sanitize_term(tag_, taxonomy_)
        self.level = level_
        if tag_.parent:
            count_ = php_count(get_ancestors(tag_.term_id, taxonomy_, "taxonomy"))
            level_ = "level-" + count_
        else:
            level_ = "level-0"
        # end if
        php_print("<tr id=\"tag-" + tag_.term_id + "\" class=\"" + level_ + "\">")
        self.single_row_columns(tag_)
        php_print("</tr>")
    # end def single_row
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_cb(self, tag_=None):
        
        
        if current_user_can("delete_term", tag_.term_id):
            return php_sprintf("<label class=\"screen-reader-text\" for=\"cb-select-%1$s\">%2$s</label>" + "<input type=\"checkbox\" name=\"delete_tags[]\" value=\"%1$s\" id=\"cb-select-%1$s\" />", tag_.term_id, php_sprintf(__("Select %s"), tag_.name))
        # end if
        return "&nbsp;"
    # end def column_cb
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_name(self, tag_=None):
        
        
        taxonomy_ = self.screen.taxonomy
        pad_ = php_str_repeat("&#8212; ", php_max(0, self.level))
        #// 
        #// Filters display of the term name in the terms list table.
        #// 
        #// The default output may include padding due to the term's
        #// current level in the term hierarchy.
        #// 
        #// @since 2.5.0
        #// 
        #// @see WP_Terms_List_Table::column_name()
        #// 
        #// @param string $pad_tag_name The term name, padded if not top-level.
        #// @param WP_Term $tag         Term object.
        #//
        name_ = apply_filters("term_name", pad_ + " " + tag_.name, tag_)
        qe_data_ = get_term(tag_.term_id, taxonomy_, OBJECT, "edit")
        uri_ = wp_get_referer() if wp_doing_ajax() else PHP_SERVER["REQUEST_URI"]
        edit_link_ = get_edit_term_link(tag_.term_id, taxonomy_, self.screen.post_type)
        if edit_link_:
            edit_link_ = add_query_arg("wp_http_referer", urlencode(wp_unslash(uri_)), edit_link_)
            name_ = php_sprintf("<a class=\"row-title\" href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(edit_link_), esc_attr(php_sprintf(__("&#8220;%s&#8221; (Edit)"), tag_.name)), name_)
        # end if
        out_ = php_sprintf("<strong>%s</strong><br />", name_)
        out_ += "<div class=\"hidden\" id=\"inline_" + qe_data_.term_id + "\">"
        out_ += "<div class=\"name\">" + qe_data_.name + "</div>"
        #// This filter is documented in wp-admin/edit-tag-form.php
        out_ += "<div class=\"slug\">" + apply_filters("editable_slug", qe_data_.slug, qe_data_) + "</div>"
        out_ += "<div class=\"parent\">" + qe_data_.parent + "</div></div>"
        return out_
    # end def column_name
    #// 
    #// Gets the name of the default primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Name of the default primary column, in this case, 'name'.
    #//
    def get_default_primary_column_name(self):
        
        
        return "name"
    # end def get_default_primary_column_name
    #// 
    #// Generates and displays row action links.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Term $tag         Tag being acted upon.
    #// @param string  $column_name Current column name.
    #// @param string  $primary     Primary column name.
    #// @return string Row actions output for terms, or an empty string
    #// if the current column is not the primary column.
    #//
    def handle_row_actions(self, tag_=None, column_name_=None, primary_=None):
        
        
        if primary_ != column_name_:
            return ""
        # end if
        taxonomy_ = self.screen.taxonomy
        tax_ = get_taxonomy(taxonomy_)
        uri_ = wp_get_referer() if wp_doing_ajax() else PHP_SERVER["REQUEST_URI"]
        edit_link_ = add_query_arg("wp_http_referer", urlencode(wp_unslash(uri_)), get_edit_term_link(tag_.term_id, taxonomy_, self.screen.post_type))
        actions_ = Array()
        if current_user_can("edit_term", tag_.term_id):
            actions_["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(edit_link_), esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), tag_.name)), __("Edit"))
            actions_["inline hide-if-no-js"] = php_sprintf("<button type=\"button\" class=\"button-link editinline\" aria-label=\"%s\" aria-expanded=\"false\">%s</button>", esc_attr(php_sprintf(__("Quick edit &#8220;%s&#8221; inline"), tag_.name)), __("Quick&nbsp;Edit"))
        # end if
        if current_user_can("delete_term", tag_.term_id):
            actions_["delete"] = php_sprintf("<a href=\"%s\" class=\"delete-tag aria-button-if-js\" aria-label=\"%s\">%s</a>", wp_nonce_url(str("edit-tags.php?action=delete&amp;taxonomy=") + str(taxonomy_) + str("&amp;tag_ID=") + str(tag_.term_id), "delete-tag_" + tag_.term_id), esc_attr(php_sprintf(__("Delete &#8220;%s&#8221;"), tag_.name)), __("Delete"))
        # end if
        if is_taxonomy_viewable(tax_):
            actions_["view"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_term_link(tag_), esc_attr(php_sprintf(__("View &#8220;%s&#8221; archive"), tag_.name)), __("View"))
        # end if
        #// 
        #// Filters the action links displayed for each term in the Tags list table.
        #// 
        #// @since 2.8.0
        #// @deprecated 3.0.0 Use {@see '{$taxonomy}_row_actions'} instead.
        #// 
        #// @param string[] $actions An array of action links to be displayed. Default
        #// 'Edit', 'Quick Edit', 'Delete', and 'View'.
        #// @param WP_Term  $tag     Term object.
        #//
        actions_ = apply_filters_deprecated("tag_row_actions", Array(actions_, tag_), "3.0.0", "{$taxonomy}_row_actions")
        #// 
        #// Filters the action links displayed for each term in the terms list table.
        #// 
        #// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $actions An array of action links to be displayed. Default
        #// 'Edit', 'Quick Edit', 'Delete', and 'View'.
        #// @param WP_Term  $tag     Term object.
        #//
        actions_ = apply_filters(str(taxonomy_) + str("_row_actions"), actions_, tag_)
        return self.row_actions(actions_)
    # end def handle_row_actions
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_description(self, tag_=None):
        
        
        if tag_.description:
            return tag_.description
        else:
            return "<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">" + __("No description") + "</span>"
        # end if
    # end def column_description
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_slug(self, tag_=None):
        
        
        #// This filter is documented in wp-admin/edit-tag-form.php
        return apply_filters("editable_slug", tag_.slug, tag_)
    # end def column_slug
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_posts(self, tag_=None):
        
        
        count_ = number_format_i18n(tag_.count)
        tax_ = get_taxonomy(self.screen.taxonomy)
        ptype_object_ = get_post_type_object(self.screen.post_type)
        if (not ptype_object_.show_ui):
            return count_
        # end if
        if tax_.query_var:
            args_ = Array({tax_.query_var: tag_.slug})
        else:
            args_ = Array({"taxonomy": tax_.name, "term": tag_.slug})
        # end if
        if "post" != self.screen.post_type:
            args_["post_type"] = self.screen.post_type
        # end if
        if "attachment" == self.screen.post_type:
            return "<a href='" + esc_url(add_query_arg(args_, "upload.php")) + str("'>") + str(count_) + str("</a>")
        # end if
        return "<a href='" + esc_url(add_query_arg(args_, "edit.php")) + str("'>") + str(count_) + str("</a>")
    # end def column_posts
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_links(self, tag_=None):
        
        
        count_ = number_format_i18n(tag_.count)
        if count_:
            count_ = str("<a href='link-manager.php?cat_id=") + str(tag_.term_id) + str("'>") + str(count_) + str("</a>")
        # end if
        return count_
    # end def column_links
    #// 
    #// @param WP_Term $tag Term object.
    #// @param string $column_name
    #// @return string
    #//
    def column_default(self, tag_=None, column_name_=None):
        
        
        #// 
        #// Filters the displayed columns in the terms list table.
        #// 
        #// The dynamic portion of the hook name, `$this->screen->taxonomy`,
        #// refers to the slug of the current taxonomy.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string $string      Blank string.
        #// @param string $column_name Name of the column.
        #// @param int    $term_id     Term ID.
        #//
        return apply_filters(str("manage_") + str(self.screen.taxonomy) + str("_custom_column"), "", column_name_, tag_.term_id)
    # end def column_default
    #// 
    #// Outputs the hidden row displayed when inline editing
    #// 
    #// @since 3.1.0
    #//
    def inline_edit(self):
        
        
        tax_ = get_taxonomy(self.screen.taxonomy)
        if (not current_user_can(tax_.cap.edit_terms)):
            return
        # end if
        php_print("""
        <form method=\"get\">
        <table style=\"display: none\"><tbody id=\"inlineedit\">
        <tr id=\"inline-edit\" class=\"inline-edit-row\" style=\"display: none\">
        <td colspan=\"""")
        php_print(self.get_column_count())
        php_print("""\" class=\"colspanchange\">
        <fieldset>
        <legend class=\"inline-edit-legend\">""")
        _e("Quick Edit")
        php_print("""</legend>
        <div class=\"inline-edit-col\">
        <label>
        <span class=\"title\">""")
        _ex("Name", "term name")
        php_print("""</span>
        <span class=\"input-text-wrap\"><input type=\"text\" name=\"name\" class=\"ptitle\" value=\"\" /></span>
        </label>
        """)
        if (not global_terms_enabled()):
            php_print("                 <label>\n                       <span class=\"title\">")
            _e("Slug")
            php_print("""</span>
            <span class=\"input-text-wrap\"><input type=\"text\" name=\"slug\" class=\"ptitle\" value=\"\" /></span>
            </label>
            """)
        # end if
        php_print("""               </div>
        </fieldset>
        """)
        core_columns_ = Array({"cb": True, "description": True, "name": True, "slug": True, "posts": True})
        columns_ = self.get_column_info()
        for column_name_,column_display_name_ in columns_:
            if (php_isset(lambda : core_columns_[column_name_])):
                continue
            # end if
            #// This action is documented in wp-admin/includes/class-wp-posts-list-table.php
            do_action("quick_edit_custom_box", column_name_, "edit-tags", self.screen.taxonomy)
        # end for
        php_print("\n           <div class=\"inline-edit-save submit\">\n               <button type=\"button\" class=\"cancel button alignleft\">")
        _e("Cancel")
        php_print("</button>\n              <button type=\"button\" class=\"save button button-primary alignright\">")
        php_print(tax_.labels.update_item)
        php_print("""</button>
        <span class=\"spinner\"></span>
        """)
        wp_nonce_field("taxinlineeditnonce", "_inline_edit", False)
        php_print("             <input type=\"hidden\" name=\"taxonomy\" value=\"")
        php_print(esc_attr(self.screen.taxonomy))
        php_print("\" />\n              <input type=\"hidden\" name=\"post_type\" value=\"")
        php_print(esc_attr(self.screen.post_type))
        php_print("""\" />
        <br class=\"clear\" />
        <div class=\"notice notice-error notice-alt inline hidden\">
        <p class=\"error\"></p>
        </div>
        </div>
        </td></tr>
        </tbody></table>
        </form>
        """)
    # end def inline_edit
# end class WP_Terms_List_Table
